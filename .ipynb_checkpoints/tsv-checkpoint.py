import pandas as pd
import matplotlib.pyplot as plt
import sys

def plot_merged_tsv(filenames):
    """
    Reads TSV files, merges their data based on elements, and plots the merged result.
    
    Parameters:
    - filenames: List of filenames of the TSV files.
    """
    # Data structure to hold merged data: {element: {property: value}}
    merged_data = {}

    # Read and merge the data from each file
    for file in filenames:
        # Extract property name from the filename, assuming it's before the first '_'
        property_name = file.split('/')[-1].split('_')[0]
        
        # Read the TSV file
        df = pd.read_csv(file, delimiter='\t', index_col=0)
        
        # Assuming the first row represents the property values for each element
        for element, value in df.iloc[0].items():
            if element not in merged_data:
                merged_data[element] = {}
            merged_data[element][property_name] = value

    # Convert merged data to DataFrame for plotting
    df_merged = pd.DataFrame(merged_data).T  # Transpose to have elements as rows and properties as columns

    plt.figure(figsize=(14, 8))
    
    # Plot each property
    for property_name in df_merged.columns:
        plt.plot(df_merged.index, df_merged[property_name], marker='o', linestyle='-', label=property_name)
    
    plt.title('Properties Across Elements')
    plt.xlabel('Elements')
    plt.ylabel('Property Value')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        plot_merged_tsv(sys.argv[1:])
    else:
        print("Please specify the TSV files to be plotted.")
