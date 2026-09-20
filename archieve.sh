#!/bin/bash
# NERSC pscratch -> 외장 디스크 / 클라우드 백업
#
# 환경변수
#   here          slac | mac | mini  (~/.zshrc 에서 export)
#   MIN_FREE_GB   목적지 볼륨에 최소 이만큼 남아 있어야 전송 시작 (기본 100)
#   DRY_RUN=1     실제로 쓰지 않고 전송 계획만 출력

set -euo pipefail

RSYNC='/opt/homebrew/bin/rsync'
[[ -x "$RSYNC" ]] || RSYNC="$(command -v rsync)"

NERSC='jiuy97@perlmutter.nersc.gov'
SCRATCH='/pscratch/sd/j/jiuy97'

MIN_FREE_GB="${MIN_FREE_GB:-100}"
DRY_RUN="${DRY_RUN:-0}"

# ------------------------------------------------------------------ 제외 목록
# 어느 목적지로 보내든 항상 빼는 것
EXCLUDE_COMMON=(
    moments.traj qn.xyz vaspout.h5
    EIGENVAL IBZKPT PCDAT POT REPORT
)
# 용량의 대부분을 차지하는 것. 클라우드로는 보내지 않는다.
# CHGCAR_sum 은 --exclude=CHGCAR 로 걸러지지 않으므로 따로 적는다.
# AECCAR0/1/2 는 LAECHG=.TRUE. 가 만드는 Bader 분석 중간 파일이다.
# chgsum.pl 과 bader 를 거쳐 ACF.dat, bader_charges.tsv,
# atoms_bader_charge.json 이 나오면 더 쓸 일이 없다. 7_prediction 에서만
# 157 GiB 를 차지했다. rsync 가 글롭을 직접 해석하므로 따옴표로 넘긴다.
EXCLUDE_HEAVY=(
    WAVECAR CHGCAR CHGCAR_sum CHG PROCAR LOCPOT 'AECCAR*'
    # 1_cation 의 MLIP 학습 체크포인트. 학습을 다시 돌리면 나오는 것들이라
    # 뺀다. *.distcp 181 GiB, inference_ckpt.pt 91 GiB 를 줄인다.
    # *.pt 로 묶으면 trainset_oc20.pt 와 catwater_mace_ft_*.pt 최종 모델까지
    # 날아가므로 inference_ckpt.pt 만 이름으로 지정한다.
    '*.distcp' inference_ckpt.pt
)
# --min-size=1 은 의도적이다. 0바이트 파일은 백업하지 않는다.
#
# --size-only 가 핵심이다. pscratch purge 를 피하려고 원격 파일 mtime 을 일괄
# touch 하면(3_RuO2 는 2026-09-06 00:59~01:00 로 전부 바뀌어 있다) 기본 비교
# 방식은 크기가 같은 파일도 mtime 이 다르다는 이유로 전부 다시 받는다.
# 하위 디렉터리 하나만 재봐도 534개 5.7GB 를 재전송하려 했고, --size-only 로는
# 0개였다. 크기가 같고 내용만 바뀐 파일은 건너뛰게 되는데, 끝난 계산을
# 보관하는 용도라 그 위험은 감수한다.
#
# -W(--whole-file) 는 클라우드 폴더 때문에 필요하다. rsync 의 델타 전송은
# 수신측 기존 파일을 읽어 체크섬을 만드는데, OneDrive 의 dataless 파일을
# 읽으면 클라우드에서 먼저 내려받는다(hydration). 통째로 덮어쓰면 그 왕복이 없다.
RSYNC_BASE=(-av --min-size=1 --size-only --whole-file)

FAILED=()

# ---------------------------------------------------------------------- 유틸
log()  { printf '[%s] %s\n'      "$(date '+%H:%M:%S')" "$*"; }
warn() { printf '[%s] 경고  %s\n' "$(date '+%H:%M:%S')" "$*" >&2; }
die()  { printf '[%s] 중단  %s\n' "$(date '+%H:%M:%S')" "$*" >&2; exit 1; }

free_gb() { df -g "$1" | awk 'NR==2 {print $4}'; }

# 목적지 볼륨 여유 공간이 기준 미달이면 1을 반환한다.
require_space() {
    local dest="$1" free
    free="$(free_gb "$dest")"
    if (( free < MIN_FREE_GB )); then
        warn "$dest 여유 ${free}GB < 기준 ${MIN_FREE_GB}GB, 건너뜀"
        return 1
    fi
    log "$dest 여유 ${free}GB"
}

# rsync 를 돌리고 종료 코드를 해석한다.
#   24  전송 중 원본 파일이 사라짐. VASP 실행 중이면 흔하고 무해하다.
#   23  일부 파일 전송 실패. 원격에 없는 디렉터리를 지정했을 때도 난다.
#   11  파일 I/O 오류. 디스크가 찼을 가능성이 높아 즉시 멈춘다.
run_rsync() {
    local label="$1"; shift
    local rc=0
    "$RSYNC" "$@" || rc=$?
    case "$rc" in
        0)  log "$label 완료" ;;
        24) log "$label 완료 (전송 중 원본 일부 사라짐)" ;;
        23) warn "$label 일부 실패 (코드 23)"; FAILED+=("$label") ;;
        11) FAILED+=("$label"); die "$label 파일 I/O 오류 (코드 11). 디스크가 찼을 수 있어 나머지를 중단합니다." ;;
        *)  warn "$label 실패 (코드 $rc)"; FAILED+=("$label") ;;
    esac
}

# pull <light|heavy> <목적지> <원격 디렉터리>...
pull() {
    local profile="$1" dest="$2"; shift 2
    local -a opts name
    opts=("${RSYNC_BASE[@]}" -e ssh)
    [[ "$DRY_RUN" == 1 ]] && opts+=(--dry-run --stats)

    for name in "${EXCLUDE_COMMON[@]}"; do opts+=("--exclude=$name"); done
    if [[ "$profile" == heavy ]]; then
        for name in "${EXCLUDE_HEAVY[@]}"; do opts+=("--exclude=$name"); done
    fi

    for name in "$@"; do
        # 디렉터리 하나 받을 때마다 다시 확인한다. 앞 전송이 공간을 먹었을 수 있다.
        require_space "$dest" || return 0
        log "$name -> $dest ($profile)"
        run_rsync "$name" "${opts[@]}" "$NERSC:$SCRATCH/$name" "$dest/"
    done
}

# NERSC 인증서는 24시간마다 만료된다. 남은 시간을 미리 알려준다.
check_cert() {
    local cert="$HOME/.ssh/nersc-cert.pub" exp exp_epoch left
    [[ -f "$cert" ]] || { warn "$cert 없음. sshproxy.sh 를 먼저 실행하세요."; return; }
    exp="$(ssh-keygen -L -f "$cert" 2>/dev/null | awk '/Valid:/ {print $5}')"
    [[ -n "$exp" ]] || return
    exp_epoch="$(date -j -f '%Y-%m-%dT%H:%M:%S' "$exp" '+%s' 2>/dev/null || echo 0)"
    (( exp_epoch > 0 )) || return
    left=$(( (exp_epoch - $(date '+%s')) / 3600 ))
    if (( left < 1 )); then
        warn "NERSC 인증서가 1시간 내 만료됩니다. sshproxy.sh 로 재발급하세요."
    else
        log "NERSC 인증서 ${left}시간 남음"
    fi
}

# ---------------------------------------------------------------------- 경로
case "${here:-}" in
    slac|mac|mini) ;;
    *) die "here 가 설정되지 않았습니다. slac, mac, mini 중 하나여야 합니다." ;;
esac

cloud="$HOME/Library/CloudStorage"
toshiba='/Volumes/TOSHIBA'
jeung2hailey='/Volumes/jeung2hailey'
stanford="$cloud/OneDrive-Stanford"
# Google Drive 전체를 OneDrive-Personal 로 복사하던 블록은 제거했다.
# FileProvider 열거가 너무 느려서 dry-run 이 37분이 지나도 끝나지 않았다.
# 아래 google 은 figures 업로드 목적지를 만드는 데만 쓴다.
# 작은따옴표 안의 백슬래시는 리터럴이라 예전 'My\ Drive' 는 존재하지 않는 경로였다.
google="$cloud/GoogleDrive-jiuy97@stanford.edu/My Drive"
tetra="$google/Tetrahedral_oxides_ML/Figures"
figures="$HOME/Desktop/7_V_bulk/figures"

# ---------------------------------------------------------------------- 실행
check_cert

# 외장 디스크는 전체 보관용이라 대용량 파일도 함께 받는다.
if [[ -d "$toshiba" ]]; then
    pull light "$toshiba" 3_V_bulk 4_V_slab 7_V_bulk 8_V_slab
else
    log "$toshiba 미마운트, 건너뜀"
fi

if [[ -d "$jeung2hailey" ]]; then
    pull light "$jeung2hailey" 1_cation 5_HEO
else
    log "$jeung2hailey 미마운트, 건너뜀"
fi

# 클라우드는 로컬 디스크를 거쳐 업로드되므로 대용량 파일을 뺀다.
if [[ -d "$stanford" ]]; then
    # 큰 것을 뒤에 둔다. 앞의 작은 것들이 먼저 끝나고, 공간이 모자라면
    # require_space 가 큰 것 앞에서 멈춘다.
    pull heavy "$stanford" 3_RuO2 4_MnO2 6_MNC 9_pourbaixGC 2_PAFC 7_prediction 1_cation
else
    log "$stanford 없음, 건너뜀"
fi

# Desktop figures -> Google Drive
if [[ -d "$tetra" ]]; then
    if [[ -d "$figures" ]]; then
        if require_space "$tetra"; then
            run_rsync 'figures' "${RSYNC_BASE[@]}" -z "$figures" "$tetra/"
        fi
    else
        warn "$figures 없음, figures 백업 건너뜀"
    fi
else
    log "$tetra 없음, 건너뜀"
fi

# ---------------------------------------------------------------------- 정리
if (( ${#FAILED[@]} > 0 )); then
    warn "실패 ${#FAILED[@]}건: ${FAILED[*]}"
    exit 1
fi
log '백업 완료'
