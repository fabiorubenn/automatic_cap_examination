Pre-processing Chain
	•	Data Curation and Traceability
		o	Each data file was assigned a unique subject ID, allowing for tracking and support for multi-file folders in future datasets.
		o	Files were batch-scanned by prefix and suffix patterns to automate selection and maintain reproducibility.
	•	Filtering and Artifact Rejection
		o	High-amplitude artifacts in the raw EEG signals were identified using a dynamic threshold based on 10 times the signal standard deviation, after channel-specific parsing.
		o	Peaks exceeding this threshold were temporarily replaced within surrounding windows using median filtering (window = 5 seconds), effectively suppressing non-biological transients.
	•	Signal Standardization and Referencing
		o	Following peak removal, signals were standardized (z-scoring: mean subtraction and division by standard deviation) to harmonize amplitude scales across subjects and channels.
		o	All data were resampled to 100 Hz to allow for compatibility between recordings with different native sampling rates and accommodate downstream time-based analysis.
	•	Epoching and File Management
		o	Data segmentation was performed into fixed-length epochs of 1 second, matching analysis requirements for event detection and alignment with manual annotations.
		o	Filtered and resampled signals were saved as separate files per channel and subject.

Detector Architecture and Version
	•	Ensemble Classifier
		o	The detector architecture consisted of an ensemble-based approach with three dedicated classifiers (one ensemble for each A-phase subtype, and a fourth classifier that is used for correction of longer A-phases, performing only A or not-A phase classification). 
		o	Ensemble forecasts were strictly limited to NREM epochs, using the manually annotated macrostructure of sleep for exclusion of non-NREM segments and aggregation of subtypes.
		o	The aggregation logic compared the probabilistic outputs of all three ensemble classifiers at each second, and, if multiple subtypes were predicted simultaneously, the subtype with the highest confidence was selected for final labeling.
	•	Post-processing 
		o	Sequences where the detected subtype varied from neighbors (single-epoch transitions) were reset to the preceding value, suppressing isolated false positives.
		o	Short-duration events (<2 epochs) were mapped to the most frequent classification within the sequence.
		o	If a sequence exceeds 60 consecutive epochs, the most frequent subtype within this sequence is used as a reference. A correction is then applied based on the fourth ensemble classifier (specialized in A-phase detection), changing all epochs in the 60-second sequence that were identified as A-phase by this classifier to the most frequent subtype of the sequence.
	•	Versioning and Output
		o	All code and classifier parameters were managed in versioned directories, with annotation for each study group.
		o	Final corrected outputs were written to subject-specific files in the format all_subtypes_corrected.csv, preserving traceability for downstream statistical analysis.

Alignment to Manual Sleep Staging
	•	Sleep stage annotations provided in 30-second intervals were interpolated to 1-second resolution, such that every 1-second epoch within a 30-second macrostructure segment inherited its stage label from the manually scored annotation.

Considered Definition of A-phase
	•	A-phase subtypes (A1, A2, A3) were defined in accordance with the CAP Atlas, which establishes specific thresholds, frequency bands, and time–frequency criteria for each subtype.
	•	Models in this work were trained and validated on a dataset explicitly annotated according to CAP Atlas standards. Thus, automated subtype classification replicates expert consensus and adheres to international guidelines.
