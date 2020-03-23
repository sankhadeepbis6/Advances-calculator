import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from ttkthemes import themed_tk as tktheme

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk, FigureCanvasTk
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.pyplot as plt

from pythonds.basic.stack import Stack
import numpy as np
import math

from pandas import DataFrame
import pandas as pd

from os import path


matplotlib.use("TkAgg")

style.use("ggplot")


def error_message_window(message_type,message_text):
    """Convert the entry string to list"""
    messagebox.showerror(message_type, message_text)


def pop_message(message_type,message_text):
    messagebox.showinfo(message_type,message_text)


def test_function(*args):
    for i in args:
        print(i, "# ti's working")


def info_window(file_name):
    window = InfoWindow(file_name)
    window.mainloop()


def restart_all_window():
    """Restart all the window to clear previous entry"""
    main()


def unknown_ope_checker(equ_ref):
    """Check for unknown operator in equation string"""
    unknown_ope = ["@", "#", "$", "%", "&", "_", "=", "{", "}", ":", ";", "'", '"', "\\", ",", "?", "`", "~"]
    for element in equ_ref:
        if element in unknown_ope:
            return False, "There is a unknown operator in the equation"
    return True, "No error"


def equation_check(equ_list):
    """The function to if the equation is invalid also return the invalid message"""
    bracket_count = 0
    all_ope = ["sin", "cos", "tan", "cosec", "sec", "cot",
               "sinh", "cosh", "tanh", "cosech", "sech", "coth",
               "sini", "cosi", "tani",
               "+", "-", "*", "/", "^", "!",
               "log", "loge", "exp", "pi", "e",
               "(", ")", "[", "]", "|",
               "x"]
    ope = ["+", "-", "*", "/", "^"]
    open_bracket_ope = ["(", "|", "["]
    close_bracket_ope = [")", "]", "|"]
    factrial_ope = ["!"]
    variable = ["x"]
    sci_ope = ["sin", "cos", "tan", "cosec", "sec", "cot",
               "sinh", "cosh", "tanh", "cosech", "sech", "coth",
               "exp", "log", "loge"]
    for index in range(len(equ_list)):

        if equ_list[index] == "(":
            bracket_count += 1
        if equ_list[index] == ")":
            bracket_count -= 1

        if equ_list[index] not in all_ope:
            if num_checker(equ_list[index]):
                continue
            else:
                error_message = "Invalid operator at " + str(index - 1) + " position"
                return False, error_message

        if equ_list[index] in ope:
            if equ_list[index+1] in ope:
                error_message = "Two operator side by side in " + str(index-1) + " posiction"
                return False, error_message
        if equ_list[index] in sci_ope:
            if not(equ_list[index+1] in open_bracket_ope):
                if equ_list[index+1] in variable:
                    continue
                else:
                    error_message = "Two scienctefic operator side by side in " + str(index-1) + " posiction"
                    return False, error_message
        if equ_list[index] in open_bracket_ope:
            if ((equ_list[index+1] in sci_ope) or equ_list[index+1] in variable or\
                equ_list[index+1] in open_bracket_ope or \
                num_checker(equ_list[index+1]) or (equ_list[index+1] in close_bracket_ope)) and \
                ((equ_list[index-1] in sci_ope) or (equ_list[index-1] in ope) or\
                 equ_list[index-1] in open_bracket_ope or num_checker(equ_list[index-1])):
                continue
            else:
                error_message = "wrong position of opening bracket in " + str(index-1) + " posiction"
                return False, error_message
        if equ_list[index] in close_bracket_ope:
            if (equ_list[index-1] in ope) or (equ_list[index-1] in sci_ope):
                error_message = "Operator before end bracket in " + str(index-1) + " position"
                return False, error_message
            if (equ_list[index+1] in ope) or (equ_list[index+1] in close_bracket_ope):
                continue
            else:
                error_message = "wrong position of closing bracket in " + str(index - 1) + " posiction"
                return False, error_message
        if equ_list[index] in factrial_ope:
            if equ_list[index-1] in variable or num_checker(equ_list[index-1]):
                continue
            else:
                error_message = "Wrong position of factrial in " + str(index - 1) + " posiction"
                return False, error_message

    if bracket_count == 0:
        return True, "No error"
    else:
        if bracket_count > 0:
            error_message = "Extra number of open brackets"
        else:
            error_message = "Extra number of close brackets"
        return False, error_message


def box_operator_checker(list_ref):
    """This function is used to correct the error of the box operator"""
    count = 0
    last_bracket_error = False

    for position in range(len(list_ref)):
        if list_ref[position] == "[" or list_ref[position] == "]":
            count += 1

    for position in range(len(list_ref)+count):
        if last_bracket_error:
            last_bracket_error = False
            continue
        elif list_ref[position] == "[":
            list_ref[position: position+1] = ["(", "["]
            last_bracket_error = True
        elif list_ref[position] == "]":
            list_ref[position: position+1] = ["]", ")"]

    return list_ref


def list_replace(list_ref, previous_value, modified_value):
    """replace a specific value of a list"""
    for index, value in enumerate(list_ref):
        if value == previous_value:
            list_ref[index] = modified_value

    return list_ref



def num_checker(num):
    """check all kind of number float or num if it is not a number returns False"""
    try:
        float(num)
        return True
    except ValueError:
        return False


def convert_integer(string_num):
    """This equation is used for factorial"""
    if "." in string_num:
        for i in range(len(string_num)):
            if string_num[i] == ".":
                point_position = i
                break
        return string_num[:point_position]
    else:
        return string_num


def equation_to_list(equ):
    """convert the string infix to a string to make it easier to convert into a post fix"""
    list_equ = []
    ope = ["+", "-", "*", "/", "^", "(", ")", "!", "|", "[", "]", "x"]  # to take x a input in infix

    j = 0
    for i in range(len(equ)):
        if equ[i] in ope:
            if (equ[i] == "x") and (equ[i-1] == "e") and (equ[i+1] == "p"):
                continue
            list_equ.append(equ[j:i])
            list_equ.append(equ[i])
            j = i + 1
    list_equ.append(equ[j:])

    while "" in list_equ:
        list_equ.remove("")

    return list_equ


def infix_to_postfix(infixexpr):
    """Take a string infix and returns string or list post fix output
    this is not necessary for post pix transformation it is added for calculation purpose"""
    infixexpr = "0+" + infixexpr + "+0"
    prec = {"!": 5, "^": 4, "*": 3, "/": 3, "+": 2, "-": 2, "[": 1.5, "|": 1,"(": 1}  # all the operators can be used in a infix
    opstack = Stack()  # a stack to store the operators temporarily
    postfix_list = []  # store final post fix expression
    token_string = infixexpr.replace(" ","")  # remove all the spaces to avoid error
    token_list = equation_to_list(token_string)  # convert the infix string to a list
    token_list = box_operator_checker(token_list)

    decider = True  # to decide the nse of |

    for token in token_list:
        if token.isalpha() or num_checker(token):
            postfix_list.append(token)
        elif token == '(':
            opstack.push(token)
        elif token == ')':
            top_token = opstack.pop()
            while top_token != '(':
                postfix_list.append(top_token)
                top_token = opstack.pop()
        elif token == ']':  # to be corrected
            top_token_third = opstack.pop()
            while top_token_third != '[':
                postfix_list.append(top_token_third)
                top_token_third = opstack.pop()
            postfix_list.append("]")
        elif token == '|':
            if decider:
                postfix_list.append(token)
                opstack.push(token)
                decider = False
            else:
                top_token = opstack.pop()
                while top_token != '|':
                    postfix_list.append(top_token)
                    top_token = opstack.pop()
                postfix_list.append(top_token)
                decider = True
        else:
            while (not opstack.isEmpty()) and (prec[opstack.peek()] >= prec[token]) and (not(token == "^")):
                  postfix_list.append(opstack.pop())
            if token == "[":
                postfix_list.append(token)
            opstack.push(token)

    while not opstack.isEmpty():
        postfix_list.append(opstack.pop())

    postfix_string = " ".join(postfix_list)  # string post fix
    return postfix_list


def calculate(postfixex="No input"):
    '''Take list post fix input and returns the calculated value'''
    ope = ["+", "-", "*", "/", "^"]
    end_bracket = ["]", "|"]
    sci_ope = ["sin", "cos", "tan", "cosec", "sec", "cot",
               "sinh", "cosh", "tanh", "cosech", "sech", "coth",
               "exp", "log", "loge"]
    if postfixex == "No input":
        return 0
    while len(postfixex) > 1:
        for i in range(len(postfixex)):
            # checks for scientific operators like sin, exp
            if postfixex[i] in ope:
                if postfixex[i-2] in sci_ope:
                    pass
                elif postfixex[i-1] in end_bracket:
                    while postfixex[i-1] in end_bracket:
                        i -= 1

                if postfixex[i-2] == "sin":
                    string_temp = str(math.sin(float(postfixex[i-1])))
                    postfixex[i-1] = string_temp
                    del postfixex[i-2:i-1]
                    break
                if postfixex[i-2] == "cos":
                    string_temp = str(math.cos(float(postfixex[i-1])))
                    postfixex[i-1] = string_temp
                    del postfixex[i-2:i-1]
                    break
                if postfixex[i-2] == "tan":
                    string_temp = str(math.tan(float(postfixex[i-1])))
                    postfixex[i-1] = string_temp
                    del postfixex[i-2:i-1]
                    break
                if postfixex[i-2] == "cosec":
                    string_temp = str(1/(math.sin(float(postfixex[i-1]))))
                    postfixex[i-1] = string_temp
                    del postfixex[i-2:i-1]
                    break
                if postfixex[i-2] == "sec":
                    string_temp = str(1/(math.cos(float(postfixex[i-1]))))
                    postfixex[i-1] = string_temp
                    del postfixex[i-2:i-1]
                    break
                if postfixex[i-2] == "cot":
                    string_temp = str(1/(math.tan(float(postfixex[i-1]))))
                    postfixex[i-1] = string_temp
                    del postfixex[i-2:i-1]
                    break

                if postfixex[i-2] == "sini":
                    string_temp = str(math.asin(float(postfixex[i-1])))
                    postfixex[i-1] = string_temp
                    del postfixex[i-2:i-1]
                    break
                if postfixex[i-2] == "cosi":
                    string_temp = str(math.acos(float(postfixex[i-1])))
                    postfixex[i-1] = string_temp
                    del postfixex[i-2:i-1]
                    break
                if postfixex[i-2] == "tani":
                    string_temp = str(math.atan(float(postfixex[i-1])))
                    postfixex[i-1] = string_temp
                    del postfixex[i-2:i-1]
                    break

                if postfixex[i-2] == "sinh":
                    string_temp = str(math.sinh(float(postfixex[i-1])))
                    postfixex[i-1] = string_temp
                    del postfixex[i-2:i-1]
                    break
                if postfixex[i-2] == "cosh":
                    string_temp = str(math.cosh(float(postfixex[i-1])))
                    postfixex[i-1] = string_temp
                    del postfixex[i-2:i-1]
                    break
                if postfixex[i-2] == "tanh":
                    string_temp = str(math.tanh(float(postfixex[i-1])))
                    postfixex[i-1] = string_temp
                    del postfixex[i-2:i-1]
                    break
                if postfixex[i-2] == "cosech":
                    string_temp = str(1/(math.sinh(float(postfixex[i-1]))))
                    postfixex[i-1] = string_temp
                    del postfixex[i-2:i-1]
                    break
                if postfixex[i-2] == "sech":
                    string_temp = str(1/(math.cosh(float(postfixex[i-1]))))
                    postfixex[i-1] = string_temp
                    del postfixex[i-2:i-1]
                    break
                if postfixex[i-2] == "coth":
                    string_temp = str(1/(math.tanh(float(postfixex[i-1]))))
                    postfixex[i-1] = string_temp
                    del postfixex[i-2:i-1]
                    break

                if postfixex[i-2] == "exp":
                    string_temp = str(math.exp(float(postfixex[i-1])))
                    postfixex[i-1] = string_temp
                    del postfixex[i-2:i-1]
                    break
                if postfixex[i-2] == "log":
                    string_temp = str(math.log10(float(postfixex[i-1])))
                    postfixex[i-1] = string_temp
                    del postfixex[i-2:i-1]
                    break
                if postfixex[i-2] == "loge":
                    value = (float(postfixex[i-1]))
                    exp = math.e
                    string_temp = str(math.log(value, exp))
                    postfixex[i-1] = string_temp
                    del postfixex[i-2:i-1]
                    break

            # check for all normal operators
            if postfixex[i] == "|" and postfixex[i+2] == "|":
                string_temp = str(math.fabs(float(postfixex[i+1])))
                postfixex[i+2] = string_temp
                del postfixex[i:i+2]
            if postfixex[i] == "[" and postfixex[i+2] == "]":
                string_temp = str(math.floor(float(postfixex[i+1])))
                postfixex[i+2] = string_temp
                del postfixex[i:i+2]
            if postfixex[i] == "!" and num_checker(postfixex[i-1]):
                string_temp = str(math.factorial(int(convert_integer(postfixex[i-1]))))
                postfixex[i] = string_temp
                del postfixex[i - 1:i]
            if postfixex[i] == "+":
                string_temp = str(float(postfixex[i - 2]) + float(postfixex[i - 1]))
                postfixex[i] = string_temp
                del postfixex[i - 2:i]
                break
            if postfixex[i] == "-":
                string_temp = str(float(postfixex[i - 2]) - float(postfixex[i - 1]))
                postfixex[i] = string_temp
                del postfixex[i - 2:i]
                break
            if postfixex[i] == "*":
                string_temp = str(float(postfixex[i - 2]) * float(postfixex[i - 1]))
                postfixex[i] = string_temp
                del postfixex[i - 2:i]
                break
            if postfixex[i] == "/":
                string_temp = str(float(postfixex[i - 2]) / float(postfixex[i - 1]))
                postfixex[i] = string_temp
                del postfixex[i - 2:i]
                break
            if postfixex[i] == "^":
                string_temp = str(float(postfixex[i - 2]) ** float(postfixex[i - 1]))
                postfixex[i] = string_temp
                del postfixex[i - 2:i]
                break

    return float(postfixex[0])


def infix_calculator(infix_ref, x_value):
    """Take the value of the infix and x and returns the value"""
    postfix_exp_list = infix_to_postfix(infix_ref)

    postfix_exp_list = list_replace(postfix_exp_list, "x", str(x_value))
    postfix_exp_list = list_replace(postfix_exp_list, "e", str(math.e))
    postfix_exp_list = list_replace(postfix_exp_list, "pi", str(math.pi))

    answer = calculate(postfix_exp_list)

    return answer


def graph_plot_file(lower_range, upper_range, laps, equ):

    if num_checker(lower_range) is False:
        error_message_window("Error", "Lower limit of x should be a numeric value")
        return
    else:
        lower_range = float(lower_range)

    if num_checker(upper_range) is False:
        error_message_window("Error", "Upper limit of x should be a numeric value")
        return
    else:
        upper_range = float(upper_range)

    result , error_status = unknown_ope_checker(equ)

    if result is False:
        error_message_window("error", error_status)
        return

    result, error_status = equation_check(equation_to_list("0+"+equ+"+0"))

    if result is False:
        error_message_window("error", error_status)
        return

    try:
        infix_calculator(equ, lower_range)
    except ValueError:
        error_message_window("error", "The lower range of x is not supported by the equation")
        return

    try:
        infix_calculator(equ, upper_range)
    except ValueError:
        error_message_window("error", "The upper range of x is not supported by the equation")
        return

    try:
        x_points = [x for x in np.arange(lower_range, upper_range, laps)]
        y_points = [infix_calculator(equ, y) for y in np.arange(lower_range, upper_range, laps)]
    except ValueError:
        error_message_window("error", "Value Error")
        return
    except NameError:
        error_message_window("error", "Name Error")
        return
    except ArithmeticError:
        error_message_window("error", "Arithmetic Error")
        return
    except TypeError:
        error_message_window("error", "type Error")
        return
    except SyntaxError:
        error_message_window("error", "Syntax Error")
        return
    except SystemError:
        error_message_window("error", "System Error")
        return

    points_file = open("graph_plot.txt", "w")

    for i in range(len(x_points)):
        arg = str(x_points[i]) + "," + str(y_points[i]) + "\n"
        points_file.write(arg)

    points_file.close()


class InfoWindow(tktheme.ThemedTk):
    def __init__(self, file_name, *args, **kwargs):
        tktheme.ThemedTk.__init__(self, *args, **kwargs)
        tktheme.ThemedTk.wm_title(self, "Information!")
        tktheme.ThemedTk.get_themes(self)
        tktheme.ThemedTk.set_theme(self, "plastik")

        self.configure(bg="#D6F4DC")

        info_file = open(file_name, "r").read()

        label = tk.Label(self, text=info_file, font="verdana 10 bold", fg="#2D3502", bg="#D6F4DC")
        label.pack()


class CalculatorApp(tktheme.ThemedTk):

    def __init__(self, *args, **kwargs):
        tktheme.ThemedTk.__init__(self, *args, **kwargs)
        tktheme.ThemedTk.iconbitmap(self, default="icon.ico")
        tktheme.ThemedTk.wm_title(self, "Calculator")
        tktheme.ThemedTk.get_themes(self)
        """
        1.aquativo 2.black 3.blue 4.clearlooks	5.elegance 6.itft1
        7.keramik 8.kroc 9.plastik 10.radiance 11.smog 12.winxpblue
        """
        tktheme.ThemedTk.set_theme(self, "plastik")

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        """Add menu bar"""
        menu_bar = tk.Menu(container)

        """Add file menu"""
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label= "Save settings", command=lambda: pop_message("Info!", "Not supported yet!"))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        """Add help"""
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Graph", command=lambda: info_window("help/graph_help.txt"))
        help_menu.add_separator()
        help_menu.add_command(label="Calculator", command=lambda: info_window("help/calculator_help.txt"))
        help_menu.add_separator()
        help_menu.add_command(label="File Plot", command=lambda: info_window("help/file_plot_help.txt"))
        help_menu.add_separator()
        help_menu.add_command(label="Bar Plot", command=lambda: info_window("help/bar_plot.txt"))
        help_menu.add_command(label="Pie Plot", command=lambda: info_window("help/pie_plot.txt"))
        help_menu.add_command(label="Line Plot", command=lambda: info_window("help/line_plot.txt"))
        help_menu.add_command(label="Density Plot", command=lambda: info_window("help/density_plot.txt"))
        help_menu.add_command(label="Area Plot", command=lambda: info_window("help/area_plot.txt"))
        menu_bar.add_cascade(label="Help", menu=help_menu)

        """Add restart"""
        restart_menu = tk.Menu(menu_bar, tearoff=0)
        restart_menu.add_command(label="Add window", command=lambda: restart_all_window())
        menu_bar.add_cascade(label="Restart", menu=restart_menu)

        """Attaching it to window"""
        tk.Tk.config(self, menu=menu_bar)

        self.frames = {}
        for F in (StartPage, PageGraph, PageCalculator, PagePlot):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()

    def show_start_page(self, event):
        """Show a frame for the given page name"""
        frame = self.frames["StartPage"]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Advanced Calculator", font=controller.title_font, fg="#1836BD")
        label.pack(side="top", fill="x", pady=10)

        button1 = ttk.Button(self, text="Equation Graph", width=20,
                             command=lambda: controller.show_frame("PageGraph"))
        button2 = ttk.Button(self, text="Calculator", width=20,
                             command=lambda: controller.show_frame("PageCalculator"))
        button3 = ttk.Button(self, text="Plot", width=20,
                             command=lambda: controller.show_frame("PagePlot"))
        button1.pack()
        button2.pack()
        button3.pack()


class PageGraph(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        frame_1 = tk.Frame(self)
        frame_2 = tk.Frame(self)
        frame_3 = tk.Frame(self)
        frame_4 = tk.Frame(self)
        frame_5 = tk.Frame(self)

        frame_1.pack(side="top", pady=2)
        frame_2.pack(side="top", pady=2)
        frame_3.pack(side="top", pady=2)
        frame_4.pack(side="top", pady=2)
        frame_5.pack(side="top", pady=2)

        label = tk.Label(frame_1, text="Graph Page", font=controller.title_font, fg="#006339")
        label.pack(side="top", fill="x", pady=10)
        button = ttk.Button(frame_1, text="Go to the start page", command=lambda: controller.show_frame("StartPage"))
        button.pack(side="top", fill=tk.X)

        var_lower_x = tk.StringVar()
        var_upper_x = tk.StringVar()
        var_equation = tk.StringVar()
        interval = 0.1

        label_lower_x = tk.Label(frame_2, text="Lower limit of x", font="fixedsys", fg="#1C4CEF")
        label_upper_x = tk.Label(frame_2, text="Upper limit of x", font="fixedsys", fg="#1C4CEF")
        entry_upper_x = ttk.Entry(frame_2, textvariable=var_upper_x)
        entry_lower_x = ttk.Entry(frame_2, textvariable=var_lower_x)
        label_equation = tk.Label(frame_3, text="Equation", font="fixedsys", fg="#1C4CEF")
        entry_equation = ttk.Entry(frame_3, textvariable=var_equation)
        button_x = ttk.Button(frame_4, text="Plot the graph",
                              command=lambda: self.draw_plot(var_lower_x.get(),
                                                             var_upper_x.get(),
                                                             interval,
                                                             var_equation.get()))
        button_info = ttk.Button(frame_4, text="Info!", command=lambda: info_window("help/graph_help.txt"))

        label_lower_x.pack(side="left", fill="x", expand=True)
        entry_lower_x.pack(side="left", fill="x", expand=True)
        label_upper_x.pack(side="left", fill="x", expand=True)
        entry_upper_x.pack(side="left", fill="x", expand=True)
        label_equation.pack(side="left", fill="x", expand=True)
        entry_equation.pack(side="left", fill="x", expand=True)
        button_x.pack(side="left", fill="x")
        button_info.pack(side="left")


    def string_to_list_string(self, input_string):
        input_string.replace(" ", "")
        output_list = input_string.split(",")

        return output_list

    def string_to_list_num(self, input_string):
        input_string = self.string_to_list_string(input_string)

        output_list = []
        for element in input_string:
            try:
                output_list.append(float(element))
            except ValueError:
                error_message_window("error", "Invalid input in Y list.\nIt must be number")
                return False

        return output_list

    def convert_to_data_frame_group(self, x_list, y_list):

        x_title = "X"
        y_title = "Y"

        data = {}
        data[x_title] = x_list
        data[y_title] = y_list

        data_frame = DataFrame(data, columns=[x_title, y_title])
        data_frame_group = data_frame[[x_title, y_title]].groupby(x_title).sum()

        return data_frame_group

    def plot_points(self, lower_range, upper_range, laps, equ):

        if num_checker(lower_range) is False:
            error_message_window("Error", "Lower limit of x should be a numeric value")
            return False, False
        else:
            lower_range = float(lower_range)

        if num_checker(upper_range) is False:
            error_message_window("Error", "Upper limit of x should be a numeric value")
            return False, False
        else:
            upper_range = float(upper_range)

        result, error_status = unknown_ope_checker(equ)

        if result is False:
            error_message_window("error", error_status)
            return False, False

        result, error_status = equation_check(equation_to_list("0+" + equ + "+0"))

        if result is False:
            error_message_window("error", error_status)
            return False, False

        try:
            infix_calculator(equ, lower_range)
        except ValueError:
            error_message_window("error", "The lower range of x is not supported by the equation")
            return False, False

        try:
            infix_calculator(equ, upper_range)
        except ValueError:
            error_message_window("error", "The upper range of x is not supported by the equation")
            return False, False

        try:
            x_points_list = [x for x in np.arange(lower_range, upper_range, laps)]
            y_points_list = [infix_calculator(equ, y) for y in np.arange(lower_range, upper_range, laps)]
        except ValueError:
            error_message_window("error", "Value Error")
            return False, False
        except NameError:
            error_message_window("error", "Name Error")
            return False, False
        except ArithmeticError:
            error_message_window("error", "Arithmetic Error")
            return False, False
        except TypeError:
            error_message_window("error", "type Error")
            return False, False
        except SyntaxError:
            error_message_window("error", "Syntax Error")
            return False, False
        except SystemError:
            error_message_window("error", "System Error")
            return False, False

        return x_points_list, y_points_list

    def draw_plot(self, lower_range, upper_range, laps, equ):

        x_points_list, y_points_list = self.plot_points(lower_range, upper_range, laps, equ)

        if x_points_list is False:
            return

        self.line_plot(x_points_list, y_points_list)

    def line_plot(self, x_list, y_list):
        data_frame_group = self.convert_to_data_frame_group(x_list, y_list)

        figure_line = plt.Figure(figsize=(6, 4), dpi=100)
        axis = figure_line.add_subplot(111)
        line = FigureCanvasTkAgg(figure_line, self)
        line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        data_frame_group.plot(kind='line', legend=True, ax=axis, color="#ff0000", fontsize=10)
        axis.set_title("Graph")

        toolbar = NavigationToolbar2Tk(line, self)
        toolbar.update()
        line._tkcanvas.pack(side="top", fill="x", pady=10)


class PageCalculator(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.winfo_toplevel().bind("<Return>", self.calculate_entry_bind)
        label_title = tk.Label(self, text="Calculator", font="courier 18 bold", fg="#006339")
        button_home_page = ttk.Button(self, text="Go to the start page",
                                      command=lambda: controller.show_frame("StartPage"))

        label_title.grid(row=0, column=0, columnspan=6, pady=3)
        button_home_page.grid(row=1, column=0, columnspan=6, pady=3)

        self.entry_equ = tk.Entry(self, width=80)
        self.entry_equ.grid(row=2, column=0, columnspan=6, pady=3, padx=20)
        self.entry_equ.focus_set()

        self.prev_ans = "0"

        button_sin = ttk.Button(self, text="sin", width=14,
                                command=lambda: self.action("sin(")).grid(row=3, column=0)
        button_cos = ttk.Button(self, text="cos", width=14,
                                command=lambda: self.action("cos(")).grid(row=3, column=1)
        button_tan = ttk.Button(self, text="tan", width=14,
                                command=lambda: self.action("tan(")).grid(row=3, column=2)
        button_cosec = ttk.Button(self, text="cosec", width=14,
                                  command=lambda: self.action("cosec(")).grid(row=3, column=3)
        button_sec = ttk.Button(self, text="sec", width=14,
                                command=lambda: self.action("sec(")).grid(row=3, column=4)
        button_cot = ttk.Button(self, text="cot", width=14,
                                command=lambda: self.action("cot(")).grid(row=3, column=5)

        button_sinh = ttk.Button(self, text="sinh", width=14,
                                 command=lambda: self.action("sinh(")).grid(row=4, column=0)
        button_cosh = ttk.Button(self, text="cosh", width=14,
                                 command=lambda: self.action("cosh(")).grid(row=4, column=1)
        button_tanh = ttk.Button(self, text="tanh", width=14,
                                 command=lambda: self.action("tanh(")).grid(row=4, column=2)
        button_cosech = ttk.Button(self, text="cosech", width=14,
                                   command=lambda: self.action("cosech(")).grid(row=4, column=3)
        button_sech = ttk.Button(self, text="sech", width=14,
                                 command=lambda: self.action("sech(")).grid(row=4, column=4)
        button_coth = ttk.Button(self, text="coth", width=14,
                                 command=lambda: self.action("coth(")).grid(row=4, column=5)

        button_sini = ttk.Button(self, text="sini", width=14,
                                 command=lambda: self.action("sini(")).grid(row=5, column=0)
        button_cosi = ttk.Button(self, text="cosi", width=14,
                                 command=lambda: self.action("cosi(")).grid(row=5, column=1)
        button_tani = ttk.Button(self, text="tani", width=14,
                                 command=lambda: self.action("tani(")).grid(row=5, column=2)

        button_exp = ttk.Button(self, text="exp", width=14,
                                command=lambda: self.action("exp(")).grid(row=5, column=3)
        button_log = ttk.Button(self, text="log", width=14,
                                command=lambda: self.action("log(")).grid(row=5, column=4)
        button_loge = ttk.Button(self, text="loge", width=14,
                                 command=lambda: self.action("loge(")).grid(row=5, column=5)

        button_start_bo = ttk.Button(self, text="[", width=14,
                                     command=lambda: self.action("[")).grid(row=6, column=0)
        button_end_bo = ttk.Button(self, text="]", width=14,
                                   command=lambda: self.action("]")).grid(row=6, column=1)
        button_start_br = ttk.Button(self, text="(", width=14,
                                     command=lambda: self.action("(")).grid(row=6, column=2)
        button_end_br = ttk.Button(self, text=")", width=14,
                                   command=lambda: self.action(")")).grid(row=6, column=3)
        button_mod = ttk.Button(self, text="|", width=14,
                                command=lambda: self.action("|")).grid(row=6, column=4)
        button_e = ttk.Button(self, text="e", width=14,
                              command=lambda: self.action("e")).grid(row=6, column=5)

        button_9 = ttk.Button(self, text="9", width=14,
                              command=lambda: self.action("9")).grid(row=7, column=2)
        button_8 = ttk.Button(self, text="8", width=14,
                              command=lambda: self.action("8")).grid(row=7, column=1)
        button_7 = ttk.Button(self, text="7", width=14,
                              command=lambda: self.action("7")).grid(row=7, column=0)
        button_6 = ttk.Button(self, text="6", width=14,
                              command=lambda: self.action("6")).grid(row=8, column=2)
        button_5 = ttk.Button(self, text="5", width=14,
                              command=lambda: self.action("5")).grid(row=8, column=1)
        button_4 = ttk.Button(self, text="4", width=14,
                              command=lambda: self.action("4")).grid(row=8, column=0)
        button_3 = ttk.Button(self, text="3", width=14,
                              command=lambda: self.action("3")).grid(row=9, column=2)
        button_2 = ttk.Button(self, text="2", width=14,
                              command=lambda: self.action("2")).grid(row=9, column=1)
        button_1 = ttk.Button(self, text="1", width=14,
                              command=lambda: self.action("1")).grid(row=9, column=0)
        button_0 = ttk.Button(self, text="0", width=14,
                              command=lambda: self.action("0")).grid(row=10, column=0)
        button_dot = ttk.Button(self, text=".", width=14,
                                command=lambda: self.action(".")).grid(row=10, column=1)
        button_pi = ttk.Button(self, text="pi", width=14,
                               command=lambda: self.action("pi")).grid(row=10, column=2)

        button_blank = ttk.Button(self, text="", width=14,
                                  command=lambda: test_function("Blank")).grid(row=7, column=3)
        button_del = ttk.Button(self, text="del", width=14,
                                  command=lambda: self.clear1()).grid(row=7, column=4)
        button_ac = ttk.Button(self, text="AC", width=14,
                                command=lambda: self.clear_all()).grid(row=7, column=5)
        button_mul = ttk.Button(self, text="*", width=14,
                                command=lambda: self.action("*")).grid(row=8, column=3)
        button_div = ttk.Button(self, text="/", width=14,
                                command=lambda: self.action("/")).grid(row=8, column=4)
        button_add = ttk.Button(self, text="+", width=14,
                                command=lambda: self.action("*")).grid(row=9, column=3)
        button_sub = ttk.Button(self, text="-", width=14,
                                command=lambda: self.action("-")).grid(row=9, column=4)
        button_ans = ttk.Button(self, text="ans", width=14,
                                command=lambda: self.action(self.prev_ans)).grid(row=10, column=3)
        button_equ = ttk.Button(self, text="=", width=14,
                                command=lambda: self.calculate_entry()).grid(row=10, column=4)

        button_info = ttk.Button(self, text="Info!", width=14,
                                 command=lambda: info_window("help/calculator_help.txt")).grid(row=10, column=5)
        button_blank = ttk.Button(self, text="", width=14,
                                  command=lambda: test_function("blank")).grid(row=9, column=5)
        button_blank = ttk.Button(self, text="", width=14,
                                  command=lambda: test_function("blank")).grid(row=8, column=5)

    def action(self, ope_ref):
        """pressed button's value is inserted into the end of the text area"""
        self.entry_equ.insert(tk.END, ope_ref)

    def clear_all(self):
        """when clear button is pressed,clears the text input area"""
        self.entry_equ.delete(0, tk.END)

    def clear1(self):
        self.entry_part = self.entry_equ.get()[:-1]
        self.entry_equ.delete(0, tk.END)
        self.entry_equ.insert(0, self.entry_part)

    def calculate_entry(self):
        equ_ref = self.entry_equ.get()
        equ_ref_corrected = "0+" + equ_ref + "+0"
        result, message = unknown_ope_checker(equ_ref_corrected)
        if result is False:
            error_message_window("error", message)
            return
        equ_list = equation_to_list(equ_ref_corrected)

        result, message = equation_check(equ_list)
        if result is False:
            error_message_window("error", message)
            return
        if "x" in equ_list:
            error_message_window("error", "x is not valid for calculator")
            return
        try:
            answer = infix_calculator(equ_ref, 0)
            self.prev_ans = str(answer)
        except ValueError:
            error_message_window("error", "Value Error")
            return
        except NameError:
            error_message_window("error", "Name Error")
            return
        except ArithmeticError:
            error_message_window("error", "Arithmetic Error")
            return
        except TypeError:
            error_message_window("error", "type Error")
            return
        except SyntaxError:
            error_message_window("error", "Syntax Error")
            return
        except SystemError:
            error_message_window("error", "System Error")
            return

        self.entry_equ.delete(0, tk.END)
        self.entry_equ.insert(0, str(answer))

    def calculate_entry_bind(self, event):
        equ_ref = self.entry_equ.get()
        equ_ref_corrected = "0+" + equ_ref + "+0"
        result, message = unknown_ope_checker(equ_ref_corrected)
        if result is False:
            error_message_window("error", message)
            return
        equ_list = equation_to_list(equ_ref_corrected)

        result, message = equation_check(equ_list)
        if result is False:
            error_message_window("error", message)
            return
        if "x" in equ_list:
            error_message_window("error", "x is not valid for calculator")
            return
        try:
            answer = infix_calculator(equ_ref, 0)
            self.prev_ans = str(answer)
        except ValueError:
            error_message_window("error", "Value Error")
            return
        except NameError:
            error_message_window("error", "Name Error")
            return
        except ArithmeticError:
            error_message_window("error", "Arithmetic Error")
            return
        except TypeError:
            error_message_window("error", "type Error")
            return
        except SyntaxError:
            error_message_window("error", "Syntax Error")
            return
        except SystemError:
            error_message_window("error", "System Error")
            return

        self.entry_equ.delete(0, tk.END)
        self.entry_equ.insert(0, str(answer))


class PagePlot(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label_color = "#216810"

        frame_1 = tk.Frame(self)
        frame_2 = tk.Frame(self)
        frame_3 = tk.Frame(self)
        frame_4 = tk.Frame(self)
        frame_5 = tk.Frame(self)
        frame_6 = tk.Frame(self)
        frame_7 = tk.Frame(self)
        frame_8 = tk.Frame(self)
        frame_9 = tk.Frame(self)
        frame_10 = tk.Frame(self)
        frame_11= tk.Frame(self)
        self.frame_12 = tk.Frame(self)

        frame_1.pack(side="top", pady=2)
        frame_2.pack(side="top", pady=2)
        frame_3.pack(side="top", pady=2)
        frame_4.pack(side="top", pady=2)
        frame_5.pack(side="top", pady=2)
        frame_6.pack(side="top", pady=2)
        frame_7.pack(side="top", pady=2)
        frame_8.pack(side="top", pady=2)
        frame_9.pack(side="top", pady=2)
        frame_10.pack(side="top", pady=2)
        frame_11.pack(side="top", pady=2)
        self.frame_12.pack(side="top", pady=2)

        label = tk.Label(frame_1, text="Plot", font="courier 18 bold", fg="#006339")
        button = ttk.Button(frame_1, text="Go to the start page",
                            command=lambda: controller.show_frame("StartPage"))

        label.pack(side="top")
        button.pack(side="top")

        self.entry_file_path = tk.Entry(frame_2, width=54)
        button_browce = ttk.Button(frame_2, text="Browce", width=26, command=lambda: self.open_file())
        self.entry_column_num = tk.Entry(frame_3, width=54)
        label_column_num = tk.Label(frame_3, text="Position", font="fixedsys", fg=label_color, width=20)
        button_plot = ttk.Button(frame_4, text="Draw Plot", width=12, command=lambda: self.plot_file())

        self.entry_file_path.pack(side="left")
        button_browce.pack(side="left")
        self.entry_column_num.pack(side="left")
        label_column_num.pack(side="left")
        button_plot.pack(side="top")

        label_separator = tk.Label(frame_5, text="OR",  font="courier 18 bold", fg="#590C0C")
        label_separator.pack(side="top")

        self.entry_x_list = tk.Entry(frame_6, width=54)
        self.entry_x_list.pack(side="left")
        label_x_list = tk.Label(frame_6, text="X values for plot", font="fixedsys", fg=label_color, width=20)
        label_x_list.pack(side="left")

        self.entry_y_list = tk.Entry(frame_7, width=54)
        self.entry_y_list.pack(side="left")
        label_y_list = tk.Label(frame_7, text="Y values for plot", font="fixedsys", fg=label_color, width=20)
        label_y_list.pack(side="left")

        self.entry_x_title = tk.Entry(frame_8, width=54)
        self.entry_x_title.pack(side="left")
        label_x_title = tk.Label(frame_8, text="X values Title", font="fixedsys", fg=label_color, width=20)
        label_x_title.pack(side="left")

        self.entry_y_title = tk.Entry(frame_9, width=54)
        self.entry_y_title.pack(side="left")
        label_y_title = tk.Label(frame_9, text="Y values Title", font="fixedsys", fg=label_color, width=20)
        label_y_title.pack(side="left")

        self.entry_title = tk.Entry(frame_10, width=54)
        self.entry_title.pack(side="left")
        label_title = tk.Label(frame_10, text="Title", font="fixedsys", fg=label_color, width=20)
        label_title.pack(side="left")

        frame_button = tk.Frame(frame_11)
        frame_button.pack(side="top")

        button_bar = ttk.Button(frame_button, text="Bar", width=15, command=lambda: self.bar_plot())
        button_pie = ttk.Button(frame_button, text="Pie", width=15, command=lambda: self.pie_plot())
        button_line = ttk.Button(frame_button, text="Line", width=15, command=lambda: self.line_plot())
        button_density = ttk.Button(frame_button, text="Density", width=15, command=lambda: self.density_plot())
        button_area = ttk.Button(frame_button, text="Area", width=15, command=lambda: self.area_plot())

        button_bar.pack(side="left")
        button_pie.pack(side="left")
        button_line.pack(side="left")
        button_density.pack(side="left")
        button_area.pack(side="left")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetype=(("XL file", "*.csv"),
                                                         ("text file", "*.txt"),
                                                         ("Word file", "*.doc",),
                                                         ("All files", "*.*")))
        self.entry_file_path.delete(0, tk.END)
        self.entry_file_path.insert(0, file_path)

    def path_checker(self, input_file_path):
        if path.exists(input_file_path):
            return True
        else:
            return False

    def plot_file(self):
        file_path = self.entry_file_path.get()

        if self.path_checker(file_path) is False:
            error_message_window("errror", "File path is not correct")
            self.entry_file_path.delete(0, tk.END)
            return

        file_data_frame = pd.read_csv(file_path)

        try:
            file_data_frame_column = file_data_frame[self.entry_column_num.get()]
        except KeyError:
            error_message_window("error", "Column name is not correct")
            self.entry_column_num.delete(0, tk.END)
            return

        x_file_list = []
        y_file_list = []

        for index in range(len(file_data_frame_column)):
            x_file_list.append(file_data_frame_column[index])
            y_file_list.append(1)

        x_title, y_title = "X", "Y"
        data = {}
        data[x_title] = x_file_list
        data[y_title] = y_file_list

        data_frame = DataFrame(data, columns=[x_title, y_title])
        data_frame_group = data_frame[[x_title, y_title]].groupby(x_title).sum()

        figure_pie = plt.Figure(figsize=(4, 4), dpi=100)
        axis = figure_pie.add_subplot(111)
        pie_figure = FigureCanvasTkAgg(figure_pie, self.frame_12)
        pie_figure.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        data_frame_group.plot(kind='pie', legend=True, ax=axis, subplots=True)
        axis.set_title(self.entry_column_num.get())

        toolbar = NavigationToolbar2Tk(pie_figure, self.frame_12)
        toolbar.update()
        pie_figure._tkcanvas.pack(side="top", fill="x", pady=10)

    def title_error_correct(self, main_title, default_title):
        if main_title == "":
            return default_title
        else:
            return main_title

    def string_to_list_string(self, input_string):
        input_string.replace(" ", "")
        output_list = input_string.split(",")

        return output_list

    def string_to_list_num(self, input_string):
        input_string = self.string_to_list_string(input_string)

        output_list = []
        for element in input_string:
            try:
                output_list.append(float(element))
            except ValueError:
                error_message_window("error", "Invalid input in Y list.\nIt must be number")
                return False

        return output_list

    def empty_string_checker(self, input_string):
        if input_string == "":
            return True
        else:
            return False

    def convert_to_data_frame(self, x_side_convection_function):
        """the input function is used to the conversion method"""

        if self.empty_string_checker(self.entry_x_list.get()):
            error_message_window("error", "X list cannot be empty")
            return False, False, False

        if self.empty_string_checker(self.entry_y_list.get()):
            error_message_window("error", "Y list cannot be empty")
            return False, False, False

        x_side = x_side_convection_function(self.entry_x_list.get())
        y_side = self.string_to_list_num(self.entry_y_list.get())
        x_title = self.entry_x_title.get()
        y_title = self.entry_y_title.get()
        title = self.entry_title.get()

        x_title = self.title_error_correct(x_title, "X Title")
        y_title = self.title_error_correct(y_title, "Y Title")

        if x_title == y_title:
            y_title = y_title + "-1"

        title = self.title_error_correct(title, x_title + " Vs. " + y_title)

        try:
            if len(x_side) != len(y_side):
                error_message_window("error", "number of input in x and y should be same")
                return False, False, False
        except TypeError:
            return False, False, False

        data = {}
        data[x_title] = x_side
        data[y_title] = y_side

        data_frame = DataFrame(data, columns=[x_title, y_title])
        data_frame_group = data_frame[[x_title, y_title]].groupby(x_title).sum()

        return data_frame, data_frame_group, title

    def bar_plot(self):

        data_frame, data_frame_group, title = self.convert_to_data_frame(self.string_to_list_string)

        if data_frame is False:
            return

        figure_bar = plt.Figure(figsize=(4, 4), dpi=100)
        axis = figure_bar.add_subplot(111)
        bar_figure = FigureCanvasTkAgg(figure_bar, self.frame_12)
        bar_figure.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        data_frame_group.plot(kind='bar', legend=True, ax=axis)
        axis.set_title(title)

        toolbar = NavigationToolbar2Tk(bar_figure, self.frame_12)
        toolbar.update()
        bar_figure._tkcanvas.pack(side="top", fill="x", pady=1)

    def pie_plot(self):

        data_frame, data_frame_group, title = self.convert_to_data_frame(self.string_to_list_string)

        if data_frame is False:
            return

        figure_pie = plt.Figure(figsize=(4, 4), dpi=100)
        axis = figure_pie.add_subplot(111)
        pie_figure = FigureCanvasTkAgg(figure_pie, self.frame_12)
        pie_figure.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        data_frame_group.plot(kind='pie', legend=True, ax=axis, subplots=True)
        axis.set_title(title)

        toolbar = NavigationToolbar2Tk(pie_figure, self.frame_12)
        toolbar.update()
        pie_figure._tkcanvas.pack(side="top", fill="x", pady=1)

    def line_plot(self):
        data_frame, data_frame_group, title = self.convert_to_data_frame(self.string_to_list_num)

        if data_frame is False:
            return

        figure_line = plt.Figure(figsize=(4, 4), dpi=100)
        axis = figure_line.add_subplot(111)
        line = FigureCanvasTkAgg(figure_line, self.frame_12)
        line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        data_frame.plot(kind='line', legend=True, ax=axis, color="#ff0000", marker='o', fontsize=10)
        axis.set_title(title)

        toolbar = NavigationToolbar2Tk(line, self.frame_12)
        toolbar.update()
        line._tkcanvas.pack(side="top", fill="x", pady=1)

    def density_plot(self):
        data_frame, data_frame_group, title = self.convert_to_data_frame(self.string_to_list_num)

        if data_frame is False:
            return

        figure_line = plt.Figure(figsize=(4, 4), dpi=100)
        axis = figure_line.add_subplot(111)
        line = FigureCanvasTkAgg(figure_line, self.frame_12)
        line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        data_frame_group.plot(kind='kde', legend=True, ax=axis, color="#ff0000", marker='o', fontsize=1)
        axis.set_title(title)

        toolbar = NavigationToolbar2Tk(line, self.frame_12)
        toolbar.update()
        line._tkcanvas.pack(side="top", fill="x", pady=1)

    def area_plot(self):
        data_frame, data_frame_group, title = self.convert_to_data_frame(self.string_to_list_string)

        if data_frame is False:
            return

        figure_line = plt.Figure(figsize=(4, 4), dpi=100)
        axis = figure_line.add_subplot(111)
        line = FigureCanvasTkAgg(figure_line, self.frame_12)
        line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        data_frame.plot(kind='area', legend=True, ax=axis, color="#ff0000", fontsize=10)
        axis.set_title(title)

        toolbar = NavigationToolbar2Tk(line, self.frame_12)
        toolbar.update()
        line._tkcanvas.pack(side="top", fill="x", pady=1)


def main():

    app = CalculatorApp()
    app.bind("<Escape>", app.show_start_page)
    app.mainloop()


if __name__ == "__main__":

    main()
