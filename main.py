import json
import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog

# Load configuration from JSON
def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Config file '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("Error", f"Config file '{file_path}' contains invalid JSON.")
        return None

# Launch application
def launch_application(app):
    try:
        app_path = app['path']
        arguments = app['arguments']
        subprocess.Popen([app_path] + arguments.split(), shell=True)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Application path '{app['path']}' not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch application: {e}")

# Create frames for categories and populate them
def create_category_frames(root, config):
    global app_buttons  # Store buttons for filtering
    app_buttons = []
    
    for category in config['categories']:
        # Frame for each category
        category_frame = tk.Frame(root, bg="lightgray", bd=2, relief=tk.SOLID)
        category_frame.pack(fill=tk.X, padx=10, pady=5)

        # Category label
        category_label = tk.Label(category_frame, text=category['name'], bg="#a0c4ff", fg="white", font=("Arial", 12, "bold"))
        category_label.pack(anchor="w", padx=5, pady=5)

        # Buttons for applications in the category
        for app in category['applications']:
            app_button = tk.Button(
                category_frame,
                text=app['name'],
                command=lambda app=app: launch_application(app),
                bg="#ffafcc",
                fg="black",
                activebackground="#ffb6c1",
                activeforeground="white",
                font=("Arial", 10)
            )
            app_button.pack(fill=tk.X, padx=10, pady=2)

            # Store the button for filtering
            app_buttons.append((app_button, app['name'].lower()))

# Filter applications based on search input
def filter_apps(event=None):
    query = search_entry.get().lower()
    for button, app_name in app_buttons:
        if query in app_name:
            button.pack(fill=tk.X, padx=10, pady=2)  # Show matching app
        else:
            button.pack_forget()  # Hide non-matching app

# Browse for JSON config file
def browse_config(root):
    file_path = filedialog.askopenfilename(
        title="Select Config File",
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
    )
    if file_path:
        config = load_config(file_path)
        if config:
            # Clear existing content in the window
            for widget in root.winfo_children():
                if not isinstance(widget, tk.Menu):  # Preserve menu
                    widget.destroy()
            create_category_frames(root, config)

# Main GUI
def create_gui():
    global search_entry
    root = tk.Tk()
    root.title("Application Launcher")

    # Set initial size and position
    root.geometry("200x600+0+0")  # Docked to the left side
    root.configure(bg="#fefae0")

    # Search Bar
    search_entry = tk.Entry(root, bg="white", fg="black", font=("Arial", 12))
    search_entry.pack(fill=tk.X, padx=10, pady=5)
    search_entry.bind("<KeyRelease>", filter_apps)  # Update results as user types

    # Add a Menu Bar
    menu_bar = tk.Menu(root)

    # Add "File" menu
    file_menu = tk.Menu(menu_bar, tearoff=False, bg="#bde0fe", fg="black", activebackground="#90e0ef", activeforeground="black")
    file_menu.add_command(label="Browse Config", command=lambda: browse_config(root))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    menu_bar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menu_bar)

    # Load default config on start
    default_config_path = "config.json"
    if os.path.exists(default_config_path):
        config = load_config(default_config_path)
        if config:
            create_category_frames(root, config)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
