from tkinter import (Tk, PhotoImage, Label, Entry, Button, Scale, IntVar,
                     BooleanVar, StringVar, Checkbutton, Frame, OptionMenu)
from .utils import resource_path
from . import constants as const


class PasswordGeneratorUI:
    """
    Класс, отвечающий за создание и отрисовку всех элементов
    пользовательского интерфейса (UI) приложения.
    """

    def __init__(self, root: Tk):
        """
        Инициализирует UI, создает и размещает все виджеты.
        """
        self.root = root
        self._configure_root_window()
        self._load_images()
        self._create_widgets()
        self._layout_widgets()

    def _configure_root_window(self):
        """Настраивает главное окно приложения."""
        self.root.title("Paasword")
        self.root.iconbitmap(resource_path("assets/images/logo.ico"))
        self.root.geometry("660x290")
        self.root.resizable(width=False, height=False)
        self.root.config(bg="#ff8e3e")

    def _load_images(self):
        """Загружает все необходимые изображения."""
        self.logo = PhotoImage(file=resource_path("assets/images/inapp_logo.png"))
        self.copy_button_image = PhotoImage(file=resource_path("assets/images/copy_button.png"))
        self.checkmark_image = PhotoImage(file=resource_path("assets/images/checkmark.png"))
        self.update_button_image = PhotoImage(file=resource_path("assets/images/update_button.png"))

    def _create_widgets(self):
        """Создает все виджеты приложения."""

        # Переменные для виджетов
        self.password_length_value = IntVar()
        self.include_numbers = BooleanVar()
        self.include_lowercase = BooleanVar()
        self.include_uppercase = BooleanVar()
        self.include_special_symbols = BooleanVar()
        self.include_uniqueness = BooleanVar()
        self.include_ambiguous_symbols = BooleanVar(value=True)
        self.include_letter_start = BooleanVar()
        self.preset_display_var = StringVar()
        self.preset_display_var.set(const.PRESET_DISPLAY_NAMES["fullstrong"])

        # Верхняя часть (лого, поле пароля, кнопки)
        self.logo_label = Label(self.root, image=self.logo, bg="#ff8e3e")
        self.password_field = Entry(self.root, width=20, font=("Consolas", 18), bg="#9e5826",
                                    readonlybackground="#9e5826", justify="center", state="readonly")
        self.copy_button = Button(self.root, width=30, height=30, bg="#ff8e3e", relief="flat",
                                  borderwidth=0, highlightthickness=0, image=self.copy_button_image)
        self.update_button = Button(self.root, width=30, height=30, bg="#ff8e3e", relief="flat",
                                    borderwidth=0, highlightthickness=0, image=self.update_button_image)

        # Настройки длины и силы пароля
        self.slider_label = Label(self.root, text="Длина пароля:", bg="#ff8e3e", font=(
            "Meiryo UI", 14), fg="black")
        self.length_slider = Scale(self.root, from_=4, to=36, orient="horizontal", width=20, borderwidth=0,
                                   highlightthickness=0, sliderrelief="flat", troughcolor="#9e5826",
                                   background="black", activebackground="black", showvalue=False,
                                   variable=self.password_length_value)
        self.password_length_field = Entry(self.root, width=4, bg="#9e5826", readonlybackground="#9e5826",
                                           font=("Meiryo UI", 11), justify="center",
                                           textvariable=self.password_length_value, state="readonly")

        self.strength_meter_label = Label(self.root, text="Сила пароля:", bg="#ff8e3e", font=("Meiryo UI", 14), fg="black")
        self.strength_meter_frame = Frame(self.root, borderwidth=0.5, relief="solid")
        self.strength_meter = []
        for _ in range(3):
            label = Label(self.strength_meter_frame, bg="#9e5826", width=5, height=1, borderwidth=0.5, relief="groove")
            self.strength_meter.append(label)

        # Чекбоксы настроек
        common_cb_options = {"selectcolor": "#ff8e3e", "font": (
            "Meiryo UI", 12), "bg": "#ff8e3e", "activebackground": "#ff8e3e"}
        self.numbers_checkbox = Checkbutton(
            self.root, text="Включать цифры (0-9)", variable=self.include_numbers, **common_cb_options)
        self.lowercase_checkbox = Checkbutton(
            self.root, text="Включать прописные буквы (a-z)", variable=self.include_lowercase, **common_cb_options)
        self.uppercase_checkbox = Checkbutton(
            self.root, text="Включать ЗАГЛАВНЫЕ буквы (A-Z)", variable=self.include_uppercase, **common_cb_options)
        self.special_symbols_checkbox = Checkbutton(
            self.root, text="Включать спец. символы (!@#...)", variable=self.include_special_symbols, **common_cb_options)
        self.uniqueness_checkbox = Checkbutton(
            self.root, text="Без повтора символов", variable=self.include_uniqueness, **common_cb_options)
        self.ambiguous_symbols_checkbox = Checkbutton(
            self.root, text="Исключить похожие (l, 1, O, 0)", variable=self.include_ambiguous_symbols, **common_cb_options)
        self.letter_start_checkbox = Checkbutton(
            self.root, text="Начинать с буквы", variable=self.include_letter_start, **common_cb_options)

        # Выпадающий список с пресетами
        self.preset_label = Label(self.root, text="Пресет:", bg="#ff8e3e", font=("Meiryo UI", 14), fg="black")

        preset_options = list(const.PRESET_DISPLAY_NAMES.values())
        self.preset_option_menu = OptionMenu(self.root, self.preset_display_var, *preset_options)
        self.preset_option_menu.config(width=15, font=("Meiryo UI", 10), bg="#9e5826", fg="white",
                                       activebackground="#9e5826", activeforeground="white",
                                       relief="flat", highlightthickness=0, highlightbackground="black",
                                       highlightcolor="black")
        self.preset_option_menu["menu"].config(font=("Meiryo UI", 10), bg="#9e5826", fg="white",
                                               activebackground="#ff8e3e", activeforeground="black",
                                               borderwidth=0, relief="flat", bd=0)

    def _layout_widgets(self):
        """Размещает все виджеты в окне с помощью grid."""
        self.logo_label.grid(row=0, column=0, columnspan=4, sticky="nw", padx=4)
        self.password_field.grid(row=1, column=0, columnspan=2, padx=12, sticky="ew")
        self.copy_button.grid(row=1, column=2, padx=(0, 12))
        self.update_button.grid(row=1, column=3, padx=(0, 12))

        # Разделение сетки на две колонки для настроек
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Левая колонка
        self.slider_label.grid(row=2, column=0, padx=10, sticky="w")
        self.length_slider.grid(row=3, column=0, padx=12, sticky="ew")
        self.password_length_field.grid(row=3, column=0, padx=(150, 0), sticky="w")
        self.lowercase_checkbox.grid(row=4, column=0, padx=10, sticky="w")
        self.uppercase_checkbox.grid(row=5, column=0, padx=10, sticky="w")
        self.numbers_checkbox.grid(row=6, column=0, padx=10, sticky="w")
        self.special_symbols_checkbox.grid(row=7, column=0, padx=10, sticky="w")

        # Правая колонка
        self.strength_meter_label.grid(row=2, column=1, padx=10, sticky="w")
        self.strength_meter_frame.grid(row=3, column=1, padx=15, sticky="w")
        for label in self.strength_meter:
            label.pack(side="left")
        self.letter_start_checkbox.grid(row=4, column=1, padx=10, sticky="w")
        self.uniqueness_checkbox.grid(row=5, column=1, padx=10, sticky="w")
        self.ambiguous_symbols_checkbox.grid(row=6, column=1, columnspan=4, padx=10, sticky="w")
        self.preset_label.grid(row=7, column=1, padx=10, sticky="sw")
        self.preset_option_menu.grid(row=7, column=1, columnspan=2, sticky="se")
