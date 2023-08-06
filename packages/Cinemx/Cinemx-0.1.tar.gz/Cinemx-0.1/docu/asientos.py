import numpy as np
import tkinter as tk

def create_seating_plan():
    global n_filas, n_columnas, seats, buttons

    n_filas = int(entry_filas.get())
    n_columnas = int(entry_columnas.get())

    # Eliminar botones y reiniciar matriz de asientos
    for row_buttons in buttons:
        for button in row_buttons:
            button.destroy()
    buttons.clear()
    seats = np.zeros((n_filas, n_columnas))

    # Crear nuevos botones
    for i in range(n_filas):
        row_buttons = []
        for j in range(n_columnas):
            button = tk.Button(frame_seats, width=4, height=2, bg='green',
                              command=lambda r=i, c=j: seat_clicked(r, c))
            button.grid(row=i, column=j, padx=2, pady=2)
            row_buttons.append(button)
        buttons.append(row_buttons)

    count_label.config(text=f"Asientos ocupados: 0")

def seat_clicked(row, col):
    if seats[row][col] == 0:
        seats[row][col] = 1
        buttons[row][col].config(bg='red')
    else:
        seats[row][col] = 0
        buttons[row][col].config(bg='green')
    count_label.config(text=f"Asientos ocupados: {np.sum(seats)}")

# Crear ventana
window = tk.Tk()
window.title("Cine")

# Crear marco para la configuración de filas y columnas
frame_config = tk.Frame(window)
frame_config.pack()

# Etiqueta y campo de entrada para la cantidad de filas
label_filas = tk.Label(frame_config, text="Filas:")
label_filas.grid(row=0, column=0)
entry_filas = tk.Entry(frame_config)
entry_filas.grid(row=0, column=1)

# Etiqueta y campo de entrada para la cantidad de columnas
label_columnas = tk.Label(frame_config, text="Columnas:")
label_columnas.grid(row=1, column=0)
entry_columnas = tk.Entry(frame_config)
entry_columnas.grid(row=1, column=1)

# Botón para crear el plan de asientos
button_crear = tk.Button(frame_config, text="Crear", command=create_seating_plan)
button_crear.grid(row=2, column=0, columnspan=2)

# Marco para la visualización de asientos
frame_seats = tk.Frame(window)
frame_seats.pack()

# Crear etiqueta para contar asientos ocupados
count_label = tk.Label(window, text="Asientos ocupados: 0")
count_label.pack()

# Variables para la matriz de asientos
n_filas = 0
n_columnas = 0
seats = np.zeros((n_filas, n_columnas))
buttons = []

window.mainloop()
