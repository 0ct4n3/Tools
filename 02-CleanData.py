import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

def limpiar_metadatos_imagen(ruta_entrada, ruta_salida):
    try:
        with Image.open(ruta_entrada) as img:
            datos_puros = Image.new(img.mode, img.size)
            datos_puros.putdata(list(img.getdata()))

            formato_original = img.format if img.format else 'PNG'
            datos_puros.save(ruta_salida, format=formato_original)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def seleccionar_imagen():
    ruta = filedialog.askopenfilename(
        title="Selecciona una imagen",
        filetypes=[
            ("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"),
            ("Todos los archivos", "*.*")
        ])
    if ruta:
        entrada_var.set(ruta)
        # Sugerir nombre de salida automático
        nombre_archivo = os.path.basename(ruta)
        nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
        ext = os.path.splitext(nombre_archivo)[1]
        salida_sugerida = os.path.join(os.path.dirname(ruta), f"{nombre_sin_ext}_limpia{ext}")
        salida_var.set(salida_sugerida)

def guardar_imagen():
    ruta = filedialog.asksaveasfilename(
        title="Guardar imagen limpia como",
        defaultextension=".png",
        filetypes=[
            ("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"),
            ("Todos los archivos", "*.*")
        ])
    if ruta:
        salida_var.set(ruta)

def procesar():
    entrada = entrada_var.get()
    salida = salida_var.get()
    if not entrada or not salida:
        messagebox.showwarning("Campos vacíos", "Debes seleccionar una imagen y definir el archivo de salida.")
        return

    if limpiar_metadatos_imagen(entrada, salida):
        messagebox.showinfo("Éxito", f"Los metadatos han sido eliminados.\nGuardado en:\n{salida}")
    else:
        messagebox.showerror("Error", "No se pudo limpiar la imagen.")

# Interfaz Gráfica
ventana = tk.Tk()
ventana.title("Limpiar metadatos de imágenes")
ventana.geometry("500x220")
ventana.resizable(False, False)

entrada_var = tk.StringVar()
salida_var = tk.StringVar()

tk.Label(ventana, text="Imagen original:").pack(pady=5)
tk.Entry(ventana, textvariable=entrada_var, width=60).pack()
tk.Button(ventana, text="Seleccionar imagen", command=seleccionar_imagen).pack(pady=5)

tk.Label(ventana, text="Guardar imagen limpia como:").pack(pady=5)
tk.Entry(ventana, textvariable=salida_var, width=60).pack()
tk.Button(ventana, text="Seleccionar destino", command=guardar_imagen).pack(pady=5)

tk.Button(ventana, text=" Limpiar Metadatos", command=procesar, bg="#EC008C", fg="white").pack(pady=10)

ventana.mainloop()
