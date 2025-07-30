from tkinter import messagebox
from random import choice, sample
import tkinter as tk

from .ui import PasswordGeneratorUI
from . import constants as const


class PasswordGeneratorApp:
    """
    Основной класс приложения, управляющий логикой, состоянием и взаимодействием с UI.
    """

    def __init__(self, root: tk.Tk):
        """
        Инициализирует приложение.
        """
        self.root = root
        self.ui = PasswordGeneratorUI(root)

        self.is_applying_preset = False

        self._bind_events()
        self.apply_preset()

    def _bind_events(self):
        """Привязывает все функции-обработчики к виджетам."""
        self.ui.copy_button.configure(command=self.copy_password)
        self.ui.update_button.configure(command=self.update_password_and_strength)
        self.ui.length_slider.configure(command=self.update_password_and_strength_on_slider_change)

        # Привязка к изменению любого чекбокса или пресета
        for cb in (self.ui.include_numbers, self.ui.include_lowercase, self.ui.include_uppercase,
                   self.ui.include_special_symbols, self.ui.include_uniqueness,
                   self.ui.include_ambiguous_symbols, self.ui.include_letter_start):
            cb.trace_add("write", self.on_settings_change)

        self.ui.preset_display_var.trace_add("write", lambda *args: self.apply_preset())

    def update_password_and_strength(self):
        """Обновляет поле с паролем и индикатор силы."""
        password = self.generate_password()
        self.update_password_field(password)
        self.update_strength_meter()

    def update_password_and_strength_on_slider_change(self, value: str):
        """
        Колбэк для слайдера. Обновляет пароль и силу.
        value приходит как строка, но он не нужен, т.к. берётся значение из IntVar.
        """
        self.update_password_and_strength()

    def on_settings_change(self, *args):
        """
        При любом изменении чекбоксов переключает пресет на "Свой" и обновляет пароль.
        """
        if self.is_applying_preset:
            return  # Игнорирование изменений, пока применяется пресет

        custom_preset_name = const.PRESET_DISPLAY_NAMES["custom"]
        if self.ui.preset_display_var.get() != custom_preset_name:
            # Блокируем обратный вызов apply_preset, чтобы не было цикла
            self.is_applying_preset = True
            self.ui.preset_display_var.set(custom_preset_name)
            self.is_applying_preset = False
        else:       # Если уже "Свой", то просто генерируем новый пароль
            self.update_password_and_strength()

    def copy_password(self):
        """Копирует сгенерированный пароль в буфер обмена."""
        password = self.ui.password_field.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)

            # Временное изменение кнопки копирования на галочку
            self.ui.copy_button.config(image=self.ui.checkmark_image)
            self.root.after(1000, lambda: self.ui.copy_button.config(image=self.ui.copy_button_image))

    def generate_password(self) -> str:
        """
        Генерирует пароль на основе выбранных пользователем настроек.
        """
        if self.ui.include_letter_start.get() and not (self.ui.include_lowercase.get() or self.ui.include_uppercase.get()):
            messagebox.showwarning(
                title="Некорректные параметры",
                message="Выбрана опция 'Начинать с буквы', но не включен ни один из наборов букв (прописные или ЗАГЛАВНЫЕ). \n\nПожалуйста, включите хотя бы один набор букв."
            )
            return ""

        length = self.ui.password_length_value.get()
        char_pool = ""
        password = []

        # Сборка основного списка (пула) символов
        if self.ui.include_lowercase.get():
            char_pool += const.LOWERCASE_LETTERS
        if self.ui.include_uppercase.get():
            char_pool += const.UPPERCASE_LETTERS
        if self.ui.include_numbers.get():
            char_pool += const.NUMBERS
        if self.ui.include_special_symbols.get():
            char_pool += const.SPECIAL_SYMBOLS

        # Исключение "похожих" символов, если нужно
        if self.ui.include_ambiguous_symbols.get():
            char_pool = "".join(c for c in char_pool if c not in const.AMBIGUOUS_SYMBOLS)

        # Обработка опции "Начинать с буквы"
        letter_pool = ""
        if self.ui.include_lowercase.get():
            letter_pool += const.LOWERCASE_LETTERS
        if self.ui.include_uppercase.get():
            letter_pool += const.UPPERCASE_LETTERS
        if self.ui.include_ambiguous_symbols.get():
            letter_pool = "".join(c for c in letter_pool if c not in const.AMBIGUOUS_SYMBOLS)

        if self.ui.include_letter_start.get() and letter_pool:
            first_char = choice(letter_pool)
            password.append(first_char)
            # Убираем первый символ из пула, если включена уникальность
            if self.ui.include_uniqueness.get():
                char_pool = char_pool.replace(first_char, '', 1)

        remaining_length = length - len(password)

        # Проверка, есть ли из чего генерировать
        if not char_pool:
            messagebox.showwarning(
                "Ошибка", "Не выбрано ни одного набора символов для генерации пароля!")
            return ""

        # Генерация оставшейся части пароля
        try:
            if self.ui.include_uniqueness.get():
                if remaining_length > len(char_pool):
                    messagebox.showwarning(
                        "Ошибка", "Невозможно сгенерировать пароль: длина больше, чем число уникальных символов.")
                    return "".join(password)
                password.extend(sample(char_pool, remaining_length))
            else:
                for _ in range(remaining_length):
                    password.append(choice(char_pool))
        except (ValueError, IndexError):
            messagebox.showwarning(
                "Ошибка", "Не удалось сгенерировать пароль с заданными параметрами.")
            return ""

        return "".join(password)

    def update_password_field(self, text: str):
        """Обновляет текстовое поле для вывода пароля."""
        self.ui.password_field.config(state="normal")
        self.ui.password_field.delete(0, "end")
        self.ui.password_field.insert(0, text)
        self.ui.password_field.config(state="readonly")

    def update_strength_meter(self):
        """
        Оценивает и отображает силу сгенерированного пароля.
        Логика основана на длине и количестве использованных наборов символов.
        """
        # Сброс индикатора
        for i in range(3):
            self.ui.strength_meter[i].config(bg="#9e5826")

        if not self.ui.password_field.get():
            return

        score = 0
        length = self.ui.password_length_value.get()

        # Очки за длину
        if length >= 8: score += 1
        if length >= 12: score += 1
        if length >= 16: score += 1

        # Очки за разнообразие символов
        num_char_sets = sum([
            self.ui.include_lowercase.get(),
            self.ui.include_uppercase.get(),
            self.ui.include_numbers.get(),
            self.ui.include_special_symbols.get()
        ])
        if num_char_sets >= 2: score += 1
        if num_char_sets >= 3: score += 1

        # Определяем цвет по очкам (максимум 5)
        if score <= 2:    # Слабый
            self.ui.strength_meter[0].config(bg="#f80000")
        elif score <= 4:  # Средний
            for i in range(2):
                self.ui.strength_meter[i].config(bg="#fefe22")
        else:             # Сильный
            for i in range(3):
                self.ui.strength_meter[i].config(bg="#32cd32")

    def apply_preset(self):
        """Применяет выбранный пресет, изменяя настройки в UI."""

        # Если этот вызов был инициирован изменением чекбокса, игнорируем его
        if self.is_applying_preset:
            return

        self.is_applying_preset = True
        try:
            preset_display_name = self.ui.preset_display_var.get()
            if not preset_display_name:
                return

            preset_name = const.REVERSE_PRESET_DISPLAY_NAMES[preset_display_name]

            # Если выбран "Свой" - ничего не делаем
            if preset_name == "custom":
                return

            # Для всех остальных пресетов - применяем конфигурацию
            config = const.PRESETS_CONFIG.get(preset_name, {})
            self.ui.include_numbers.set(config.get("numbers", False))
            self.ui.include_lowercase.set(config.get("lowercase", False))
            self.ui.include_uppercase.set(config.get("uppercase", False))
            self.ui.include_special_symbols.set(config.get("special", False))
            self.ui.include_uniqueness.set(config.get("unique", False))
            self.ui.include_ambiguous_symbols.set(config.get("no_ambiguous", False))
            self.ui.include_letter_start.set(config.get("start_with_letter", False))
            self.ui.length_slider.set(config.get("length", 12))

            # После изменения настроек сразу генерируем новый пароль
            self.update_password_and_strength()

        finally:
            self.is_applying_preset = False

    def run(self):
        """Запускает главный цикл приложения."""
        self.root.mainloop()
