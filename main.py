from app.logic import PasswordGeneratorApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    app.run()
