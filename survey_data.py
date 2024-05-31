# Import libraries
import pandas as pd
import os
from functools import reduce

def survey_data(data_files):
    # Files and directory of them
    file_names = data_files
    directory = '/Users/anja/Desktop/data_mt/'

    # Columns needed from raw file
    desired_columns = ['participant', # participant id
                       'survey_start.question3', # Age
                       'survey_start.question4', # Gender
                       'survey_start.question2', # Handedness
                       'survey_end.question3.Row 1', # answer stored as "Column 1" "Column 2" etc.
                       'survey_end.question3.Row 2',
                       'survey_end.question3.Row 3',
                       'survey_end.question3.Row 4',
                       'survey_end.question3.Row 5',
                       'survey_end.question3.Row 6',
                       'survey_end.question3.Row 7',
                       'survey_end.question3.Row 8',
                       'survey_end.question3.Row 9',
                       'survey_end.question3.Row 10',
                       'survey_end.question3.Row 11',
                       'survey_end.question3.Row 12',
                       'survey_end.question3.Row 13',
                       'survey_end.question3.Row 14',
                       'survey_end.question3.Row 15',
                       'survey_end.question3.Row 16',
                       'survey_end.question3.Row 17',
                       'survey_end.question3.Row 18',
                       'survey_end.question3.Row 19',
                       'survey_end.question3.Row 20',
                       'survey_end.question4.Row 1',
                       'survey_end.question4.Row 2',
                       'survey_end.question4.Row 3',
                       'survey_end.question4.Row 4'
                       ] 

    # Create empty list to store files
    dfs = []
    # Read the csv files and create columns in case some are missing
    for file_name in file_names:
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

        # Creating subsets of data because every trail has several rows in raw data
        first_subset = df[['participant', 'survey_start.question3','survey_start.question4','survey_start.question2']].dropna()
        second_subset = df[['survey_end.question3.Row 1', 
                            'survey_end.question3.Row 2',
                            'survey_end.question3.Row 3',
                            'survey_end.question3.Row 4',
                            'survey_end.question3.Row 5',
                            'survey_end.question3.Row 6',
                            'survey_end.question3.Row 7',
                            'survey_end.question3.Row 8',
                            'survey_end.question3.Row 9',
                            'survey_end.question3.Row 10',
                            'survey_end.question3.Row 11',
                            'survey_end.question3.Row 12',
                            'survey_end.question3.Row 13',
                            'survey_end.question3.Row 14',
                            'survey_end.question3.Row 15',
                            'survey_end.question3.Row 16',
                            'survey_end.question3.Row 17',
                            'survey_end.question3.Row 18',
                            'survey_end.question3.Row 19',
                            'survey_end.question3.Row 20',
                            'survey_end.question4.Row 1',
                            'survey_end.question4.Row 2',
                            'survey_end.question4.Row 3',
                            'survey_end.question4.Row 4']].dropna()


        # Merging dataframes together so that there is only one line per trial
        all_subsets = [first_subset, second_subset]
        merged_df = reduce(lambda left, right: pd.merge(left, right, on='ident_block_trial', how='left'), all_subsets)

        # Append the DataFrame to the list of dataframes
        dfs.append(merged_df)

    # Concatenating files together
    concatenated_df = pd.concat(dfs, ignore_index=True)

    # Rename identifier, stim1, stim2, choice_confirmation.keys columns
    new_names = {'survey_start.question3' : 'age',
                'survey_start.question4' : 'gender',
                'survey_start.question2' : 'handedness',
                'survey_end.question3.Row 1' : 'cesdr_poor_appetite', 
                'survey_end.question3.Row 2' : 'cesdr_shake_off_blues',
                'survey_end.question3.Row 3' : 'cesdr_keep_mind',
                'survey_end.question3.Row 4' : 'cesdr_felt_depressed',
                'survey_end.question3.Row 5' : 'cesdr_restless_sleep',
                'survey_end.question3.Row 6' : 'cesdr_sad',
                'survey_end.question3.Row 7' : 'cesdr_get_going',
                'survey_end.question3.Row 8' : 'cesdr_nothing_made_happy',
                'survey_end.question3.Row 9' : 'cesdr_bad_person',
                'survey_end.question3.Row 10' : 'cesdr_lost_interest_activities',
                'survey_end.question3.Row 11' : 'cesdr_more_sleep',
                'survey_end.question3.Row 12' : 'cesdr_slowly',
                'survey_end.question3.Row 13' : 'cesdr_fidgety',
                'survey_end.question3.Row 14' : 'cesdr_wish_dead',
                'survey_end.question3.Row 15' : 'cesdr_hurt_myself',
                'survey_end.question3.Row 16' : 'cesdr_tired',
                'survey_end.question3.Row 17' : 'cesdr_not_like_myself',
                'survey_end.question3.Row 18' : 'cesdr_lost_weight',
                'survey_end.question3.Row 19' : 'cesdr_trouble_sleep',
                'survey_end.question3.Row 20' : 'cesdr_not_focus',
                'survey_end.question4.Row 1' : 'ie4_own_boss',
                'survey_end.question4.Row 2' : 'ie4_will_succeed',
                'survey_end.question4.Row 3' : 'ie4_determined_by_others',
                'survey_end.question4.Row 4' : 'ie4_fate'
                 }
    concatenated_df = concatenated_df.rename(columns=new_names)

    return concatenated_df
