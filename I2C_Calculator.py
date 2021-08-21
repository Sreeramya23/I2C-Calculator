from tkinter import Tk, StringVar, messagebox
from tkinter.ttk import *
import csv

# mode, X:(Vol/V, trise/ns, Cb/pF, fscl/KHz)
mode_values = {"S": (0.4, 1000, 400, 100), "F": (0.4, 300, 400, 400), "F+": (0.4, 120, 550, 1000)}


class InvalidInputError(ValueError):
    def __init__(self, value):
        self.value = value


def check_vdd() -> float:
    try:
        vdd = float(vdd_entry.get())
        if vdd >= 5.5 or vdd <= 0.0:
            raise InvalidInputError(vdd)
    except InvalidInputError:
        messagebox.showwarning("showwarning", "Warning! Voltage must be in the range (0,5.5)")
    else:
        return vdd


def check_Cb(mode_n) -> int:
    try:
        Cb = int(cb_entry.get())
        if not mode_values[mode_n][2] > Cb > 0.0:
            raise InvalidInputError(Cb)
    except InvalidInputError:
        messagebox.showwarning("showwarning",
                               f"Warning! Capacitance must be in the range (0, {mode_values[mode_n][2]})"
                               + f" for {mode_n} mode")
    else:
        return Cb


def Calculate_resistance(min_n: float, res_file: str) -> str:
    with open(res_file) as file:
        read = csv.reader(file)
        for row in read:
            for x in row:
                if float(x) > min_n:
                    return x


def results(lst) -> None:
    box.insert("", "end", values=lst)


def calculate():
    box.delete(*box.get_children())
    mode_n = clicked.get()
    Iol = 3  # mA
    Vol = mode_values[mode_n][0]  # V
    vdd_value = check_vdd()  # V
    Cb_value = check_Cb(mode_n)  # nF
    trise = mode_values[mode_n][1]  # ns
    fscl = mode_values[mode_n][3]  # KHz
    if not (vdd_value is None or Cb_value is None):
        Rpmin = ((vdd_value - Vol) * 1000) / Iol  # ohm
        Rpmax = (trise * 10 ** 6) / (0.8473 * Cb_value)  # ohm
        Rpstd_5 = Calculate_resistance(Rpmin, 'Rpstd_5.csv')
        Rpstd_1 = Calculate_resistance(Rpmin, 'Rpstd_1.csv')
        result_tuple = (int(Rpmin), int(Rpmax), Rpstd_1, Rpstd_5, mode_n, fscl)
        results(result_tuple)


if __name__ == '__main__':
    root: Tk = Tk()
    root.geometry('800x500')
    root.title("I2C Calculator")
    root.configure(bg='sky blue')

    vdd_entry = StringVar()
    cb_entry = StringVar()

    label1 = Label(root, text='I2C Calculator', font=('Times', 30, 'bold'),
                   background='sky blue', foreground='dark blue')
    label1.place(x=270, y=0)

    result_columns = ('Rpmin (Ohms)', 'Rpmax (Ohms)', 'Rpstd_1% (Ohms)', 'Rpstd_5% (Ohms)', 'Mode', 'fscl (KHz)')
    style1 = Style()
    style1.configure('Treeview', foreground='Red')
    box = Treeview(root, columns=result_columns, show='headings', selectmode='browse')

    for n, element in enumerate(result_columns):
        box.heading(n, text=element)
        box.column(n, width=110)
    box.place(x=70, y=50)

    style2 = Style()
    style2.configure('TButton', foreground='dark blue', font=('Times', 20, 'bold'), background='dark blue')
    btn = Button(root, text="Calculate", style="TButton", command=calculate)
    btn.place(x=320, y=300)

    label2 = Label(root, text='Mode: ', font=('Times', 20, 'bold'), background='sky blue', foreground='dark blue')
    label2.place(x=10, y=400)

    label3 = Label(root, text='Vdd (V): ', font=('Times', 20, 'bold'), background='sky blue', foreground='dark blue')
    label3.place(x=400, y=400)

    entry_box1 = Entry(root, textvariable=vdd_entry, font=('calibre', 10, 'normal'))
    entry_box1.place(x=520, y=410)

    label4 = Label(root, text='Cb (pF): ', font=('Times', 20, 'bold'), background='sky blue', foreground='dark blue')
    label4.place(x=400, y=440)

    entry_box2 = Entry(root, textvariable=cb_entry, font=('calibre', 10, 'normal'))
    entry_box2.place(x=520, y=450)

    options = ('S', 'F', 'F+')
    clicked = StringVar()
    drop = OptionMenu(root, clicked, options[1], *options)
    drop.configure(width=30)
    drop.place(x=10, y=450)
    root.mainloop()
