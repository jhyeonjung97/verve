import numpy as np
import matplotlib.pyplot as plt

def linear_scaling_oxide(Eo_OH):
    Eo_O = 1.64 * Eo_OH + 1.48
    Eo_OH = 0.61 * Eo_O - 0.90
    Eo_OOH = 0.64 * Eo_O + 2.03
    Go_OH = Eo_OH + 0.35
    Go_O = Eo_O + 0.05
    Go_OOH = Eo_OOH + 0.40
    
    Go1 = Go_OH
    Go2 = Go_O - Go_OH
    Go3 = Go_OOH - Go_O
    Go4 = 4.92 - Go_OOH
    
    Go_max = max(Go1, Go2, Go3, Go4)
    Go_min = min(Go1, Go2, Go3, Go4)
    
    return Go1, Go2, Go3, Go4, Go_max, Go_min

def linear_scaling_metal(Em_OH):
    Em_O = 2 * Em_OH - 0.10
    Em_OOH = 0.53 * Em_O + 3.18
    Gm_OH = Em_OH + 0.35 - 0.20
    Gm_O = Em_O + 0.05
    Gm_OOH = Em_OOH + 0.40 - 0.20

    Gm1 = Gm_OH
    Gm2 = Gm_O - Gm_OH
    Gm3 = Gm_OOH - Gm_O
    Gm4 = 4.92 - Gm_OOH
    
    Gm_max = max(Gm1, Gm2, Gm3, Gm4)
    Gm_min = min(Gm1, Gm2, Gm3, Gm4)

    return Gm1, Gm2, Gm3, Gm4, Gm_max, Gm_min
    
E_OH_values = np.linspace(-2, 4, 300)
Go1_values, Go2_values, Go3_values, Go4_values, Go_max_values, Go_min_values = [], [], [], [], [], []
Gm1_values, Gm2_values, Gm3_values, Gm4_values, Gm_max_values, Gm_min_values = [], [], [], [], [], []

for E_OH in E_OH_values:
    Go1, Go2, Go3, Go4, Go_max, Go_min = linear_scaling_oxide(E_OH)
    Go1_values.append(Go1)
    Go2_values.append(Go2)
    Go3_values.append(Go3)
    Go4_values.append(Go4)
    Go_max_values.append(Go_max)
    Go_min_values.append(Go_min)
    Gm1, Gm2, Gm3, Gm4, Gm_max, Gm_min = linear_scaling_metal(E_OH)
    Gm1_values.append(Gm1)
    Gm2_values.append(Gm2)
    Gm3_values.append(Gm3)
    Gm4_values.append(Gm4)
    Gm_max_values.append(Gm_max)
    Gm_min_values.append(Gm_min)

print(min(Go_max_values)-1.23)
print(min(Gm_max_values)-1.23)

plt.figure(figsize=(8, 6))
plt.xlabel('$E_{OH}$')
plt.ylabel('Energy (eV)')

plt.plot(E_OH_values, Go1_values, label='G1_oxide', linestyle=':', color=(0.67, 0.85, 0.90))
plt.plot(E_OH_values, Go2_values, label='G2_oxide', linestyle=':', color=(0.28, 0.46, 0.71))
plt.plot(E_OH_values, Go3_values, label='G3_oxide', linestyle=':', color=(0.00, 0.40, 0.80))
plt.plot(E_OH_values, Go4_values, label='G4_oxide', linestyle=':', color=(0.00, 0.20, 0.40))
plt.plot(E_OH_values, Go_max_values, label='OER_oxide', color='b')
plt.plot(E_OH_values, Go_min_values, label='ORR_oxide', color='b')
plt.plot(E_OH_values, Gm1_values, label='G1_metal', linestyle=':', color=(1.00, 0.80, 0.60))
plt.plot(E_OH_values, Gm2_values, label='G2_metal', linestyle=':', color=(1.00, 0.60, 0.20))
plt.plot(E_OH_values, Gm3_values, label='G3_metal', linestyle=':', color=(1.00, 0.50, 0.00))
plt.plot(E_OH_values, Gm4_values, label='G4_metal', linestyle=':', color=(0.80, 0.40, 0.00))
plt.plot(E_OH_values, Gm_max_values, label='OER_metal', color='r')
plt.plot(E_OH_values, Gm_min_values, label='ORR_metal', color='r')

plt.xlim(-2, 4)
plt.ylim(4, -1)

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
