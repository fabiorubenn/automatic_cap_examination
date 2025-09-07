import csv
import os
import pandas as pd
from io import StringIO

# directory_to_search = "D:\\Github\\EnsembleCNN\\KCData-C3C4\\examined_final_files\\All_CSV_files\\Completely new subjects\\Corrected\\Output annotations"
# directory_to_search_annotations = "D:\\Github\\EnsembleCNN\\KCData-C3C4\\examined_final_files\\All annotations\\Completely new subjects"

#directory_to_search = "D:\Github\EnsembleCNN\KC_OSA\OSA_V2\data\EEG csv"
#directory_to_search_annotations = "D:\Github\EnsembleCNN\KC_OSA\OSA_V2\data\Annotations every second"

#directory_to_search = 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA Ana\Group 1 OSA-Control\CSV'
#directory_to_search = 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA Ana\Group 2 OSA-PTSD\CSV'
directory_to_search = 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA KCL\Csv'
#directory_to_search_annotations = "D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA Ana\Group 1 OSA-Control\Annotations every second"
#directory_to_search_annotations = "D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA Ana\Group 2 OSA-PTSD\Annotations every second"
directory_to_search_annotations = "D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA KCL\Annotations every second"

mapping = {'W': 0, 'REM': 0, 'N1': 1, 'N2': 2, 'N3': 3}

# List all files in the folders
files = os.listdir(directory_to_search)
files_annotations = os.listdir(directory_to_search_annotations)

# Iterate over each file in the main directory
for file_name in files:
    # Check if the file ends with "_accumulative_annotations_corrected.csv"
    if file_name.endswith("_accumulative_annotations_corrected.csv"):
        # Extract the subject code from the file name
        subject_code = file_name.split("resampled ")[1].split("_C")[0]
        print("Subject Code:", subject_code)
        
        # Check if there's a corresponding annotation file
        for annotation_file_name in files_annotations:
            if annotation_file_name.startswith(subject_code) and annotation_file_name.endswith(".csv"):
                print("Annotation File Name:", annotation_file_name)
                
                # Load content of the CSV file
                with open(os.path.join(directory_to_search, file_name), 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    annotation_content_with_a_phases = [row for row in csv_reader]
                
                # Load content of the annotation file
                with open(os.path.join(directory_to_search_annotations, annotation_file_name), 'r') as annotation_file:
                    annotation_content_with_sleep_stages = annotation_file.read()

                break  
        
        annotation_content_with_sleep_stages_df = pd.read_csv(StringIO(annotation_content_with_sleep_stages))
        # Extract the last column (Description)
        annotation_content_with_sleep_stages_df = annotation_content_with_sleep_stages_df['Description']
        
        # Apply mapping to the Description column
        annotation_content_with_sleep_stages_df = annotation_content_with_sleep_stages_df.map(mapping)
        
        # Convert annotation_content_with_a_phases to DataFrame
        annotation_content_with_a_phases_df = pd.DataFrame(annotation_content_with_a_phases, columns=["Line Number", "Phase", "Duration"]).drop(0)
        
        # Create a copy of the DataFrame
        annotation_content_with_a_phases_df_n1 = annotation_content_with_a_phases_df.copy()
        annotation_content_with_a_phases_df_n2 = annotation_content_with_a_phases_df.copy()
        annotation_content_with_a_phases_df_n3 = annotation_content_with_a_phases_df.copy()
        
        for slee_stage in range (1, 4):
            # Iterate over each row in the DataFrame
            for index, row in annotation_content_with_a_phases_df.iterrows():
                index_number = row['Line Number']
                
                # Check if the index number exists in annotation_content_with_sleep_stages_df and is associated with a value of 1
                if int(index_number) not in annotation_content_with_sleep_stages_df.index or annotation_content_with_sleep_stages_df[int(index_number)] != slee_stage:
                    # Drop the row if the condition is not met
                    if slee_stage == 1:
                        annotation_content_with_a_phases_df_n1.drop(index, inplace=True)
                    elif slee_stage == 2:
                        annotation_content_with_a_phases_df_n2.drop(index, inplace=True)
                    else:
                        annotation_content_with_a_phases_df_n3.drop(index, inplace=True)
            # Define the new file name
            new_file_name = file_name.replace(".csv", "_sleep_stage_N" + str(slee_stage) + ".csv")
            
            # Save the DataFrame to a CSV file with the new file name
            if slee_stage == 1:
                annotation_content_with_a_phases_df_n1.to_csv(os.path.join(directory_to_search, new_file_name), index=False)
            elif slee_stage == 2:
                annotation_content_with_a_phases_df_n2.to_csv(os.path.join(directory_to_search, new_file_name), index=False)
            else:
                annotation_content_with_a_phases_df_n3.to_csv(os.path.join(directory_to_search, new_file_name), index=False)
            print("Profuced file: ", new_file_name)
