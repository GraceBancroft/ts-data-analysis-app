from setup import *


def get_auto(test_type):
    """
    A generic function used to get all the rows of a specific autoshaping test. After the csv is generated, it
     will ask for the user to save the file in a directory. Used for Habituation 1 and 2, and Autoshaping.

    :param test_type: A string that represents one of the autoshaping test types.
    """

    df = data_setup(test_type)
    if df is not None:
        save_file_message(df)


def get_auto_first_day(test_type):
    """
    A generic function used to get all the first days of a specific general touchscreen test. After the csv is
    generated, it will ask for the user to save the file in a directory. Used for Habituation 1 and 2, and Autoshaping.

    :param test_type: A string that represents one of the general touchscreen test types.
    """

    df = data_setup(test_type)
    if df is not None:
        df = df.loc[df['Day'] == 1]
        save_file_message(df)


def get_auto_last_day(test_type):
    """
    A generic function used to get all the last days of a specific general touchscreen test. After the csv is
    generated, it will ask for the user to save the file in a directory. Used for Habituation 1 and 2, and Autoshaping.

    :param test_type: A string that represents one of the general touchscreen test types.
    """

    df = data_setup(test_type)
    if df is not None:
        df = df.drop_duplicates(subset='ID', keep='last')
        save_file_message(df)


def check_enter_day(enter_day):
    """
    This function checks to make sure that the selected day value is valid.

    :param enter_day: An Entry widget that contains the numerical value of the day
    :return: The numerical value of the day in the Entry widget
    :except ValueError: If the value is empty or the value is not numeric, this function will stop and return.
    """

    try:
        selected_day = int(enter_day.get())
        return selected_day
    except ValueError:
        mb.showerror('General Touchscreen Error',
                     'check_enter_day() error: Either the value is empty or the value is not numeric!')
        print('check_enter_day() error: Either the value is empty or the value is not numeric!')
        return


def check_enter_id(enter_id):
    """
    This function checks to make sure that the selected id value is valid.

    :param enter_id: An Entry widget that contains the numerical value of the id
    :return: The numerical value of the id in the Entry widget
    :except ValueError: If the value is empty or the value is not numeric, this function will stop and return.
    """

    try:
        selected_id = int(enter_id.get())
        return selected_id
    except ValueError:
        mb.showerror('General Touchscreen Error',
                     'check_enter_id() error: Either the value is empty or the value is not numeric!')
        print('check_enter_id() error: Either the value is empty or the value is not numeric!')
        return


def get_auto_select_day(test_type, enter_day):
    """
    A generic function used to get all rows on a selected days of a specific general touchscreen test. After the csv is
    generated, it will ask for the user to save the file in a directory. Used for Habituation 1 and 2, and Autoshaping.

    :param test_type: A string that represents one of the general touchscreen test types.
    :param enter_day: An Entry widget that contains the selected day value
    """

    # check that the inputs to the criteria widgets are valid
    selected_day = check_enter_day(enter_day)
    if selected_day is None:
        mb.showerror('General Touchscreen Error',
                     'get_general_ts_select_day() error: Either the day value is empty or the value is not numeric!')
        print('get_general_ts_select_day() error: Either the day value is empty or the value is not numeric!')
        return

    df = data_setup(test_type)
    if df is not None:
        df = df.loc[df['Day'] == selected_day]
        save_file_message(df)


def get_auto_select_id(test_type, enter_id):
    """
    A generic function used to get all rows on a selected id of a specific general touchscreen test. After the csv is
    generated, it will ask for the user to save the file in a directory. Used for Habituation 1 and 2, and Autoshaping.

    :param test_type: A string that represents one of the general touchscreen test types.
    :param enter_id: An Entry widget that contains the selected id value
    """

    # check that the inputs to the criteria widgets are valid
    selected_id = check_enter_id(enter_id)
    if selected_id is None:
        mb.showerror('General Touchscreen Error',
                     'get_general_ts_select_id() error: Either the id value is empty or the value is not numeric!')
        print('get_general_ts_select_id() error: Either the id value is empty or the value is not numeric!')
        return

    df = data_setup(test_type)
    if df is not None:
        df = df.loc[df['Day'] == selected_id]
        save_file_message(df)

def auto_widget_check(widget):
    """
    This function checks the Auto select id and select day widgets. It checks if the value given is a valid numeric
    value, otherwise it print an error message and return None.

    :param widget: An entry widget that contains the value of the selected id/day.
    :return: None: If the function doesn't pass the widget check, it will stop and return None.
    """

    try:
        widget_value = int(widget.get())
    except ValueError:
        mb.showerror('LD Probe Error', 'auto_widget_check() error: The selected day/id is invalid or empty!')
        print('auto_widget_check() error: The selected day/id is invalid or empty!')
        return None

    return widget_value

def auto_select_block(block_number):
    """
    This function creates a csv file for the LD Probe test. Each row will be the last days of a specific block. This
    function works better if there are multiple blocks that are being entered. For single blocks, please use the Last
    Day Difficulty All button! Afterward, the function will ask the user to save the newly created csv file in a
    directory.

    :param block_number: An entry widget that contains the value for the block number.
    :return: None: If the function doesn't pass the widget check, it will stop and return None.
    """

    if auto_widget_check(block_number) is not None:
        selected_block = auto_widget_check(block_number)
    else:
        mb.showerror('LD Probe Error', 'auto_select_block() error: The block number criteria is empty or invalid!')
        print('auto_select_block() error: The block number criteria is empty or invalid!')
        return None

    block_day_range_max = 4 * selected_block
    block_day_range_min = block_day_range_max - 3
    block_day_total_range = [*range(block_day_range_min, block_day_range_max + 1, 1)]

    df = data_setup('Auto')
    if df is not None:
        df = df.loc[(df['Day'] == block_day_total_range[1]) | (df['Day'] == block_day_total_range[3])]

        save_file_message(df)

def make_auto_buttons(tk, root):
    """
    This function creates all the general touchscreen buttons found on the General Touchscreen sub-menu.

    :param tk: The TKinter library
    :param root: A specific frame where all the buttons will live on.
    """

    # creates hab 1 button
    hab_one_btn = tk.Button(root, text='Habituation 1', command=lambda: get_auto('Hab1'), width=30)
    hab_one_btn.grid(row=0, column=0)

    # visual spacer between hab 1 and hab 2
    spacer_btn_two = tk.Label(root, text='', width=57, bg='#D6D6D6')
    spacer_btn_two.grid(row=8, columnspan=2)

    # creates all the hab 2 buttons
    hab_two_btn = tk.Button(root, text='Habituation 2 (All)', command=lambda: get_auto('Hab2'), width=30)
    hab_two_btn.grid(row=1, column=0)
    hab_two_first_btn = tk.Button(root, text='Habituation 2 (First Day)', command=lambda: get_auto_first_day('Hab2'),
                             width=30)
    hab_two_first_btn.grid(row=10, column=0)
    hab_two_last_btn = tk.Button(root, text='Habituation 2 (Last Day)', command=lambda: get_auto_last_day('Hab2'),
                            width=30)
    hab_two_last_btn.grid(row=11, column=0)
    hab_two_sel_day_text = tk.Entry(root, width=30, justify='center')
    hab_two_sel_day_text.grid(row=12, column=1)
    hab_two_sel_day_btn = tk.Button(root, text='Habituation 2(Select Day)',
                               command=lambda: get_auto_select_day('Hab2', hab_two_sel_day_text), width=30)
    hab_two_sel_day_btn.grid(row=12, column=0)
    hab_two_sel_id_text = tk.Entry(root, width=30, justify='center')
    hab_two_sel_id_text.grid(row=13, column=1)
    hab_two_sel_id_btn = tk.Button(root, text='Habituation 2 (Select ID)',
                              command=lambda: get_auto_select_id('Hab2', hab_two_sel_id_text), width=30)
    hab_two_sel_id_btn.grid(row=13, column=0)

    # visual spacer between hab 2 and auto
    spacer_btn_two = tk.Label(root, text='', width=57, bg='#D6D6D6')
    spacer_btn_two.grid(row=8, columnspan=2)

    # creates all the auto buttons
    auto_btn = tk.Button(root, text='Autoshaping (All)', command=lambda: get_auto('Auto'), width=30)
    auto_btn.grid(row=1, column=0)
    auto_first_btn = tk.Button(root, text='Autoshaping (First Day)', command=lambda: get_auto_first_day('Auto'),
                                  width=30)
    auto_first_btn.grid(row=10, column=0)
    auto_last_btn = tk.Button(root, text='Autoshaping (Last Day)', command=lambda: get_auto_last_day('Auto'),
                                 width=30)
    auto_last_btn.grid(row=11, column=0)
    auto_sel_day_text = tk.Entry(root, width=30, justify='center')
    auto_sel_day_text.grid(row=12, column=1)
    auto_sel_day_btn = tk.Button(root, text='Autoshaping (Select Day)',
                                    command=lambda: get_auto_select_day('Auto', auto_sel_day_text), width=30)
    auto_sel_day_btn.grid(row=12, column=0)
    auto_sel_id_text = tk.Entry(root, width=30, justify='center')
    auto_sel_id_text.grid(row=13, column=1)
    auto_sel_id_btn = tk.Button(root, text='Autoshaping (Select ID)',
                                   command=lambda: get_auto_select_id('Auto', auto_sel_id_text), width=30)
    auto_sel_id_btn.grid(row=13, column=0)

    auto_block_number = tk.Entry(root, width=30, justify='center')
    auto_block_number.grid(row=4, column=1)
    auto_button_select_block = tk.Button(root, text='LD Probe (Select Block)',
                                             command=lambda: auto_select_block(
                                                 auto_block_number), width=30)
    auto_button_select_block.grid(row=4, column=0)

