import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

# ================= GLOBAL ================= #
cover_path = ""
secret_path = ""

# ================= FUNCTIONS ================= #

def upload_cover():
    global cover_path, cover_img
    cover_path = filedialog.askopenfilename()
    if cover_path:
        img = Image.open(cover_path)
        img.thumbnail((300, 300))  # better scaling
        cover_img = ImageTk.PhotoImage(img)
        cover_label.config(image=cover_img)
        cover_label.image = cover_img

def upload_secret():
    global secret_path, secret_img
    secret_path = filedialog.askopenfilename()
    if secret_path:
        img = Image.open(secret_path)
        img.thumbnail((300, 300))
        secret_img = ImageTk.PhotoImage(img)
        secret_label.config(image=secret_img)
        secret_label.image = secret_img

def encode():
    global output_img
    if not cover_path or not secret_path:
        messagebox.showerror("Error", "Upload both images")
        return

    cover = Image.open(cover_path).convert('RGB')
    secret = Image.open(secret_path).convert('RGB')
    secret = secret.resize(cover.size)

    ca = np.array(cover, dtype=np.uint8)
    sa = np.array(secret, dtype=np.uint8)

    stego = (ca & 0xF0) | (sa >> 4)
    Image.fromarray(stego).save("stego.png")

    img = Image.open("stego.png")
    img.thumbnail((300, 300))
    output_img = ImageTk.PhotoImage(img)
    output_label.config(image=output_img)
    output_label.image = output_img

def decode():
    global output_img
    try:
        stego = Image.open("stego.png").convert('RGB')
    except:
        messagebox.showerror("Error", "No encoded image")
        return

    sa = np.array(stego, dtype=np.uint8)
    revealed = (sa & 0x0F) << 4

    Image.fromarray(revealed).save("revealed.png")

    img = Image.open("revealed.png")
    img.thumbnail((300, 300))
    output_img = ImageTk.PhotoImage(img)
    output_label.config(image=output_img)
    output_label.image = output_img

# ================= GUI ================= #

root = tk.Tk()
root.title("Steganography Tool")
root.geometry("900x600")

# Make window responsive
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

main_frame = tk.Frame(root, bg="#1e272e")
main_frame.grid(row=0, column=0, sticky="nsew")

main_frame.rowconfigure(1, weight=1)
main_frame.columnconfigure((0,1,2), weight=1)

# Title
title = tk.Label(main_frame, text="Image Steganography",
                 font=("Arial", 20, "bold"),
                 bg="#1e272e", fg="white")
title.grid(row=0, column=0, columnspan=3, pady=10)

# Image Labels (NO WHITE BACKGROUND)
cover_label = tk.Label(main_frame, text="Cover Image",
                       bg="#2f3640", fg="white")
cover_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

secret_label = tk.Label(main_frame, text="Secret Image",
                        bg="#2f3640", fg="white")
secret_label.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

output_label = tk.Label(main_frame, text="Output",
                        bg="#2f3640", fg="white")
output_label.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

# Buttons Frame
btn_frame = tk.Frame(main_frame, bg="#1e272e")
btn_frame.grid(row=2, column=0, columnspan=3, pady=20)

tk.Button(btn_frame, text="Upload Cover", command=upload_cover,
          width=20, bg="#3498db", fg="white").grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="Upload Secret", command=upload_secret,
          width=20, bg="#9b59b6", fg="white").grid(row=0, column=1, padx=10)

tk.Button(btn_frame, text="Encode", command=encode,
          width=20, bg="#27ae60", fg="white").grid(row=1, column=0, pady=10)

tk.Button(btn_frame, text="Decode", command=decode,
          width=20, bg="#e67e22", fg="white").grid(row=1, column=1, pady=10)

root.mainloop()