import csv
import os 
#directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\EDF_K_C3-C4\Group 1 (Fibro)"
#directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\EDF_K_C3-C4\Group 2 (NT)"
#directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\EDF_K_C3-C4\Group 3 (NREM)"
#directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\EDF_K_C3-C4\Group 4 (RBD)"
#directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\EDF_K_C3-C4\Group 5 (Control)"


#directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\EDF_K_C3-C4_V2\C3-C4\Group 5 (Control)"
#directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\EDF_K_C3-C4_V2\C3-C4\Group 4 (RBD)"
#directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\EDF_K_C3-C4_V2\C3-C4\Group 3 (NREM)"
#directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\EDF_K_C3-C4_V2\C3-C4\Group 2 (NT)"
#directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\EDF_K_C3-C4_V2\C3-C4\Group 1 (Fibro)"

#directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Completely new subjects"
# directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 1 (Fibro)"
# directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 2 (NT)"
# directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 3 (NREM)"
# directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 4 (RBD)"
# directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 5 (Control)"
# directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 4 (RBD) missing"

# directory_to_search = "D:\Github\EnsembleCNN\KC_OSA\KCL OSA data"
directory_to_search = "D:\Github\EnsembleCNN\KC_OSA\OSA_V2\data\EEG csv"


os.chdir(directory_to_search) 

all_files = os.listdir(directory_to_search)


matching_files = [filename for filename in all_files if filename.endswith("all_subtypes.csv")]


for input_csv_file in matching_files:

    # Initialize variables to track accumulative annotations
    accumulative_annotations = []
    current_annotation = None
    start_line = None
    
    # Open the input CSV file and read it line by line
    with open(input_csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line_number, row in enumerate(reader):
            annotation_str = row[0] 
            annotation = float(annotation_str)
            if annotation > 0:
                if current_annotation is None:
                    start_line = line_number + 1
                    #start_line = line_number
                current_annotation = 1
                annotate = int(annotation_str)
            else:
                if current_annotation is not None:
                    #end_line = line_number - 1
                    end_line = line_number 
                    duration = end_line - start_line + 1
                    accumulative_annotations.append([start_line, annotate, duration])
                    current_annotation = None
    
    # Save the result to a new CSV file
    output_csv_file = input_csv_file[:-4] + '_accumulative_annotations.csv'
    with open(output_csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Line Number', 'Phase', 'Duration'])
        writer.writerows(accumulative_annotations)

print(f"Accumulative annotations saved to {output_csv_file}")