#encoding=utf-8
from tkinter import Tk, LEFT, Entry, RIGHT, RAISED, BOTH, X, Message, W, \
    filedialog, StringVar, IntVar, messagebox, Toplevel
from tkinter.ttk import Style, Frame, Label, Button, Checkbutton

from lottery_player import create_lottery_helper_file
from spinner import Spinner


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
        initialdir="C:/", title="Selecione",
        filetypes=(("arquivo excel", "*.xlsx"), ("all files", "*.*")))
    return file_path


class Application(Frame):
    default_title_font = ('Arial', '14')
    default_text_font = ('Arial', '12')


    def __init__(self):
        super(Application, self).__init__()
        self.init_ui()

    def init_ui(self):
        # Master Configurations
        self.master.geometry('300x300')
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
        self.file_path.set('C:\\')
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
        try:
            max_combinations = int(self.max_combinations.get())
        except ValueError:
            max_combinations = None
        is_random = self.random.get()
        filepath = self.file_path.get()
        self.popup_dialog()
        self.wait_window(self.top)
        create_lottery_helper_file(range_min, range_max, n_digits,
                                   max_combinations, is_random, filepath)
        self.top.destroy()
        messagebox.showinfo('Finalizado', 'Arquivo Gerado com Sucesso em: '
                                          '{}'.format(filepath))

    def on_file_search_click(self):
        file_path = prompt_file_save_path()
        self.file_path.set(file_path)

    def on_cancel(self):
        self.master.quit()


def initiate_main_interface():
    root = Tk()
    root.geometry('300x300+300+300')
    app = Application()
    root.mainloop()