# ---------------------------------------------------------------------------- #
#                                RPN Calculator                                #
# ---------------------------------------------------------------------------- #

# import os       # For testing
import PySimpleGUI as sg
from Calculator import Calculator
import webbrowser

DOC_URL = 'https://epageler.github.io/documentation/RPN_Financial_Calculator/RPN-Financial-Calculator-Documentation.html'

# For testing, clear Terminal
# os.system('cls')


# ----------------------- Instantiate Calculator Object ---------------------- #

calc = Calculator()

# ------------------------ Calculator Button Attributes ----------------------- #

# Attributes for Std Buttons
bt = {'size': (5, 2), 'font': ('Calibri', 14, "bold"), 'button_color': ("white", "black")}
# Attributes for Number Buttons
bn = {'size': (5, 2), 'font': ('Calibri', 14, "bold"), 'button_color': ("white", "#263238")}
# Attributes for Enter Button
be = {'size': (12, 2), 'font': ('Calibri', 14, "bold"), 'button_color': ("white", "#01579B")}
# Attributes for Backspace Button
bs = {'size': (12, 2), 'font': ('Calibri', 14, "bold"), 'button_color': ("white", "#7a3820")}
# Attributes for Zero Button
bz = {'size': (12, 2), 'font': ('Calibri', 14, "bold"), 'button_color': ("white", "#263238")}
# Attributes for Finance Buttons
bf = {'size': (5, 2), 'font': ('Calibri', 14, "bold"), 'button_color': ("white", '#334C1E')}


# -------------------------------- Menu layout ------------------------------- #
menu_def = [
    ['File',
        ['Exit']],
    ['Edit',
        ['Copy', 'Paste', '---', 'Clear Stack', 'Clear Memory Registers', 'Clear Finance Registers', 'Clear All']],
    ['View',
        ['Set Decimal Places to Show',
            ['Float', '1 Decimal Place', '2 Decimal Places', '3 Decimal Places',
             '4 Decimal Places', '5 Decimal Places', '6 Decimal Places'],
         '---',
         'Show/Hide Internals']],
    ['Help',
        ['About', 'Open Documentation online']]
]

# ----------------------- Right Click Menu for Display ---------------------- #

display_right_click_menu = [
    'Set Decimal Places to Show',
    ['Float', '1 Decimal Place', '2 Decimal Places',
     '3 Decimal Places', '4 Decimal Places', '5 Decimal Places',
     '6 Decimal Places']
]

# --------------------------- Calc Main View layout -------------------------- #

calc_col = [
    [sg.VPush()],

    # Display
    [sg.T('0', expand_x=True, justification='left', background_color='white',
          text_color='black', font=('Lucida Console', 20), relief='sunken', right_click_menu=display_right_click_menu, tooltip='Right Click to Change Number of Decimal Places to Display', key='-DISPLAY-')],
    [sg.VPush()],

    # Row 1 of Buttons
    [sg.B('n', **bf), sg.B('STO', **bt), sg.B('RCL', **bt),  sg.B('CLx', **bt),
     sg.B('🠄', **bs, key='BS'), sg.B('Enter  ^', key='-ENTER-', **be)],

    # Row 2 of Buttons
    [sg.B('i', **bf), sg.B('LN', **bt), sg.B('1/x', **bt), sg.B('x⇄y', **bt, key='-SWAP-'),
     sg.B('7', **bn), sg.B('8', **bn), sg.B('9', **bn), sg.B('/', **bt)],

    # Row 3 of Buttons
    [sg.B('PV', **bf), sg.B('e ˣ', **bt), sg.B('\u221A x', **bt), sg.B('R ↓',  **bt, key='-ROTATE-'),
     sg.B('4', **bn), sg.B('5', **bn), sg.B('6', **bn), sg.B('x', **bt)],

    # Row 4 of Buttons
    [sg.B('PMT', **bf), sg.B('π', **bt), sg.B('x \u00b2', **bt), sg.B('CLR\nAll', **bt, key='-CLR_ALL-'),
     sg.B('1', **bn), sg.B('2', **bn), sg.B('3', **bn), sg.B('-', **bt)],

    # Row 5 of Buttons
    [sg.B('FV', **bf), sg.B('BEG /\nEND', **bf, tooltip='Toggle Cash Flow timing between Beginning & End of Period'),
     sg.B('y ˣ', **bt), sg.B('+/-', **bt), sg.B('0', **bz), sg.B('.', **bn), sg.B('+', **bt)],

    # Cash Flow Timing Display
    [sg.T('CF Timing:', font=('Calibri', 13, 'bold')),
     sg.T(' END ', font=('Lucida Console', 13), background_color='white',
          text_color='black', relief='sunken',
          tooltip='Toggle Cash Flow Timing by Using BEG/END Key.', key='-CF Timing-'),
     sg.Push()]
    # background_color = '#334C1E',

    # [sg.VPush()]
]


# ----------------------------- Internals Layout ---------------------------- #

# Styling for Tab Layouts
# th is for heading in tabs
th = {"font": ("Calibri", 14), "background_color": "white", "text_color": "black"}
# tr is styling for row descriptors
tr = {"font": ("Lucida Console", 12, 'bold'), "background_color": "white", "text_color": "grey"}
# td is styling for row dynamic data
td = {"font": ("Lucida Console", 12, 'bold'), "background_color": "white", "text_color": "black"}


stack_layout = [
    [sg.T("Stack Registers", **th)],
    [sg.T("t :", **tr), sg.T("0", **td, key='-TREG-')],
    [sg.T("z :", **tr), sg.T("0", **td, key='-ZREG-')],
    [sg.T("y :", **tr), sg.T("0", **td, key='-YREG-')],
    [sg.T("x :", **tr), sg.T("0", **td, key='-XREG-')],
    [sg.T(' ', **tr, size=25)]    # size is specified to set width of tab group
]

memory_layout = [[sg.T("Memory Registers", **th)],
                 [sg.T('0 :', **tr), sg.T('0', **td, key=('-M0-'))],
                 [sg.T('1 :', **tr), sg.T('0', **td, key=('-M1-'))],
                 [sg.T('2 :', **tr), sg.T('0', **td, key=('-M2-'))],
                 [sg.T('3 :', **tr), sg.T('0', **td, key=('-M3-'))],
                 [sg.T('4 :', **tr), sg.T('0', **td, key=('-M4-'))],
                 [sg.T('5 :', **tr), sg.T('0', **td, key=('-M5-'))],
                 [sg.T('6 :', **tr), sg.T('0', **td, key=('-M6-'))],
                 [sg.T('7 :', **tr), sg.T('0', **td, key=('-M7-'))],
                 [sg.T('8 :', **tr), sg.T('0', **td, key=('-M8-'))],
                 [sg.T('9 :', **tr), sg.T('0', **td, key=('-M9-'))],
                 ]

finance_layout = [
    [sg.T("Finance Registers", **th)],
    [sg.T("  n : ", **tr), sg.T("0", key='-n-', ** td)],
    [sg.T("  i : ", **tr), sg.T("0", key='-i-', **td)],
    [sg.T(" PV : ", **tr), sg.T("0", key='-PV-', **td)],
    [sg.T("PMT : ", **tr), sg.T("0", key='-PMT-', **td)],
    [sg.T(" FV : ", **tr), sg.T("0", key='-FV-', **td)],
    [sg.T('CF Timing:', **tr), sg.T('end', key='-WHEN-', **td)],
    [sg.T(" ", **tr)],
]

tab_group_layout = [
    # tab 1
    [sg.Tab("Stack", stack_layout, element_justification="l", background_color="white")],
    # tab 2
    [sg.Tab("Memory", memory_layout, element_justification="l", background_color="white")],
    # tab 3
    [sg.Tab("Finance", finance_layout, element_justification="l", background_color="white")],
]

internals_col = [[sg.TabGroup(tab_group_layout,
                              font=('Calibri', 12),
                              title_color='white',
                              tab_background_color='grey',
                              selected_title_color='black',
                              selected_background_color='white')]
                 ]

# ------------------------------- Total Layout ------------------------------- #

layout = [[sg.Menu(menu_def)],
          [sg.T("RPN Financial Calculator", font=('Calibri', 20, "bold")), sg.Push()],
          [sg.Column(calc_col),
           sg.Column(internals_col,
                     visible=False,
                     vertical_alignment='top',
                     element_justification='center',
                     key='-INTERNALS-')],

          ]

window = sg.Window('RPN Financial Calculator', layout, icon='./calculator.ico',
                   element_justification='c', return_keyboard_events=True)

# ---------------------------------------------------------------------------- #
#                                  Event Loop                                  #
# ---------------------------------------------------------------------------- #

while True:
    event, values = window.read()
    # print(event, values)     # For testing
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    # Basic vs Internals selects View
    elif event == 'Show/Hide Internals':
        if window['-INTERNALS-'].visible:
            window['-INTERNALS-'].update(visible=False)
        else:
            window['-INTERNALS-'].update(visible=True)
    elif event in ('Copy'):
        sg.clipboard_set(calc.x)
    elif event in ('Paste'):
        text = sg.clipboard_get()
        display, error = calc.paste_value_to_stack(text)
        if error != '':
            sg.popup_error(error, font=('Calibri', 14))
        window['-DISPLAY-'].update(display)
        window['-XREG-'].update(calc.x)
    elif event in ('Float', '0 Decimal Places', '1 Decimal Place', '2 Decimal Places', '3 Decimal Places',
                   '4 Decimal Places', '5 Decimal Places', '6 Decimal Places'):
        display, error = calc.set_decimal_places(event)
        if error != '':
            sg.popup_error(error, font=('Calibri', 14))
        window["-DISPLAY-"].update(display)   # update calculator display
    elif event == ('BEG /\nEND'):
        if calc.when == 'end':
            calc.when = 'begin'
            window['-CF Timing-'].update(' BEG ')
        else:
            calc.when = 'end'
            window['-CF Timing-'].update(' END ')
        window['-WHEN-'].update(calc.when)
    elif event == 'About':
        sg.popup('RPN Financial Calculator, V1.0.', font=('Calibri', 14))
    elif event == 'Open Documentation online':
        ans = sg.popup_yes_no('Open Documentation online?', font=('Calibri', 14))
        if ans == 'Yes':
            try:
                webbrowser.open(DOC_URL)
            except:
                sg.popup('Documentation online is unavailable.', font=('Calibri', 14))
    else:
        # Update calc object. display is contents of display. error to be shown on popup
        display, error = calc.update((event))
        if error != "":
            sg.popup_error(error, font=('Calibri, 14'))
        window["-DISPLAY-"].update(display)   # update calculator display

        # update Internals view
        # Stack
        window['-TREG-'].update(calc.t)
        window['-ZREG-'].update(calc.z)
        window['-YREG-'].update(calc.y)
        window['-XREG-'].update(calc.x)

        # Memory
        if error == '':
            for i in range(0, 10):
                window[f"-M{i}-"].update(calc.m[i])

        # Finance Registers
        window['-n-'].update(calc.n)
        window['-i-'].update(calc.i)
        window['-PV-'].update(calc.pv)
        window['-PMT-'].update(calc.pmt)
        window['-FV-'].update(calc.fv)
        window['-WHEN-'].update(calc.when)

window.close()
