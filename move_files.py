import os
import shutil






#folder_to_organize = "Completely new subjects"
#folder_to_organize = "Group 1 (Fibro)"
#folder_to_organize = "Group 2 (NT)"
#folder_to_organize = "Group 3 (NREM)"
#folder_to_organize = "Group 4 (RBD)"
#folder_to_organize = "Group 4 (RBD) missing"
# folder_to_organize = "Group 5 (Control)"

#folder_to_organize = "EEG csv"
#folder_to_organize = 'Csv'
folder_to_organize = 'CSV'






def move_files(source_folder, destination_folder, extension=".csv"):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate through files in the source folder
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(extension):
            source_path = os.path.join(source_folder, filename)
            destination_path = os.path.join(destination_folder, filename)
            try:
                # Move the file to the destination folder
                shutil.move(source_path, destination_path)
                print(f"Moved '{filename}' to '{destination_folder}'")
            except Exception as e:
                print(f"Error moving '{filename}': {e}")





# Specify your source folder of the files
#source_folder = "D:\\Github\\EnsembleCNN\\KCData-C3C4\\examined_final_files\\All_CSV_files\\" + folder_to_organize
#source_folder = "D:\\Github\\EnsembleCNN\\KC_OSA\\OSA_V2\\data\\" + folder_to_organize


#source_folder = "D:\\Github\\EnsembleCNN\\KC_06_2025\\OneDrive_1_03-06-2025\\OSA KCL\\" + folder_to_organize
#source_folder = "D:\\Github\\EnsembleCNN\\KC_06_2025\\OneDrive_1_03-06-2025\\OSA Ana\\Group 2 OSA-PTSD\\" + folder_to_organize
source_folder = "D:\\Github\\EnsembleCNN\\KC_06_2025\\OneDrive_1_03-06-2025\\OSA Ana\\Group 1 OSA-Control\\" + folder_to_organize



# Specify the destination folder (where .mat files will be moved) and move them
destination_folder = source_folder + "\\Input"
move_files(source_folder, destination_folder, extension=".mat")

# Specify the destination folder (where _corrected.csv files will be moved) and move them
destination_folder = source_folder + "\\Corrected"
move_files(source_folder, destination_folder, extension="_corrected.csv")

# Specify the destination folder (where the ramaining .csv files will be moved) and move them
destination_folder = source_folder + "\\Uncorrected"
move_files(source_folder, destination_folder)


def move_files_with_pattern(source_folder, destination_folder, pattern):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate through files in the source folder
    for filename in os.listdir(source_folder):
        if pattern in filename:
            source_path = os.path.join(source_folder, filename)
            destination_path = os.path.join(destination_folder, filename)
            try:
                # Move the file to the destination folder
                shutil.move(source_path, destination_path)
                print(f"Moved '{filename}' to '{destination_folder}'")
            except Exception as e:
                print(f"Error moving '{filename}': {e}")
         
                
         
            
         
            
# Organize the folders
#source_folder = "D:\\Github\\EnsembleCNN\\KCData-C3C4\\examined_final_files\\All_CSV_files\\"+ folder_to_organize + "\\Corrected"
#source_folder = "D:\\Github\\EnsembleCNN\\KC_OSA\\OSA_V2\\data\\" + folder_to_organize + "\\Corrected"
#source_folder = "D:\\Github\\EnsembleCNN\\KC_06_2025\\OneDrive_1_03-06-2025\\OSA KCL\\" + folder_to_organize  + "\\Corrected"
#source_folder = "D:\\Github\\EnsembleCNN\\KC_06_2025\\OneDrive_1_03-06-2025\\OSA Ana\\Group 2 OSA-PTSD\\" + folder_to_organize  + "\\Corrected"
source_folder = "D:\\Github\\EnsembleCNN\\KC_06_2025\\OneDrive_1_03-06-2025\\OSA Ana\\Group 1 OSA-Control\\" + folder_to_organize  + "\\Corrected"



destination_folder = source_folder + "\\N1 API"
move_files_with_pattern(source_folder, destination_folder, pattern="_N1_")
destination_folder = source_folder + "\\N2 API"
move_files_with_pattern(source_folder, destination_folder, pattern="_N2_")
destination_folder = source_folder + "\\N3 API"
move_files_with_pattern(source_folder, destination_folder, pattern="_N3_")
destination_folder = source_folder + "\\Non-REM API"
move_files_with_pattern(source_folder, destination_folder, pattern="phaseIndex")
destination_folder = source_folder + "\\Output annotations"
move_files(source_folder, destination_folder)






#source_folder = "D:\\Github\\EnsembleCNN\\KCData-C3C4\\examined_final_files\\All_CSV_files\\"+ folder_to_organize + "\\Uncorrected"
#source_folder = "D:\\Github\\EnsembleCNN\\KC_OSA\\OSA_V2\\data\\" + folder_to_organize + "\\Uncorrected"
#source_folder = "D:\\Github\\EnsembleCNN\\KC_06_2025\\OneDrive_1_03-06-2025\\OSA KCL\\" + folder_to_organize  + "\\Uncorrected"
#source_folder = "D:\\Github\\EnsembleCNN\\KC_06_2025\\OneDrive_1_03-06-2025\\OSA Ana\\Group 2 OSA-PTSD\\" + folder_to_organize  + "\\Uncorrected"
source_folder = "D:\\Github\\EnsembleCNN\\KC_06_2025\\OneDrive_1_03-06-2025\\OSA Ana\\Group 1 OSA-Control\\" + folder_to_organize  + "\\Uncorrected"



destination_folder = source_folder + "\\N1 API"
move_files_with_pattern(source_folder, destination_folder, pattern="_N1_")
destination_folder = source_folder + "\\N2 API"
move_files_with_pattern(source_folder, destination_folder, pattern="_N2_")
destination_folder = source_folder + "\\N3 API"
move_files_with_pattern(source_folder, destination_folder, pattern="_N3_")
destination_folder = source_folder + "\\Non-REM API"
move_files_with_pattern(source_folder, destination_folder, pattern="phaseIndex")
destination_folder = source_folder + "\\Output annotations"
move_files(source_folder, destination_folder)