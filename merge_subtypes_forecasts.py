import csv
import os
import numpy as np
from collections import Counter

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
#directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 1 (Fibro)"
#directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 2 (NT)"
#directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 3 (NREM)"
#directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 4 (RBD)"
#directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 5 (Control)"

# directory_to_search = "D:\Github\EnsembleCNN\KC_OSA\KCL OSA data"
#directory_to_search = "D:\Github\EnsembleCNN\KC_OSA\OSA_V2\data\EEG csv"

#directory_to_search = 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA Ana\Group 1 OSA-Control\CSV'
#directory_to_search = 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA Ana\Group 2 OSA-PTSD\CSV'
directory_to_search = 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA KCL\Csv'

os.chdir(directory_to_search) 

all_files = os.listdir(directory_to_search)


# Define the file names for the three input CSV files
file1_name = [filename for filename in all_files if filename.endswith("_notA1Phase_A1Phase.csv")]
file2_name = [filename for filename in all_files if filename.endswith("_notA2Phase_A2Phase.csv")]
file3_name = [filename for filename in all_files if filename.endswith("_notA3Phase_A3Phase.csv")]
file4_name = [filename for filename in all_files if filename.endswith("_notAPhase_APhase.csv")]



for i in range (len(file1_name)):
    
    count = 0
    
    # Open the input CSV files
    with open(file1_name[i], 'r') as file1, open(file2_name[i], 'r') as file2, open(file3_name[i], 'r') as file3, open(file4_name[i], 'r') as file4:
        # Read the CSV files as lists of lists
        csv_reader1 = list(csv.reader(file1))
        csv_reader2 = list(csv.reader(file2))
        csv_reader3 = list(csv.reader(file3))
        csv_reader4 = list(csv.reader(file4))
        csv_reader1_prob = list(csv.reader(open(file1_name[i][:-22]+"notA1Phase_A1Phase_probabilistic_output.csv")))
        csv_reader2_prob = list(csv.reader(open(file1_name[i][:-22]+"notA2Phase_A2Phase_probabilistic_output.csv")))
        csv_reader3_prob = list(csv.reader(open(file1_name[i][:-22]+"notA3Phase_A3Phase_probabilistic_output.csv")))

        
    # Define the output CSV file name
    output_file_name = file1_name[i][:-22] + 'all_subtypes.csv'
    
    # Initialize an empty list for the output row
    output_row = []
    
    # Create a new CSV file for output
    with open(output_file_name, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        row = 0
        
        # Iterate through the rows of the input lists
        for row1, row2, row3 in zip(csv_reader1, csv_reader2, csv_reader3):
    
            # Iterate through the values in each row and determine the output value
            if float(row1[0]) > 0:
                if  float(row2[0]) > 0 or float(row3[0]) > 0:
                    if float(row2[0]) > 0 and float(row3[0]) > 0: # All 3 subtypes were predicted
                        if csv_reader1_prob[row] >= csv_reader2_prob[row] and csv_reader1_prob[row] >= csv_reader3_prob[row]:
                            output_row.append(1)
                        elif csv_reader2_prob[row] >= csv_reader3_prob[row]:
                            output_row.append(2)
                        else:
                            output_row.append(3)
                    elif float(row2[0]) > 0: # Only A2 and A1
                        if csv_reader1_prob[row] >= csv_reader2_prob[row]:
                            output_row.append(1)
                        else: 
                            output_row.append(2)
                    else: # Only A3 and A1
                        if csv_reader1_prob[row] >= csv_reader3_prob[row]:
                            output_row.append(1)
                        else: 
                            output_row.append(3)
                else:
                    output_row.append(1)
            elif float(row2[0]) > 0:
                if float(row3[0]) > 0: # A2 and A3 
                    if csv_reader2_prob[row] >= csv_reader3_prob[row]:
                        output_row.append(2)
                    else: 
                        output_row.append(3)
                else:
                    output_row.append(2)
            elif float(row3[0]) > 0:
                output_row.append(3)
            else:
                output_row.append(0)  # If none of the input lists have a '1'
            
            row += 1

            
    for k in range (1, len (output_row) - 1): 
        if output_row [k - 1] != output_row [k] and output_row [k + 1] != output_row [k]: 
            output_row [k] = output_row [k - 1]

    count = 1
    for i in range(len(output_row)):
        if output_row[i] > 0:
            count += 1
        else:
            if count >= 2:
                # Find the most frequent value in the sequence
                sequence = output_row[i - count + 1 : i + 1]
                try:
                    most_frequent_num = Counter(sequence).most_common(1)[0][0]
                except IndexError:
                    # Handle the case where the sequence is empty
                    most_frequent_num = 0

                if count <= 60:        
                    for j in range(i - count + 1, i + 1):
                        output_row[j] = most_frequent_num
                else: # Correct longer sequences if alternating classifications
                    for j in range(i - count + 1, i + 1):
                        if output_row[j] != most_frequent_num:
                            output_row[j] = 0
            count = 1
            
    count = 1
    for i in range(len(output_row)):
        if output_row[i] > 0:
            count += 1
        else:
            if count >= 2:
                sequence = output_row[i - count + 1 : i + 1]
                try:
                    most_frequent_num = Counter(sequence).most_common(1)[0][0]
                except IndexError:
                    most_frequent_num = 0
            
                if Counter(sequence).most_common(1)[0][1] > 60: # Correct longer sequences of the same classification
                    for j in range(i - count + 1, i + 1):
                        if float(csv_reader4[j][0]):
                            output_row[j] = most_frequent_num
                        else:
                            output_row[j] = 0
            count = 1
    
    for k in range (1, len (output_row) - 1): 
        if output_row [k - 1] != output_row [k] and output_row [k + 1] != output_row [k] and output_row [k] == 0: 
            output_row [k - 1] = 0

    
    # Wrap each integer in a list before passing it to writerows
    data_to_write = [[value] for value in output_row]
    
    with open(output_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data_to_write)
    
    print(f"Output file '{output_file_name}' has been created.")