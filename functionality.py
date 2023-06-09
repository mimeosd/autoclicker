import tkinter as tk

class PopupWindow(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x100")
        self.resizable(False, False)
        
        label = tk.Label(self, text=message)
        label.pack(pady=20)
        
        ok_button = tk.Button(self, text="OK", width=10, command=self.destroy)
        ok_button.pack(pady=10)