% select the directory to work
%directory = 'Completely new subjects';
%directory = 'Updated subjects\Group 1 (Fibro)';
%directory = 'Updated subjects\Group 2 (NT)';
%directory = 'Updated subjects\Group 3 (NREM)';
% directory = 'Updated subjects\Group 4 (RBD)';

%directory = 'D:\Github\EnsembleCNN\KC_OSA\KCL OSA data';
%directory = 'D:\Github\EnsembleCNN\KC_OSA\OSA_V2\data\EEG csv';

%directory = 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA Ana\Group 1 OSA-Control\CSV'
%directory = 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA Ana\Group 2 OSA-PTSD\CSV'
directory = 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA KCL\Csv'

cd 'D:\Github\EnsembleCNN\KC_06_2025\OneDrive_1_03-06-2025\OSA KCL\Csv'

% select if figures should be plotted
plot_figure = 1;

% suppress all warnings
warning('off', 'all');

% chage directory
disp(['Working in directory: ', directory]);

% get the current directory path
current_directory = pwd;

% list all files in the current directory
files = dir(current_directory);
% initialize an empty cell array to store matching file names
matchingFiles = {};
files_names = {};
% loop through the files and check if they match the criteria of starting
% with "summary" and end in ".csv"
for i = 1:numel(files)
    if endsWith(files(i).name, '.csv')
        matchingFiles{end+1} = fullfile(directory, files(i).name);
        files_names{end+1} = files(i).name;
    end
end
threshold_multiplier = 10;
sampling_frequency = 100; 
% check if any matching files were found
if isempty(matchingFiles)
    disp('No matching CSV files found.');
else
    % cycle over the matching files, the loop is made for a possible future 
    % were all data might be in a single folder with multiple summary files
    % at this moment it will only find one file due to the current file 
    % structure
    for i = 1:numel(matchingFiles)
        % construct the full file path
        filePath = matchingFiles{i};

        % read the CSV file into a table based on the header
        data = readtable(filePath);

        disp (['Examining file: ', files_names{i}]);

        % load the file
        original_signal = table2array(readtable(files_names{i}));

        % threshold for clipping
        threshold = std(original_signal) * threshold_multiplier;
        % window for peak detection 
        window_size = sampling_frequency * 5; 

        % remove high-amplitude peaks
        cleaned_eeg_data = removeHighAmplitudePeaks(original_signal, threshold, window_size);

        % standardize the signal
        mean_eeg = mean(cleaned_eeg_data);
        std_eeg = std(cleaned_eeg_data);
        resampled = (cleaned_eeg_data - mean_eeg) / std_eeg;

        % resample the signal
        %resamplig_rate = 100;
        %resampled = resample(standardized_eeg, resamplig_rate, sampling_frequency);

        new_file_path_resampled = fullfile(current_directory, ['standardized and resampled ', files_names{i}(1:end-4), '.mat']);
        save(new_file_path_resampled, 'resampled');

        % plot original and cleaned EEG data for comparison
        if plot_figure == 1
            figure;
            subplot(3, 1, 1);
            plot(original_signal, 'r');
            title('Original EEG Data');
            subplot(3, 1, 2);
            plot(cleaned_eeg_data, 'g');
            title('Cleaned EEG Data');
            subplot(3, 1, 3);
            plot(resampled, 'b');
            title('Resampled and standardized EEG Data');
        end
    end
end
disp('Finished.');

function cleaned_eeg = removeHighAmplitudePeaks(eeg_data, threshold, window_size)
    cleaned_eeg = eeg_data;
    % identify peaks exceeding the threshold
    peaks = find(abs(eeg_data) > threshold);
    % apply median filtering only to the identified peaks
    for i = 1:length(peaks)
        start_idx = max(1, peaks(i) - window_size / 2);
        end_idx = min(length(eeg_data), peaks(i) + window_size / 2);
        cleaned_eeg(start_idx:end_idx) = medfilt1(eeg_data(start_idx:end_idx), window_size);
    end
end


