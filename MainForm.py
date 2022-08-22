import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from ClientMqtt import ClientMqtt
from MyPsutil import MyPsutil
from Config import Config
import json


class MainForm(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        self.server = ttk.StringVar()
        self.port = ttk.StringVar()
        self.topic = ttk.StringVar()
        self.process = ttk.StringVar()
        self.topic_process = ttk.StringVar()
        self.afterid = ttk.StringVar()
        self.client_mqtt = None

        self.button_connect = None
        self.button_disconnect = None
        self.button_browser = None
        self.button_save = None
        self.entry_server = None
        self.entry_port = None
        self.entry_topic = None
        self.combobox_process = None
        self.entry_topic_process = None

        self.process_values = None

        self.init_process_combobox()

        self.create_form_config()
        self.create_form_path()
        self.create_buttons()

        self.read_config()

    def init_process_combobox(self):
        self.process_values = MyPsutil.show_activate_processess()

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
                                    width=10)
        self.entry_port.grid(row=1, column=1, padx=2, sticky=ttk.W, pady=10)

        label = ttk.Label(frame, text="Tópico")
        label.grid(row=2, column=0, padx=1, sticky=ttk.E, pady=10)

        self.entry_topic = ttk.Entry(frame, textvariable=self.topic, width=70)
        self.entry_topic.grid(row=2, column=1, padx=2, sticky=ttk.W, pady=10)

    def create_form_path(self):
        label_frame = ttk.Labelframe(self, text='Monitoração Processo')
        label_frame.pack(fill="x", padx=10, pady=10)

        frame = ttk.Frame(label_frame)
        frame.pack(fill="x", padx=20, pady=20)

        label = ttk.Label(frame, text="Processo")
        label.grid(row=0, column=0, padx=1, sticky=ttk.E, pady=10)

        self.combobox_process = ttk.Combobox(frame, textvariable=self.process, width=50, values=self.process_values)
        self.combobox_process.grid(row=0, column=1, padx=2, sticky=ttk.W, pady=10)

        label = ttk.Label(frame, text="Tópico")
        label.grid(row=1, column=0, padx=1, sticky=ttk.E, pady=10)

        self.entry_topic_process = ttk.Entry(frame, textvariable=self.topic_process, width=70)
        self.entry_topic_process.grid(row=1, column=1, padx=2, sticky=ttk.W, pady=10)

    def create_buttons(self):
        frame = ttk.Frame(self)
        frame.pack(fill="x", padx=10, pady=5)

        self.button_connect = ttk.Button(frame, text="Conectar", bootstyle="success")
        self.button_connect.pack(side=LEFT, padx=5, pady=10)

        self.button_disconnect = ttk.Button(frame, text="Desconectar", bootstyle="danger", state="disabled")
        self.button_disconnect.pack(side=LEFT, padx=5, pady=10)

        self.button_save = ttk.Button(frame, text="Salvar Configuração", bootstyle="default", command=self.on_save)
        self.button_save.pack(side=RIGHT, pady=10)

    def on_connect(self):
        print("Conectar")
        # if not self.validate_form():
        try:
            self.client_mqtt = ClientMqtt("MONITOR_PC", self.topic.get(), self.server.get(), int(self.port.get()))
            self.change_buttons_state(True)
            self.after(0, self.loop)
        except Exception as err:
            messagebox.showerror(title="Erro", message=err)

    def on_disconnect(self):
        print("Desconectar")
        self.client_mqtt.loop_stop()
        self.change_buttons_state(False)
        self.after_cancel(self.afterid.get())

    def on_save(self):
        # if not self.validate_form():
        config = Config(self.server.get(), self.port.get(), self.topic.get(), self.process.get(),
                        self.topic_process.get())

        try:
            with open('config.json', 'w') as f:
                json.dump(config.__dict__, f)
                messagebox.showinfo(title="Info", message="Configuração salva com sucesso.")
        except Exception:
            messagebox.showerror(title="Erro", message="Falha ao salvar arquivo de configuração.")

    def loop(self):
        def show_message_error(message):
            self.change_buttons_state(False)
            self.after_cancel(self.afterid.get())
            messagebox.showerror(title="Erro", message=message)

        try:
            if self.client_mqtt.connected:
                result = MyPsutil.check_process_exist(self.process.get())

                if result:
                    print("Gera alarme")
                    self.client_mqtt.publish(self.topic_process.get(), '1')
                else:
                    print("Sem alarme")
                    self.client_mqtt.publish(self.topic_process.get(), '0')

                self.afterid.set(self.after(5000, self.loop))
            else:
                show_message_error("Cliente desconectado do broker de maneira inesperada.")

        except FileNotFoundError as err:
            show_message_error(err)
        except Exception as err:
            show_message_error(err)

    def change_buttons_state(self, state):
        if state:
            self.button_connect["state"] = "disabled"
            self.button_disconnect["state"] = "normal"
            self.button_browser["state"] = "disabled"
            self.button_save["state"] = "disabled"
            self.entry_server["state"] = "readonly"
            self.entry_port["state"] = "readonly"
            self.entry_topic["state"] = "readonly"
            self.combobox_process["state"] = "readonly"
        else:
            self.button_connect["state"] = "normal"
            self.button_disconnect["state"] = "disabled"
            self.button_browser["state"] = "normal"
            self.button_save["state"] = "normal"
            self.entry_server["state"] = "normal"
            self.entry_port["state"] = "normal"
            self.entry_topic["state"] = "normal"
            self.combobox_process["state"] = "normal"

    def read_config(self):
        try:
            with open('config.json', 'r') as f:
                data = json.load(f)
                config = Config(**data)
                self.server.set(config.server)
                self.port.set(config.port)
                self.topic.set(config.topic)
                self.process.set(config.process)
                self.topic_process.set(config.topic_process)
        except PermissionError:
            messagebox.showwarning(title="Atenção", message="Sem permissão para abrir o arquivo de configuração.")
        except FileNotFoundError:
            messagebox.showwarning(title="Atenção", message="Arquivo de configuração não encontrado.")
        except Exception:
            messagebox.showwarning(title="Atenção", message="Falha ao abir arquivo de configuração.")

