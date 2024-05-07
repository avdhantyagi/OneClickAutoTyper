import pyperclip
from pynput.keyboard import Controller
import time
import tkinter as tk
import pyautogui

class DraggableWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Paste Code with Delay")
        self.root.overrideredirect(True)

        self.x = 0
        self.y = 0
        self.is_running = False
        self.remaining_time = 0

        self.paste_button = tk.Button(root, text="Paste", command=self.on_click)
        self.paste_button.pack(pady=5)

        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

        root.update_idletasks()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root_width = root.winfo_width()
        root_height = root.winfo_height()
        self.x = (screen_width - root_width) // 2
        self.y = (screen_height - root_height) // 2
        self.root.geometry('+{}+{}'.format(self.x, self.y))

        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)
        self.root.bind("<B1-Motion>", self.on_motion)

        # Make the window always stay on top
        self.root.wm_attributes("-topmost", True)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def on_motion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry("+{}+{}".format(x, y))

    def on_click(self):
        if not self.is_running:
            self.is_running = True
            self.remaining_time = 5
            self.update_status()
            self.root.after(1000, self.paste_code_with_delay)
        else:
            self.is_running = False
            self.update_status()

    def paste_code_with_delay(self):
        if self.remaining_time <= 0:
            keyboard = Controller()
            javacode = pyperclip.paste()
            javacode = javacode.split('\n')
            for i in javacode:
                keyboard.type("\r")
                keyboard.type(i.strip() + " ")
                pyautogui.write("")

            # Reset status
            self.is_running = False
            self.update_status()
        else:
            self.remaining_time -= 1
            self.update_status()
            self.root.after(1000, self.paste_code_with_delay)

    def update_status(self):
        if self.is_running:
            status = "Started: Remaining {}s".format(self.remaining_time)
        else:
            status = "Stopped"
        self.status_label.config(text=status)

# Create tkinter window
root = tk.Tk()

# Create DraggableWindow instance
app = DraggableWindow(root)

# Run the tkinter main loop
root.mainloop()
