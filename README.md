# Pre-processing Chain

## Data Curation and Traceability
- Each data file was assigned a unique subject ID, allowing for tracking and support for multi-file folders in future datasets.
- Files were batch-scanned by prefix and suffix patterns to automate selection and maintain reproducibility.

## Filtering and Artifact Rejection
- High-amplitude artifacts in the raw EEG signals were identified using a dynamic threshold based on 10× the signal standard deviation, after channel-specific parsing.
- Peaks exceeding this threshold were temporarily replaced within surrounding windows using **median filtering** (`window = 5 seconds`), effectively suppressing non-biological transients.

## Signal Standardization and Referencing
- Following peak removal, signals were standardized using **z-scoring** (mean subtraction and division by standard deviation) to harmonize amplitude scales across subjects and channels.
- All data were resampled to **100 Hz** to allow compatibility between recordings with different native sampling rates and to accommodate downstream time-based analysis.

## Epoching and File Management
- Data segmentation was performed into fixed-length epochs of **1 second**, matching analysis requirements for event detection and alignment with manual annotations.
- Filtered and resampled signals were saved as separate files per channel and subject.

---

# Detector Architecture and Version

## Ensemble Classifier
- The detector architecture consisted of an ensemble-based approach with **three dedicated classifiers** (one ensemble for each A-phase subtype), and a **fourth classifier** used for correction of longer A-phases, performing only **A vs. non-A phase** classification.
- Ensemble forecasts were strictly limited to **NREM epochs**, using the manually annotated sleep macrostructure to exclude non-NREM segments and aggregate subtypes.
- The aggregation logic compared the probabilistic outputs of all three subtype classifiers at each second. If multiple subtypes were predicted simultaneously, the subtype with the **highest confidence** was selected for final labeling.

## Post-processing
- Sequences where the detected subtype varied from neighbors (i.e., **single-epoch transitions**) were reset to the preceding value, suppressing isolated false positives.
- **Short-duration events** (<2 epochs) were mapped to the most frequent classification within the sequence.
- If a sequence exceeded **60 consecutive epochs**, the most frequent subtype within this sequence was used as a reference. A correction was then applied based on the **fourth ensemble classifier**, changing all epochs in the 60-second sequence that were identified as A-phase by this classifier to the most frequent subtype of the sequence.

## Versioning and Output
- All code and classifier parameters were managed in **versioned directories**, with annotation for each study group.
- Final corrected outputs were written to **subject-specific files** in the CSV format, and accumulated versions were produced, preserving traceability for downstream statistical analysis.

---

# Alignment to Manual Sleep Staging

- Sleep stage annotations provided in **30-second intervals** were interpolated to **1-second resolution**, such that every 1-second epoch within a 30-second macrostructure segment inherited its stage label from the manually scored annotation.

---

# Considered Definition of A-phase

- A-phase subtypes (**A1**, **A2**, **A3**) were defined in accordance with the **CAP Atlas**, which establishes specific thresholds, frequency bands, and time–frequency criteria for each subtype.
- Models in this work were trained and validated on a dataset explicitly annotated according to CAP Atlas standards, using the models developed in **10.1093/sleep/zsac217**. Thus, automated subtype classification replicates expert consensus and adheres to international guidelines.
