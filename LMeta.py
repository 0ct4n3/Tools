import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ExifTags
import os

def seleccionar_imagen():
    ruta = filedialog.askopenfilename(
        filetypes=[
            ("Imágenes", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff;*.webp"),
            ("Todos los archivos", "*.*")
        ]
    )
    if not ruta:
        return

    extension = os.path.splitext(ruta)[1].lower()
    formatos_conocidos = [".jpg", ".jpeg", ".tiff"]  # formatos que normalmente tienen EXIF

    try:
        imagen = Image.open(ruta)
        exif_data = imagen._getexif()

        resultado.delete("1.0", tk.END)
        resultado.insert(tk.END, f"🖼️ Imagen: {os.path.basename(ruta)}\n\n")

        if exif_data:
            resultado.insert(tk.END, "📂 Metadatos encontrados:\n\n")
            for tag_id, valor in exif_data.items():
                etiqueta = ExifTags.TAGS.get(tag_id, tag_id)
                resultado.insert(tk.END, f"{etiqueta:25}: {valor}\n")
        else:
            if extension in formatos_conocidos:
                resultado.insert(tk.END, "❌ No se encontraron metadatos EXIF.\n")
            else:
                resultado.insert(tk.END, "⚠️ Este tipo de imagen normalmente no contiene metadatos EXIF.\n")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo analizar la imagen: {e}")

# Crear ventana
ventana = tk.Tk()
ventana.title("Visor de Metadatos de Imágenes")
ventana.configure(bg="#121212")
ventana.geometry("700x500")

# Botón para seleccionar imagen
boton = tk.Button(ventana, text="📁 Seleccionar Imagen", command=seleccionar_imagen, 
                  bg="#EC008C", fg="white", font=("Consolas", 12, "bold"))
boton.pack(pady=10)

# Área de texto para mostrar resultados
resultado = tk.Text(ventana, bg="#1e1e1e", fg="#00FF00", font=("Consolas", 10), wrap=tk.WORD)
resultado.pack(expand=True, fill="both", padx=10, pady=10)

ventana.mainloop()
