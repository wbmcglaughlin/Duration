import os

import PySimpleGUI as sg

from src.app_information import get_app_data_path, DEBUG_MODE, get_app_archive_path, get_duration_node_list
from src.user_data import get_today_duration, get_total_project_time

BAR_COLORS = ('#23a0a0', '#56d856', '#be45be', '#5681d8', '#d34545', '#BE7C29')


def generate_layout():
    layout = []

    if DEBUG_MODE:
        layout += [[sg.Text("DEBUG MODE")]]

    layout += [[sg.TabGroup(
        [[
            sg.Tab('main', main_tab()),
            sg.Tab('add', add_tab()),
            sg.Tab('info', info_tab()),
            sg.Tab('archive', archive_tab())
        ]],
        key='-TAB_GROUP-',
        enable_events=True
    )]]

    layout += [[sg.Text('Refresh', font='Any 8', key='-REFRESH-', enable_events=True),
                sg.Text("Cancel", font='Any 8', key='-CANCEL-', enable_events=True),
                sg.Text("Open Data", font='Any 8', key='-DATA_FOLDER-', enable_events=True),
                sg.Text("Archive", font='Any 8', key='-ARCHIVE_DURATION-', enable_events=True),
                sg.Text('❎', enable_events=True, key='Exit Text')
                ]]

    return layout


def main_tab():
    duration_nodes_list = get_duration_node_list()

    bar_color = sg.theme_progress_bar_color()
    this_color = BAR_COLORS[1 % len(BAR_COLORS)]

    main_tab_layout = [[sg.Text("Duration: ", key='-NAME-'),
                        sg.ProgressBar(100, 'h', size=(10, 18), key='-PROG-', bar_color=(this_color, bar_color[1])),
                        sg.Text("", key='-START_TIME-'),
                        sg.Text("", key='-ELAPSED_TIME-')
                        ]]

    default_duration = '' if len(duration_nodes_list) == 0 else duration_nodes_list[0]

    main_tab_layout += [[
        sg.Text('Selected:'),
        sg.Combo(duration_nodes_list, default_value=default_duration,
                 size=(20, 1), key='-DATA_TYPE-', readonly=True),
        sg.Combo(list([15, 30, 45, 60]), default_value=45, size=(5, 1), key='-DURATION_TIME-', readonly=True),
        sg.Text('Start', enable_events=True, key='START'),
        sg.Text('End', enable_events=True, key='END')
    ]]

    return main_tab_layout


def add_tab():
    add_tab_layout = [[
        sg.Text('New:'),
        sg.InputText(size=(20, 1), key='-ADD_TYPE-'),
        sg.Text('Add', enable_events=True, key='ADD')
    ]]

    return add_tab_layout


def info_tab():
    info_tab_layout = [
        [
            sg.Text('Time Today:'),
            sg.Text(f'{get_today_duration():.2f}', key='-TIME_TODAY-')
        ],
        [
            sg.Text('Project Time: '),
            sg.Text('-', key='-PROJECT_TIME-'),
            sg.Text('Project Time Today:'),
            sg.Text(f'-', key='-PROJECT_TIME_TODAY-')
        ]
    ]

    return info_tab_layout


def archive_tab():
    archive_tab_layout_table = []
    archived_durations = os.listdir(get_app_archive_path())
    for archived_duration_path in archived_durations:
        archive_tab_layout_table.append(
            [sg.Text(archived_duration_path), sg.Text(f'{get_total_project_time(archived_duration_path, True):.2f}')]
        )

    default_duration = '' if len(archived_durations) == 0 else archived_durations[0]

    archive_tab_layout = [
        [
            sg.Text('Archive'),
            sg.Combo(archived_durations, default_value=default_duration,
                     size=(20, 1), key='-DATA_TYPE-', readonly=True),
            sg.Text('Open Archive', font='Any 8', enable_events=True, key='-OPEN_ARCHIVE-')
        ]
    ]

    return archive_tab_layout


def archive_window_tab():
    archive_tab_layout_table = []
    archived_durations = os.listdir(get_app_archive_path())
    for archived_duration_path in archived_durations:
        archive_tab_layout_table.append(
            [archived_duration_path, f'{get_total_project_time(archived_duration_path, True):.2f}']
        )

    archive_tab_layout = [
        [
            sg.Table(archive_tab_layout_table,
                     headings=['Duration', 'Total Time'],
                     max_col_width=25,
                     auto_size_columns=True,
                     justification='right',
                     # alternating_row_color='lightblue',
                     num_rows=min(len(archive_tab_layout_table), 20))
        ],
        [sg.Text('❎', enable_events=True, key='Exit Text')]
    ]

    return archive_tab_layout


def settings_tab():
    pass
