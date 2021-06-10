from tkinter import Button, Label, StringVar, sys, ttk
from data_base_functions import DBHandler
from graphic_settings_and_texts import settings


class GameGUI(object):

    def __init__(self, root):
        """В этом методе инициализируются графические параметры приложения и создается подключение к базе данных."""
        self.root = root
        self.root.resizable(False, False)
        self.data_base_path = 'hieroglyph_data_base.db'
        self.game_information_path = 'game_information.txt'
        self.data_base = DBHandler('hieroglyph_data_base.db')
        self.root.title(settings['title'])
        self.root.geometry(settings['size'])
        self.game_button = Button(root, text=settings['begin_game_label'], command=self.new_game,
                                  height=2, width=19, font=settings['font_small'])
        self.game_label = Label(root, text=settings['begin_game_button'], font=settings['font_small'])

        self.help_button = Button(root, text=settings['help_button'], command=self.get_help,
                                  height=2, width=19, font=settings['font_small'])
        self.help_label = Label(root, text=settings['help_label'],
                                font=settings['font_small'])
        self.exit_button = Button(root, text=settings['exit_button'], command=self.exit_game,
                                  height=2, width=19, font=settings['font_small'])
        self.exit_label = Label(root, text=settings['exit_label'], font=settings['font_small'])
        self.return_menu = Button(root, text=settings['main_menu'], command=self.main_menu,
                                  height=2, width=19, font=settings['font_small'])
        self.lessons = self.data_base.request_name_lessons()
        self.lesson_box = ttk.Combobox(root, height=2, width=19, font=settings['font_small'], values=self.lessons)
        self.lesson_box.set(settings['choose_lesson'])
        self.choose_lesson_button = Button(root, height=1, text=settings['choose_lesson'],
                                           font=settings['font_small'], command=self.submit)
        self.characters_str = StringVar()
        self.hint_str = StringVar()
        self.end_str = StringVar()
        self.end_str.set("")
        self.current_symbol = 0
        self.progress_str = StringVar()
        self.characters = Label(root, textvariable=self.characters_str, font=settings['font_chars'])
        self.hint = Label(root, textvariable=self.hint_str, font=settings['font_medium'])
        self.end_game = Label(root, textvariable=self.hint_str, font=settings['font_medium'])
        self.next_symbol_button = Button(root, height=2, width=19, text=settings['next_hieroglyph'],
                                         font=settings['font_small'], command=self.get_next)
        self.prev_symbol_button = Button(root, height=2, width=19, text=settings['prev_hieroglyph'],
                                         font=settings['font_small'], command=self.get_prev)
        self.progress = Label(root, textvariable=self.progress_str, font=settings['font_progress'])
        self.current_lesson = []
        self.information_label = Label(root, text=self.get_info_game(), font=settings['font_info'])
        self.hint_status = False
        self.hint_button = Button(root, width=19, text=settings['hide_button'],
                                  command=self.show_hint, font=settings['font_small'])
        self.main_menu()

    def get_info_game(self):
        """Этот метод отвечает за выгрузку из текстового файла текста-помощи по приложению."""
        with open(self.game_information_path, 'r', encoding='utf-8') as file:
            info = ""
            for line in file:
                info += line
            return info

    def main_menu(self):
        """Этот метод отвечает за открытие окна главного меню приложения."""
        self.close_all()
        self.game_button.place(x=350, y=150)
        self.game_label.place(x=270, y=100)
        self.help_button.place(x=350, y=300)
        self.help_label.place(x=200, y=250)
        self.exit_button.place(x=350, y=450)
        self.exit_label.place(x=270, y=400)

    def submit(self):
        """Этот метод ответчает за подтверждение нажатия кнопки 'Выберите урок'."""
        self.current_symbol = 0
        if self.lesson_box.get() != settings['choose_lesson']:
            self.current_lesson = self.data_base.request_lesson(self.lesson_box.get())
            self.progress_str.set(f"{self.current_symbol + 1}/{len(self.current_lesson)}")
            self.progress.place(x=480, y=20)
            self.characters.place(x=350, y=250)
            self.characters_str.set(self.current_lesson[self.current_symbol][0])
            self.hint_str.set(self.current_lesson[self.current_symbol][1])

    def get_help(self):
        """Этот метод отвечает за открытие окна помощи по приложению."""
        self.close_all()
        self.information_label.place(x=1, y=100)
        self.return_menu.place(x=300, y=400)

    def close_all(self):
        """Этот метод отвечает за исчезновение с окна прилоежния всех существующих кнопок и текста."""
        self.next_symbol_button.place_forget()
        self.prev_symbol_button.place_forget()
        self.hint_button.place_forget()
        self.lesson_box.place_forget()
        self.choose_lesson_button.place_forget()
        self.game_label.place_forget()
        self.game_button.place_forget()
        self.help_button.place_forget()
        self.help_label.place_forget()
        self.exit_button.place_forget()
        self.exit_label.place_forget()
        self.information_label.place_forget()
        self.return_menu.place_forget()
        self.characters.place_forget()
        self.hint.place_forget()
        self.progress.place_forget()

    def new_game(self):
        """Этот метод отвечает за начало новой игры."""
        self.close_all()
        self.lesson_box.place(x=20, y=10)
        self.choose_lesson_button.place(x=60, y=60)
        self.next_symbol_button.place(x=20, y=120)
        self.prev_symbol_button.place(x=20, y=200)
        self.hint_button.place(x=20, y=280)
        self.return_menu.place(x=20, y=360)
        self.help_button.place(x=20, y=440)
        self.exit_button.place(x=20, y=520)

    def get_next(self):
        """Этот метод отвечает за нажатие кнопки 'Следующий иероглиф'."""
        if self.lesson_box.get() == settings['choose_lesson']:
            self.hint_str.set(settings['choose_your_lesson'])
            self.hint.place(x=320, y=180)
        else:
            if self.current_symbol < len(self.current_lesson) - 1:
                self.current_symbol += 1
                self.progress_str.set(f"{self.current_symbol + 1}/{len(self.current_lesson)}")
                self.progress.place(x=480, y=20)
                self.characters.place(x=350, y=250)
                self.characters_str.set(self.current_lesson[self.current_symbol][0])
                self.hint_str.set(self.current_lesson[self.current_symbol][1])
            else:
                self.progress.place(x=480, y=20)
                self.characters.place(x=350, y=250)
                self.characters_str.set("")
                self.hint_status = False
                self.show_hint()
                self.progress.place_forget()
                self.hint_str.set(settings['seen_all'])

    def get_prev(self):
        """Этот метод отвечает за нажатие кнопки 'Предыдущий иероглиф'."""
        if self.lesson_box.get() == settings['choose_lesson']:
            self.hint_str.set(settings['choose_your_lesson'])
            self.hint.place(x=320, y=180)
        else:
            if self.current_symbol > 0 and self.hint_str.get() != settings['seen_all']:
                self.current_symbol -= 1
            if self.current_lesson:
                self.progress_str.set(f"{self.current_symbol + 1}/{len(self.current_lesson)}")
                self.progress.place(x=480, y=20)
                self.characters.place(x=350, y=250)
                self.characters_str.set(self.current_lesson[self.current_symbol][0])
                self.hint_str.set(self.current_lesson[self.current_symbol][1])

    def show_hint(self):
        """Этот метод отвечает за нажатие кнопки 'Увидеть/скрыть подсказку'."""
        if self.hint_status:
            self.hint.place_forget()
            self.hint_status = False
        else:
            self.hint.place(x=320, y=180)
            self.hint_status = True

    def exit_game(self):
        """Этот метод отвечает за закрытие окна приложения."""
        sys.exit(0)

