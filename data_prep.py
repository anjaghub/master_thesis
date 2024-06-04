# Import libraries
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from functools import reduce
from datetime import datetime

def swap_lose_win(identifier):
# Function to swap 'lose' with 'win' and vice versa
    if 'lose' in identifier:
        return identifier.replace('lose', 'win')
    elif 'win' in identifier:
        return identifier.replace('win', 'lose')
    return identifier


def map_choice_location(value):
# Function to change frame location and keys into choice location
    if value == 'g' or value == '-0.3':
        return 'left'
    elif value == 'k' or value == '0.3':
        return 'right'
    else:
        return 'unknown'
    
    
# Function to parse the custom datetime format
def parse_custom_datetime(dt_str):
    return datetime.strptime(dt_str, '%Y-%m-%d_%Hh%M.%S.%f')


def prepare_data(data_files):
    """Function which performs data preprocessing for the experimental data by 
    - First taking all the data files from defined location 
    - Checking one by one which columns are availabe and creating columns which are missing
    - Creating data subsets and merging data together which belongs to one trial (because of aweful datastorage from PsychoPy)
    - Creating combined columns for information which is stored in multiple columns
    - Correcting the condition variables for the 10% random trials
    - Change variable contents so they are easier to understand
    - Renaming columns
    - Creating indices for trials
    - Parse date and time
    - Select only the relevant columns for output

    Args:
        data_files (array of strings): names of all files which should be analysed

    Returns:
        data frame: holds all preprocessed data in one data frame
    """

    # Directory of files
    directory = '/Users/anja/Desktop/data_mt/'

    # Columns needed from raw file
    desired_columns = ['ident_block_trial', # identifier to determine trial, because dataset is off
                        'yc_resp.keys', #keys for color choice in yc condition
                        'too_slow_choice.started', # in yc and cc condition when selecting or confirming color
                        'wrong_answer_choice.started', # in yc and cc condition when selecting or confirming color
                        'participant', # participant id
                        'session', # session id
                        'date', # date when data collection happened
                        'owner_confirm_2.keys', # yc owner confirmation with which key?,
                        'owner_confirm_2.rt', # relevant reaction time
                        'block', # number of block
                        'trial', # number of trial in block
                        'chooser', # cc or yc trial?
                        'stim1', # left color square
                        'stim2', # right color square
                        'choice_frame_location', # cozmos color choice
                        'owner', # predefined outcome owner
                        'value', # predefined outcome value
                        'value_distribution', # identifies chance trials
                        'identifier_chooser_owner_value', # identifier of condition set, must be corrected for chance trials
                        'choice_confirmation.keys', # in cc condition what key was used to confirm color choice
                        'owner_confirm.keys', # in cc condition what was confirmed
                        'owner_confirm.rt', # relevant reaction time
                        'wrong_answer.started', # in cc and yc condition when confirming owner
                        'too_slow.started', # in cc and yc condition when confirming owner
                        'experiment_trials.thisTrialN',
                        'cc_owner.started', # time when the owner confirm dialog in cc trials was started (to measure if something was off with keep)
                        'cc_owner.stopped',
                        'yc_owner.started', # time when the owner confirm dialog in yc trials was started (to measure if something was off with keep)
                        'yc_owner.stopped'
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

        # List of columns to fill NAs with 0
        columns_to_fill = ['cc_owner.started', 'cc_owner.stopped', 'yc_owner.started', 'yc_owner.stopped']
        # Fill NAs with 0 in the specified columns
        df[columns_to_fill] = df[columns_to_fill].fillna(0)

        # Creating subsets of data because every trail has several rows in raw data
        first_subset = df[['ident_block_trial','participant','session','date']].drop_duplicates().dropna() # auto create
        second_subset = df[['ident_block_trial','block','trial','chooser','stim1','stim2','choice_frame_location','owner','value','value_distribution','identifier_chooser_owner_value','experiment_trials.thisTrialN']].dropna() # condition file
        third_subset = df[['ident_block_trial','yc_resp.keys']].dropna() # you choose color choice
        fourth_subset = df[['ident_block_trial', 'owner_confirm_2.keys', 'owner_confirm_2.rt', 'yc_owner.started', 'yc_owner.stopped']].dropna() # yc owner confirmation
        fifth_subset = df[['ident_block_trial','choice_confirmation.keys']].dropna() # cc chooses color choice confirmation
        sixth_subset = df[['ident_block_trial','owner_confirm.keys', 'owner_confirm.rt', 'cc_owner.started', 'cc_owner.stopped']].dropna() # cc chooses owner confirmation
        seventh_subset = df[['ident_block_trial','wrong_answer.started']].dropna()
        eighth_subset = df[['ident_block_trial','too_slow.started']].dropna()
        ninth_subset = df[['ident_block_trial','too_slow_choice.started']].dropna()
        tenth_subset = df[['ident_block_trial','wrong_answer_choice.started']].dropna()

        # Merging dataframes together so that there is only one line per trial
        all_subsets = [first_subset, second_subset, third_subset, fourth_subset, fifth_subset, sixth_subset, seventh_subset, eighth_subset, ninth_subset, tenth_subset]
        merged_df = reduce(lambda left, right: pd.merge(left, right, on='ident_block_trial', how='left'), all_subsets)

        # Append the DataFrame to the list of dataframes
        dfs.append(merged_df)

    # Concatenating files together
    concatenated_df = pd.concat(dfs, ignore_index=True)

    # Changing some of the columns so that they make more sense:
    # Putting the reaction times in one column
    concatenated_df['owner_confirm_rt'] = concatenated_df['owner_confirm_2.rt'].combine_first(concatenated_df['owner_confirm.rt'])
    # Putting the owner confirm keys in one column
    concatenated_df['owner_confirm_keys'] = concatenated_df['owner_confirm_2.keys'].combine_first(concatenated_df['owner_confirm.keys'])
    # Putting choice_frame_location and yc_resp.keys together and change their values in left and right
    concatenated_df['choice_location'] = concatenated_df['yc_resp.keys'].combine_first(concatenated_df['choice_frame_location'])
    concatenated_df['choice_location'] = concatenated_df['choice_location'].apply(map_choice_location)
    # Putting owner confirm times in one column
    concatenated_df['owner_confirm_started'] = concatenated_df['cc_owner.started'].combine_first(concatenated_df['yc_owner.started'])
    concatenated_df['owner_confirm_stopped'] = concatenated_df['cc_owner.stopped'].combine_first(concatenated_df['yc_owner.stopped'])
    concatenated_df['owner_confirm_duration'] = concatenated_df['owner_confirm_stopped'] - concatenated_df['owner_confirm_started']

    # Create bool columns for too slow and wrong responses
    concatenated_df['bool_wrong_color_confirm'] = ~concatenated_df['wrong_answer_choice.started'].isna()
    concatenated_df['bool_slow_color_choice_or_confirm'] = ~concatenated_df['too_slow_choice.started'].isna() # for yc and cc same column used
    concatenated_df['bool_wrong_owner_confirm'] = ~concatenated_df['wrong_answer.started'].isna()
    concatenated_df['bool_slow_owner_confirm'] = ~concatenated_df['too_slow.started'].isna()

    # Correct identifier for the 10% samples where value were changed
    concatenated_df.loc[concatenated_df['value_distribution'] == 10, 'identifier_chooser_owner_value'] = concatenated_df.loc[concatenated_df['value_distribution'] == 10, 'identifier_chooser_owner_value'].apply(swap_lose_win)
    # Correct value for the 10% samples where value were changed
    concatenated_df.loc[concatenated_df['value_distribution'] == 10, 'value'] = concatenated_df.loc[concatenated_df['value_distribution'] == 10, 'value'].apply(swap_lose_win)

    # Rename identifier, stim1, stim2, choice_confirmation.keys columns
    new_names = {'date':'raw_date',
                 'stim1': 'left_color', 
                 'stim2': 'right_color', 
                 'choice_confirmation.keys': 'choice_confirm_keys', 
                 'identifier_chooser_owner_value':'identifier_chooser_owner_value_corr',
                 'experiment_trials.thisTrialN':'trial_index_within_block',
                 }
    concatenated_df = concatenated_df.rename(columns=new_names)

    # Change trial index by one because it's originally starting with 0
    concatenated_df['trial_index_within_block'] = concatenated_df['trial_index_within_block'] + 1

    # Create date and time column from date
    concatenated_df['parsed_datetime'] = concatenated_df['raw_date'].apply(parse_custom_datetime)
    # Extract the date and time components
    concatenated_df['date'] = concatenated_df['parsed_datetime'].dt.date
    concatenated_df['time'] = concatenated_df['parsed_datetime'].dt.time

    # Select new relevant columns and get rid of the old ones which are not necessary anymore
    relevant_columns = ['date', # date when data collection happened
                        'time',
                        'session', # session id
                        'participant', # participant id
                        'block', # number of block
                        'trial', # number of trial in block
                        'identifier_chooser_owner_value_corr', # distribution corrected identifier from: identifier_chooser_owner_value
                        'chooser', # cc or yc trial?
                        'left_color', # left color square
                        'right_color', # right color square
                        'choice_location',# from 'choice_frame_location' and 'yc_resp.keys'
                        'choice_confirm_keys', # from .keys; in cc condition what key was used to confirm color choice
                        'value', # predefined outcome value
                        'value_distribution', # identifies chance trials
                        'owner', # predefined outcome owner
                        'owner_confirm_keys', 
                        'owner_confirm_rt', # relevant reaction time
                        'bool_slow_color_choice_or_confirm',
                        'bool_wrong_color_confirm', 
                        'bool_slow_owner_confirm',
                        'bool_wrong_owner_confirm',
                        'trial_index_within_block',
                        'owner_confirm_started',
                        'owner_confirm_stopped',
                        'owner_confirm_duration'
                        ] 

    concatenated_df = concatenated_df[relevant_columns]
    return concatenated_df
