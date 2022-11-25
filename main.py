from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.linalg import solve
from tkinter import Tk, Frame, Button, N, S, E, W, Label, Entry, StringVar, DoubleVar, filedialog
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

class MainWindow(Tk):
    def _read_data_from_table(self):
        res = []
        for i in range(len(self._matrix)):
            row = []
            for j in range(len(self._matrix[0])):
                row += [self._matrix[i][j].get()]
            res += [row]
        return res
    
    def _save_plot(self, e):
        fname = filedialog.asksaveasfilename()
        if fname: self._figure.savefig(fname)

    def _save_data(self, e):
        fname = filedialog.asksaveasfilename()
        if fname: np.savetxt(fname, self._X)

    def _calc(self, e):
        A = np.array(
            self._read_data_from_table()
        )
        
        B = np.array([170,180,140,180,350]).reshape((5,1))
        self._X = solve(A, B)
        labels = self._df.columns[1:]
        
        self._figure = plt.Figure(figsize=(6,5), dpi=100)
        ax = self._figure.add_subplot()
        chart = FigureCanvasTkAgg(self._figure, self.graph_frame)
        chart.get_tk_widget().pack(fill='both', expand=1)
        ax.pie(self._X.flatten(), labels=labels, shadow=1)
                          #      Хардкод имени файла - плохо!
    def _load_data(self): #          v
        self._df = pd.read_excel("./data.ods", engine="odf")
    
    def _display_data(self):
        i = 0
        self._matrix = []
        for column_name in self._df.columns:
            Label(self.coeff_frame, text=column_name).grid(row=0, 
                 column=i, 
                 sticky=E+W)
            self.coeff_frame.columnconfigure(i, weight=1)
            row = []
            for j in range(len(self._df[column_name])):
                value = self._df[column_name][j]
                if type(value) == str:
                    var = StringVar(self, value=value)
                else:
                    var = DoubleVar(self, value=value)
                    row += [var]
                Entry(self.coeff_frame, textvariable=var).grid(row=j+1, 
                     column=i, 
                     sticky=E+W)
            if row: self._matrix += [row]
            i += 1
            
    def __init__(self):
        self._button_names = {
            'Рассчитать': self._calc,
            'Сохранить данные': self._save_data,
            'Сохранить диаграмму': self._save_plot,
        }
        super().__init__() 
        self._configure()
        self._bind_events()
        
        self._load_data()
        self._display_data()
    
    def _configure(self):
        self.title("Решение СЛАУ")
        self.coeff_frame = Frame(self, width=800, height=100, bg="red")
        self.graph_frame = Frame(self, width=400, height=100, bg="green")
        self.bttns_frame = Frame(self, width=400, height=100, bg="white")
        self.coeff_frame.grid(row=0, column=0, columnspan=2, sticky=N+S+E+W)
        self.graph_frame.grid(row=1, column=0, sticky=N+S+E+W)
        self.bttns_frame.grid(row=1, column=1, sticky=N+S+E+W)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        for btn_text in self._button_names:
            Button(self.bttns_frame, name=btn_text, text=btn_text).pack(fill='both', expand=1)
        
    def _bind_events(self):
        self.bind("<Escape>", lambda x: self.destroy())
        for btn_text in self._button_names:
            self.bttns_frame.children[btn_text].bind('<Button-1>', 
                                     self._button_names[btn_text])
            
if __name__ == '__main__':
    slau = MainWindow()
    slau.mainloop()
    
    
    
#        