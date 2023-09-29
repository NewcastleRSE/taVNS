import tkinter as tk
from tkinter import ttk


class ConfigTab(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__()
        label = tk.Label(self, text="Some label")
        label.pack(padx=10, pady=10)