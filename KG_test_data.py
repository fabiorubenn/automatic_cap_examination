"""
##############################################################################
#
# Examine a subject
#
##############################################################################
"""
"""
# import lybraries
"""
import scipy.io as spio  # to load the .mat files with the data
import numpy as np  # for mathematical notation and examination
import tensorflow as tf  # for clearing the secction, realeasing the GPU memory after a training cycle
import os  # to change the working directory
import gc # to release the holded memory in the garbage collector

"""
# Select database
"""

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

#directory_to_search = "D:\Github\EnsembleCNN\KC_OSA\KCL OSA data"
#directory_to_search = "D:\Github\EnsembleCNN\KC_OSA\OSA_V2\data\EEG csv"

#directory_to_search = 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA Ana\Group 1 OSA-Control\CSV'
#directory_to_search = 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA Ana\Group 2 OSA-PTSD\CSV'
directory_to_search = 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA KCL\Csv'


"""
# Control variables
"""
OverLap = [8, 12, 8]  # number of overlapping seconds to be considered in the overlapping windows of A phase analysis (need to be 0 or an odd number), either [0] if no overlapping or [amount of overlapping for right, amount of overlapping for center, amount of overlapping for left] to use overlapping
OverLapH = [16, 14, 16]  # number of overlapping seconds to be considered in the overlapping windows of NREM analysis (need to be 0 or an odd number), either [0] if no overlapping or [amount of overlapping for right, amount of overlapping for center, amount of overlapping for left] to use overlapping


# for A-phase
OverlappingRight = OverLap[0] - 1  # total duration of overlapp to the right, for the A phase analyis, without the epoch related to the label
OverlappingCenter = OverLap[1] - 1  # total duration of overlapp to the right and left, for the A phase analyis, without the epoch related to the label
OverlappingLeft = OverLap[2] - 1  # total duration of overlapp to the left, for the A phase analyis, without the epoch related to the label
overlapingSide = [0, 1, 2]  # if the model should consider overlapping windows, then test the thre considered overlapping scenarios
# for NREM

OverlappingRightH = OverLapH[0] - 1
OverlappingCenterH = OverLapH[1] - 1
OverlappingLeftH = OverLapH[2] - 1
overlapingSideH = [0, 1, 2]



def find_files_with_suffix(directory, suffix):
    matching_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(suffix):
                matching_files.append(os.path.join(root, file))
    
    return matching_files


for classifier_selection in range (0, 4, 1): #0 for A-not A, 1 for A1-not A1, 2 for A2-not A2, 3 for A3-not A3

    print("\n\n\nClassifier: ", classifier_selection)
    
    if directory_to_search[-9:] == '(Control)':
        start = -28 # for Group 5 (Control)
    else:
        start = -24 # for all other groups
    
    
    all_files = os.listdir(directory_to_search)
    matching_files = [filename for filename in all_files if filename.startswith("standardized and resampled") and filename.endswith(".mat")]
    
    for file_path in matching_files:
        tf.keras.backend.clear_session()
        gc.collect() # to release the holded memory in the garbage collector  
        
        #if file_path [27:30] == '62 ':
    
        """
        # create the overlappign data
        """
        for a in range(0, len(overlapingSide), 1):  # test the three overllaping scenarios if overlapping should be considered or only one examine one classifier if overlapping is not considered (OverLap = 0)
            """    
            # load the data
            """
            os.chdir(directory_to_search)  # change the working directory
            
            data = file_path
            mat = spio.loadmat(data, squeeze_me=True)  # load the subject's data
            data = mat.get('resampled')  # dictionary holding the subject's data
            #data = (data - np.mean(data)) / np.std(data)  # standardize the data
        
            os.chdir("D:\Github\EnsembleCNN\Data") 
        
            """
            # produce the overlapping scenarios for A phase
            """
            Datadata = data # select the variable holding the subject's data
            counting = 0 # conting variable to hold the number of evaluated epochs
            if overlapingSide[a] == 0:  # test overlapping to the right: first 100 points refer to the epoch's label and the remaining poins are overlapping to the right
                features = 100 * (OverlappingRight * 2 + 1)  # number of features fed to the classifier at each epoch
                DatadataV2 = np.zeros(((int(len(Datadata) / 100) - OverlappingRight * 2), OverlappingRight * 2 * 100 + 100))  # variable that will hold the reshaped subject's data
                for x in range(0, int((len(Datadata) / 100 - OverlappingRight * 2 - OverlappingRight)), 1):  # produce the OverlappingRight data for each epoch wheer it is possible to produce data
                    DatadataV2[counting,] = Datadata[(x * 100): (x * 100 + 100) + OverlappingRight * 100 * 2]  # copy the OverlappingRight data to the variable
                    counting = counting + 1  # increase the number of examined subejcts
            elif overlapingSide[a] == 1:  # test overlapping to the left and right: central 100 points refer to the epoch's label and the remaining poins are overlapping to either left or right
                features = 100 * (OverlappingCenter * 2 + 1)
                DatadataV2 = np.zeros(((int(len(Datadata) / 100) - OverlappingCenter * 2), OverlappingCenter * 2 * 100 + 100))
                for x in range(OverlappingCenter, int((len(Datadata) / 100 - OverlappingCenter * 2)), 1):
                    DatadataV2[counting,] = Datadata[(x * 100) - OverlappingCenter * 100: (x * 100 + 100) + OverlappingCenter * 100]
                    counting = counting + 1
            else:  # test overlapping to the left: last 100 points refer to the epoch's label and the remaining poins are overlapping to the left
                features = 100 * (OverlappingLeft * 2 + 1)
                DatadataV2 = np.zeros(((int(len(Datadata) / 100) - OverlappingLeft * 2), OverlappingLeft * 2 * 100 + 100))
                for x in range(0, int((len(Datadata) / 100 - OverlappingLeft * 2 - OverlappingLeft)), 1):
                    DatadataV2[counting,] = Datadata[(x * 100): (x * 100 + 100) + OverlappingLeft * 100 * 2]
                    counting = counting + 1
            dataA = DatadataV2
            """
            # produce the overlapping scenarios for NREM
            """
            Datadata = data
            counting = 0
            if overlapingSideH[a] == 0:
                featuresH = 100 * (OverlappingRightH * 2 + 1)
                DatadataV2 = np.zeros(((int(len(Datadata) / 100) - OverlappingRightH * 2), OverlappingRightH * 2 * 100 + 100))
                for x in range(0, int((len(Datadata) / 100 - OverlappingRightH * 2 - OverlappingRightH)), 1):
                    DatadataV2[counting,] = Datadata[(x * 100): (x * 100 + 100) + OverlappingRightH * 100 * 2]
                    counting = counting + 1
            elif overlapingSideH[a] == 1:
                featuresH = 100 * (OverlappingCenterH * 2 + 1)
                DatadataV2 = np.zeros(((int(len(Datadata) / 100) - OverlappingCenterH * 2), OverlappingCenterH * 2 * 100 + 100))
                for x in range(OverlappingCenterH, int((len(Datadata) / 100 - OverlappingCenterH * 2)), 1):
                    DatadataV2[counting,] = Datadata[(x * 100) - OverlappingCenterH * 100: (x * 100 + 100) + OverlappingCenterH * 100]
                    counting = counting + 1
            else:
                featuresH = 100 * (OverlappingLeftH * 2 + 1)
                DatadataV2 = np.zeros(((int(len(Datadata) / 100) - OverlappingLeftH * 2), OverlappingLeftH * 2 * 100 + 100))
                for x in range(0, int((len(Datadata) / 100 - OverlappingLeftH * 2 - OverlappingLeftH)), 1):
                    DatadataV2[counting,] = Datadata[(x * 100): (x * 100 + 100) + OverlappingLeftH * 100 * 2]
                    counting = counting + 1
            dataH = DatadataV2
            """
            # A phase classification
            """
            XTest = dataA.reshape(len(dataA), features, 1)
            if classifier_selection == 0:
                model = tf.keras.models.load_model('insAPhase_OverlappingSide_' + str (overlapingSide [a]) + "_subject_" + str(1) +"_epoch_" + str(0)) # load the trained model
            elif classifier_selection == 1: 
                model = tf.keras.models.load_model('new_ins_subtype_1_APhase_OverlappingSide_' + str (overlapingSide [a]) + "_subject_" + str(1) +"_epoch_" + str(0)) # load the trained model
            elif classifier_selection == 2:
                model = tf.keras.models.load_model('new_ins_subtype_2_APhase_OverlappingSide_' + str (overlapingSide [a]) + "_subject_" + str(1) +"_epoch_" + str(0)) # load the trained model
            else:
                model = tf.keras.models.load_model('new_ins_subtype_3_APhase_OverlappingSide_' + str (overlapingSide [a]) + "_subject_" + str(1) +"_epoch_" + str(0)) # load the trained model
            #model = tf.keras.models.load_model('nfleAPhase_OverlappingSide_' + str (overlapingSide [a]) + "_subject_" + str(1) +"_epoch_" + str(0)) # load the trained model
            proba = model.predict(XTest)  # estimate the probability of the labels of the testing set
            predictiony_pred = np.zeros(len(XTest))  # variable that will hold the A phase labels predicted by the classifier
            for x in range(len(XTest)):  # check all epochs
                if proba[x, 0] > 0.5:  # examine the classification threshold
                    predictiony_pred[x] = 0  # predicted not-A
                else:
                    predictiony_pred[x] = 1  # predicted A
            capPredictedPredicted = predictiony_pred  # save the A phase predictions
            """
            # post-processing procedure
            """
            for k in range(len(capPredictedPredicted) - 1):  # check the classified epochs to be corrected
                if k > 0:  # the procedure cannot be applied to the first and last epoch because it consides the previous and next epoch for the correction
                    if capPredictedPredicted[k - 1] == 0 and capPredictedPredicted[k] == 1 and capPredictedPredicted[k + 1] == 0:  # correct 010 to 000
                        capPredictedPredicted[k] = 0  # corrected label
            for k in range(len(capPredictedPredicted) - 1):
                if k > 0:
                    if capPredictedPredicted[k - 1] == 1 and capPredictedPredicted[k] == 0 and capPredictedPredicted[k + 1] == 1:  # correct 101 to 111
                        capPredictedPredicted[k] = 1
            if a == 0:  # variable holding the prediction of each CNN composing the classifier ensemble for the A phase estimation
                PredictionYA0 = proba[:, 1]  # results for the overlapping on the right
            elif a == 1:
                PredictionYA1 = proba[:, 1]  # results for the overlapping on the left and right
            else:
                PredictionYA2 = proba[:, 1]  # results for the overlapping on the left
        
            """
            # NREM classification
            """
            XTestH = dataH
            XTestH = XTestH.reshape(len(XTestH), featuresH, 1)
            if classifier_selection == 0:
                model = tf.keras.models.load_model('insNREM_OverlappingSide_' + str (overlapingSide [a]) + "_subject_" + str(1) +"_epoch_" + str(0)) 
            elif classifier_selection == 1: 
                model = tf.keras.models.load_model('new_ins_subtype_1_NREM_OverlappingSide_' + str (overlapingSide [a]) + "_subject_" + str(1) +"_epoch_" + str(0)) 
            elif classifier_selection == 2: 
                model = tf.keras.models.load_model('new_ins_subtype_2_NREM_OverlappingSide_' + str (overlapingSide [a]) + "_subject_" + str(1) +"_epoch_" + str(0)) 
            else:
                model = tf.keras.models.load_model('new_ins_subtype_3_NREM_OverlappingSide_' + str (overlapingSide [a]) + "_subject_" + str(1) +"_epoch_" + str(0)) 
            proba2 = model.predict(XTestH)
            predictiony_predh = np.zeros(len(XTestH))
            for x in range(len(XTestH)):
                if proba2[x, 0] > 0.5:
                    predictiony_predh[x] = 0
                else:
                    predictiony_predh[x] = 1
            capPredictedPredictedh = predictiony_predh
            for k in range(len(capPredictedPredictedh) - 1):
                if k > 0:
                    if capPredictedPredictedh[k - 1] == 0 and capPredictedPredictedh[k] == 1 and capPredictedPredictedh[k + 1] == 0:
                        capPredictedPredictedh[k] = 0
        
            for k in range(len(capPredictedPredictedh) - 1):
                if k > 0:
                    if capPredictedPredictedh[k - 1] == 1 and capPredictedPredictedh[k] == 0 and capPredictedPredictedh[k + 1] == 1:
                        capPredictedPredictedh[k] = 1
            if a == 0:
                PredictionYN0 = proba2[:, 1]
            elif a == 1:
                PredictionYN1 = proba2[:, 1]
            else:
                PredictionYN2 = proba2[:, 1]
            """
            # Examine the CAP cycles
            """
            examineCAP = 0  # variable to controle when the model can perform the CAP cycle examination
            if a > 1:  # already checked the tree types of overlapping and now it is going for the majority voting to combine the information
                """
                # algiment contant for the A phase and NREM
                """
                # align corection for the right
                if OverlappingRight * 2 >= OverlappingCenter:
                    if OverlappingRightH * 2 >= OverlappingCenterH:
                        if OverlappingRight * 2 >= OverlappingRightH * 2:
                            CorrectRightA = 0
                            CorrectRightH = OverlappingRight * 2 - OverlappingRightH * 2
                        else:
                            CorrectRightA = OverlappingRightH * 2 - OverlappingRight * 2
                            CorrectRightH = 0
                    else:
                        if OverlappingRight * 2 >= OverlappingCenterH * 2:
                            CorrectRightA = 0
                            CorrectRightH = OverlappingRight * 2 - OverlappingCenterH * 2
                        else:
                            CorrectRightA = OverlappingCenterH * 2 - OverlappingRight * 2
                            CorrectRightH = 0
                else:
                    if OverlappingRightH * 2 >= OverlappingCenterH:
                        if OverlappingCenter * 2 >= OverlappingRightH * 2:
                            CorrectRightA = 0
                            CorrectRightH = OverlappingCenter * 2 - OverlappingRightH * 2
                        else:
                            CorrectRightA = OverlappingRightH * 2 - OverlappingCenter * 2
                            CorrectRightH = 0
                    else:
                        if OverlappingCenter * 2 >= OverlappingCenterH * 2:
                            CorrectRightA = 0
                            CorrectRightH = OverlappingCenter * 2 - OverlappingCenterH * 2
                        else:
                            CorrectRightA = OverlappingCenterH * 2 - OverlappingCenter * 2
                            CorrectRightH = 0
                # align corection for the left
                if OverlappingLeft * 2 >= OverlappingCenter:
                    if OverlappingLeftH * 2 >= OverlappingCenterH:
                        if OverlappingLeft * 2 >= OverlappingLeftH * 2:
                            CorrectLeftA = 0
                            CorrectLeftH = OverlappingLeft * 2 - OverlappingLeftH * 2
                        else:
                            CorrectLeftA = OverlappingLeftH * 2 - OverlappingLeft * 2
                            CorrectLeftH = 0
                    else:
                        if OverlappingLeft * 2 >= OverlappingCenterH * 2:
                            CorrectLeftA = 0
                            CorrectLeftH = OverlappingLeft * 2 - OverlappingCenterH * 2
                        else:
                            CorrectLeftA = OverlappingCenterH * 2 - OverlappingLeft * 2
                            CorrectLeftH = 0
                else:
                    if OverlappingLeftH * 2 >= OverlappingCenterH:
                        if OverlappingCenter * 2 >= OverlappingLeftH * 2:
                            CorrectLeftA = 0
                            CorrectLeftH = OverlappingCenter * 2 - OverlappingLeftH * 2
                        else:
                            CorrectLeftA = OverlappingLeftH * 2 - OverlappingCenter * 2
                            CorrectLeftH = 0
                    else:
                        if OverlappingCenter * 2 >= OverlappingCenterH * 2:
                            CorrectLeftA = 0
                            CorrectLeftH = OverlappingCenter * 2 - OverlappingCenterH * 2
                        else:
                            CorrectLeftA = OverlappingCenterH * 2 - OverlappingCenter * 2
                            CorrectLeftH = 0
                """
                # create the array with the classified epochs, if no overlapping was used then two of the prediction arrays will composed of only zeros and the majority voting will copy the results of either the A phase or the NREM assessment
                """
                # align the labels
                if OverlappingRight * 2 >= OverlappingCenter:  # identify the largest overlapping to the right
                    OverlappingRightCorrectR = 0
                    OverlappingCenterCorrectR = (OverlappingRight * 2) - OverlappingCenter
                    OverlappingLeftCorrectR = OverlappingRight * 2
                else:
                    OverlappingRightCorrectR = OverlappingCenter - (OverlappingRight * 2)
                    OverlappingCenterCorrectR = 0
                    OverlappingLeftCorrectR = OverlappingCenter
                if OverlappingLeft * 2 >= OverlappingCenter:  # identify the largest overlapping to the left
                    OverlappingRightCorrectL = OverlappingLeft * 2
                    OverlappingCenterCorrectL = (OverlappingLeft * 2) - OverlappingCenter
                    OverlappingLeftCorrectL = 0
                else:
                    OverlappingRightCorrectL = OverlappingCenter * 2
                    OverlappingCenterCorrectL = 0
                    OverlappingLeftCorrectL = (OverlappingCenter * 2) - OverlappingLeft
                PredictionYA0R = PredictionYA0[OverlappingRightCorrectL: len(PredictionYA0) - OverlappingRightCorrectR]  # overlapping right
                PredictionYA1R = PredictionYA1[OverlappingCenterCorrectL: len(PredictionYA1) - OverlappingCenterCorrectR]  # overlapping center
                PredictionYA2R = PredictionYA2[OverlappingLeftCorrectL: len(PredictionYA2) - OverlappingLeftCorrectR]  # overlapping left
                PredictionYA3 = np.asarray([PredictionYA0R, PredictionYA1R, PredictionYA2R])  # combine the three arrays to form a matrix
                PredictionYA3 = PredictionYA3[:, CorrectRightA: len(PredictionYA2R) - CorrectLeftA]  # align the A phase and NREM predictions
                # Weighted voting
                cappredictiony_predhA = np.zeros(len(PredictionYA3[0]))  # arry that wil contain the majority vonting output
                cappredictiony_predhA_prob = np.zeros(len(PredictionYA3[0]))  # arry that wil contain the majority vonting raw output
                for combinationA in range(0, len(cappredictiony_predhA),1):  # check line by line the output of the classifiers
                    cappredictiony_predhATemp = np.sum(PredictionYA3[:, combinationA])
                    if cappredictiony_predhATemp >= 1.5:  # majority voting, if two of the three classifiers predicted 1 then it is 1 otherwise leave the 0
                        cappredictiony_predhA[combinationA] = 1
                        cappredictiony_predhA_prob[combinationA] = cappredictiony_predhATemp
        
                # for NREM
                if OverlappingRightH * 2 >= OverlappingCenterH:  # identify the largest overlapping to the right
                    OverlappingRightCorrectR = 0
                    OverlappingCenterCorrectR = (OverlappingRightH * 2) - OverlappingCenterH
                    OverlappingLeftCorrectR = OverlappingRightH * 2
                else:
                    OverlappingRightCorrectR = OverlappingCenterH - (OverlappingRightH * 2)
                    OverlappingCenterCorrectR = 0
                    OverlappingLeftCorrectR = OverlappingCenterH
                if OverlappingLeftH * 2 >= OverlappingCenterH:  # identify the largest overlapping to the left
                    OverlappingRightCorrectL = OverlappingLeftH * 2
                    OverlappingCenterCorrectL = (OverlappingLeftH * 2) - OverlappingCenterH
                    OverlappingLeftCorrectL = 0
                else:
                    OverlappingRightCorrectL = OverlappingCenterH * 2
                    OverlappingCenterCorrectL = 0
                    OverlappingLeftCorrectL = (OverlappingCenterH * 2) - OverlappingLeftH
                PredictionYN0R = PredictionYN0[OverlappingRightCorrectL: len(PredictionYN0) - OverlappingRightCorrectR]
                PredictionYN1R = PredictionYN1[OverlappingCenterCorrectL: len(PredictionYN1) - OverlappingCenterCorrectR]
                PredictionYN2R = PredictionYN2[OverlappingLeftCorrectL: len(PredictionYN2) - OverlappingLeftCorrectR]
                PredictionYN3 = np.asarray([PredictionYN0R, PredictionYN1R, PredictionYN2R])
                PredictionYN3 = PredictionYN3[:, CorrectRightH: len(PredictionYN2R) - CorrectLeftH]
                cappredictiony_predhN = np.zeros(len(PredictionYN3[0]))
                for combinationN in range(0, len(cappredictiony_predhN), 1):
                    cappredictiony_predhNTemp = np.sum(PredictionYN3[:, combinationN])
                    if cappredictiony_predhNTemp >= 1.5:
                        cappredictiony_predhN[combinationN] = 1
                examineCAP = 1  # perform the CAP examination
                """
                # essemble for the A phase estimation
                """
                for k in range(len(cappredictiony_predhN)):  # decrese the missclassification by converting the classified A phases into not-A when the NREM classifiers indicates a period of REM/wake (A phase can only occur during NREM sleep)
                    if cappredictiony_predhN[k] == 0:
                        cappredictiony_predhA[k] = 0
                for k in range(len(cappredictiony_predhA) - 1):
                    if k > 0:
                        if cappredictiony_predhA[k - 1] == 0 and cappredictiony_predhA[k] == 1 and cappredictiony_predhA[k + 1] == 0:
                            cappredictiony_predhA[k] = 0
        
                for k in range(len(cappredictiony_predhA) - 1):
                    if k > 0:
                        if cappredictiony_predhA[k - 1] == 1 and cappredictiony_predhA[k] == 0 and cappredictiony_predhA[k + 1] == 1:
                            cappredictiony_predhA[k] = 1
        
                """
                # essemble for the NREM estimation
                """
                for k in range(len(cappredictiony_predhN) - 1):
                    if k > 0:
                        if cappredictiony_predhN[k - 1] == 0 and cappredictiony_predhN[k] == 1 and cappredictiony_predhN[k + 1] == 0:
                            cappredictiony_predhN[k] = 0
        
                for k in range(len(cappredictiony_predhN) - 1):
                    if k > 0:
                        if cappredictiony_predhN[k - 1] == 1 and cappredictiony_predhN[k] == 0 and cappredictiony_predhN[k + 1] == 1:
                            cappredictiony_predhN[k] = 1
        
            """
            # classify the CAP cycles with the Finite State Machine (FSM)
            """
            if examineCAP == 1:
                # CAP cycles predicted from the estimated A phase
                searchval = 1  # look for A phase, corresponding to 1, while not-A is 0
                predictedCAP = np.copy(cappredictiony_predhA)  # variable to be examined by the FSM, holding the classified A phase locations
                capPredicted = np.zeros(len(predictedCAP))  # variable to hold the FSM results
                ii = np.where(predictedCAP == searchval)[0]  # find the index of all A phases
                jj = [t - s for s, t in zip(ii, ii[1:])]  # find the duration all A phases
                counting = 0  # variable to control the maximum duration of the identified A phase is lower than 60 s
                for i in range(len(ii)):  # examine all identified A phases
                    if i < len(ii) - 1:  # examine untli the last identified A phase
                        if jj[i] == 1:  # identified A phase, 1 indicated that the diference from the previous A phase epoch is 1 s so it is still the same A phase
                            capPredicted[ii[i]] = 4  # score as 4 to mark as a candidate for valid A phase of a CAP cycle
                        elif jj[i] <= 60:  # if the difference is not 1 then it finished the A phase and this new idenfified A phase needs to be less than 60 s apart from the previous to be a valid CAP cycle
                            capPredicted[capPredicted == 4] = 2  # score as 2 to mark as a candidate for valid CAP cycle
                            capPredicted[ii[i]: ii[i + 1]] = 2  # score the B phase, that is between the A phases as 2 to be aprt of the CAP cycle
                            counting = counting + 1  # increasse the number of candidates for valid CAP cycle identified
                        elif counting >= 2:  # if the difference between teo A phases is longer than 60 s then it finiched the CAP sequence, and if at least two CAP cycles were idenfied as candidate for valid CAP cycle then a correct CAP cycle was found
                            capPredicted[capPredicted == 2] = 1  # convert the scores 2 to 1 to indicate that a valid CAP cycle was found
                            capPredicted[capPredicted == 4] = 0  # convert the scores 4 to 0 to eliminate the A phases that were not scored as part of the valid CAP cycles
                            counting = 0  # restart the conting for the valid CAP cycles
                        else:  # the conditions for scoring a valid CAP cycle were not met do clear the scored values
                            capPredicted[capPredicted == 4] = 0  # eliminate the scored A phases that were not part of a valid CAP cycle
                            capPredicted[capPredicted == 2] = 0  # eliminate the CAP cycle that was not valid because a minimum sequence of 2 CAP cycles are required to score the CAP cycles as valid
                            counting = 0  # restart the conting for the valid CAP cycles
                    else:  # finished checking the data for the A phases
                        capPredicted[capPredicted == 4] = 0  # eliminate the scored A phases that were not part of a valid CAP cycle
                        capPredicted[capPredicted == 2] = 0  # eliminate the CAP cycle that was not valid because a minimum sequence of 2 CAP cycles are required to score the CAP cycles as valid
                capPredicted[capPredicted == 2] = 0  # eliminate the CAP cycle that was not valid because a minimum sequence of 2 CAP cycles are required to score the CAP cycles as valid
                # save the CAP assessment results of the cycle
                CAPtotalInter = sum(capPredicted)  # total number of epochs classified as part of a CAP cycle
                
        """
        " API
        """        
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
            
        
        API_MetricsAverages=np.zeros(5)
        API_MetricsAveragesAfterCorrection=np.zeros(5)
        
        os.chdir(directory_to_search) 
        
        time30s = 30 # value in seconds for the acumulation
        time60s = 60 
        time30m = 60*30 
        time60m = 60*60 
            
        # From the model predictions
        A = cappredictiony_predhA
        N = cappredictiony_predhN
        
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
        
        
        start = 0  # Set your starting index here
        
        while start <= len(file_path) - 4:
            try:
                if classifier_selection == 0:
                    np.savetxt(file_path[start:-4] + "_AphaseIndexPlot_NearRealTime.csv", AphaseIndex, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_AphaseIndexPlot_30seconds.csv", AphaseInde30s, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_AphaseIndexPlot_60seconds.csv", AphaseInde60s, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_AphaseIndexPlot_30minutes.csv", AphaseInde30m, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_AphaseIndexPlot_60minutes.csv", AphaseInde60m, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_AphaseIndexMetrics_notCorrected_NRT_30s_30m_60s_60m.csv", AphaseInde60m, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_notAPhase_APhase.csv", A, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_notNREM_NREM.csv", N, delimiter=",")
                elif classifier_selection == 1:
                    np.savetxt(file_path[start:-4] + "_A1phaseIndexPlot_NearRealTime.csv", AphaseIndex, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_A1phaseIndexPlot_30seconds.csv", AphaseInde30s, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_A1phaseIndexPlot_60seconds.csv", AphaseInde60s, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_A1phaseIndexPlot_30minutes.csv", AphaseInde30m, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_A1phaseIndexPlot_60minutes.csv", AphaseInde60m, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_A1phaseIndexMetrics_notCorrected_NRT_30s_30m_60s_60m.csv", AphaseInde60m, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_notA1Phase_A1Phase.csv", A, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_notA1Phase_A1Phase_probabilistic_output.csv", cappredictiony_predhA_prob, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_notNREM_NREM_used_for_A1phase.csv", N, delimiter=",")
                elif classifier_selection == 2:
                    np.savetxt(file_path[start:-4] + "_A2phaseIndexPlot_NearRealTime.csv", AphaseIndex, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_A2phaseIndexPlot_30seconds.csv", AphaseInde30s, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_A2phaseIndexPlot_60seconds.csv", AphaseInde60s, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_A2phaseIndexPlot_30minutes.csv", AphaseInde30m, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_A2phaseIndexPlot_60minutes.csv", AphaseInde60m, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_A2phaseIndexMetrics_notCorrected_NRT_30s_30m_60s_60m.csv", AphaseInde60m, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_notA2Phase_A2Phase.csv", A, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_notA2Phase_A2Phase_probabilistic_output.csv", cappredictiony_predhA_prob, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_notNREM_NREM_used_for_A2phase.csv", N, delimiter=",")
                else:
                    np.savetxt(file_path[start:-4] + "_A3phaseIndexPlot_NearRealTime.csv", AphaseIndex, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_A3phaseIndexPlot_30seconds.csv", AphaseInde30s, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_A3phaseIndexPlot_60seconds.csv", AphaseInde60s, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_A3phaseIndexPlot_30minutes.csv", AphaseInde30m, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_A3phaseIndexPlot_60minutes.csv", AphaseInde60m, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_A3phaseIndexMetrics_notCorrected_NRT_30s_30m_60s_60m.csv", AphaseInde60m, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_notA3Phase_A3Phase.csv", A, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_notA3Phase_A3Phase_probabilistic_output.csv", cappredictiony_predhA_prob, delimiter=",")
                    np.savetxt(file_path[start:-4] + "_notNREM_NREM_used_for_A3phase.csv", N, delimiter=",")
                break  # exit the loop if no errors occur
            except Exception as e:
                print(f"An error occurred: {e}")
                start += 1  # Try with the next index range