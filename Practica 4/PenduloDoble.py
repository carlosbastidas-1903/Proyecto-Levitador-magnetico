import qrcode

# 1. Define tus enlaces
# Reemplaza cada URL con el enlace de "Compartir" de Google Drive correspondiente a cada GIF.
# (He dejado el enlace que me diste como ejemplo en el general).
enlaces_gifs = {
    "qr_general.png": "https://drive.google.com/file/d/1wi7nl5aFo_i74CaCZ5YGRzGMWjZZx6rA/view?usp=sharing",
    "qr_lineal.png":  "https://drive.google.com/file/d/1uAHL9U7DySXHOKQJesIhkuVZufR4Llj2/view?usp=sharing",
    "qr_energia.png": "https://drive.google.com/file/d/1lJUkqEkDgbp8-Nvai6f3Y-FLSorVVjGH/view?usp=sharing",
    "qr_caos.png":    "https://drive.google.com/file/d/1ykDor7rkXfBlULoJzh4tS0Qi0VYrGn5I/view?usp=sharing"
}

# 2. Configurar el color institucional de tu póster (Azul UTP: RGB 46, 49, 146)
# Si los prefieres negros clásicos, cambia fill_color a "black" más abajo.
color_utp = (46, 49, 146)

print("Generando códigos QR para el póster...")

# 3. Bucle para generar y guardar cada QR
for nombre_archivo, url in enlaces_gifs.items():
    # Configurar el diseño del QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H, # Alta corrección (ideal para escanear en pantallas/papel)
        box_size=10,
        border=2, # Borde reducido para aprovechar el espacio en el póster
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Generar la imagen aplicando el color
    img_qr = qr.make_image(fill_color=color_utp, back_color="white")
    
    # Guardar en la carpeta actual
    img_qr.save(nombre_archivo)
    print(f" ✔️ Generado: {nombre_archivo}")

print("\n¡Listo! Mueve estas 4 imágenes a la misma carpeta donde tienes tu archivo .tex y compila tu póster.")