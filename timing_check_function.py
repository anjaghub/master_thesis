# Import libraries
import pandas as pd
import os
from pathlib import Path

def check_timing():
    # List all data files which should be preprocessed
    directory = Path('/Users/anja/Desktop/data_mt')
    data_files = [file.name for file in directory.glob('*.csv')]

    # Columns needed from raw file
    desired_columns = ['ident_block_trial', # identifier to determine trial, because dataset is off
                        'participant',
                        'cc_owner.started', # time when the owner confirm dialog in cc trials was started (to measure if something was off with keep)
                        'cc_owner.stopped',
                        'yc_owner.started', # time when the owner confirm dialog in yc trials was started (to measure if something was off with keep)
                        'yc_owner.stopped',
                        'balance.started',
                        'balance.stopped',
                        'fixation.started',
                        'fixation.stopped',
                        'round_info.started',
                        'round_info.stopped',
                        'yc_choice.started',
                        'yc_choice.stopped',
                        'cc_choice.started',
                        'cc_choice.stopped',
                        'cc_choice_confirm.started',
                        'cc_choice_confirm.stopped',
                        'yc_draw_frame.started',
                        'yc_draw_frame.stopped',
                        'yc_value.started',
                        'yc_value.stopped',
                        'yc_owner_confirm.started',
                        'yc_owner_confirm.stopped',
                        'cc_value.started',
                        'cc_value.stopped',
                        'cc_owner_confirm.started',
                        'cc_owner_confirm.stopped'
                        ] 

    # Create empty list to store files
    dfs = []
    # Read the csv files and create columns in case some are missing
    for file_name in data_files:
        file_path = os.path.join(directory, file_name)
        # Get the available columns
        df_initial = pd.read_csv(file_path, nrows=0) 
        available_columns = df_initial.columns.tolist()
        # Determine which desired columns are available in csv
        existing_columns = [col for col in desired_columns if col in available_columns]
        # Read the CSV file, using only the existing columns
        df = pd.read_csv(file_path, usecols=existing_columns)
        # Add the missing columns with empty values
        for col in desired_columns:
            if col not in df.columns:
                df[col] = pd.NA

        dfs.append(df)

    # Concatenating files together
    concatenated_df = pd.concat(dfs, ignore_index=True)

    # Putting owner times in one column
    concatenated_df['owner_started'] = concatenated_df['cc_owner.started'].combine_first(concatenated_df['yc_owner.started'])
    concatenated_df['owner_stopped'] = concatenated_df['cc_owner.stopped'].combine_first(concatenated_df['yc_owner.stopped'])
    # Putting value times in one column
    concatenated_df['value_started'] = concatenated_df['cc_value.started'].combine_first(concatenated_df['yc_value.started'])
    concatenated_df['value_stopped'] = concatenated_df['cc_value.stopped'].combine_first(concatenated_df['yc_value.stopped'])
    # Putting owner confirm times in one column
    concatenated_df['owner_confirm_started'] = concatenated_df['cc_owner_confirm.started'].combine_first(concatenated_df['yc_owner_confirm.started'])
    concatenated_df['owner_confirm_stopped'] = concatenated_df['cc_owner_confirm.stopped'].combine_first(concatenated_df['yc_owner_confirm.stopped'])
    # Putting choice confirm times in one column
    concatenated_df['choice_confirm_started'] = concatenated_df['cc_choice_confirm.started'].combine_first(concatenated_df['yc_draw_frame.started'])
    concatenated_df['choice_confirm_stopped'] = concatenated_df['cc_choice_confirm.stopped'].combine_first(concatenated_df['yc_draw_frame.stopped'])

    # Calculate durations
    concatenated_df['round_info_duration'] = concatenated_df['round_info.stopped'] - concatenated_df['round_info.started']
    concatenated_df['fixation_duration'] = concatenated_df['fixation.stopped'] - concatenated_df['fixation.started']
    concatenated_df['balance_duration'] = concatenated_df['balance.stopped'] - concatenated_df['balance.started']

    concatenated_df['cc_choice_duration'] = concatenated_df['cc_choice.stopped'] - concatenated_df['cc_choice.started']
    concatenated_df['yc_choice_duration'] = concatenated_df['yc_choice.stopped'] - concatenated_df['yc_choice.started']

    concatenated_df['owner_confirm_duration'] = concatenated_df['owner_confirm_stopped'] - concatenated_df['owner_confirm_started']
    concatenated_df['value_duration'] = concatenated_df['value_stopped'] - concatenated_df['value_started']
    concatenated_df['owner_duration'] = concatenated_df['owner_stopped'] - concatenated_df['owner_started']
    concatenated_df['choice_confirm_duration'] = concatenated_df['choice_confirm_stopped'] - concatenated_df['choice_confirm_started']

    # Select relevant columns 
    relevant_columns = ['ident_block_trial',
                        'participant',
                        'owner_duration',
                        'round_info_duration',
                        'fixation_duration',
                        'cc_choice_duration',
                        'choice_confirm_duration',
                        'value_duration',
                        'owner_confirm_duration',
                        'yc_choice_duration',
                        'balance_duration'
                        ] 

    concatenated_df = concatenated_df[relevant_columns]

    # sort out durations which were too long
    subset_1 = concatenated_df[concatenated_df['owner_duration'] > 1.1]
    subset_2 = concatenated_df[concatenated_df['round_info_duration'] > 1.6]
    subset_3 = concatenated_df[concatenated_df['fixation_duration'] > 1.1]
    subset_4 = concatenated_df[concatenated_df['cc_choice_duration'] > 2.1]
    subset_5 = concatenated_df[concatenated_df['choice_confirm_duration'] > 0.6]
    subset_6 = concatenated_df[concatenated_df['value_duration'] > 1.1]
    subset_7 = concatenated_df[concatenated_df['owner_confirm_duration'] > 0.6]
    subset_8 = concatenated_df[concatenated_df['yc_choice_duration'] > 2.1]
    subset_9 = concatenated_df[concatenated_df['balance_duration'] > 1.1]

    # putting subsets together
    data_frame = pd.concat([subset_1,
                            subset_2,
                            subset_3,
                            subset_4,
                            subset_5,
                            subset_6,
                            subset_7,
                            subset_8,
                            subset_9
                            ], ignore_index=True)
    
    # only take unique participants and trials
    data_frame = data_frame[['ident_block_trial', 'participant']].drop_duplicates()

    return data_frame



