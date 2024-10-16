import tkinter as tk  # для работы с интерфейсом
def process_command(event=None):
    # Получаем команду из поля ввода
    command = input_entry.get()

    # Очищаем поле ввода
    input_entry.delete(0, tk.END)

    # Добавляем команду в экран
    text_display.configure(state="normal") # Разрешаем редактирование текстового виджета text_display
    text_display.insert(tk.END, f"$: {command}\n")




    text_display.configure(state="disabled") # Запрещаем редактирование текстового виджета text_display

# Создаем окно
root = tk.Tk()
root.title("Command Interface")

# Создаем экран для отображения текста команд
text_display = tk.Text(root, width=50, height=10, state="disabled")
text_display.pack(pady=10)

# Создаем поле ввода и кнопку
input_frame = tk.Frame(root) # Создаем фрейм для размещения поля ввода и кнопки
input_entry = tk.Entry(input_frame, width=40) # Создаем поле ввода внутри фрейма input_frame
input_entry.pack(side=tk.LEFT, padx=5) # Размещаем поле ввода слева внутри фрейма
input_button = tk.Button(input_frame, text="Enter", command=process_command) #Создаем кнопку "Enter" внутри фрейма input_frame
input_button.pack(side=tk.LEFT, padx=5) # Размещаем кнопку справа внутри фрейма
input_frame.pack(pady=10) # Размещаем фрейм input_frame внутри окна root

# Привязываем обработчик клавиши Enter к методу process_command
input_entry.bind("<Return>", process_command)

# Запускаем главный цикл
root.mainloop()

