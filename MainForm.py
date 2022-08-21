import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
import os
from tkinter import messagebox


class MainForm(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        self.server = ttk.StringVar()
        self.port = ttk.StringVar()
        self.topic = ttk.StringVar()
        self.path = ttk.StringVar()
        self.topic_path = ttk.StringVar()
        self.afterid = ttk.StringVar()
        self.client_mqtt = None

        self.button_connect = None
        self.button_disconnect = None
        self.button_browser = None
        self.button_save = None
        self.entry_server = None
        self.entry_port = None
        self.entry_topic = None
        self.entry_path = None
        self.entry_topic_path = None

        self.create_form_config()
        self.create_form_path()
        self.create_buttons()

    def create_form_config(self):
        label_frame = ttk.Labelframe(self, text='Configurações MQTT')
        label_frame.pack(fill="x", padx=10, pady=10)

        frame = ttk.Frame(label_frame)
        frame.pack(fill="x", padx=20, pady=20)

        label = ttk.Label(frame, text="Servidor")
        label.grid(row=0, column=0, padx=1, sticky=ttk.E, pady=10)

        self.entry_server = ttk.Entry(frame,
                                      textvariable=self.server,
                                      justify="center",
                                      width=30,
                                      )
        self.entry_server.grid(row=0, column=1, padx=2, sticky=ttk.W, pady=10)

        label = ttk.Label(frame, text="Porta")
        label.grid(row=1, column=0, padx=1, sticky=ttk.E, pady=10)

        self.entry_port = ttk.Entry(frame,
                                    textvariable=self.port,
                                    justify="center",
                                    width=10,
                                   )
        self.entry_port.grid(row=1, column=1, padx=2, sticky=ttk.W, pady=10)

        label = ttk.Label(frame, text="Tópico")
        label.grid(row=2, column=0, padx=1, sticky=ttk.E, pady=10)

        self.entry_topic = ttk.Entry(frame, textvariable=self.topic, width=70)
        self.entry_topic.grid(row=2, column=1, padx=2, sticky=ttk.W, pady=10)

    def create_form_path(self):
        label_frame = ttk.Labelframe(self, text='Monitoração Pasta')
        label_frame.pack(fill="x", padx=10, pady=10)

        frame = ttk.Frame(label_frame)
        frame.pack(fill="x", padx=20, pady=20)

        label = ttk.Label(frame, text="Pasta")
        label.grid(row=0, column=0, padx=1, sticky=ttk.E, pady=10)

        self.entry_path = ttk.Entry(frame, textvariable=self.path, width=70, state="disabled")
        self.entry_path.grid(row=0, column=1, padx=2, sticky=ttk.W, pady=10)

        self.button_browser = ttk.Button(frame, text="Browse", bootstyle=(INFO, OUTLINE))
        self.button_browser.grid(row=0, column=2, padx=2, pady=10)

        label = ttk.Label(frame, text="Tópico")
        label.grid(row=1, column=0, padx=1, sticky=ttk.E, pady=10)

        self.entry_topic_path = ttk.Entry(frame, textvariable=self.topic_path, width=70)
        self.entry_topic_path.grid(row=1, column=1, padx=2, sticky=ttk.W, pady=10)

    def create_buttons(self):
        frame = ttk.Frame(self)
        frame.pack(fill="x", padx=10, pady=5)

        self.button_connect = ttk.Button(frame, text="Conectar", bootstyle="success")
        self.button_connect.pack(side=LEFT, padx=5, pady=10)

        self.button_disconnect = ttk.Button(frame, text="Desconectar", bootstyle="danger", state="disabled")
        self.button_disconnect.pack(side=LEFT, padx=5, pady=10)

        self.button_save = ttk.Button(frame, text="Salvar Configuração", bootstyle="default")
        self.button_save.pack(side=RIGHT, pady=10)
