from MainForm import MainForm
import ttkbootstrap as ttk


if __name__ == "__main__":

    app = ttk.Window(
        title="Monitor Censura MQTT",
        themename="superhero",
        resizable=(False, False)
    )
    MainForm(app)

    app.mainloop()
