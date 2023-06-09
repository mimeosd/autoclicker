import tkinter as tk
import threading
import pyautogui



class App:
    def __init__(self, root):
        self.root = root
        

        self.start_button = tk.Button(self.root, text="Start Clicking", command=self.start_clicking)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop Clicking", state="disabled", command=self.stop_clicking)
        self.stop_button.pack()

    

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = App(root)
#     root.mainloop()
