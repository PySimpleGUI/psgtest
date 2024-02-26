'''
Copyright 2021-2024 PySimpleSoft, Inc. and/or its licensors. All rights reserved.

Redistribution, modification, or any other use of PySimpleGUI or any portion thereof is subject
to the terms of the PySimpleGUI License Agreement available at https://eula.pysimplegui.com.

You may not redistribute, modify or otherwise use PySimpleGUI or its contents except pursuant
to the PySimpleGUI License Agreement.
'''

import os.path
import sys
import subprocess
import PySimpleGUI as sg
import time
import psutil
import signal

version = '5.0.0'
__version__ = version.split()[0]


'''
M""M                     dP            dP dP                   
M  M                     88            88 88                   
M  M 88d888b. .d8888b. d8888P .d8888b. 88 88 .d8888b. 88d888b. 
M  M 88'  `88 Y8ooooo.   88   88'  `88 88 88 88ooood8 88'  `88 
M  M 88    88       88   88   88.  .88 88 88 88.  ... 88       
M  M dP    dP `88888P'   dP   `88888P8 dP dP `88888P' dP       
MMMM
'''


def pip_install_thread(window, sp):
    window.write_event_value('-THREAD-', (sp, 'Install thread started'))
    for line in sp.stdout:
        oline = line.decode().rstrip()
        window.write_event_value('-THREAD-', (sp, oline))



def pip_install_latest():

    pip_command = '-m pip install --upgrade --no-cache-dir PySimpleGUI>=5'

    python_command = sys.executable  # always use the currently running interpreter to perform the pip!
    if 'pythonw' in python_command:
        python_command = python_command.replace('pythonw', 'python')

    layout = [[sg.Text('Installing PySimpleGUI', font='_ 14')],
              [sg.Multiline(s=(90, 15), k='-MLINE-', reroute_cprint=True, reroute_stdout=True, echo_stdout_stderr=True, write_only=True, expand_x=True, expand_y=True)],
              [sg.Push(), sg.Button('Downloading...', k='-EXIT-'), sg.Sizegrip()]]

    window = sg.Window('Pip Install PySimpleGUI Utilities', layout, finalize=True, keep_on_top=True, modal=True, disable_close=True, resizable=True)

    window.disable_debugger()

    sg.cprint('Installing with the Python interpreter =', python_command, c='white on purple')

    sp = sg.execute_command_subprocess(python_command, pip_command, pipe_output=True, wait=False)

    window.start_thread(lambda: pip_install_thread(window, sp), end_key='-THREAD DONE-')

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or (event == '-EXIT-' and window['-EXIT-'].ButtonText == 'Done'):
            break
        elif event == '-THREAD DONE-':
            sg.cprint('\n')
            show_package_version('PySimpleGUI')
            sg.cprint('Done Installing PySimpleGUI.  Click Done and the program will restart.', c='white on red', font='default 12 italic')
            window['-EXIT-'].update(text='Done', button_color='white on red')
        elif event == '-THREAD-':
            sg.cprint(values['-THREAD-'][1])

    window.close()

def suggest_upgrade_gui():
    layout = [[sg.Image(sg.EMOJI_BASE64_HAPPY_GASP), sg.Text(f'PySimpleGUI 5+ Required', font='_ 15 bold')],
              [sg.Text(f'PySimpleGUI 5+ required for this program to function correctly.')],
              [sg.Text(f'You are running PySimpleGUI {sg.version}')],
              [sg.Text('Would you like to upgrade to the latest version of PySimpleGUI now?')],
              [sg.Push(), sg.Button('Upgrade', size=8, k='-UPGRADE-'), sg.Button('Cancel', size=8)]]

    window = sg.Window(title=f'Newer version of PySimpleGUI required', layout=layout, font='_ 12')

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Cancel'):
            window.close()
            break
        elif event == '-UPGRADE-':
            window.close()
            pip_install_latest()
            sg.execute_command_subprocess(sys.executable, __file__, pipe_output=True, wait=False)
            break


def make_str_pre_38(package):
    return f"""
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import pkg_resources
try:
    ver=pkg_resources.get_distribution("{package}").version.rstrip()
except:
    ver=' '
print(ver, end='')
"""

def make_str(package):
    return f"""
import importlib.metadata

try:
    ver = importlib.metadata.version("{package}")
except importlib.metadata.PackageNotFoundError:
    ver = ' '
print(ver, end='')
"""


def show_package_version(package):
    """
    Function that shows all versions of a package
    """
    interpreter = sg.execute_py_get_interpreter()
    sg.cprint(f'{package} upgraded to ', end='', c='red')
    # print(f'{interpreter}')
    if sys.version_info.major == 3 and sys.version_info.minor in (6, 7):  # if running Python version 3.6 or 3.7
        pstr = make_str_pre_38(package)
    else:
        pstr = make_str(package)
    temp_file = os.path.join(os.path.dirname(__file__), 'temp_py.py')
    with open(temp_file, 'w') as file:
        file.write(pstr)
    sg.execute_py_file(temp_file, interpreter_command=interpreter, pipe_output=True, wait=True)
    os.remove(temp_file)



def upgrade_check():
    if not sg.version.startswith('5'):
        suggest_upgrade_gui()
        exit()


"""
                             dP                       dP   
                             88                       88   
88d888b. .d8888b. .d8888b. d8888P .d8888b. .d8888b. d8888P 
88'  `88 Y8ooooo. 88'  `88   88   88ooood8 Y8ooooo.   88   
88.  .88       88 88.  .88   88   88.  ...       88   88   
88Y888P' `88888P' `8888P88   dP   `88888P' `88888P'   dP   
88                     .88                                 
dP                 d8888P


3.0 21-Apr-2023 - Expanded regression tests. Now works correctly. Added ability to run across all interpreters. Made regression threaded.
3.1 21-Apr-2023 - Removed "Edit Me" button. Instead you should use the right-click Edit Me that is standard in PySimpleGUI utilities
3.2 23-Apr-2023 - Added piped output for Regression Tests - now creates tabs for tests when running regression and will keep open any that fail
                  Added cleaning up of all potentially running processes upon exit. Makes quitting with lots of tests running MUCH easier since don't have to manually kill them
3.3 23-Apr-2023 - Remove the entry from sp_to_filename when killing process
3.4 29-Apr-2023 - Allow non-python programs to be run.  If the file does not end in .py or .pyw, then the file will be executed directly
5.0.0 26-Feb-2024   - New 5.0.0 release

"""


DEFAULT_OUTPUT_SIZE = (80,5)
file_list_dict = {}
sp_to_mline_dict = {}
sp_to_filename = {}

'''
M""MMMMM""MM          dP                               MM""""""""`M                                     
M  MMMMM  MM          88                               MM  mmmmmmmM                                     
M         `M .d8888b. 88 88d888b. .d8888b. 88d888b.    M'      MMMM dP    dP 88d888b. .d8888b. .d8888b. 
M  MMMMM  MM 88ooood8 88 88'  `88 88ooood8 88'  `88    MM  MMMMMMMM 88    88 88'  `88 88'  `"" Y8ooooo. 
M  MMMMM  MM 88.  ... 88 88.  .88 88.  ... 88          MM  MMMMMMMM 88.  .88 88    88 88.  ...       88 
M  MMMMM  MM `88888P' dP 88Y888P' `88888P' dP          MM  MMMMMMMM `88888P' dP    dP `88888P' `88888P' 
MMMMMMMMMMMM             88                            MMMMMMMMMMMM                                     
                         dP
'''


def get_file_list_dict():
    """
    Returns dictionary of files
    Key is short filename
    Value is the full filename and path

    :return: Dictionary of demo files
    :rtype: Dict[str:str]
    """

    demo_path = get_demo_path()
    demo_files_dict = {}
    for dirname, dirnames, filenames in os.walk(demo_path):
        for filename in filenames:
            if filename.endswith('.py') or filename.endswith('.pyw'):
                fname_full = os.path.join(dirname, filename)
                if filename not in demo_files_dict.keys():
                    demo_files_dict[filename] = fname_full
                else:
                    # Allow up to 100 dupicated names. After that, give up
                    for i in range(1, 100):
                        new_filename = f'{filename}_{i}'
                        if new_filename not in demo_files_dict:
                            demo_files_dict[new_filename] = fname_full
                            break

    return demo_files_dict


def get_file_list():
    """
    Returns list of filenames of files to display
    No path is shown, only the short filename

    :return: List of filenames
    :rtype: List[str]
    """
    return sorted(list(get_file_list_dict().keys()))


def get_demo_path():
    """
    Get the top-level folder path
    :return: Path to list of files using the user settings for this file.  Returns folder of this file if not found
    :rtype: str
    """
    demo_path = sg.user_settings_get_entry('-test script folder-', os.path.dirname(__file__))

    return demo_path


def get_theme():
    """
    Get the theme to use for the program
    Value is in this program's user settings. If none set, then use PySimpleGUI's global default theme
    :return: The theme
    :rtype: str
    """
    # First get the current global theme for PySimpleGUI to use if none has been set for this program
    try:
        global_theme = sg.theme_global()
    except:
        global_theme = sg.theme()
    # Get theme from user settings for this program.  Use global theme if no entry found
    user_theme = sg.user_settings_get_entry('-theme-', '')
    if user_theme == '':
        user_theme = global_theme
    return user_theme

def get_next_program(list_of_programs):
    global file_list_dict

    for file in list_of_programs:
        if file not in file_list_dict:
            file_to_run = file
        else:
            file_to_run = str(file_list_dict[file])
        yield file, file_to_run



def tcprint(window, item, colors=None):
    """
    Threaded cprint - like cprint but with only 1 argument to print.
    Used by threads to cprint to a window

    :param window:
    :param item:
    :param colors:
    :return:
    """
    window.write_event_value(('-CPRINT-', item, colors), None)


'''
M""""""""M dP                                        dP 
Mmmm  mmmM 88                                        88 
MMMM  MMMM 88d888b. 88d888b. .d8888b. .d8888b. .d888b88 
MMMM  MMMM 88'  `88 88'  `88 88ooood8 88'  `88 88'  `88 
MMMM  MMMM 88    88 88       88.  ... 88.  .88 88.  .88 
MMMM  MMMM dP    dP dP       `88888P' `88888P8 `88888P8 
MMMMMMMMMM
'''

def piped_output_thread(window: sg.Window, sp: subprocess.Popen, regression=False):
    """
    The thread that's used to run the subprocess so that the GUI can continue and the stdout/stderror is collected

    :param window:
    :param sp:
    :return:
    """

    window.write_event_value('-THREAD-', (sp, '===THEAD STARTING==='))
    window.write_event_value('-THREAD-', (sp, '----- STDOUT & STDERR Follows ----'))
    for line in sp.stdout:
        oline = line.decode().rstrip()
        window.write_event_value('-THREAD-', (sp, oline))
    if regression:
        window.write_event_value('-THREAD-', (sp, '===THEAD DONE REGRESSION==='))
    else:
        window.write_event_value('-THREAD-', (sp, '===THEAD DONE==='))




'''
MM"""""""`YM                                                       
MM  mmmmm  M                                                       
M'        .M 88d888b. .d8888b. .d8888b. .d8888b. .d8888b. .d8888b. 
MM  MMMMMMMM 88'  `88 88'  `88 88'  `"" 88ooood8 Y8ooooo. Y8ooooo. 
MM  MMMMMMMM 88       88.  .88 88.  ... 88.  ...       88       88 
MM  MMMMMMMM dP       `88888P' `88888P' `88888P' `88888P' `88888P' 
MMMMMMMMMMMM                                                       
                                                                   
MM""""""""`M                                     
MM  mmmmmmmM                                     
M'      MMMM dP    dP 88d888b. .d8888b. .d8888b. 
MM  MMMMMMMM 88    88 88'  `88 88'  `"" Y8ooooo. 
MM  MMMMMMMM 88.  .88 88    88 88.  ...       88 
MM  MMMMMMMM `88888P' dP    dP `88888P' `88888P' 
MMMMMMMMMMMM
'''



def kill_proc(pid, sig=signal.SIGTERM, include_parent=True, timeout=None, on_terminate=None):
    """Kill a process tree (including grandchildren) with signal
    "sig" and return a (gone, still_alive) tuple.
    "on_terminate", if specified, is a callabck function which is
    called as soon as a child terminates.
    """
    if pid == os.getpid():
        raise RuntimeError("I refuse to kill myself")
    parent = psutil.Process(pid)
    parent.send_signal(sig)
    sg.Print(f'tried killing {pid} with parent {parent}')

def kill_proc_tree(pid, sig=signal.SIGTERM, include_parent=True, timeout=None, on_terminate=None):
    """Kill a process tree (including grandchildren) with signal
    "sig" and return a (gone, still_alive) tuple.
    "on_terminate", if specified, is a callabck function which is
    called as soon as a child terminates.
    """
    try:
        if pid == os.getpid():
            raise RuntimeError("I refuse to kill myself")
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        if include_parent:
            children.append(parent)
        for p in children:
            p.send_signal(sig)
        gone, alive = psutil.wait_procs(children, timeout=timeout, callback=on_terminate)
    except Exception as e:
        print(f'Error killing process {e}')
        sg.cprint(f'Error killing process {e}', colors='white on red')
        return (None, None)
    return (gone, alive)


'''
MM"""""""`MM                                                       oo                   
MM  mmmm,  M                                                                            
M'        .M .d8888b. .d8888b. 88d888b. .d8888b. .d8888b. .d8888b. dP .d8888b. 88d888b. 
MM  MMMb. "M 88ooood8 88'  `88 88'  `88 88ooood8 Y8ooooo. Y8ooooo. 88 88'  `88 88'  `88 
MM  MMMMM  M 88.  ... 88.  .88 88       88.  ...       88       88 88 88.  .88 88    88 
MM  MMMMM  M `88888P' `8888P88 dP       `88888P' `88888P' `88888P' dP `88888P' dP    dP 
MMMMMMMMMMMM               .88                                                          
                       d8888P                                                           
M""""""""M                     dP            
Mmmm  mmmM                     88            
MMMM  MMMM .d8888b. .d8888b. d8888P .d8888b. 
MMMM  MMMM 88ooood8 Y8ooooo.   88   Y8ooooo. 
MMMM  MMMM 88.  ...       88   88         88 
MMMM  MMMM `88888P' `88888P'   dP   `88888P' 
MMMMMMMMMM
'''




def regression_thread(window:sg.Window, program_list, block_size, iterations, kill_after=None, interpreter_path=None, pipe_output=False):
    global sp_to_mline_dict, sp_to_filename

    tcprint(window , f"-------- Start Regression using {interpreter_path} --------", colors='white on green')
    block_count = 0
    if interpreter_path is not None:
        interpreter_paths = [interpreter_path, ]
    else:
        interpreter_paths = []
        for interpreter in interpreter_dict.values():
            ipath = sg.user_settings_get_entry(interpreter, '')
            if ipath:
                interpreter_paths.append(ipath)
    for interpreter_path in interpreter_paths:
        tcprint(window, f'Testing interpreter {interpreter_path}', colors='white on blue')
        for iteration in range(iterations):
            tcprint(window, f'Starting Iteration Number {iteration}', 'white on red')
            for file, file_to_run in get_next_program(program_list):
                tcprint(window, f'Starting {file_to_run}', 'white on purple')
                sp = sg.execute_command_subprocess(interpreter_path, f'"{file_to_run}"', pipe_output=pipe_output)
                if pipe_output:
                    window.write_event_value('-MAKE TAB-', (sp, file))
                    window.start_thread(lambda: piped_output_thread(window, sp, regression=True), '-PIPE THREAD DONE-')

                if kill_after is not None:
                    window.timer_start(kill_after * 1000, ('-TIMER THREAD-', sp), repeating=False)
                    if (block_count+1) % block_size == 0:
                        time.sleep(kill_after)
                block_count += 1
    tcprint(window , f"-------- DONE WITH REGRESSION TEST -------", colors='white on green')


'''
M"""""`'"""`YM          dP                   M""""""""M          dP       
M  mm.  mm.  M          88                   Mmmm  mmmM          88       
M  MMM  MMM  M .d8888b. 88  .dP  .d8888b.    MMMM  MMMM .d8888b. 88d888b. 
M  MMM  MMM  M 88'  `88 88888"   88ooood8    MMMM  MMMM 88'  `88 88'  `88 
M  MMM  MMM  M 88.  .88 88  `8b. 88.  ...    MMMM  MMMM 88.  .88 88.  .88 
M  MMM  MMM  M `88888P8 dP   `YP `88888P'    MMMM  MMMM `88888P8 88Y8888' 
MMMMMMMMMMMMMM                               MMMMMMMMMM
'''


def make_output_tab(tab_text, key, tab_key):
    tab = sg.Tab(tab_text, [[sg.Multiline(
        size=(sg.user_settings_get_entry('-output width-', DEFAULT_OUTPUT_SIZE[0]), sg.user_settings_get_entry('-output height-', DEFAULT_OUTPUT_SIZE[1])),
        expand_x=True, expand_y=True, write_only=True, key=key, auto_refresh=True, font=sg.user_settings_get_entry('-output font-', 'Courier 10')), ],
        [sg.B('Copy To Clipboard', k=('-COPY-', key)), sg.B('Clear', k=('-CLEAR-', key)), sg.B('Close Tab', k=('-CLOSE-', tab_key))]],
                 right_click_menu=['', [f'Close::{tab_key}', 'Exit']], k=tab_key, )

    return tab



"""
MP""""""`MM            dP     dP   oo                            
M  mmmmm..M            88     88                                 
M.      `YM .d8888b. d8888P d8888P dP 88d888b. .d8888b. .d8888b. 
MMMMMMM.  M 88ooood8   88     88   88 88'  `88 88'  `88 Y8ooooo. 
M. .MMM'  M 88.  ...   88     88   88 88    88 88.  .88       88 
Mb.     .dM `88888P'   dP     dP   dP dP    dP `8888P88 `88888P' 
MMMMMMMMMMM                                         .88          
                                                d8888P
"""

# Dictionary of Python version numbers to KEY that is used in settings file and settings GUI layout
interpreter_dict = {'3.4': '-P34-', '3.5': '-P35-', '3.6': '-P36-', '3.7': '-P37-',
                    '3.8': '-P38-', '3.9': '-P39-', '3.10': '-P310-', '3.11': '-P311-', '3.12': '-P312-', 'Other':'-P OTHER-'}

def settings_window():
    """
    Show the settings window.
    This is where the folder paths and program paths are set.
    Returns True if settings were changed

    :return: True if settings were changed
    :rtype: (bool)
    """

    try:  # in case running with old version of PySimpleGUI that doesn't have a global PSG settings path
        global_theme = sg.theme_global()
    except:
        global_theme = ''


    layout = [[sg.T('Program Settings', font='_ 25'), sg.Image(data=sg.EMOJI_BASE64_PONDER)],
              [sg.Frame('Path to Tree of Test Programs', [[sg.Combo(sorted(sg.user_settings_get_entry('-folder names-', [])),
                                                                    default_value=sg.user_settings_get_entry('-test script folder-', get_demo_path()),
                                                                    size=(50, 1), key='-FOLDERNAME-'),
                                                           sg.FolderBrowse('Folder Browse', target='-FOLDERNAME-'), sg.B('Clear History')]], font='_ 14')],
              [sg.Frame('Python Interpreters (path to each python executible)', [[sg.Radio('', 1, k=(interpreter_dict[k],'-RADIO-')), sg.T(k, s=(5, 1)),
                                                                                  sg.In(sg.user_settings_get_entry(interpreter_dict[k], ''),
                                                                                        k=interpreter_dict[k]), sg.FileBrowse()] for k in interpreter_dict])],


              [sg.Frame('Theme', [[sg.T('Leave blank to use global default'), sg.T(global_theme)],
                                  [sg.Combo([''] + sg.theme_list(), sg.user_settings_get_entry('-theme-', ''), readonly=True, k='-THEME-')]], font='_ 14')],

              [sg.Frame('Text Output Settings', [[sg.T('Font and size (e.g. Courier 10) for the output:'),
                                                  sg.In(sg.user_settings_get_entry('-output font-', 'Courier 10'), k='-MLINE FONT-', s=(15, 1))],
                                                 [sg.T('Output size Width x Height in chars'),
                                                  sg.In(sg.user_settings_get_entry('-output width-', DEFAULT_OUTPUT_SIZE[0]), k='-MLINE WIDTH-', s=(4, 1)),
                                                  sg.T(' x '),
                                                  sg.In(sg.user_settings_get_entry('-output height-', DEFAULT_OUTPUT_SIZE[1]), k='-MLINE HEIGHT-', s=(4, 1))]],
                        font='_ 14')],

              [sg.Frame('Double-click Will...', [[sg.R('Run', 2, sg.user_settings_get_entry('-dclick runs-', False), k='-DCLICK RUNS-'),
                                                  sg.R('Edit', 2, sg.user_settings_get_entry('-dclick edits-', False), k='-DCLICK EDITS-'),
                                                  sg.R('Nothing', 2, sg.user_settings_get_entry('-dclick none-', False), k='-DCLICK NONE-')]], font='_ 14')],

              [sg.B('Ok', bind_return_key=True), sg.B('Cancel')],
              ]

    window = sg.Window('Settings', layout, finalize=True)

    current_interpreter = sg.user_settings_get_entry('-current interpreter-', list(interpreter_dict.keys())[0])
    interpreter_radio_key = (interpreter_dict[current_interpreter], '-RADIO-') if current_interpreter in interpreter_dict.keys() else None
    window[interpreter_radio_key].update(True)
    settings_changed = False

    while True:
        event, values = window.read()
        if event in ('Cancel', sg.WIN_CLOSED):
            break
        if event == 'Ok':
            sg.user_settings_set_entry('-test script folder-', values['-FOLDERNAME-'])
            sg.user_settings_set_entry('-theme-', values['-THEME-'])
            sg.user_settings_set_entry('-folder names-', list(set(sg.user_settings_get_entry('-folder names-', []) + [values['-FOLDERNAME-'], ])))
            sg.user_settings_set_entry('-dclick runs-', values['-DCLICK RUNS-'])
            sg.user_settings_set_entry('-dclick edits-', values['-DCLICK EDITS-'])
            sg.user_settings_set_entry('-dclick nothing-', values['-DCLICK NONE-'])
            for key in interpreter_dict.values():
                sg.user_settings_set_entry(key, values[key])
            sg.user_settings_set_entry('-output font-', values['-MLINE FONT-'])
            sg.user_settings_set_entry('-output width-', values['-MLINE WIDTH-'])
            sg.user_settings_set_entry('-output height-', values['-MLINE HEIGHT-'])
            current_interpreter = current_interpreter_path = ''
            for k in interpreter_dict.keys():
                if values[(interpreter_dict[k], '-RADIO-')]:
                    current_interpreter = k
                    current_interpreter_path = values[interpreter_dict[k]]
            sg.user_settings_set_entry('-current interpreter-', current_interpreter)
            sg.user_settings_set_entry('-interpreter path-', current_interpreter_path)
            settings_changed = True
            break
        elif event == 'Clear History':
            sg.user_settings_set_entry('-folder names-', [])
            window['-FOLDERNAME-'].update(values=[], value='')

    window.close()
    return settings_changed




'''
M"""""`'"""`YM          dP                
M  mm.  mm.  M          88                
M  MMM  MMM  M .d8888b. 88  .dP  .d8888b. 
M  MMM  MMM  M 88'  `88 88888"   88ooood8 
M  MMM  MMM  M 88.  .88 88  `8b. 88.  ... 
M  MMM  MMM  M `88888P8 dP   `YP `88888P' 
MMMMMMMMMMMMMM                            

M""MMM""MMM""M oo                dP                     
M  MMM  MMM  M                   88                     
M  MMP  MMP  M dP 88d888b. .d888b88 .d8888b. dP  dP  dP 
M  MM'  MM' .M 88 88'  `88 88'  `88 88'  `88 88  88  88 
M  `' . '' .MM 88 88    88 88.  .88 88.  .88 88.88b.88' 
M    .d  .dMMM dP dP    dP `88888P8 `88888P' 8888P Y8P  
MMMMMMMMMMMMMM
'''


def make_window():
    """
    Creates the main window
    :return: The main window object
    :rtype: (sg.Window)
    """
    global file_list_dict, sp_to_mline_dict, sp_to_filename


    icon = b'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAABmJLR0QA/wD/AP+gvaeTAAADv0lEQVRogd2Zy0tVQRzHP1bkDa1NtCgtolQIKwlcCJYtFRRsX0S7+gPS9tqDFlmLHhi1lhSF8LHQDKQnLYOgiMRF5SbBV6SW3Ra/3+mcbuece+aeOcfsC8O5zuM739/M/GZ+M0I6KAf6gHlN/UBlSn1bQzkwA2Rz0gxQtoa6jNGHCB9EhJcBQ5r3YA11GWMeEe0d/d2aN2urkw22iELwXb9FPmU/UujfGnqQ0R9C/KUcGNa8njXU9RdG+duRTdOTuCL8ptsUWQscEFPLJksioHAhVgYiDWdPBTZnxNYSKwg2ZuSpBY7Yzm4Tzg6UVP1Q/Dc+kqQh6zbi9S6VKBGv1aVlE15hUSLedWFIlIh3XTi7I9BGCJQ6vCPcT3DE2+dT/59BIyJqSv+uAr7g7+wVWmdK8xpTVRqCDPAWEdXuyS9DHHtOUx+uEWjdrLbNpKI0Dy4igt4BxQbtNgNvtG1nArqMcARYAX4CDQW0b9C2K8q1JigGXiMj2h2Dp1s5XmM2o9ZwRQVMAltj8JQA75XrsgVdRqhDXkBWgeMW+Oo9fEct8EVCBtdJr1nk7cLdxbZY5A3EDeK/muRL15M2ogGZ/qQNWaWwXTASMshZkQWuJtWJcjvnUiIH5eWkO1AU4/rgRdvkNcihFbSrHAJGgGVNw0B1jP6OaV8rwOEYPH9gA/AKGaGbPuWHcO8f3jRHPGNuKc9LLF0HzijhR/wPvhEtH0WCwgpgDDeMLxTbgE/KczoGDwClwGclO+lTXgQsafl+T36F5n0j3mieUp5PqqVgXFKiZwGCvIZ4Q/RKgg1pAcaBRWBBfzcH9F8EPFeuSwVZAOwAviJOVxtSz7n5jSEGVAKPcB8fvHBCfr8UFMrXqoavqskYHdrBQJ561Yhj5wqbBQ546rVo/hJwHtipqQ13VoNmZkDLO0yNKMV9l6qPUL8acewlZDkN5hgB8Fj5zvu0d26L4wH89bhX5ZIIen7jnDZ8YdIoD5wteqdP2S4tmw9p/0LrnPUrDHoOatXvvWgaU8F9/baG1srBNGL9HotCxpWzzafsAuFLC2Cv1pk26dRxvlh7dw6acZ29HVlOuxAjlgl3dpAYzGkfGZPaKGzbLQSdmG+/Dg5qvQ8mHd7RRr2mSiOgGVlCC+Q/EL3oVU23TTrbj5y8zguJzSVmilLgrmpZBPaZErQgI5ZFnj+7gCbkBdHmP1FzsUn7aNI+nafXBaLNnC9qgAmSv9rmSxPkuZdEjUzrgBPICVsFbAc2RmxrilXkBH+HBKsPkTtJKH4B042N7RpiCBAAAAAASUVORK5CYII='
    sg.set_options(icon=icon)
    theme = get_theme()
    if not theme:
        theme = sg.OFFICIAL_PYSIMPLEGUI_THEME
    sg.theme(theme)
    # First the window layout...2 columns

    filter_tooltip = "Filter files\nEnter a string in box to narrow down the list of files.\nFile list will update with list of files with string in filename."

    regression_frame_layout = [
        [sg.CBox('Kill test after', default=False, k='-REGRESSION KILL-'), sg.Input(15, s=4, justification='r', k='-REGRESSION SECONDS-'), sg.Text('seconds (regression tests)')],
        [sg.T('Run'), sg.I(5, s=4, justification='r', k='-REGRESSION BLOCK SIZE-'), sg.T('programs at a time')],
        [sg.T('Stress test using'), sg.Input(1, s=4, justification='r', k='-STRESS RUNS-'), sg.T('iterations')],
        [sg.B('Run Regression'), sg.B('Run Regression All Interpreters')]]

    left_col = sg.Column([
        [sg.T('Test Cases (choose 1 or more)', font='_ 15')],
        [sg.Listbox(values=get_file_list(), select_mode=sg.SELECT_MODE_EXTENDED, size=(50, 20), bind_return_key=True, key='-DEMO LIST-', expand_x=True,
                    expand_y=True)],
        # [sg.Listbox(values=get_file_list(), select_mode=sg.SELECT_MODE_EXTENDED, size=(50,20), bind_return_key=True, key='-DEMO LIST-')],
        [sg.Text('Filter (F1):', tooltip=filter_tooltip), sg.Input(size=(25, 1), focus=True, enable_events=True, key='-FILTER-', tooltip=filter_tooltip),
         sg.T(size=(15, 1), k='-FILTER NUMBER-')],
        [sg.T('Run a single file:'), sg.Input(size=35, k='-SINGLE FILE-')],
        [sg.Button('Run'), sg.B('Edit'), sg.B('Clear'), sg.B('Run All Interpreters')],
        [sg.CBox('Show test program\'s output in this window', default=True, k='-SHOW OUTPUT-')],
        [sg.Frame('Regression & Stress Testing', regression_frame_layout)],
    ], element_justification='l', expand_x=True, expand_y=True)

    output_tab_layout = [
        [sg.Multiline(
            size=(sg.user_settings_get_entry('-output width-', DEFAULT_OUTPUT_SIZE[0]), sg.user_settings_get_entry('-output height-', DEFAULT_OUTPUT_SIZE[1])),
            write_only=True, key='-ML-', reroute_stdout=False, reroute_stderr=False, echo_stdout_stderr=False, reroute_cprint=True, auto_refresh=True,
            expand_x=True, expand_y=True, font=sg.user_settings_get_entry('-output font-', 'Courier 10'))],
        [sg.B('Copy To Clipboard', key=('-COPY-', '-ML-')), sg.B('Clear', k=('-CLEAR-', '-ML-'))]]

    bottom_right = [
        [sg.B('Settings'), sg.Button('Exit')],
        [sg.T('psgtest ver ' + version + '   PySimpleGUI ver ' + sg.version.split(' ')[0] + '  tkinter ver ' + sg.tclversion_detailed, font='Default 8', pad=(0, 0))],
        [sg.T('Python ver ' + sys.version, font='Default 8', pad=(0, 0))]]

    # tab1 = sg.Tab('Output',old_right_col, k='-TAB1-',  expand_x=True, expand_y=True)
    tab1 = sg.Tab('Output', output_tab_layout, k='-TAB1-', )

    tab_group = sg.TabGroup([[tab1, ]], k='-TABGROUP-', expand_x=True, expand_y=True, font='_ 8', tab_location='topleft')
    # tab_group = sg.TabGroup([[tab1,]], k='-TABGROUP-')

    right_col = [[tab_group]] + bottom_right
    choose_folder_at_top = sg.pin(sg.Column([[sg.T('Click settings to set top of your tree or choose a previously chosen folder'),
                                              sg.Combo(sorted(sg.user_settings_get_entry('-folder names-', [])),
                                                       default_value=sg.user_settings_get_entry('-test script folder-', ''), size=(50, 30), key='-FOLDERNAME-',
                                                       enable_events=True, readonly=True)]], pad=(0, 0), k='-FOLDER CHOOSE-', expand_x=True, expand_y=True))

    interpreter_list = []
    for key, value in interpreter_dict.items():
        if sg.user_settings_get_entry(value, ''):
            interpreter_list.append(key)

    interpreter_list = sorted(interpreter_list)
    if len(interpreter_list) == 0:  # no interpreters found in settings file, so set one using the currently running version of Python
        default_interpreter = f'{sys.version_info[0]}.{sys.version_info[1]}'
        sg.user_settings_set_entry('-current interpreter-', default_interpreter)
        sg.user_settings_set_entry('-interpreter path-', sys.executable)
        key = interpreter_dict[default_interpreter]
        sg.user_settings_set_entry(key, sys.executable)
    else:
        default_interpreter = interpreter_list[0]
    choose_interpreter_at_top = sg.pin(sg.Column([[sg.T('Launch using'),
                                                   sg.Combo(sorted(interpreter_list),
                                                            default_value=sg.user_settings_get_entry('-current interpreter-', default_interpreter),
                                                            size=(4, 10), key='-INTERPRETER TOP-', enable_events=True, readonly=True)]],
                                                 pad=(0, 0), k='-INTEPRETER CHOOSE-', expand_x=True, expand_y=True))

    # ----- Full layout -----

    layout = [[sg.Image(data=icon, background_color='white'), sg.Text(f'psgtest - Simple Python Testing - Ver {version}', font='Any 20')],
              [sg.T('Testing Using Interpreter: ' + sg.user_settings_get_entry('-current interpreter-', ''), font='Default 12', k='-CURRENT INTERPRETER-'),
               sg.T('Interpreter path: ' + sg.user_settings_get_entry('-interpreter path-', ''), font='Default 12', k='-INTERPRETER PATH-')],
              [choose_folder_at_top, choose_interpreter_at_top],
              # [sg.Column([[left_col],[ lef_col_find_re]], element_justification='l',  expand_x=True, expand_y=True), sg.Column(right_col, element_justification='c', expand_x=True, expand_y=True)],
              [sg.Pane([sg.Column([[left_col]], element_justification='l', expand_x=True, expand_y=True),
                        sg.Column(right_col, element_justification='c', expand_x=True, expand_y=True)], orientation='h', relief=sg.RELIEF_SUNKEN, k='-PANE-',
                       expand_x=True, expand_y=True), sg.Sizegrip()],
              # [sg.Pane([sg.Column([[left_col]], element_justification='l',  expand_x=True, expand_y=True), sg.Column(right_col, element_justification='c', expand_x=True, expand_y=True) ], orientation='h', relief=sg.RELIEF_SUNKEN, k='-PANE-'), sg.Sizegrip()],
              ]

    # --------------------------------- Create Window ---------------------------------
    window = sg.Window('psgtest', layout, finalize=True, resizable=True, use_default_focus=False, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_LOC_EXIT, auto_save_location=True)
    # window.set_min_size(window.size)

    # Rebild the dynamically created tabs
    if sp_to_mline_dict is not None:
        for sp in sp_to_mline_dict.keys():
            mline_key = sp_to_mline_dict[sp]
            file = sp_to_filename[sp]
            tab = make_output_tab(file, mline_key, file)
            window['-TABGROUP-'].add_tab(tab)

    window.bind('<F1>', '-FOCUS FILTER-')
    window.set_min_size(window.size)
    return window


'''
M"""""`'"""`YM          oo          
M  mm.  mm.  M                      
M  MMM  MMM  M .d8888b. dP 88d888b. 
M  MMM  MMM  M 88'  `88 88 88'  `88 
M  MMM  MMM  M 88.  .88 88 88    88 
M  MMM  MMM  M `88888P8 dP dP    dP 
MMMMMMMMMMMMMM
'''

def main():
    """
    The main program that contains the event loop.
    It will call the make_window function to create the window.
    """

    sg.user_settings_filename(filename='psgtest.json')
    upgrade_check()

    global file_list_dict, sp_to_mline_dict, sp_to_filename



    def start_batch(list_of_programs, interpreter=None):
        if interpreter is None:
            current_interpreter = sg.user_settings_get_entry('-current interpreter-')
            if current_interpreter != values['-INTERPRETER TOP-']:
                current_interpreter = values['-INTERPRETER TOP-']
            if current_interpreter in interpreter_dict.keys():
                interpreter_path = sg.user_settings_get_entry(interpreter_dict[current_interpreter])
            else:
                interpreter_path = sg.user_settings_get_entry('-interpreter path-')
            # interpreter_path = sg.user_settings_get_entry('-interpreter path-', '')
        else:
            current_interpreter = interpreter
            interpreter_path = sg.user_settings_get_entry(interpreter_dict[interpreter])

        if interpreter_path:
            sg.cprint(f"Running using {current_interpreter}....", c='white on green', end='')
            sg.cprint('')
        else:
            sg.cprint(f'No valid interpreter has been chosen for {current_interpreter}', c='white on red')
            return


        for file, file_to_run in get_next_program(list_of_programs):
            sg.cprint(file_to_run, text_color='white', background_color='purple')
            pipe_output = values['-SHOW OUTPUT-']
            if file_to_run.endswith(('.py', '.pyw')):
                sp = sg.execute_command_subprocess(interpreter_path, f'"{file_to_run}"', pipe_output=pipe_output)
            else:
                sp = sg.execute_command_subprocess(f'"{file_to_run}"', pipe_output=pipe_output)
            # sg.Print(sg.obj_to_string_single_obj(sp))
            sp_to_filename[sp] = file
            mline_key = f'{file}-MLINE-'
            if mline_key not in sp_to_mline_dict.values():
                tab = make_output_tab(file, mline_key, file)
                window['-TABGROUP-'].add_tab(tab)
            else:
                if not window[file].visible:
                    window[file].update(visible=True)
            sp_to_mline_dict[sp] = mline_key
            window[file].select()
            # Let a thread handle getting all the output so that the rest of the GUI keep running

            if pipe_output:
                window.start_thread(lambda: piped_output_thread(window, sp), '-PIPE THREAD DONE-')
                if values['-REGRESSION KILL-']:
                    try:
                        seconds = float(values['-REGRESSION SECONDS-'])
                    except:
                        seconds = 15
                    window.timer_start(seconds*1000, ('-TIMER THREAD-',  sp), repeating=False)


    sg.user_settings_filename(filename='psgtest.json')
    os.environ['PYTHONUNBUFFERED'] = '1'
    file_list_dict = get_file_list_dict()
    file_list = get_file_list()
    try:
        window = make_window()
    except Exception as e:
        if sg.popup_yes_no('Exception making the Window... likely means a corrupt settings file.', f'Exception: {e}', 'Do you want to clear your settings?', title='Exception making window') == 'Yes':
            sg.user_settings_delete_filename(filename='psgtest.json')
            sg.popup_auto_close('Settings file deleted... please restart the program')
        else:
            sg.popup_auto_close('Cancelling operation... See what you can do about the problem...')
        exit()
    window['-FILTER NUMBER-'].update(f'{len(file_list)} files')
    counter = 0
    dont_close_tab = {}
    regression_programs = []
    try:
        while True:
            event, values = window.read()
            # print(event, values)
            counter += 1
            if event in (sg.WINDOW_CLOSED, 'Exit'):
                break
            if event == '-DEMO LIST-':  # if double clicked (used the bind return key parm)
                if sg.user_settings_get_entry('-dclick runs-'):
                    event = 'Run'
                elif sg.user_settings_get_entry('-dclick edits-'):
                    event = 'Edit'
            # if event is a tuple, then it's from a tab and will have the button and the mline in the tab
            if event[0] == '-CPRINT-':
                sg.cprint(event[1], colors=event[2])
            elif event[0] == '-CLEAR-':
                window[event[1]].update('')
            elif event[0] == '-COPY-':
                    sg.clipboard_set(window[event[1]].get().rstrip())
                    sg.cprint('Copied to clipboard', key=event[1])
            elif event[0] == '-CLOSE-':
                    window[event[1]].update(visible=False)
            elif event[0] == '-TIMER THREAD-':
                thread_sp = event[1]
                sg.cprint(f'killing pid {thread_sp.pid}')
                kill_proc_tree(thread_sp.pid)
                try:
                    file = sp_to_filename[thread_sp]
                    if not dont_close_tab.get(file, False):
                        window[file].update(visible=False)
                except:
                    pass
                del sp_to_filename[thread_sp]
                # del sp_to_mline_dict[thread_sp]
            elif event == '-THREAD-':                   # received message from thread to display
                thread_sp = values['-THREAD-'][0]
                line = values['-THREAD-'][1]
                sg.cprint(line, key=sp_to_mline_dict[thread_sp])
                if 'Traceback' in line:
                    sg.popup_error(f'Error during running {sp_to_filename[thread_sp]}', non_blocking=True)
                    dont_close_tab[sp_to_filename[thread_sp]] = True
                if line == '===THEAD DONE===':
                    sg.cprint(f'{sp_to_filename[thread_sp]}', c='white on purple')
                    sg.cprint(f'Completed', c='white on green')
                    if regression_programs:
                        next_program = regression_programs[0]
                        start_batch((next_program,))
                        del regression_programs[0]
            elif event == 'Run':
                if values['-SINGLE FILE-']:
                    start_batch([values['-SINGLE FILE-']])
                else:
                    start_batch(values['-DEMO LIST-'])
            elif event == 'Run All Interpreters':
                for interpreter in interpreter_dict.keys():
                    if values['-SINGLE FILE-']:
                        start_batch([values['-SINGLE FILE-']], interpreter)
                    else:
                        start_batch(values['-DEMO LIST-'], interpreter)
            elif event == 'Version':
                sg.cprint(sg.get_versions(), c='white on green')
            elif event == '-MAKE TAB-':
                sp, file = values[event]
                sp_to_filename[sp] = file
                mline_key = f'{file}-MLINE-'
                if mline_key not in sp_to_mline_dict.values():
                    tab = make_output_tab(file, mline_key, file)
                    window['-TABGROUP-'].add_tab(tab)
                else:
                    if not window[file].visible:
                        window[file].update(visible=True)
                sp_to_mline_dict[sp] = mline_key
                window[file].select()
            elif event == '-FILTER-':
                new_list = [i for i in file_list if values['-FILTER-'].lower() in i.lower()]
                window['-DEMO LIST-'].update(new_list)
                window['-FILTER NUMBER-'].update(f'{len(new_list)} files')
            elif event == '-FOCUS FILTER-':
                window['-FILTER-'].set_focus()
            elif event == 'Settings':
                if settings_window() is True:
                    pipe_output = values['-SHOW OUTPUT-']
                    window.close()
                    window = make_window()
                    file_list_dict = get_file_list_dict()
                    file_list = get_file_list()
                    window['-FILTER NUMBER-'].update(f'{len(file_list)} files')
                    window['-SHOW OUTPUT-'].update(pipe_output)
            elif event == 'Clear':
                file_list = get_file_list()
                window['-FILTER-'].update('')
                window['-FILTER NUMBER-'].update(f'{len(file_list)} files')
                window['-DEMO LIST-'].update(file_list)
                window['-ML-'].update('')
            elif event == '-FOLDERNAME-':
                sg.user_settings_set_entry('-test script folder-', values['-FOLDERNAME-'])
                file_list_dict = get_file_list_dict()
                file_list = get_file_list()
                window['-DEMO LIST-'].update(values=file_list)
                window['-FILTER NUMBER-'].update(f'{len(file_list)} files')
                window['-ML-'].update('')
                window['-FILTER-'].update('')
            elif event == '-INTERPRETER TOP-':
                if values['-INTERPRETER TOP-'] in interpreter_dict.keys():
                    interpreter_path = sg.user_settings_get_entry(interpreter_dict[values['-INTERPRETER TOP-']], '')
                else:
                    interpreter_path = None
                sg.user_settings_set_entry('-current interpreter-', values['-INTERPRETER TOP-'])
                sg.user_settings_set_entry('-interpreter path-', interpreter_path)
                window['-CURRENT INTERPRETER-'].update('Testing Using Interpreter: ' + sg.user_settings_get_entry('-current interpreter-', ''))
                window['-INTERPRETER PATH-'].update('Interpreter path: ' + sg.user_settings_get_entry('-interpreter path-', ''))
            elif event == 'Edit':
                for file in values['-DEMO LIST-']:
                    sg.cprint('EDITING: ', c='white on green')
                    sg.cprint(f'{file_list_dict[file]}', c='white on purple')
                    sg.execute_editor(file_list_dict[file])
            elif event.startswith('Close'):
                tab_key = event[event.index("::") + 2:]
                window[tab_key].update(visible=False)
                # tab_to_close_key = values['-TABGROUP-']
                # window[tab_to_close_key].update(visible=False)
            elif event == 'Version':
                sg.cprint(sg.get_versions(), c='white on green')
                sg.popup_scrolled(sg.get_versions(), non_blocking=True)
            elif event == 'Edit Me':
                sg.execute_editor(__file__)
            elif event == 'File Location':
                sg.cprint('This Python file is:', __file__, c='white on green')
            elif event == 'Run Regression':
                if values['-SINGLE FILE-']:
                    regression_programs = [values['-SINGLE FILE-'],]
                else:
                    regression_programs = values['-DEMO LIST-']
                # start the first batch
                if values['-REGRESSION KILL-']:
                    kill_after = int(values['-REGRESSION SECONDS-'])
                else:
                    kill_after = None
                window.start_thread(lambda: regression_thread(window, regression_programs, int(values['-REGRESSION BLOCK SIZE-']), int(values['-STRESS RUNS-']), kill_after,  sg.user_settings_get_entry('-interpreter path-', ''), values['-SHOW OUTPUT-']), '-DONE-')
            elif event == 'Run Regression All Interpreters':
                if values['-SINGLE FILE-']:
                    regression_programs = [values['-SINGLE FILE-'],]
                else:
                    regression_programs = values['-DEMO LIST-']
                # start the first batch
                if values['-REGRESSION KILL-']:
                    kill_after = int(values['-REGRESSION SECONDS-'])
                else:
                    kill_after = None
                window.start_thread(lambda: regression_thread(window, regression_programs, int(values['-REGRESSION BLOCK SIZE-']), int(values['-STRESS RUNS-']), kill_after,  None, values['-SHOW OUTPUT-']), '-DONE-')
    except Exception as e:
        sg.Print('WHOA!  Exception in the main event loop', e, wait=True)
        sg.popup_error_with_traceback('Exception in event loop', e)

    # clean up any tests that are still running
    for sp in sp_to_filename.keys():
        print(f'Clean-up killing {sp.pid}')
        kill_proc_tree(sp.pid)

    window.close()




if __name__ == '__main__':
    main()
