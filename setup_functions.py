import numpy as np
import pandas as pd


def get_header_names(raw_data_headers, header_index_range):
    """
    This function takes in the raw data column headers and header index list and creates a list with the header names

    :param raw_data_headers: A list of all the column names from raw data
    :param header_index_range: A list of indices for a specific parameter
    :return: header_names_list: A list of header names that correspond to the header_index_range list
    """

    header_names_list = list()
    for index in header_index_range:
        header_names_list.append(raw_data_headers[index])

    return header_names_list


def convert_to_int(header_index_range, raw_data_headers, dataframe):
    """
    This function converts a specific range of the dataframe into a numeric type dataframe.

    :param header_index_range: A list of indices for specific parameters
    :param raw_data_headers: A list of all the column names from raw data
    :param dataframe: A dataframe with columns that need to be converted from strings to numerics
    :return: dataframe: A dataframe with a specific section converted from strings to numerics
    """

    # replace NaNs and - (no values/blank spaces) with a very large placeholder number
    dataframe.replace(np.nan, '999999999', regex=True, inplace=True)
    dataframe.replace('^[-]{1}$', '999999999', regex=True, inplace=True)

    header_names_range = get_header_names(raw_data_headers, header_index_range)

    # turn this header range from strings to numerics
    dataframe[header_names_range] = dataframe[header_names_range].apply(pd.to_numeric)

    # replace that very large placeholder number with NaNs again
    dataframe.replace('999999999', np.nan, regex=True, inplace=True)
    dataframe.replace(999999999, np.nan, regex=True, inplace=True)

    return dataframe


def index_range(keyword, header_list):
    """
    This function takes in a keyword and a list of column header names and creates a list of indices that contains the
    specified keyword.

    :param keyword: A header or part of a header that you are interested in.
    :param header_list: A list of column header names from raw data.
    :return: index_list: A list of indices that correspond to where the specific keyword shows up in the raw data column
    header list
    """

    index_list = list()
    for header in header_list:
        if header.startswith(keyword):
            index_list.append(header_list.index(header))

    return index_list


def get_missing_reversal_trials(df):
    """
    This function fixes the missing trial numbers to the 1st/2nd reversal. If an animal does not reach the 1st reversal,
    all the trials are counted towards the first reversal. If an animal does not reach the 2nd reversal and reaches the
    1st reversal, all trials after the 1st reversal are counted towards the 2nd reversal. This is not reflected in the
    ABET raw data!

    :param df: The cleaned dataframe that has LD Train/LD Probe data.
    """
    for index in df.iterrows():
        if np.isnan(index[1]['NumberOfTrialTo1stReversal']):
            # if not reach first reversal, make it the total number of trials
            df.at[index[0], 'NumberOfTrialTo1stReversal'] = df.at[index[0], 'NumberOfTrial']
        if np.isnan(index[1]['NumberOfTrialTo2ndReversal']) and index[1]['NumberOfReversal'] > 0:
            # if not reach second reversal and made more than one reversal, make it the difference
            df.at[index[0], 'NumberOfTrialTo2ndReversal'] = df.at[index[0], 'NumberOfTrial'] - df.at[
                index[0], 'NumberOfTrialTo1stReversal']


def get_fixed_session_time(df, df2):
    """
    This function fixes the duration for each reversal, measured in seconds. The ABET raw data gives absolute time
    instead of duration.

    :param df: The cleaned dataframe that has LD Train/LD Probe data.
    :param df2: A dataframe that represents the raw ABET data
    """

    for index in df.iterrows():
        if index[1]['NumberOfReversal'] == 0:
            df.at[index[0], 'SessionLengthTo1stReversalDuration'] = df.at[index[0], 'SessionLength']
        elif index[1]['NumberOfReversal'] == 1:
            df.at[index[0], 'SessionLengthTo2ndReversalDuration'] = df.at[index[0], 'SessionLength'] - df.at[
                index[0], 'SessionLengthTo1stReversalDuration']
        else:
            df.at[index[0], 'SessionLengthTo2ndReversalDuration'] = df2.at[index[
                                                                               0], 'No trials to criterion - Condition (2)'] - \
                                                                    df2.at[index[
                                                                               0], 'No trials to criterion - Condition (1)']


def get_percent_correctness_first(df1, df2, column_names):
    """
    This function gets/fixes the percent correctness to the 1st reversal. If an animal does not reach the 1st reversal,
    the overall percent correctness is the 1st reversal percent correctness. If an animal does not reach the
    2nd reversal and reaches the 1st reversal, all trials after the 1st reversal are counted towards the 2nd reversal
    percent correctness. This is not reflected in the ABET raw data!

    :param df1: A dataframe that represents the raw ABET data file
    :param df2: A dataframe that represents the cleaned LD Train/LD Probe data
    :param column_names: A list of column names used to determine the percent correctness
    """

    for index in df1.iterrows():
        stop_point = df1.at[index[0], 'No trials to criterion - Generic Evaluation (1)']
        # if did not reach first reversal, make the value the correct percentage value
        if np.isnan(stop_point) or index[1]['End Summary - Times Criteria reached (1)'] == 0:
            stop_point = df1.at[index[0], 'End Summary - Trials Completed (1)']
            df1.at[index[0], 'PercentCorrectTo1stReversal'] = df1.at[index[
                                                                         0], 'End Summary - Percentage Correct (1)']
            int_stop_point = int(stop_point)

            df1.at[index[0], 'PercentCorrectTo1stReversal'] = (df1[column_names[0:int_stop_point + 1]].mean(axis=1)[
                index[0]]) * 100
            df2.at[index[0], 'NumberOfTrialTo1stReversal'] = int_stop_point + 1
        else:
            int_stop_point = int(stop_point)
            df1.at[index[0], 'PercentCorrectTo1stReversal'] = (df1[column_names[0:int_stop_point]].mean(axis=1)[
                index[0]]) * 100


def get_percent_correctness_second(df1, df2, column_names):
    """
    This function gets/fixes the percent correctness to the 2nd reversal. If an animal does not reach the 1st reversal,
    the percent correctness for the 2nd reversal is NaN. If an animal does not reach the 2nd reversal and reaches the
    1st reversal, all trials after the 1st reversal are counted towards the 2nd reversal percent correctness. This is
    not reflected in the ABET raw data!

    :param df1: A dataframe that represents the raw ABET data file
    :param df2: A dataframe that represents the cleaned LD Train/LD Probe data
    :param column_names: A list of column names used to determine the percent correctness
    """

    for index in df1.iterrows():
        start_point = df1.at[index[0], 'No trials to criterion - Generic Evaluation (1)']
        stop_point = df2.at[index[0], 'NumberOfTrialTo2ndReversal'] + start_point
        if np.isnan(start_point) or np.isnan(stop_point):
            df1.at[index[0], 'PercentCorrectTo2ndReversal'] = np.nan
        elif index[1]['End Summary - Times Criteria reached (1)'] == 1:
            int_start_point = int(start_point)
            list_wo_nans = df1[column_names[int_start_point:]].count(axis=1).tolist()
            df1.at[index[0], 'PercentCorrectTo2ndReversal'] = \
                (df1[column_names[int_start_point:]].mean(axis=1)[index[0]]) * 100
            df2.at[index[0], 'NumberOfTrialTo2ndReversal'] = list_wo_nans[index[0]]
        else:
            int_start_point = int(start_point)
            int_stop_point = int(stop_point)
            df1.at[index[0], 'PercentCorrectTo2ndReversal'] = \
                (df1[column_names[int_start_point:int_stop_point]].mean(axis=1)[index[0]]) * 100


def get_test_type(df1, column_names):
    """
    This function determines the type of location discrimination test that the animal performed on. If the animal ran on
    type = easy, then the squares will be far apart (7 and 12). If the animal ran on type = hard, then the squares will
    be closer together (9 and 10). If the animal ran on type = intermediate, then the squares will be in the middle
    (8 and 11). Otherwise, the type will be undetermined.

    Note that these are all bottom row squares!

    :param df1: A dataframe that represents the cleaned LD Train/LD Probe data
    :param column_names: A list of column names used to determine the type
    """

    some_list = df1[column_names].values.tolist()
    for index in df1.iterrows():
        if 8.0 in some_list[index[0]] or 11.0 in some_list[index[0]]:
            df1.at[index[0], 'Type'] = 'intermediate'
        elif 9.0 in some_list[index[0]] or 10.0 in some_list[index[0]]:
            df1.at[index[0], 'Type'] = 'hard'
        elif 7.0 in some_list[index[0]] or 12.0 in some_list[index[0]]:
            df1.at[index[0], 'Type'] = 'easy'
        else:
            df1.at[index[0], 'Type'] = 'undetermined'


def get_mean_latency_first(df1, column_names):
    """
    This function gets the mean latency to the 1st reversal. If an animal does not reach the 1st reversal,
    the overall mean latency is the 1st reversal mean latency.

    :param df1: A dataframe that represents the raw ABET data file
    :param df2: A dataframe that represents the cleaned LD Train/LD Probe data
    :param column_names: A list of column names used to determine the mean latency
    """

    for index in df1.iterrows():
        stop_point = df1.at[index[0], 'No trials to criterion - Generic Evaluation (1)']
        # if did not reach first reversal, make the value the correct mean latency value
        if np.isnan(stop_point) or index[1]['End Summary - Times Criteria reached (1)'] == 0:
            stop_point = df1.at[index[0], 'End Summary - Trials Completed (1)']
            int_stop_point = int(stop_point)

            df1.at[index[0], 'MeanLatencyTo1stReversal'] = (df1[column_names[0:int_stop_point + 1]].mean(axis=1)[
                index[0]])
        else:
            int_stop_point = int(stop_point)
            df1.at[index[0], 'MeanLatencyTo1stReversal'] = (df1[column_names[0:int_stop_point]].mean(axis=1)[
                index[0]])

def get_correct_touch_latency_first(df1, column_names):
    """
    This function gets the mean correct touch latency to the 1st reversal. If an animal does not reach the 1st reversal,
    the overall mean correct_touch_latency is the 1st reversal mean latency.

    :param df1: A dataframe that represents the raw ABET data file
    :param df2: A dataframe that represents the cleaned LD Train/LD Probe data
    :param column_names: A list of column names used to determine the correct touch latency
    """

    for index in df1.iterrows():
        stop_point = df1.at[index[0], 'No trials to criterion - Generic Evaluation (1)']
        # if did not reach first reversal, make the value the correct mean latency value
        if np.isnan(stop_point) or index[1]['End Summary - Times Criteria reached (1)'] == 0:
            stop_point = df1.at[index[0], 'End Summary - Trials Completed (1)']
            int_stop_point = int(stop_point)

            df1.at[index[0], 'CorrectTouchLatencyTo1stReversal'] = (df1[column_names[0:int_stop_point + 1]].mean(axis=1)[
                index[0]])
        else:
            int_stop_point = int(stop_point)
            df1.at[index[0], 'CorrectTouchLatencyTo1stReversal'] = (df1[column_names[0:int_stop_point]].mean(axis=1)[
                index[0]])

def get_iti_blank_touch_first(df1, left_column_names, right_column_names):
    """
    This function gets the number of blank iti touches to the 1st reversal. If an animal does not reach the 1st reversal,
    the total blank iti touches is the 1st reversal blank iti touches.

    :param df1: A dataframe that represents the raw ABET data file
    :param left_column_names: A list of column names used to determine the number left iti blank touches
    :param right_column_names: A list of column names used to determine the number right iti blank touches
    """

    for index in df1.iterrows():
        stop_point = df1.at[index[0], 'No trials to criterion - Generic Evaluation (1)']
        # if did not reach first reversal, make the value the correct mean latency value
        if np.isnan(stop_point) or index[1]['End Summary - Times Criteria reached (1)'] == 0:
            stop_point = df1.at[index[0], 'End Summary - Trials Completed (1)']
            int_stop_point = int(stop_point)

            df1.at[index[0], 'ITIBlankTouchesTo1stReversal'] = (df1[left_column_names[0:int_stop_point + 1]].sum(axis=1)
                [index[0]] + (df1[right_column_names[0:int_stop_point + 1]].sum(axis=1)[index[0]]))
            #mean or sum?
            # when I used sum: total_iti = 1st reversal
            # when I used mean: 1/2 total_iti = 1st reversal
        else:
            int_stop_point = int(stop_point)
            df1.at[index[0], 'ITIBlankTouchesTo1stReversal'] = (df1[left_column_names[0:int_stop_point]].sum(axis=1)[
                index[0]] + (df1[right_column_names[0:int_stop_point]].sum(axis=1)[index[0]]))
