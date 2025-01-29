import ctypes
import time
import tkinter as tk
from tkinter import ttk
from tkinter import Scale

# Load Windows API for virtual desktops
try:
    import pygetwindow as gw
    from pywintypes import com_error
    from win32com.client import Dispatch
except ImportError:
    print("Missing dependencies. Install them using: pip install pygetwindow pywin32")
    exit(1)

class VirtualDesktopWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Desktop Widget")
        self.root.geometry("250x100")
        self.root.attributes('-topmost', True)
        self.root.configure(bg='white')
        
        self.dragging = False
        
        # Make window draggable
        self.root.bind("<ButtonPress-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.do_drag)
        
        # Label to display virtual desktop info
        self.label = ttk.Label(root, text="Fetching data...", font=("Arial", 14))
        self.label.pack(expand=True, pady=5)
        
        # Transparency slider
        self.transparency_slider = Scale(root, from_=0.3, to=1.0, resolution=0.1, orient='horizontal', command=self.set_transparency)
        self.transparency_slider.set(1.0)
        self.transparency_slider.pack()
        
        self.update_virtual_desktops()
        self.root.after(1000, self.refresh)

    def start_drag(self, event):
        self.dragging = True
        self.offset_x = event.x
        self.offset_y = event.y

    def do_drag(self, event):
        if self.dragging:
            x = self.root.winfo_x() + event.x - self.offset_x
            y = self.root.winfo_y() + event.y - self.offset_y
            self.root.geometry(f"+{x}+{y}")
    
    def get_virtual_desktop_info(self):
        try:
            objShell = Dispatch("Shell.Application")
            desktops = objShell.Windows()
            return len(desktops), ctypes.windll.user32.GetThreadDesktop(0)
        except com_error:
            return 1, 1

    def update_virtual_desktops(self):
        total, current = self.get_virtual_desktop_info()
        self.label.config(text=f"Desktops: {total}\nActive: {current}")

    def set_transparency(self, value):
        self.root.attributes('-alpha', float(value))
    
    def refresh(self):
        self.update_virtual_desktops()
        self.root.after(1000, self.refresh)

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualDesktopWidget(root)
    root.mainloop()
