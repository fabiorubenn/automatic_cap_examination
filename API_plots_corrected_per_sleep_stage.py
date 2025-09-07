import csv
import os 
import numpy as np
import math 

def CalculateNerRealTIme (A, N, AphaseIndex):
    ContingA=0
    ContingN=0
    ContingAInd=0
    ContingNInd=0
    indes = 0
    for k in range (0, len(A), 1):
        if A[k] > 0:
            ContingA+=1
            ContingAInd+=1
        if N[k] > 0:
            ContingN+=1 
            ContingNInd+=1
        if ContingN > 0:
            AphaseIndex[k]=ContingA/ContingN
        indes+=1
    return AphaseIndex
        
def CalculateAccumulation (time, A, N, AphaseIndexInd):
    ContingA=0
    ContingN=0
    ContingAInd=0
    ContingNInd=0
    indes = 0
    inc=0
    for k in range (0, len(A), 1):
        if A[k] > 0:
            ContingA+=1
            ContingAInd+=1
        if N[k] > 0:
            ContingN+=1 
            ContingNInd+=1
        if indes == time:
            indes = 0
            if ContingNInd > 0:
                AphaseIndexInd[inc]=ContingAInd/ContingNInd
            ContingAInd=0
            ContingNInd=0 
            inc+=1
        indes+=1
    return AphaseIndexInd

# directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 4 (RBD) missing"
# directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Completely new subjects"
# directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 1 (Fibro)"
# directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 2 (NT)"
# directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 3 (NREM)"
# directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 4 (RBD)"
#directory_to_search = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All_CSV_files\Group 5 (Control)"

#directory_to_search = "D:\Github\EnsembleCNN\KC_OSA\OSA_V2\data\EEG csv"

#directory_to_search = 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA Ana\Group 1 OSA-Control\CSV'
#directory_to_search = 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA Ana\Group 2 OSA-PTSD\CSV'
directory_to_search = 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA KCL\Csv'

os.chdir(directory_to_search) 
all_files = os.listdir(directory_to_search)


# directory_to_search_annotations = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All annotations\Group 4 (RBD) missing"
# directory_to_search_annotations = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All annotations\Completely new subjects"
# directory_to_search_annotations = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All annotations\Group 1 (Fibro)"
# directory_to_search_annotations = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All annotations\Group 2 (NT)"
# directory_to_search_annotations = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All annotations\Group 3 (NREM)"
# directory_to_search_annotations = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All annotations\Group 4 (RBD)"
#directory_to_search_annotations = "D:\Github\EnsembleCNN\KCData-C3C4\examined_final_files\All annotations\Group 5 (Control)"
#directory_to_search_annotations = "D:\Github\EnsembleCNN\KC_OSA\OSA_V2\data\Annotations every second"

#directory_to_search_annotations = "D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA Ana\Group 1 OSA-Control\Annotations every second"
#directory_to_search_annotations = "D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA Ana\Group 2 OSA-PTSD\Annotations every second"
directory_to_search_annotations = "D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA KCL\Annotations every second"


# Create a mapping dictionary
mapping = {'W': 0, 'REM': 0, 'N1': 1, 'N2': 2, 'N3': 3}

for sleep_stage in range(1, 4):
    
    for classifier_selection in range(0,4,1):
        
        
        API_MetricsAverages=np.zeros(5)
        API_MetricsAveragesAfterCorrection=np.zeros(5)
        
        os.chdir(directory_to_search) 
        
        time30s = 30 # value in seconds for the acumulation
        time60s = 60 
        time30m = 60*30 
        time60m = 60*60 
        
        # matching_files = [filename for filename in all_files if filename.endswith("_notA1Phaseall_subtypes_corrected.csv")]
        matching_files = [filename for filename in all_files if filename.endswith("_all_subtypes_corrected.csv")]
        
        for input_csv_file in matching_files:
    
            data = np.genfromtxt(input_csv_file, delimiter=',', skip_header=False)
        
            print("\n\n\nA phase: ", classifier_selection)    
            if classifier_selection == 0: # A phase
                data[data > 0] = 1
            elif classifier_selection == 1: # A1
                data[data > 1] = 0
            elif classifier_selection == 2: # A2
                data[data < 2] = 0
                data[data > 2] = 0
            else: # A3
                data[data < 3] = 0
    
    
            if input_csv_file.find("_C4") != -1:
                # Extract number code from the current file name using regular expression
                number = input_csv_file.replace("standardized and resampled ", "").replace("_C4", "")
                # number = number.replace("_notA1Phaseall_subtypes_corrected.csv", "")
                number = number.replace("_all_subtypes_corrected.csv", "")
                csv_file_to_search = f"standardized and resampled {number}_C4_notA3Phase_A3Phase_REMWARE_NREM_from_database.csv"
            else:
                number = input_csv_file.replace("standardized and resampled ", "").replace("_C3", "")
                # number = number.replace("_notA1Phaseall_subtypes_corrected.csv", "")
                number = number.replace("_all_subtypes_corrected.csv", "")
                csv_file_to_search = f"standardized and resampled {number}_C3_notA3Phase_A3Phase_REMWARE_NREM_from_database.csv"
            
    
            matching_csv_files = [file for file in os.listdir(directory_to_search) if file.endswith(".csv") and csv_file_to_search in file]
            forecast = np.array(np.genfromtxt(matching_csv_files[0], delimiter=',')).astype(int)
                    
            # From the model predictions
            A = data
            N = forecast
            
            
            ######### Per sleep stage
            
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
            
            # From the model predictions
            A = np.where(labels_macro != sleep_stage, 0, A)
            N = np.where(labels_macro != sleep_stage, 0, N) 
            
            #####
     

            AphaseIndex = np.zeros((len(A)))
            AphaseIndex = CalculateNerRealTIme (A, N, AphaseIndex)
            AphaseInde30s = np.zeros(math.ceil((len(N)/(time30s)))-1)
            AphaseInde30s = CalculateAccumulation (time30s, A, N, AphaseInde30s)
            AphaseInde60s = np.zeros(math.ceil((len(N)/(time60s)))-1)
            AphaseInde60s = CalculateAccumulation (time60s, A, N, AphaseInde60s)
            AphaseInde30m = np.zeros(math.ceil((len(N)/(time30m)))-1)
            AphaseInde30m = CalculateAccumulation (time30m, A, N, AphaseInde30m)
            AphaseInde60m = np.zeros(math.ceil((len(N)/(time60m)))-1)
            AphaseInde60m = CalculateAccumulation (time60m, A, N, AphaseInde60m)
            
            API_MetricsAverages[0] = np.mean(AphaseIndex)*100
            API_MetricsAverages[1] = np.mean(AphaseInde30s)*100
            API_MetricsAverages[2] = np.mean(AphaseInde60s)*100
            API_MetricsAverages[3] = np.mean(AphaseInde30m)*100
            API_MetricsAverages[4] = np.mean(AphaseInde60m)*100
            
            if classifier_selection == 0:
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_AphaseIndexPlot_NearRealTime_corrected.csv", AphaseIndex, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_AphaseIndexPlot_30seconds_corrected.csv", AphaseInde30s, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_AphaseIndexPlot_60seconds_corrected.csv", AphaseInde60s, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_AphaseIndexPlot_30minutes_corrected.csv", AphaseInde30m, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_AphaseIndexPlot_60minutes_corrected.csv", AphaseInde60m, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_AphaseIndexMetrics_notCorrected_NRT_30s_30m_60s_60m_corrected.csv", AphaseInde60m, delimiter=",")
            elif classifier_selection == 1:
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_A1phaseIndexPlot_NearRealTime_corrected.csv", AphaseIndex, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_A1phaseIndexPlot_30seconds_corrected.csv", AphaseInde30s, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_A1phaseIndexPlot_60seconds_corrected.csv", AphaseInde60s, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_A1phaseIndexPlot_30minutes_corrected.csv", AphaseInde30m, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_A1phaseIndexPlot_60minutes_corrected.csv", AphaseInde60m, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_A1phaseIndexMetrics_notCorrected_NRT_30s_30m_60s_60m_corrected.csv", AphaseInde60m, delimiter=",")
            elif classifier_selection == 2:
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_A2phaseIndexPlot_NearRealTime_corrected.csv", AphaseIndex, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_A2phaseIndexPlot_30seconds_corrected.csv", AphaseInde30s, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_A2phaseIndexPlot_60seconds_corrected.csv", AphaseInde60s, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_A2phaseIndexPlot_30minutes_corrected.csv", AphaseInde30m, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_A2phaseIndexPlot_60minutes_corrected.csv", AphaseInde60m, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_A2phaseIndexMetrics_notCorrected_NRT_30s_30m_60s_60m_corrected.csv", AphaseInde60m, delimiter=",")
            else:
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_A3phaseIndexPlot_NearRealTime_corrected.csv", AphaseIndex, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_A3phaseIndexPlot_30seconds_corrected.csv", AphaseInde30s, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_A3phaseIndexPlot_60seconds_corrected.csv", AphaseInde60s, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_A3phaseIndexPlot_30minutes_corrected.csv", AphaseInde30m, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_A3phaseIndexPlot_60minutes_corrected.csv", AphaseInde60m, delimiter=",")
                np.savetxt(input_csv_file[:-4] + "_sleep_stage_N" + str(sleep_stage) + "_A3phaseIndexMetrics_notCorrected_NRT_30s_30m_60s_60m_corrected.csv", AphaseInde60m, delimiter=",")
