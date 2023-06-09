import tkinter as tk
from tkinter import messagebox, PhotoImage
from pystray import Icon, MenuItem
import pyautogui
from PIL import Image
from functionality import PopupWindow
import threading
import keyboard
import json
import random



class AutoClickerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app
        self.running = False

    def run(self):
        pyautogui.FAILSAFE = True
        self.running = True
        max_clicks = int(self.app.automation_count_value.get())
        click_count = 0

        self.interval = float(self.app.minutes_value.get()) * 60 + float(self.app.seconds_value.get()) + float(self.app.miliseconds_value.get()) / 1000


        # checkboxes = {
        #     self.app.ctrl_var.get(): 'ctrl',
        #     self.app.alt_var.get(): 'alt',
        #     self.app.shift_var.get(): 'shift'
        #     }
        
        checkboxes = {
            'ctrl': self.app.ctrl_var.get(),
            'alt': self.app.alt_var.get() ,
            'shift': self.app.shift_var.get()
            }
        
        keys_to_press = [checkbox for checkbox, key in checkboxes.items() if key]

        while self.running and (max_clicks == 0 or click_count < max_clicks):
            
            if keys_to_press:
                print("Keys to press:", keys_to_press)

                for key in keys_to_press:
                    keyboard.press(key)

                pyautogui.click(interval=self.interval)

                for key in keys_to_press:
                    keyboard.release(key)
                    click_count += 1
                    print(f"Clicked {click_count}")
                    self.app.start_clicking_btn.config(state="disabled")
                    
                    if keyboard.is_pressed(self.app.info_shortcut_value.get()):
                        self.running = False
                        self.app.start_clicking_btn.config(state="normal")
                        self.app.stop_clicking_btn.config(state="disabled")

                    elif keyboard.is_pressed(self.app.info_shortcut_value.get()) and self.running == False:
                        self.running = True

                    
            else:
                pyautogui.click(interval=self.interval)
                click_count += 1
                print(f"Clicked {click_count}")
                self.app.start_clicking_btn.config(state="disabled")
                if keyboard.is_pressed(self.app.info_shortcut_value.get()):
                        self.running = False
                        self.app.start_clicking_btn.config(state="normal")
                        self.app.stop_clicking_btn.config(state="disabled")

                elif keyboard.is_pressed(self.app.info_shortcut_value.get()) and self.running == False:
                    self.running = True


    def stop(self):
        self.running = False

class App:
    def __init__(self, root) -> None:
        self.root = root
        self.auto_clicker_thread = AutoClickerThread(self.root)

        self.root.resizable(False, False)
        self.root.title('AutoClicker')
        self.icon = PhotoImage(file="assets/hacker.png")
        self.root.iconphoto(True, self.icon)
        self.root.config(padx=5, pady=5)

        self.running_status = False

        

        # Buttons for sharing
        self.button_sharing_holder = tk.LabelFrame(self.root, highlightthickness=0, borderwidth=0)
        self.button_sharing_holder.grid(row=0, column=0, sticky="ew")

        self.menu_button = tk.Button(self.button_sharing_holder, text="Menu")
        self.menu_button.grid(row=0, column=0)
        
        self.tutorial_button = tk.Button(self.button_sharing_holder, text="Tutorials")
        self.tutorial_button.grid(row=0, column=1)
        
        self.twitter_button = tk.Button(self.button_sharing_holder, text="Twitter")
        self.twitter_button.grid(row=0, column=2)
        
        self.facebook_button = tk.Button(self.button_sharing_holder, text="Facebook")
        self.facebook_button.grid(row=0, column=3)
        
        self.share_button = tk.Button(self.button_sharing_holder, text="Share")
        self.share_button.grid(row=0, column=4)


        # Top container starts here
        self.top_container = tk.LabelFrame(self.root, text="Keyboard Shortcut Key to Start / Stop Clicking", padx=5, pady=5)
        self.top_container.grid(row=1, column=0, columnspan=10, sticky="ew")

        self.info_shortcut = tk.Label(self.top_container, text="Keyboard Key to \nStart/ Stop Clicking :", justify="left")
        self.info_shortcut.grid(row=0, column=0)

        self.info_shortcut_value = tk.Entry(self.top_container)
        self.info_shortcut_value.grid(row=0, column=1)

        self.save_keyboard_button = tk.Button(self.top_container, text="Save Keyboard Key", width=15, command=self.save_keyboard_key)
        self.save_keyboard_button.grid(row=0, column=2)
        
        self.remove_keyboard_button = tk.Button(self.top_container, text="Remove Key", width=15, command=self.remove_keyboard_key)
        self.remove_keyboard_button.grid(row=0, column=3)

        # Holder for rightmost option
        self.top_container_rightmost = tk.LabelFrame(self.top_container, borderwidth=0, highlightthickness=0)
        self.top_container_rightmost.grid(row=0, column=4)


        self.check_box_rightmost_var = tk.BooleanVar()
        
        self.check_box_rightmost = tk.Checkbutton(self.top_container_rightmost, text="Click only if Mouse \n Not moving", justify="left", variable=self.check_box_rightmost_var, command=self.toggle_entry_state)
        self.check_box_rightmost.grid(row=0, columnspan=3)

        self.right_most_label = tk.Label(self.top_container_rightmost, text="For: ")
        self.right_most_label.grid(row=1, column=0)

        self.right_most_label_value = tk.Entry(self.top_container_rightmost, width=7)
        self.right_most_label_value.insert(0, 5)
        self.right_most_label_value.grid(row=1, column=1)

        self.right_most_label_1 = tk.Label(self.top_container_rightmost, text="Seconds")
        self.right_most_label_1.grid(row=1, column=2)

        # Rightmost holder ends here


        # Middle holder starts here

        self.middle_container = tk.LabelFrame(self.root, text="Auto Clicking Time Delay, Location, Distance, Number of Clicks etc")
        self.middle_container.grid(row=2, column=0, columnspan=10, sticky="ew")


        self.middle_holder_0 = tk.LabelFrame(self.middle_container, highlightthickness=0, borderwidth=0)
        self.middle_holder_0.grid(row=0, column=0, padx=5)

        self.random_delay_button = tk.Button(self.middle_holder_0, text="Extra Random Delay", command=self.extra_random_delay)
        self.random_delay_button.grid(row=0, column=0, columnspan=3)

        self.ctrl_var = tk.BooleanVar()
        self.alt_var = tk.BooleanVar()
        self.shift_var = tk.BooleanVar()

        self.ctrl_box = tk.Checkbutton(self.middle_holder_0, text="Ctrl", variable=self.ctrl_var)
        self.ctrl_box.grid(row=1, column=0)
        
        self.alt_box = tk.Checkbutton(self.middle_holder_0, text="Alt", variable=self.alt_var)
        self.alt_box.grid(row=1, column=1)
        
        self.shift_box = tk.Checkbutton(self.middle_holder_0, text="Shift", variable=self.shift_var)
        self.shift_box.grid(row=1, column=2)


        self.middle_holder_1 = tk.LabelFrame(self.middle_container, text="Minutes")
        self.middle_holder_1.grid(row=0, column=1, padx=5)

        self.minutes_value = tk.Entry(self.middle_holder_1, width=7)
        self.minutes_value.insert(0, "0")
        self.minutes_value.pack(padx=10, pady=10)
        
        
        self.middle_holder_2 = tk.LabelFrame(self.middle_container, text="Seconds")
        self.middle_holder_2.grid(row=0, column=2, padx=5)

        self.seconds_value = tk.Entry(self.middle_holder_2, width=7)
        self.seconds_value.insert(0, "0")
        self.seconds_value.pack(padx=10, pady=10)
        
        
        self.middle_holder_3 = tk.LabelFrame(self.middle_container, text="Miliseconds")
        self.middle_holder_3.grid(row=0, column=3, padx=5)

        self.miliseconds_value = tk.Entry(self.middle_holder_3, width=7)
        self.miliseconds_value.insert(0, "0")
        self.miliseconds_value.pack(padx=10, pady=10)
        
        self.middle_holder_4 = tk.LabelFrame(self.middle_container, text="Number of Clicks to Automate")
        self.middle_holder_4.grid(row=0, column=4, columnspan=2, padx=5)




        self.automation_count_value = tk.Entry(self.middle_holder_4, width=7)
        self.automation_count_value.insert(0, "0")
        self.automation_count_value.grid(row=0, column=0, padx=10, pady=10)

        self.automation_info = tk.Label(self.middle_holder_4, text="0 => Infinite\nuntill Stopped")
        self.automation_info.grid(row=0, column=1)

        self.middle_holder_5 = tk.LabelFrame(self.middle_container, borderwidth=0, highlightthickness=0)
        self.middle_holder_5.grid(row=0, column=6)

        self.l_but = tk.Button(self.middle_holder_5, text="L")
        self.l_but.grid(row=0, column=0)
        
        self.d_but = tk.Button(self.middle_holder_5, text="D")
        self.d_but.grid(row=1, column=0)

        # Middle holder ends here

        # Pre-Bottom holder starts here
        self.pre_bottom_holder = tk.LabelFrame(self.root, borderwidth=0, highlightthickness=0)
        self.pre_bottom_holder.grid(row=3, column=0)

        self.mouse_info_label = tk.Label(self.pre_bottom_holder, text="Mouse Shortcut to Start Clicking =>")
        self.mouse_info_label.grid(row=0, column=0, columnspan=2)

        # Choosing mouse button to automate
        self.mouse_btn_left = tk.Checkbutton(self.pre_bottom_holder, text="Left")
        self.mouse_btn_left.grid(row=0, column=2)
        
        self.mouse_btn_middle = tk.Checkbutton(self.pre_bottom_holder, text="Middle")
        self.mouse_btn_middle.grid(row=0, column=3)
        
        self.mouse_btn_right = tk.Checkbutton(self.pre_bottom_holder, text="Right")
        self.mouse_btn_right.grid(row=0, column=4)
        
        self.mouse_btn_4th = tk.Checkbutton(self.pre_bottom_holder, text="4th Button")
        self.mouse_btn_4th.grid(row=0, column=5)
        
        self.mouse_btn_5th = tk.Checkbutton(self.pre_bottom_holder, text="5th Button")
        self.mouse_btn_5th.grid(row=0, column=6)

        self.r_button = tk.Button(self.pre_bottom_holder, text="R")
        self.r_button.grid(row=0, column=7)

        # Pre bottom holder ends here

        # Bottom holder starts here
        self.bottom_holder = tk.LabelFrame(self.root, borderwidth=0, highlightthickness=0)
        self.bottom_holder.grid(row=4, column=0)

        self.start_clicking_btn = tk.Button(self.bottom_holder, text="Start Clicking", height=3, command=self.start_clicking)
        self.start_clicking_btn.grid(column=0, row=0, padx=5)
        
        self.stop_clicking_btn = tk.Button(self.bottom_holder, text="Stop Clicking", state="disabled", height=3, command=self.stop_clicking)
        self.stop_clicking_btn.grid(column=1, row=0, padx=5)


        self.action_sub_holder = tk.LabelFrame(self.bottom_holder, text="Select Action", pady=4, padx=5)
        self.action_sub_holder.grid(row=0, column=2)


        # TODO See why option menu bugs out (slows down)
        options = ["Left Click", "Middle Click", "Right Click", "4th Button", "5th Button"]
        clicked = tk.StringVar()
        clicked.set(None)
        self.action_chooser = tk.OptionMenu(self.action_sub_holder, clicked, *options)
        self.action_chooser.pack()

        self.status_subholder = tk.LabelFrame(self.bottom_holder, borderwidth=0, highlightthickness=0)
        self.status_subholder.grid(row=0, column=3)

        self.cursor_change_option = tk.Checkbutton(self.status_subholder, text="Cursor Change")
        self.cursor_change_option.grid(row=0, column=0)

        self.status = tk.Label(self.status_subholder, text="Current status")
        self.status.grid(row=1, column=0)

        
        self.hide_to_tray_btn = tk.Button(self.bottom_holder, text="Hide to System Tray", width=15, height=2, command=self.minimize_to_tray)
        self.hide_to_tray_btn.grid(row=0, column=4)

        self.mouse_coordinates = tk.LabelFrame(self.bottom_holder, text="Mouse Position", padx=5)
        self.mouse_coordinates.grid(row=0, column=5, padx=5)

        self.mouse_x_label = tk.Label(self.mouse_coordinates, text="X: ")
        self.mouse_x_label.grid(row=0, column=0)
        
        self.mouse_x_label_value = tk.Label(self.mouse_coordinates, text="value")
        self.mouse_x_label_value.grid(row=0, column=1)
        
        self.mouse_y_label = tk.Label(self.mouse_coordinates, text="Y: ")
        self.mouse_y_label.grid(row=1, column=0)
        
        self.mouse_y_label_value = tk.Label(self.mouse_coordinates, text="val y ")
        self.mouse_y_label_value.grid(row=1, column=1)

        # Handles loading data from keyboard
        self.load_keyboard_key()
        
        if self.info_shortcut_value.get() != None:
            keyboard.add_hotkey(self.info_shortcut_value.get(), self.start_clicking)



    # Logic starts here

    def show_warning(self):
        """ Handles not implemented warning"""
        popup = PopupWindow(self.root, "Error", "Not implemented.")
        self.root.wait_window(popup)


    def toggle_entry_state(self) -> None:
        """ Toggles right most state of entry widget (top container)"""
        # print(self.ctrl_var.get())
        # print(self.alt_var.get())
        # print(self.shift_var.get())
        if self.check_box_rightmost_var.get():
            self.right_most_label_value.config(state="normal")
        else:
            self.right_most_label_value.config(state="disabled")

    def extra_random_delay(self):
        self.minutes_value.delete(0, tk.END)
        self.minutes_value.insert(0, str(random.randint(0, 100)))
        
        self.seconds_value.delete(0, tk.END)
        self.seconds_value.insert(0, str(random.randint(0, 100)))
        
        self.miliseconds_value.delete(0, tk.END)
        self.miliseconds_value.insert(0, str(random.randint(0, 1000)))

    # Handles minimization options
    def quit_window(self, icon, item):
        icon.stop()
        self.root.destroy()

    def minimize_to_tray(self, icon=None, item=None):
        self.root.withdraw()
        image = Image.open("assets/hacker.ico")
        if item is None:
            menu = [MenuItem("Quit", self.quit_window), MenuItem("Show", self.restore_from_tray)]
        else:
            menu = item

        if icon is None:
            icon = Icon("name", image, "AutoClicker", menu)
        else:
            icon.set_image(image)
            icon.set_menu(menu)
        icon.run()

    def restore_from_tray(self, icon, item):
        icon.stop()
        self.root.after(0, self.root.deiconify)

    def update_mouse_coordinates(self):
        while True:
            x, y = pyautogui.position()
            self.mouse_x_label_value.config(text=str(x))
            self.mouse_y_label_value.config(text=str(y))

    
    
    # Bug occurs when starting script manually - button goes into disabled mode.

    def start_clicking(self, event=None):
        if not self.auto_clicker_thread.is_alive():
            shortcut_key = self.info_shortcut_value.get()
            if shortcut_key.lower() != "none":
                self.root.bind(shortcut_key, self.start_clicking)  
            self.start_clicking_btn.config(state="disabled")
            self.stop_clicking_btn.config(state="normal")
            self.auto_clicker_thread = AutoClickerThread(self)
            self.auto_clicker_thread.start()
            self.status['text'] = 'Running'
        
            

    def stop_clicking(self):
        if self.auto_clicker_thread.is_alive():
            self.auto_clicker_thread.stop()
            self.start_clicking_btn.config(state="normal")
            self.stop_clicking_btn.config(state="disabled")
            self.status['text'] = 'Idle'


    def on_hotkey_pressed(self):
        self.start_clicking(None)

    def save_keyboard_key(self):
        key = self.info_shortcut_value.get()
        data = {"keyboard_key": key}
        with open("config.json", "w") as file:
            json.dump(data, file)

    def remove_keyboard_key(self):
        self.info_shortcut_value.delete(0, tk.END)
        data = {"keyboard_key": ""}
        with open("config.json", "w") as file:
            json.dump(data, file)


    # Retrieving the key value
    def load_keyboard_key(self):
        try:
            with open("config.json", "r") as file:
                data = json.load(file)
            key = data.get("keyboard_key")
            if key:
                self.info_shortcut_value.delete(0, tk.END)
                self.info_shortcut_value.insert(0, key)
        except FileNotFoundError:
            self.info_shortcut_value.insert(0, "None")



    def run(self) -> None:
        import threading
        mouse_coordinates_thread = threading.Thread(target=self.update_mouse_coordinates)
        mouse_coordinates_thread.daemon = True
        mouse_coordinates_thread.start()

        self.root.mainloop()

