# ---------------------------------------------------------------------------- #
#                               class Calculator                               #
# ---------------------------------------------------------------------------- #

from decimal import *
import numpy_financial as npf

# Value of pi as a string from the math module.
# (This avoids having to import the entire math module)
PI = "3.141592653589793"

getcontext().prec = 9


class Calculator():
    def __init__(self):
        # Initialize Stack registers
        self.x, self.y, self.z, self.t = '0', '0', '0', '0'
        # Initialize Memory registers
        self.m = ['0']*10
        # Initialize Finance registers
        self.n, self.i, self.pv, self.pmt, self.fv = '0', '0', '0', '0', '0'
        self.when = 'end'
        # Last Calculator Action
        self.last_event = "enter"
        # Initialize return variables
        self.display = ''
        self.error = ''
        # Initialize decimal places for display
        self.decimal_places = 'float'

    def push_stack(self):
        self.t = self.z
        self.z = self.y
        self.y = self.x

    def paste_value_to_stack(self, value):
        try:
            temp = Decimal(value)
        except:
            error = 'Clipboard must contain valid number.'
            return (self.display, error)
        self.push_stack()
        self.x = value
        self.last_event = 'calc'
        self.set_display(self.decimal_places)
        return (self.display, '')

    def append_to_x(self, char):
        self.x += char

    def pop_stack(self):
        top_of_stack = self.x
        self.x = self.y
        self.y = self.z
        self.z = self.t
        self.t = '0'
        return top_of_stack

    def rotate_stack(self):
        temp = self.x
        self.x = self.y
        self.y = self.z
        self.z = self.t
        self.t = temp

    def swap_x_and_y(self):
        temp = self.y
        self.y = self.x
        self.x = temp

    def clear_stack(self):
        self.x, self.y, self.z, self.t = '0', '0', '0', '0'

    def clear_memory(self):
        for i in range(0, 10):
            self.m[i] = '0'

    def clear_finance_registers(self):
        self.n, self.i, self.pv, self.pmt, self.fv = '0', '0', '0', '0', '0'
        self.when = 'end'

    def clear_x(self):
        self.x = '0'

    def backspace(self):
        self.x = self.x[:-1]
        if len(self.x) == 0 or self.x == '-':
            self.x = '0'

    def set_display(self, format):
        if self.x == '.':
            self.display = '.'
            return
        elif self.x == '0.':
            self.display = '0.'
            return
        if format == 'float':
            self.display = f"{Decimal(self.x)}"
        else:
            self.display = f"{Decimal(self.x):,.{self.decimal_places}f}"

    def set_decimal_places(self, event):
        if event == 'Float':
            self.decimal_places = 'float'
        else:
            self.decimal_places = event[0]
        self.set_display(self.decimal_places)
        return (self.display, '')

    def digit(self, event):
        if self.last_event in ('enter'):
            self.x = event
            self.last_event = 'digit'
        elif self.last_event == 'digit' or self.last_event == 'decimal':
            self.x += event
            self.last_event = 'digit'
        elif self.last_event in ('calc', 'finance'):
            self.push_stack()
            self.x = event
            self.last_event = 'digit'
        elif self.last_event in ('STO'):
            self.m[int(event)] = self.x
            self.last_event = 'enter'
        elif self.last_event in ('RCL'):
            self.push_stack()
            self.x = self.m[int(event)]
            self.last_event = 'enter'

    def decimal_point(self, event):
        if self.last_event in ('enter', 'finance'):
            self.x = '0.'
            self.last_event = 'decimal'
        elif self.last_event in ('decimal'):
            self.error = 'Decimal point already entered.'
        elif self.last_event in ('digit'):
            if '.' not in self.x:
                self.x += '.'
            else:
                self.error = 'Decimal point already entered.'
        elif self.last_event in ('calc'):
            self.push_stack()
            self.x = '0.'
            self.last_event = 'decimal'
        elif self.last_event in ('STO', 'RCL'):
            self.error = 'Error. Expected id of memory register (0-9).'

    def stack_ops(self, event):
        if self.last_event in ('STO', 'RCL'):
            self.error = 'Error. Expected id of memory register (0-9).'
            self.last_event = 'enter'
        else:
            if event in ('-ENTER-', '\r'):
                # Remove redundant leading zeroes
                while len(self.x) >= 2 and self.x[0] == '0' and self.x[1] != '.':
                    self.x = self.x[1:]
                self.push_stack()
                self.last_event = 'enter'
            elif event in ('CLx', 'Escape:27'):
                self.x = '0'
                self.last_event = 'digit'
            elif event in ('-SWAP-'):
                self.swap_x_and_y()
                self.last_event = 'calc'
            elif event in ('-ROTATE-'):
                self.rotate_stack()
            elif event in ('BS', 'BackSpace:8'):
                self.backspace()
            elif event in ('Clear Stack'):
                self.clear_stack()
            elif event in ('Clear Memory Registers'):
                self.clear_memory()
            elif event in ('Clear Finance Registers'):
                self.clear_finance_registers()
            elif event in ('Clear All', '-CLR_ALL-'):
                self.clear_stack()
                self.clear_memory()
                self.clear_finance_registers()
                self.last_event = 'enter'
            elif event in ('π'):
                pi = str(Decimal(PI))
                self.push_stack()
                self.x = pi
                self.last_event = 'calc'

    def memory_ops(self, event):
        if self.last_event in ('STO', 'RCL'):
            self.error = 'Error. Expected id of memory register (0-9).'
            self.last_event = 'enter'
        else:
            self.last_event = event

    def unary_ops(self, event):
        if self.last_event in ('STO', 'RCL'):
            self.error = 'Error. Expected id of memory register (0-9).'
        else:
            if event in ('+/-'):
                if self.x != '0' and self.x != '0.':
                    self.x = str(Decimal(self.x)*Decimal('-1'))
            elif event == '1/x':
                if self.x != '0':
                    x = self.pop_stack()
                    result = str(Decimal('1')/Decimal(x))
                    self.push_stack()
                    self.x = result
                    self.last_event = 'calc'
                else:
                    self.error = "Cannot Divide by Zero."
            elif event == '\u221A x':    # Square Root
                if Decimal(self.x) >= 0:
                    x = self.pop_stack()
                    result = str(Decimal(x).sqrt())
                    self.push_stack()
                    self.x = result
                    self.last_event = 'calc'
                else:
                    self.error = "Cannot take square root of negative number."
            elif event == 'x \u00b2':     # Square
                x = self.pop_stack()
                result = str(Decimal(x)*Decimal(x))
                self.push_stack()
                self.x = result
                self.last_event = 'calc'
            elif event == 'e ˣ':     # e to the x
                x = self.pop_stack()
                result = str(Decimal(x).exp())
                self.push_stack()
                self.x = result
                self.last_event = 'calc'
            elif event == 'LN':     # Natural Log
                if Decimal(self.x) > 0:
                    x = self.pop_stack()
                    result = str(Decimal(x).ln())
                    self.push_stack()
                    self.x = result
                    self.last_event = 'calc'
                else:
                    self.error = "Cannot take natural log of number less than or equal to zero."
            elif event == 'π':     # Constant pi
                self.push_stack()
                self.x = PI    # PI is the constant pi as a string
                self.last_event = 'calc'

    def binary_ops(self, event):
        if self.last_event in ('STO', 'RCL'):
            self.error = 'Error. Expected id of memory register (0-9).'
        else:
            if event in ('+'):
                x = self.pop_stack()
                y = self.pop_stack()
                result = str(Decimal(y)+Decimal(x))
                self.push_stack()
                self.x = result
                self.last_event = 'calc'
            elif event in ('-'):
                x = self.pop_stack()
                y = self.pop_stack()
                result = str(Decimal(y)-Decimal(x))
                self.push_stack()
                self.x = result
                self.last_event = 'calc'
            elif event in ('x', '*'):
                x = self.pop_stack()
                y = self.pop_stack()
                result = str(Decimal(y)*Decimal(x))
                self.push_stack()
                self.x = result
                self.last_event = 'calc'
            elif event in ('/'):
                if self.x != '0':
                    x = self.pop_stack()
                    y = self.pop_stack()
                    result = str(Decimal(y)/Decimal(x))
                    self.push_stack()
                    self.x = result
                    self.last_event = 'calc'
                else:
                    self.error = "Cannot Divide by Zero."
            elif event == "y ˣ":
                if self.y != '0':
                    x = self.pop_stack()
                    y = self.pop_stack()
                    result = str(Decimal(y)**Decimal(x))
                    self.push_stack()
                    self.x = result
                    self.last_event = 'calc'
                else:
                    self.error = 'Base of exponentiation calculation must not be zero,\n i.e. y cannot be zero.'

    def finance_ops(self, event):
        if self.last_event in ('STO'):
            self.error = 'Error. Expected id of memory register (0-9).'
            self.last_event = 'enter'
        elif self.last_event in ('RCL'):
            self.push_stack()
            if event in ('n'):
                self.x = self.n
            elif event in ('i'):
                self.x = self.i
            elif event in ('PV'):
                self.x = self.pv
            elif event in ('PMT'):
                self.x = self.pmt
            elif event in ('FV'):
                self.x = self.fv
            self.last_event = 'calc'
        elif self.last_event in ('finance'):
            # Get financial registers as floats for use in numpy_financial
            n_fl = float(self.n)
            i_fl = float(self.i)
            pv_fl = float(self.pv)
            pmt_fl = float(self.pmt)
            fv_fl = float(self.fv)
            if event == 'n':
                n_fl = npf.nper(rate=i_fl/100, pv=pv_fl, pmt=pmt_fl, fv=fv_fl, when=self.when)
                n_fl = float(n_fl)   # Must convert to float since npf returns array_like object for nper
                result = str(round(n_fl, 9))  # Round & convert to string
                if result == 'nan':
                    self.set_invalid_fin_calc_msg()
                    result = '0'
                self.n = result
            elif event == 'i':
                i_fl = npf.rate(nper=n_fl, pv=pv_fl, pmt=pmt_fl, fv=fv_fl, when=self.when)*100
                result = str(round(i_fl, 9))
                if result == 'nan':
                    self.set_invalid_fin_calc_msg()
                    result = '0'
                self.i = result
            elif event == 'PV':
                pv_fl = npf.pv(nper=n_fl, rate=i_fl/100, pmt=pmt_fl, fv=fv_fl, when=self.when)
                if abs(pv_fl-int(pv_fl)) < 0.0001:
                    pv_fl = int(pv_fl)
                result = str(round(pv_fl, 9))
                self.pv = result
            elif event == 'PMT':
                pmt_fl = npf.pmt(nper=n_fl, rate=i_fl/100, pv=pv_fl, fv=fv_fl, when=self.when)
                try:
                    if abs(pmt_fl-int(pmt_fl)) < 0.0001:
                        pmt_fl = int(pmt_fl)
                    result = str(round(pmt_fl, 9))
                except:
                    self.set_invalid_fin_calc_msg()
                    result = '0'
                self.pmt = result
            elif event == 'FV':
                fv_fl = npf.fv(nper=n_fl, rate=i_fl/100, pv=pv_fl, pmt=pmt_fl, when=self.when)
                if abs(fv_fl-int(fv_fl)) < 0.0001:
                    fv_fl = int(fv_fl)
                result = str(round(fv_fl, 9))
                self.fv = result
            self.x = result
            self.last_event = 'calc'
        # if last_event was not 'finance', then store x into appropriate finance register
        elif event in ('n'):
            if Decimal(self.x) > 0:
                self.n = self.x
                self.last_event = 'finance'
            else:
                self.error = 'Invalid entry.\nNumber of periods should be greater than 0.'
        elif event in ('i'):
            if Decimal(self.x) >= 0:
                self.i = self.x
                self.last_event = 'finance'
            else:
                self.error = 'Invalid entry.\nInterest rate should be greater than or equal to 0.'
        elif event in ('PV'):
            self.pv = self.x
            self.last_event = 'finance'
        elif event in ('PMT'):
            self.pmt = self.x
            self.last_event = 'finance'
        elif event in ('FV'):
            self.fv = self.x
            self.last_event = 'finance'

    def set_invalid_fin_calc_msg(self):
        self.error = 'Invalid inputs to financial calculation.\nBe sure to check signs on cash flows.'

    def update(self, event):
        # print(
        #     f"Entering-- event: {event} last_event: {self.last_event} x: {self.x} y: {self.y} z: {self.z} t: {self.t}")

        # Clear error message
        self.error = ""

        if event in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):    # Digit?
            self.digit(event)

        elif event in ('.'):     # Decimal point?
            self.decimal_point(event)

        elif event in ('STO', 'RCL'):   # Memory Operation?
            self.memory_ops(event)

        elif event in ('n', 'i', 'PV', 'PMT', 'FV'):     # Financial Operation?
            self.finance_ops(event)

        elif event in ('-ENTER-', '\r',  'CLx', 'Escape:27', '-SWAP-', '-ROTATE-',
                       'BS', 'BackSpace:8', 'Clear Stack', 'Clear Memory Registers', 'Clear Finance Registers', 'Clear All', '-CLR_ALL-', 'π'):   # Stack operation?
            self.stack_ops(event)

        elif event in ('+/-', '1/x', '\u221A x', 'x \u00b2', 'e ˣ', 'LN'):    # Unary operation?
            # \u221A x is sqrt of x
            # x \u00b2 is x squared
            self.unary_ops(event)

        elif event in ('+', '-', 'x', '*', '/', 'y ˣ'):    # Binary opearation?
            self.binary_ops(event)

        else:      # Everything else is an invalid keyboard entry
            self.error = 'Invalid keyboard entry.'

        self.set_display(self.decimal_places)

        # print(f"Exiting-- last_event: {self.last_event} x: {self.x} y: {self.y} z: {self.z} t: {self.t}")
        # print('-----------------------------------------')

        return (self.display, self.error)
