from tkinter import filedialog
from tkinter import *
from emailer import Mailer
import time

ml = Mailer()


# Сохранение настроек
def save_setup():
    ml.setup(server_var.get(), port_var.get(), email_var.get(), login_var.get(), password_var.get())
    # заносим изменения в локальные переменные
    ml.read_setup()


# Модульное окно с настройками
def modal_w():
    # Читаем изменеия в файле
    ml.read_setup()

    # Устанавливаем переменные
    server_var.set(ml.server)
    port_var.set(ml.port)
    email_var.set(ml.email)
    login_var.set(ml.login)
    password_var.set(ml.password)

    # Создаем окно
    top = Toplevel(root)
    top.title('Настройки')
    top.geometry(f'300x220+500+200')  # ширина=500, высота=300, x=500, y=200
    top.resizable(False, False)  # размер окна не может быть изменён

    # Заполняем окна ввода в модальном окне
    lbl_server = Label(master=top, width=10, height=2, text='Сервер: ')
    lbl_server.grid(row=1, column=0)
    server_entry = Entry(master=top, textvariable=server_var, width=30)
    server_entry.grid(row=1, column=1)

    lbl_port = Label(master=top, width=10, height=2, text='Порт: ')
    lbl_port.grid(row=2, column=0)
    port_entry = Entry(master=top, textvariable=port_var, width=30)
    port_entry.grid(row=2, column=1)

    lbl_email = Label(master=top, width=10, height=2, text='Email: ')
    lbl_email.grid(row=3, column=0)
    email_entry = Entry(master=top, textvariable=email_var, width=30)
    email_entry.grid(row=3, column=1)

    lbl_login = Label(master=top, width=10, height=2, text='Логин: ')
    lbl_login.grid(row=4, column=0)
    login_entry = Entry(master=top, textvariable=login_var, width=30)
    login_entry.grid(row=4, column=1)

    lbl_login = Label(master=top, width=10, height=2, text='Пароль: ')
    lbl_login.grid(row=5, column=0)
    login_entry = Entry(master=top, textvariable=password_var, width=30)
    login_entry.grid(row=5, column=1)

    button_top_level = Button(top, text='Сохранить настройки', command=save_setup)
    button_top_level.grid(row=6, column=1)


def get_file():
    global file_path
    filename = filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"),))
    file_path.set(filename)


def send_mail():
    global msg                                                        # Переменная для выводимого в окно сообщения
    global file_path                                                  # Путь до файла с рассылкой
    ml.read_setup()                                                   # Читаем файл настройки
    try:
        a = ml.spam(file_path.get())                                  # Получаем генератор из функции рассылки
        for i in a:                                                   # Выполняем пошагово генератор и получаем последний отправленный адресс
            msg.set(i)                                                # Устанавливаем текст сообщения для вывода
            root.update()                                             # Обновляем главное окно программы для отображения изменений в сообщении
        msg.set('Рассылка отправлена!')                               # По завершению отправки меняем текст сообщения на финальный
    except Exception as e:
        msg.set('Ошибка! Последний адрес отправки: ' + i)



root = Tk()
root.title('Tania - meow sender')
root.geometry(f'500x200+500+200')  # ширина=500, высота=200, x=300, y=200
root.resizable(False, False)  # размер окна может быть изменён только по горизонтали

login_var = StringVar()
password_var = StringVar()
server_var = StringVar()
port_var = StringVar()
email_var = StringVar()

# файл с рассылкой
file_path = StringVar()
file_path.set('Выберите scv файл с данными о рассылке')
lbl_file = Label(master=root, width=50, height=5, textvariable=file_path)
lbl_file.grid(row=1, column=1)
button_file = Button(text="Выберите файл", command=get_file)
button_file.grid(row=1, column=2)

# lbl_date = Label(master=root, width=50, height=3, text='Введите дату в удобном для вас формате: ')
# # lbl_date.grid(row=3, column=1)
# # date_doc = StringVar()
# # date_entry = Entry(textvariable=date_doc)
# # date_entry.grid(row=3, column=2)

# Запускаем рассылку
button_send = Button(text="Отправить рассылку", command=send_mail)
button_send.grid(row=2, column=1)

button_set = Button(root, text='Настройки', command=modal_w)
button_set.grid(row=2, column=2)

msg = StringVar()
lbl_msg = Label(master=root, width=50, height=5, fg='red', textvariable=msg)
lbl_msg.grid(row=3, column=1)

root.mainloop()

# ------------- html разметку доделать --------------------------
