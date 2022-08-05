import functools

from general_touchscreen import *
from ld_train import *
from ld_probe import *
from acquisition_extinction import *

hab_one_parameters = ['RewardIRBeamBrokenCount', 'ScreenIRBeamBrokenCount', 'CrossedRewardToScreen',
                      'CrossedScreenToReward', 'BottomWindowTouches', 'TopWindowTouches', 'TrayEnteredCount']

hab_two_parameters = ['NumberOfTrial', 'RewardIRBeamBrokenCount', 'ScreenIRBeamBrokenCount', 'BottomLeftWindowTouches',
                      'BottomRightWindowTouches', 'TopWindowTouches', 'TrayEnteredCount', 'MeanRewardCollectionLatency']

it_parameters = ['ImagesTouched', 'Corrects', 'BlankTouches', 'TotalITITouches', 'MeanCorrectTouchLatency',
                 'MeanBlankTouchLatency', 'MeanRewardCollectionLatency']

mt_parameters = ['Corrects', 'TotalBlankTouches', 'TotalITITouches', 'MeanCorrectTouchLatency', 'MeanBlankTouchLatency',
                 'MeanRewardCollectionLatency']

pi_parameters = ['NumberOfTrial', 'PercentCorrect', 'TotalITITouches', 'MeanCorrectTouchLatency',
                 'MeanCorrectRightTouchLatency', 'MeanCorrectLeftTouchLatency', 'MeanCorrectLeftRightTouchLatency',
                 'MeanBlankTouchLatency', 'MeanRewardCollectionLatency']

ld_parameters = ['NumberOfTrial', 'PercentCorrect', 'NumberOfReversal', 'TotalITITouches', 'TotalBlankTouches',
                 'MeanRewardCollectionLatency', 'MeanCorrectTouchLatency', 'MeanIncorrectTouchLatency',
                 'SessionLengthTo1stReversalDuration', 'SessionLengthTo2ndReversalDuration',
                 'NumberOfTrialTo1stReversal', 'NumberOfTrialTo2ndReversal', 'PercentCorrectTo1stReversal',
                 'PercentCorrectTo2ndReversal']

acq_parameters = ['Corrects', 'BlankTouches', 'TotalITITouches', 'MeanCorrectTouchLatency', 'MeanBlankTouchLatency',
                  'MeanRewardTouchLatency']

ext_parameters = ['Responses', 'Omissions', 'TotalITITouches', 'MeanResponseTouchLatency', 'MeanBlankTouchLatency',
                  'MeanTrayEntryLatency']

auto_hab_one_parameters = ['BackIRBeamBrokenCount', 'ScreenLeftIRBeamBrokenCount', 'ScreenRightIRBeamBrokenCount',
                           'CrossedBackToScreen', 'CrossedScreenToBack', 'LeftTouches', 'RightTouches',
                           'TrayEnteredCount']

auto_hab_two_parameters = ['NumberOfTrial', 'LeftApproaches', 'RightApproaches', 'LeftTouches', 'RightTouches',
                           'BackBeamBrokenCount', 'TrayEnteredCount', 'MeanRewardCollectionLatency']

auto_parameters = ['NumberOfTrial', 'ApproachesToLitCS+', 'ApproachesToLitCS-', 'TotalApproachesToCS+',
                   'TotalApproachesToCS-', 'Approach Difference', 'TouchesToLitCS+', 'TouchesToLitCS-',
                   'TotalTouchesToCS+', 'TotalTouchesToCS-', 'MeanRewardCollectionLatency']

script_location = os.path.dirname(os.path.abspath(__file__))


def block_parsing_ld_probe(df, test_type, total_blocks, parameters_list, writer):
    """
    This function is used for the LD Probe test. This function writes all the animal rows for all the blocks the current
    parameter sheet.

    :param df: A dataframe that represents the cleaned LD Probe data.
    :param test_type: A string that represents the difficulty of the LD Probe test.
    :param total_blocks: An integer that represents the maximum value of blocks within the dataframe
    :param parameters_list: The list of parameters used to create each sheet of the Excel Workbook.
    :param writer: Used to write and save the dataframe to the sheet on the Excel Workbook.
    """

    for para in parameters_list:
        all_blocks = list()
        for block_number in range(1, int(total_blocks) + 1):
            block_data = df.loc[(df['Block'] == block_number) & (df['Type'] == test_type)]
            block_data = block_data[['ID', 'Date', para, 'Type', 'Block']]
            all_blocks.append(block_data)
        merged_df = functools.reduce(lambda left, right: pd.merge(left, right, on='ID', how='outer'), all_blocks)
        merged_df.to_excel(writer, sheet_name=test_type + ' ' + para[0:25], index=False, freeze_panes=(1, 1))
    writer.save()


def ld_probe_parameterized(df):
    """
    This function is used for the LD Probe test. The function creates an Excel Workbook with each sheet being a testable
    parameter from the LD Probe test. On each sheet, there will be the performance of each animal for all the blocks
    based on difficulty (easy or hard). The Excel Workbook will be saved in the same location as the application.

    :param df: A dataframe that represents cleaned LD Probe data.
    """

    try:
        writer_easy = pd.ExcelWriter('All Blocks Parameters Easy.xlsx', engine='xlsxwriter')
        print('A file called All Blocks Parameters Easy.xlsx has been created at:', script_location)
        writer_hard = pd.ExcelWriter('All Blocks Parameters Hard.xlsx', engine='xlsxwriter')
        print('A file called All Blocks Parameters Hard.xlsx has been created at:', script_location)
    except PermissionError:
        mb.showerror('Parameterized Error',
                     'ld_probe_parameterized() error: All Blocks Parameters Easy/Hard.xlsx might be open! '
                     ' Please close it before proceeding!')
        print('ld_probe_parameterized() error: All Blocks Parameters Easy/Hard.xlsx might be open! '
              'Please close it before proceeding!')
        return None

    max_blocks = df['Block'].max()

    block_parsing_ld_probe(df, 'easy', max_blocks, ld_parameters, writer_easy)
    block_parsing_ld_probe(df, 'hard', max_blocks, ld_parameters, writer_hard)


def day_parsing_ld_train(df, test_type, max_days, parameters_list, writer):
    """
    This function is used for the LD Train test. This function writes all the animal rows for all the days the animal
    performed the test for the current parameter.

    :param df: A dataframe that represents the cleaned LD Train data.
    :param test_type: A string that represents the difficulty of the LD Probe test.
    :param max_days: An integer that represents the maximum value of days within the dataframe
    :param parameters_list: The list of parameters used to create each sheet of the Excel Workbook.
    :param writer: Used to write and save the dataframe to the sheet on the Excel Workbook.
    """

    for para in parameters_list:
        all_days = list()
        for day in range(1, int(max_days) + 1):
            day_data = df.loc[(df['Day'] == day) & (df['Type'] == test_type)]
            day_data = day_data[['ID', 'Date', 'Day', para, 'Type']]
            all_days.append(day_data)
        merged_df = functools.reduce(lambda left, right: pd.merge(left, right, on='ID', how='outer'), all_days)
        merged_df.to_excel(writer, sheet_name='int ' + para[0:25], index=False, freeze_panes=(1, 1))
    writer.save()


def ld_train_parameterized(df):
    """
    This function is used for the LD Train test. The function creates an Excel Workbook with each sheet being a testable
    parameter from the LD Train test. On each sheet, there will be the performance of each animal for all the days
    the animal performed the test. The Excel Workbook will be saved in the same location as the application.

    :param df: A dataframe that represents the cleaned LD Train data.

    """
    try:
        writer_intermediate = pd.ExcelWriter('LD Train All Days Parameters.xlsx', engine='xlsxwriter')
        print('A file called LD Train All Days Parameters.xlsx has been created at:', script_location)
    except PermissionError:
        mb.showerror('Parameterized Error', 'LD Train All Days Parameters.xlsx is opened! Please close them!')
        print(
            'LD Train All Days Parameters.xlsx is opened! Please close them!')
        return None

    max_days = df['Day'].max()
    day_parsing_ld_train(df, 'intermediate', max_days, ld_parameters, writer_intermediate)


def general_by_day_parsing(df, max_days, parameters_list, writer, test_name):
    """
    This function is a generic function for multiple test. This function writes all the animal rows for all the days
    the animal performed the test for the current parameter.

    :param df: A dataframe that represents the cleaned test data.
    :param max_days: An integer that represents the maximum value of days within the dataframe
    :param parameters_list: The list of parameters used to create each sheet of the Excel Workbook.
    :param writer: Used to write and save the dataframe to the sheet on the Excel Workbook.
    :param test_name: A string that represents the test name used for data setup.
    :return:
    """

    for para in parameters_list:
        all_days = list()
        for day in range(1, int(max_days) + 1):
            day_data = df.loc[(df['Day'] == day)]
            day_data = day_data[['ID', 'Date', 'Day', para]]
            all_days.append(day_data)
        merged_df = functools.reduce(lambda left, right: pd.merge(left, right, on='ID', how='outer'), all_days)
        merged_df.to_excel(writer, sheet_name=test_name + para[0:25], index=False, freeze_panes=(1, 1))
    writer.save()


def general_parameterized(df, name, parameter_list, test_name):
    """
    This function is used for the multiple test. The function creates an Excel Workbook with each sheet being a testable
    parameter from multiple test. On each sheet, there will be the performance of each animal for all the days
    the animal performed the test. The Excel Workbook will be saved in the same location as the application.

    :param df: A dataframe that represents the cleaned test data.
    :param name: A string that represents the name of the test the animal ran used for naming the file.
    :param parameter_list: The list of parameters used to create each sheet of the Excel Workbook.
    :param test_name: A string that represents the test name used for data setup.
    :return:
    """
    try:
        some_writer = pd.ExcelWriter(name + ' All Days Parameters.xlsx', engine='xlsxwriter')
    except PermissionError:
        mb.showerror('Parameterized Error', name + ' All Days Parameters.xlsx is opened! Please close them!')
        print(name, 'All Days Parameters.xlsx', 'is opened! Please close them!')
        return
    max_days = df['Day'].max()
    general_by_day_parsing(df, max_days, parameter_list, some_writer, test_name)


def general_para_button(data_setup_name, file_name, parameter_list):
    """
    This function creates the parameterized Excel Workbook for multiple test.

    :param data_setup_name: A string that represents the name of the test used for data setup
    :param file_name: A string that represents the the name of the test used to name the file.
    :param parameter_list: A list that represents all the parameters that will be on each sheet of the workbook
    """

    df = data_setup(data_setup_name)
    if df is not None:
        general_parameterized(df, file_name, parameter_list, data_setup_name)
        print('A file called', file_name, 'All Days Parameters.xlsx has been created at:', script_location)


def pi_para_button(min_trials, percent_one, percent_two):
    """
    This function creates the parameterized Excel Workbook for the Punish Incorrect test.

    :param min_trials: An entry widget that contains the value of the minimum required trials
    :param percent_one: An entry widget that contains the value of the percent correctness for the first day
    :param percent_two: An entry widget that contains the value of the percent correctness for the second day
    """

    try:
        minimum_trials = int(min_trials.get())
    except ValueError:
        mb.showerror('Parameterized Error', 'pi_para_button() error: The minimum trials is empty or invalid!')
        print('pi_para_button() error: The minimum trials is empty or invalid!')
        return

    try:
        correct_one = int(percent_one.get())
    except ValueError:
        mb.showerror('Parameterized Error',
                     'pi_para_button() error: The percent correctness for the first day is empty or invalid!')
        print('pi_para_button() error: The percent correctness for the first day is empty or invalid!')
        return

    try:
        correct_two = int(percent_two.get())
    except ValueError:
        mb.showerror('Parameterized Error',
                     'pi_para_button() error: The percent correctness for the second day is empty or invalid!')
        print('pi_para_button() error: The percent correctness for the second day is empty or invalid!')
        return

    df = data_setup('PI')
    if df is not None:
        get_punish_incorrect_normal(df, minimum_trials, correct_one, correct_two)
        general_parameterized(df, 'Punish Incorrect', pi_parameters, 'PI')


def acq_para_button(criteria, correct_amount, session_length):
    """
    This function creates the parameterized Excel Workbook for the Acquisition test.

    :param criteria: An entry widget that contains the value of the n days in a row
    :param correct_amount: An entry widget that contains the value of the correct trials amount
    :param session_length: An entry widget that contains the value of the session length
    """

    try:
        criteria_value = int(criteria.get())
    except ValueError:
        mb.showerror('Parameterized Error',
                     'acq_para_button() error: The n days in a row criteria is empty or invalid!')
        print('acq_para_button() error: The n days in a row criteria is empty or invalid!')
        return None

    try:
        correct_trials_num = int(correct_amount.get())
    except ValueError:
        mb.showerror('Parameterized Error', 'acq_para_button() error: The correct trials criteria is empty or invalid!')
        print('acq_para_button() error: The correct trials criteria is empty or invalid!')
        return None

    try:
        session_time_sec = int(session_length.get())
    except ValueError:
        mb.showerror('Parameterized Error', 'acq_para_button() error: The session length criteria is empty or invalid!')
        print('acq_para_button() error: The session length criteria is empty or invalid!')
        return None

    df = data_setup('Acq')
    if df is not None:
        get_acquisition_normal(df, criteria_value, correct_trials_num, session_time_sec)
        general_parameterized(df, 'Acquisition', acq_parameters, 'Acq')


def ext_para_button(criteria, omissions_amount):
    """
    This function creates the parameterized Excel Workbook for the Extinction test.


    :param criteria: An entry value that contains the value of the n days and the n+1 days
    :param omissions_amount: An entry value that contains the value of the omissions amount
    """

    criteria_list = criteria.get().split('/')

    try:
        criteria_value = int(criteria_list[0])
        criteria_max_days = int(criteria_list[1])
    except ValueError:
        mb.showerror('Parameterized Error', 'ext_para_button() error: The n/n+1 days criteria is empty or invalid!')
        print('ext_para_button() error: The n/n+1 days criteria is empty or invalid!')
        return

    try:
        omissions_count = int(omissions_amount.get())
    except ValueError:
        mb.showerror('Parameterized Error', 'ext_para_button() error: The omissions amount is empty or invalid')
        print('ext_para_button() error: The omissions amount is empty or invalid')
        return

    df = data_setup('Ext')
    if df is not None:
        get_extinction_all(df, criteria_value, criteria_max_days, omissions_count)
        general_parameterized(df, 'Extinction', ext_parameters, 'Ext')


def ld_train_para_button(criteria, min_reversal_number):
    """
    This function creates the parameterized Excel Workbook for the LD Train test.

    :param criteria: An entry widget that contains the value of the n days out of n+1 days.
    :param min_reversal_number: An entry widget that contains the value of the minimum required reversal number
    :return:
    """

    criteria_list = criteria.get().split('/')

    try:
        min_rev = int(min_reversal_number.get())
    except ValueError:
        mb.showerror('Parameterized Error',
                     'ld_train_para_button() error: The minimum required reversal number is empty or invalid!')
        print('ld_train_para_button() error: The minimum required reversal number is empty or invalid!')
        return None

    try:
        criteria_value = int(criteria_list[0])
        criteria_max_days = int(criteria_list[1])
    except ValueError:
        mb.showerror('Parameterized Error',
                     'ld_train_para_button() error: The n/n+1 days criteria is empty or invalid!')
        print('ld_train_para_button() error: The n/n+1 days criteria is empty or invalid!')
        return None

    df = data_setup('LD Train')
    if df is not None:
        ld_train_delete_other_difficulties(df)
        get_ld_train_normal(df, criteria_value, criteria_max_days, min_rev)
        ld_train_parameterized(df)


def ld_probe_para_button():
    """
    This function creates the parameterized Excel Workbook for the LD Probe test.
    """

    df = data_setup('LD Probe')
    if df is not None:
        ld_probe_delete_other_difficulties(df)
        get_last_day_difficulty(df)
        ld_probe_parameterized(df)


def make_parameterized_button(tk, root):
    """
    This function creates all the parameterized buttons found on the Parameterized sub-menu.

    :param tk: The TKinter library
    :param root: A specific frame where all the buttons will live on.
    """

    # creates general touchscreen buttons
    hab_one_para_btn = tk.Button(root, text='Habituation 1 Parameterized',
                                 command=lambda: general_para_button('Hab1', 'Habituation 1', hab_one_parameters),
                                 width=30)
    hab_one_para_btn.grid(row=0, column=0)
    hab_two_para_btn = tk.Button(root, text='Habituation 2 Parameterized',
                                 command=lambda: general_para_button('Hab2', 'Habituation 2', hab_two_parameters),
                                 width=30)
    hab_two_para_btn.grid(row=1, column=0)
    it_para_btn = tk.Button(root, text='Initial Touch Parameterized',
                            command=lambda: general_para_button('IT', 'Initial Touch', it_parameters),
                            width=30)
    it_para_btn.grid(row=2, column=0)
    mt_para_btn = tk.Button(root, text='Must Touch Parameterized',
                            command=lambda: general_para_button('MT', 'Must Touch', mt_parameters),
                            width=30)
    mt_para_btn.grid(row=3, column=0)
    mi_para_btn = tk.Button(root, text='Must Initiate Parameterized',
                            command=lambda: general_para_button('MI', 'Must Initiate', mt_parameters),
                            width=30)
    mi_para_btn.grid(row=4, column=0)

    # visual spacer between general ts and punish incorrect
    spacer_btw_ts_pi = tk.Label(root, text='', bg='#D6D6D6', width=57)
    spacer_btw_ts_pi.grid(row=5, columnspan=2)

    # creates the punish incorrect criteria widgets
    pi_para_min_trials_labels = tk.Label(root, text='Enter the min req trial amount:')
    pi_para_min_trials_labels.grid(row=6, column=0)
    pi_para_min_trials_text = tk.Entry(root, width=30, justify='center')
    pi_para_min_trials_text.grid(row=6, column=1)

    pi_para_correct_one_label = tk.Label(root, text='Enter the min % correct for first day:')
    pi_para_correct_one_label.grid(row=7, column=0)
    pi_para_correct_one_text = tk.Entry(root, width=30, justify='center')
    pi_para_correct_one_text.grid(row=7, column=1)

    pi_para_correct_two_label = tk.Label(root, text='Enter the min % correct for second day:')
    pi_para_correct_two_label.grid(row=8, column=0)
    pi_para_correct_two_text = tk.Entry(root, width=30, justify='center')
    pi_para_correct_two_text.grid(row=8, column=1)

    # creates the punish incorrect button
    pi_para_btn = tk.Button(root, text='Punish Incorrect Parameterized',
                            command=lambda: pi_para_button(pi_para_min_trials_text, pi_para_correct_one_text,
                                                           pi_para_correct_two_text), width=30)
    pi_para_btn.grid(row=9, column=0)

    # visual spacer between punish incorrect and ld train
    spacer_btw_pi_ld = tk.Label(root, text='', bg='#D6D6D6', width=57)
    spacer_btw_pi_ld.grid(row=10, columnspan=2)

    # creates the ld train criteria widgets
    ld_train_criteria_label = tk.Label(root, text='Enter criteria as n days/n+1 days: ')
    ld_train_criteria_label.grid(row=11, column=0)
    ld_train_criteria_text = tk.Entry(root, width=30, justify='center')
    ld_train_criteria_text.grid(row=11, column=1)

    ld_train_min_rev_num_label = tk.Label(root, text='Enter the min reversal number: ')
    ld_train_min_rev_num_label.grid(row=12, column=0)
    ld_train_min_rev_num_text = tk.Entry(root, width=30, justify='center')
    ld_train_min_rev_num_text.grid(row=12, column=1)

    # creates the ld buttons
    ld_train_para_btn = tk.Button(root, text='LD Train Parameterized',
                                  command=lambda: ld_train_para_button(ld_train_criteria_text,
                                                                       ld_train_min_rev_num_text), width=30)
    ld_train_para_btn.grid(row=13, column=0)

    ld_probe_para_btn = tk.Button(root, text='LD Probe Parameterized', command=ld_probe_para_button, width=30)
    ld_probe_para_btn.grid(row=14, column=0)

    # visual spacer between ld and acquisition
    spacer_btw_ld_acq = tk.Label(root, text='', bg='#D6D6D6', width=57)
    spacer_btw_ld_acq.grid(row=15, columnspan=2)

    # creates the acquisition criteria widgets
    acq_para_label = tk.Label(root, text='Enter criteria as n days in a row: ')
    acq_para_label.grid(row=16, column=0)
    acq_para_text = tk.Entry(root, width=30, justify='center')
    acq_para_text.grid(row=16, column=1)

    acq_para_corrects_label = tk.Label(root, text='Enter the min corrects amount:')
    acq_para_corrects_label.grid(row=17, column=0)
    acq_para_corrects_text = tk.Entry(root, width=30, justify='center')
    acq_para_corrects_text.grid(row=17, column=1)

    acq_para_session_len_label = tk.Label(root, text='Enter the min session length time:')
    acq_para_session_len_label.grid(row=18, column=0)
    acq_para_session_len_text = tk.Entry(root, width=30, justify='center')
    acq_para_session_len_text.grid(row=18, column=1)

    # creates the acquisition button
    acq_para_btn = tk.Button(root, text='Acquisition Parameterized',
                             command=lambda: acq_para_button(acq_para_text, acq_para_corrects_text,
                                                             acq_para_session_len_text),
                             width=30)
    acq_para_btn.grid(row=19, column=0)

    # visual spacer between acquisition and extinction
    spacer_btw_acq_ext = tk.Label(root, text='', bg='#D6D6D6', width=57)
    spacer_btw_acq_ext.grid(row=20, columnspan=2)

    # creates extinction criteria widgets
    ext_para_label = tk.Label(root, text='Enter criteria as n days/n+1 days:')
    ext_para_label.grid(row=21, column=0)
    ext_para_text = tk.Entry(root, width=30, justify='center')
    ext_para_text.grid(row=21, column=1)

    ext_para_omissions_label = tk.Label(root, text='Enter the min omissions req:')
    ext_para_omissions_label.grid(row=22, column=0)
    ext_para_omissions_text = tk.Entry(root, width=30, justify='center')
    ext_para_omissions_text.grid(row=22, column=1)

    # creates extinction buttons
    ext_para_btn = tk.Button(root, text='Extinction Parameterized',
                             command=lambda: ext_para_button(ext_para_text, ext_para_omissions_text),
                             width=30)
    ext_para_btn.grid(row=23, column=0)
