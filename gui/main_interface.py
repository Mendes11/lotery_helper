#encoding=utf-8
import os

from tkinter import LEFT, X, IntVar, RIGHT, filedialog, BOTH, Message, RAISED, \
    StringVar, Toplevel, messagebox, Tk, W
from tkinter.ttk import Entry, Frame, Label, Checkbutton, Style, Button

from gui.spinner import Spinner
from lottery_player.lottery_player import (expected_list_size,
                                           create_lottery_helper_file)


BASE_DIR = os.getenv('ProgramFiles(x86)') or os.getenv('ProgramFiles') or \
           os.getcwd()

def generate_input(frame, label, input_class=None):
    if input_class is None:
        input_class = Entry
    container = Frame(frame)
    container.pack(fill=X)
    Label(container, text=label, font=('Arial', '12')).pack(
        side=LEFT, padx=5, pady=5)
    input_obj = input_class(container)
    if input_class == Checkbutton:
        var = IntVar()
        input_obj = input_class(container, variable=var)
        input_obj.pack(side=RIGHT, fill=X, padx=5)
        return var
    else:
        input_obj.pack(side=RIGHT, fill=X, padx=5, expand=True)
    return input_obj


def prompt_file_save_path():
    file_path = filedialog.asksaveasfilename(
        initialdir=BASE_DIR, title="Selecione",
        filetypes=(("arquivo excel", "*.xlsx"), ("all files", "*.*")))
    if file_path.split('.')[-1] != 'xlsx':
        file_path += '.xlsx'
    return file_path


class Application(Frame):
    default_title_font = ('Arial', '14')
    default_text_font = ('Arial', '12')


    def __init__(self):
        super(Application, self).__init__()
        self.init_ui()

    def init_ui(self):
        # Master Configurations
        self.master.geometry('400x320')
        self.style = Style()
        self.style.theme_use('default')
        self.master.title(u'Gerador de Números de Loteria')
        self.pack(expand=True, fill=BOTH)

        message_frame = Frame(self)
        message_frame.pack(side=LEFT, expand=True, fill=X)
        Message(message_frame, anchor=W, width=300,
                font=self.default_title_font,
                text='Preencha o Formulário e clique em GERAR para gerar '
                     'os valores desejados: ').pack(fill=X, expand=True)
        # Form Frame
        self.form_frame = Frame(self.master, relief=RAISED, borderwidth=1)
        self.form_frame.pack(fill=BOTH, expand=True, padx=5)
        self.range_min = generate_input(self.form_frame, 'Valor Mínimo: ')
        self.range_min['text'] = 1
        self.range_max = generate_input(self.form_frame, 'Valor Máximo: ')
        self.range_max['text'] = 25
        self.n_digits = generate_input(self.form_frame, 'Número de Dígitos: ')
        self.n_digits['text'] = 5
        self.max_combinations = generate_input(self.form_frame,
                                               'Número Máximo de '
                                               'Combinações: ')
        self.random = generate_input(self.form_frame, 'Geração Randômica',
                                     input_class=Checkbutton)
        # File Path Frame
        self.file_path_frame = Frame(self.form_frame)
        self.file_path_frame.pack(fill=BOTH, expand=True)
        self.file_path_input = generate_input(self.file_path_frame,
                                              'Arquivo: ')
        self.search_button = Button(self.file_path_frame, text="Procurar",
                                    command=self.on_file_search_click)
        self.search_button.pack(side=RIGHT)

        # Text Variable Binding to file_path_input
        self.file_path = StringVar()
        self.file_path.set(BASE_DIR)
        self.file_path_input['textvariable'] = self.file_path

        # Buttons
        self.buttons_frame = Frame(self.master)
        self.buttons_frame.pack(fill=BOTH, expand=True)
        self.close_button = Button(self.buttons_frame, text="Fechar", width=10,
                                   command=self.on_cancel)
        self.close_button.pack(side=RIGHT, padx=5, pady=5)
        self.ok_button = Button(self.buttons_frame, command=self.on_confirm,
                                text="Gerar", width=10)
        self.ok_button.pack(side=RIGHT)

    def popup_dialog(self):
        self.top = Toplevel(self)
        Label(self.top, text='Gerando Arquivo...').pack()
        Spinner(self.top, size=48).pack(side=LEFT, padx=4)

    def on_confirm(self):
        try:
            range_min = int(self.range_min.get())
            range_max = int(self.range_max.get())
            n_digits = int(self.n_digits.get())
        except ValueError:
            messagebox.showerror('Erro', 'Digite apenas números')
            return
        max_size = expected_list_size(range_min, range_max, n_digits)
        try:
            max_combinations = int(self.max_combinations.get())
            if max_combinations > max_size:
                messagebox.showerror('Erro',
                                     'Número Máximo de Combinações: {} é Maior '
                                     'do que o número total de combinações: '
                                     '{}'.format(max_combinations, max_size))
                return
        except ValueError:
            max_combinations = None
        is_random = self.random.get()
        filepath = self.file_path.get()
        #self.popup_dialog()
        #self.wait_window(self.top)
        try:
            create_lottery_helper_file(range_min, range_max, n_digits,
                                       max_combinations, is_random, filepath)
        except BaseException as e:
            messagebox.showerror("Erro", e)
        #self.top.destroy()
        total_combinations = max_size if max_combinations is None else \
            max_combinations
        messagebox.showinfo('Finalizado',
                            'Arquivo Gerado com Sucesso em: {}, '
                            'com um total de {} combinações'
                            ''.format(filepath, total_combinations))

    def on_file_search_click(self):
        file_path = prompt_file_save_path()
        self.file_path.set(file_path)

    def on_cancel(self):
        self.master.quit()


def initiate_main_interface():
    root = Tk()
    root.geometry('350x350+300+300')
    app = Application()
    root.mainloop()