import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont
import os
from fontTools.ttLib import TTFont

class TextGridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Py Bitmap Font Generator")
        ctk.set_appearance_mode("dark")

        self.font_file_path = None
        self.font_name = None  # Название шрифта

        # Параметры по умолчанию
        self.text = "ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮёйцукенгшщзхъфывапролджэячсмитьбюABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,;:?!-_~#\"'&()[]|`\\/@+=*$<>%"
        self.rows = 14
        self.cols = 14
        self.cell_size = 100
        self.font_size = 48
        self.text_color = '#FFFFFF'  # Белый цвет для текста по умолчанию

        # Создание элементов интерфейса
        self.create_widgets()

    def create_widgets(self):
        self.root.geometry("460x400")

        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Поле ввода текста
        self.text_label = ctk.CTkLabel(main_frame, text="Текст:")
        self.text_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.text_entry = ctk.CTkEntry(main_frame, width=200)
        self.text_entry.grid(row=0, column=1, padx=10, pady=5)
        self.text_entry.insert(0, self.text)

        # Поле ввода количества строк
        self.rows_label = ctk.CTkLabel(main_frame, text="Количество строк:")
        self.rows_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.rows_entry = ctk.CTkEntry(main_frame)
        self.rows_entry.grid(row=1, column=1, padx=10, pady=5)
        self.rows_entry.insert(0, str(self.rows))

        # Поле ввода количества столбцов
        self.cols_label = ctk.CTkLabel(main_frame, text="Количество столбцов:")
        self.cols_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.cols_entry = ctk.CTkEntry(main_frame)
        self.cols_entry.grid(row=2, column=1, padx=10, pady=5)
        self.cols_entry.insert(0, str(self.cols))

        # Поле ввода размера клетки
        self.cell_size_label = ctk.CTkLabel(main_frame, text="Размер клетки (пиксели):")
        self.cell_size_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.cell_size_entry = ctk.CTkEntry(main_frame)
        self.cell_size_entry.grid(row=3, column=1, padx=10, pady=5)
        self.cell_size_entry.insert(0, str(self.cell_size))

        # Поле ввода размера шрифта
        self.font_size_label = ctk.CTkLabel(main_frame, text="Размер шрифта:")
        self.font_size_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.font_size_entry = ctk.CTkEntry(main_frame)
        self.font_size_entry.grid(row=4, column=1, padx=10, pady=5)
        self.font_size_entry.insert(0, str(self.font_size))

        # Кнопка выбора файла шрифта
        self.choose_font_button = ctk.CTkButton(main_frame, text="Выбрать файл шрифта", command=self.choose_font_file)
        self.choose_font_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Кнопка изменения цвета текста
        self.text_color_button = ctk.CTkButton(main_frame, text="Выбрать цвет текста", command=self.choose_text_color)
        self.text_color_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Кнопка создания изображения
        self.create_image_button = ctk.CTkButton(main_frame, text="Создать изображение", command=self.create_image)
        self.create_image_button.grid(row=7, column=0, columnspan=2, pady=20)

    def choose_font_file(self):
        self.font_file_path = filedialog.askopenfilename(title="Выберите файл шрифта", filetypes=[("TrueType font", "*.ttf")])
        if self.font_file_path:
            try:
                font = TTFont(self.font_file_path)
                self.font_name = font["name"].getName(1, 3, 1, 1033).string.decode("utf-16-be")
                messagebox.showinfo("Шрифт выбран", f"Выбран шрифт: {self.font_name}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить шрифт из файла: {self.font_file_path}")
                self.font_name = None

    def choose_text_color(self):
        color_code = colorchooser.askcolor(title="Выберите цвет текста")
        if color_code:
            self.text_color = color_code[1]

    def create_image(self):
        # Обновление параметров
        self.text = self.text_entry.get()
        self.rows = int(self.rows_entry.get())
        self.cols = int(self.cols_entry.get())
        self.cell_size = int(self.cell_size_entry.get())
        self.font_size = int(self.font_size_entry.get())

        if not self.font_name:
            messagebox.showerror("Ошибка", "Шрифт не выбран.")
            return

        # Создание имени выходного файла
        output_file = f"{self.font_name}_size{self.font_size}_bitmap.png"

        # Создание изображения с прозрачным фоном
        img_width = self.cols * self.cell_size
        img_height = self.rows * self.cell_size
        image = Image.new('RGBA', (img_width, img_height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)

        # Загрузка шрифта
        try:
            font = ImageFont.truetype(self.font_file_path, self.font_size)
        except IOError:
            messagebox.showerror("Ошибка", f"Не удалось загрузить шрифт из файла: {self.font_file_path}")
            return

        # Заполнение сетки
        for i, char in enumerate(self.text):
            row = i // self.cols
            col = i % self.cols
            if row >= self.rows:
                break
            x = col * self.cell_size + (self.cell_size - self.font_size) // 2
            y = row * self.cell_size + (self.cell_size - self.font_size) // 2
            draw.text((x, y), char, font=font, fill=self.text_color)

        # Сохранение изображения
        image.save(output_file)
        image.show()
        messagebox.showinfo("Успех", f"Изображение успешно создано и сохранено как {output_file}")

def main():
    root = ctk.CTk()
    app = TextGridApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
