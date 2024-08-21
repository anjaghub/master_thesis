# Import libraries
import pandas as pd
import os
from functools import reduce

def map_handedness(handedness):
    # Function which maps the answer of the handedness question to understandable values
    if handedness == 'Item 1':
        handedness_new = 'right'
    elif handedness == 'Item 2':
        handedness_new = 'left'
    else:
        handedness_new = 'other'
    return handedness_new

def map_gender(gender):
    # Function which maps the answer to the gender question to understandable values
    if gender == 'Item 1':
        gender_new = 'female'
    elif gender == 'Item 2':
        gender_new = 'male'
    else:
        gender_new = 'other'   
    return gender_new

def map_cesdr_values(value):
    if value == 'Column 1': # not at all or less than
        return 0
    elif value == 'Column 2': # 1-2 days
        return 1
    elif value == 'Column 3': # 3-4 days
        return 2
    elif value == 'Column 4': # 5-7 days
        return 3
    else: # everyday in two weeks
        return 4
    
def map_ie4_values(value):
    if value == 'Column 1': # doesn't apply
        return 1
    elif value == 'Column 2': # applies a bit
        return 2
    elif value == 'Column 3': # applies somewhat
        return 3
    elif value == 'Column 4': # applies mostly
        return 4
    else: # applies completely
        return 5

def survey_data(data_files):
    """ Function which performs data preprocessing for the questionnaire data by
    - First taking all the data files from defined location 
    - Checking one by one which columns are availabe and creating columns which are missing
    - Creating data subsets and merging data together which belongs to one trial (because of aweful datastorage from PsychoPy)
    - Renaming columns
    - Change variable contents so they are easier to understand

    Args:
        data_files (array of strings): names of all files which should be analysed

    Returns:
        data frame: holds all preprocessed data in one data frame
    """

    # Directory of files
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

        # Reset index if necessary
        first_subset.reset_index(drop=True, inplace=True)
        second_subset.reset_index(drop=True, inplace=True)
        
        # Merging dataframes together so that there is only one line per trial
        merged_df = pd.concat([first_subset, second_subset], axis=1)

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

    # Change the values of the CESDR columns according to analysis standard
    columns_to_map = [col for col in concatenated_df.columns if 'cesdr' in col]
    for column in columns_to_map:
        concatenated_df[column] = concatenated_df[column].apply(map_cesdr_values)
    # Create the total CESDR score
    concatenated_df['cesdr_total_score'] = concatenated_df[columns_to_map].sum(axis=1)

    # Change the values of the ie4 columns according to analysis standard
    columns_to_map = [col for col in concatenated_df.columns if 'ie4' in col]
    for column in columns_to_map:
        concatenated_df[column] = concatenated_df[column].apply(map_ie4_values)   
    # Reverse external scores
    concatenated_df["ie4_determined_by_others"] = 6 - concatenated_df["ie4_determined_by_others"]
    concatenated_df["ie4_fate"] = 6 - concatenated_df["ie4_fate"] 
    # Create total IE4 scores
    concatenated_df['ie4_internal_total_score'] = concatenated_df['ie4_own_boss'] + concatenated_df['ie4_will_succeed']
    concatenated_df['ie4_external_total_score'] = concatenated_df['ie4_fate'] + concatenated_df['ie4_determined_by_others']

    # Exchange gender and handedness values with sense making content
    concatenated_df['gender'] = concatenated_df['gender'].apply(map_gender)
    concatenated_df['handedness'] = concatenated_df['handedness'].apply(map_handedness)

    return concatenated_df
