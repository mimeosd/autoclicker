import pyautogui
import tkinter as tk
import keyboard


def start_proc():
    global run_state
    run_state = True
    pyautogui.FAILSAFE = True
    run_state = True
    try:
        target = int(ammount_to_click.get())
        target_interval = float(interval_label_value.get())
    except ValueError:
        pass
    current = 1
    while run_state:
        if keyboard.is_pressed('q'):
            run_state = False
            break
        pyautogui.click(clicks=2, interval=0.01)
        #print('Clicked')
        try:
            if current < target:
                current += 1
            elif current > target:
                pass
            else:
                break
            
        except UnboundLocalError:
            pass

        

pyautogui.FAILSAFE = True

run_state = False


MAIN_FONT = ('Roboto', 12)

root = tk.Tk()
root.resizable(False, False)
root.title('AutoClicker')


# Main frame holder
buttons_frame = tk.LabelFrame(root, text='Setting up...', font=MAIN_FONT)
buttons_frame.grid(row=0, column=0)


ammount_to_click_label = tk.Label(buttons_frame, text='Set ammount of clicks')
ammount_to_click_label.grid(row=0, column=0, padx=3, pady=5)

ammount_to_click = tk.Entry(buttons_frame, font=MAIN_FONT, width=5)
ammount_to_click.grid(row=0, column=1, padx=3, pady=5)

# Interval
interval_label = tk.Label(buttons_frame, text='Set interval between clicks')
interval_label.grid(row=1, column=0, padx=3, pady=5)

interval_label_value = tk.Entry(buttons_frame, font=MAIN_FONT, width=5)
interval_label_value.grid(row=1, column=1, padx=3, pady=5)

# Default setting of start procedure
keyboard.add_hotkey('w', start_proc)

root.mainloop()
