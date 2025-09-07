import csv
import os 
import numpy as np
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

# directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 4 (RBD) missing"
# directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Completely new subjects"
# directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 1 (Fibro)"
# directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 2 (NT)"
# directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 3 (NREM)"
# directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 4 (RBD)"
#directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 5 (Control)"

#directory_to_search = "D:\Github\EnsembleCNN\KC_OSA\OSA_V2\data\EEG csv"

directory_to_search = 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA Ana\Group 1 OSA-Control\CSV'
#directory_to_search = 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA Ana\Group 2 OSA-PTSD\CSV'
#directory_to_search = 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA KCL\Csv'



# directory_to_search_annotations = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All annotations\Group 4 (RBD) missing"
# directory_to_search_annotations = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All annotations\Completely new subjects"
# directory_to_search_annotations = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All annotations\Group 1 (Fibro)"
# directory_to_search_annotations = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All annotations\Group 2 (NT)"
# directory_to_search_annotations = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All annotations\Group 3 (NREM)"
# directory_to_search_annotations = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All annotations\Group 4 (RBD)"
#directory_to_search_annotations = "D:\Github\EnsembleCNN\KC_OSA\OSA_V2\data\Annotations every second"

directory_to_search_annotations = "D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA Ana\Group 1 OSA-Control\Annotations every second"
#directory_to_search_annotations = "D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA Ana\Group 2 OSA-PTSD\Annotations every second"
#directory_to_search_annotations = "D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA KCL\Annotations every second"



# Create a mapping dictionary
mapping = {'W': 0, 'REM': 0, 'N1': 1, 'N2': 1, 'N3': 1}

os.chdir(directory_to_search) 
all_files = os.listdir(directory_to_search)

for a_phase in range (0,4,1): #0 for A-not A, 1 for A1-not A1, 2 for A2-not A2, 3 for A3-not A3

    print("\n\n\nA phase: ", a_phase)    
    if a_phase == 0:
        matching_files = [filename for filename in all_files if filename.endswith("_notAPhase_APhase.csv")]
        annotate = 'A phase'
    elif a_phase == 1:
        matching_files = [filename for filename in all_files if filename.endswith("_notA1Phase_A1Phase.csv")]
        annotate = 'A1 subtype'
    elif a_phase == 2:
        matching_files = [filename for filename in all_files if filename.endswith("_notA2Phase_A2Phase.csv")]
        annotate = 'A2 subtype'
    else:
        matching_files = [filename for filename in all_files if filename.endswith("_notA3Phase_A3Phase.csv")]
        annotate = 'A3 subtype'
    
    for input_csv_file in matching_files:
        if input_csv_file.find("_C4") != -1:
            # Extract number code from the current file name using regular expression
            number = input_csv_file.replace("standardized and resampled ", "").replace("_C4", "")
        else:
            number = input_csv_file.replace("standardized and resampled ", "").replace("_C3", "")
        
        if a_phase == 0:
            number = number.replace("_notAPhase_APhase.csv", "")
        elif a_phase == 1:
            number = number.replace("_notA1Phase_A1Phase.csv", "")
        elif a_phase == 2:
            number = number.replace("_notA2Phase_A2Phase.csv", "")
        else:
            number = number.replace("_notA3Phase_A3Phase.csv", "")

    
        csv_file_to_search = f"{number}.csv"
        # Search for the CSV file
        matching_csv_files = [file for file in os.listdir(directory_to_search_annotations) if file.endswith(".csv") and csv_file_to_search in file]
                
        
        forecast = np.array(np.genfromtxt(input_csv_file, delimiter=',')).astype(int)
        labels_macro = np.genfromtxt(directory_to_search_annotations+'\\'+matching_csv_files[0], delimiter=',', skip_header=1, usecols=-1, dtype=str)
 
        print(len(labels_macro) - len(forecast))
        if len(labels_macro) > len(forecast):
            if len(labels_macro) - len(forecast) < 61:
                if len(labels_macro) - len(forecast) < 30:
                    labels_macro = np.array(labels_macro[30:])
                    forecast = forecast[:len(labels_macro)]
                else:
                    labels_macro = np.array(labels_macro[30:])
                    labels_macro = np.array(labels_macro[:len(forecast)])
            else:
                labels_macro = np.array(labels_macro[30:-31])
        else:
            labels_macro = np.array(labels_macro[30:]) 
            forecast = forecast[:len(labels_macro)]
        
        if len(labels_macro) > len(forecast):
            labels_macro = np.array(labels_macro[:len(forecast)])
            
        print(len(labels_macro) - len(forecast))
        labels_macro = np.where(np.isin(labels_macro, list(mapping.keys())), [mapping[val] for val in labels_macro], labels_macro).astype(int)
        
        
        # Correct values in forecasts based on macro labels
        forecast = np.where(labels_macro == 0, 0, forecast)
        np.savetxt(input_csv_file[:-4] + "_corrected.csv", forecast, delimiter=",") # Save the corrected forecasts
        
       
        
        # Initialize variables to track accumulative annotations
        accumulative_annotations = []
        current_annotation = None
        start_line = None
        

        for line_number, row in enumerate(forecast):
            annotation_str = row  # Assuming the 0s and 1s are in the first column
            annotation = float(annotation_str)
            if annotation > 0:
                if current_annotation is None:
                    start_line = line_number + 1
                    #start_line = line_number
                current_annotation = 1
            else:
                if current_annotation is not None:
                    #end_line = line_number - 1
                    end_line = line_number 
                    duration = end_line - start_line + 1
                    accumulative_annotations.append([start_line, annotate, duration])
                    current_annotation = None
    
        # Save the result to a new CSV file
        output_csv_file = input_csv_file[:-4] + '_accumulative_annotations_corrected.csv'
        with open(output_csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Line Number', 'Phase', 'Duration'])
            writer.writerows(accumulative_annotations)
        
        # Save the NREM-REMorWake to a new CSV file
        np.savetxt(input_csv_file[:-4] + '_REMWARE_NREM_from_database.csv', labels_macro, delimiter=",")
            
