from MainForm import MainForm
import ttkbootstrap as ttk
from pystray import MenuItem as item
import pystray
from PIL import Image
import threading


# Define a function for quit the window
def quit_window(icon):
    icon.stop()
    app.destroy()


# Define a function to show the window again
def show_window(icon):
    icon.stop()
    app.after(0, app.deiconify())


# Hide the window and show on the system taskbar
def hide_window():
    app.withdraw()
    image = Image.open("favicon.ico")
    menu = (item('Exibir', show_window), item('Sair', quit_window))
    icon = pystray.Icon("name", image, "Monitor MQTT", menu)
    icon.run()


def hide_window_threading():
    threading.Thread(daemon=True, target=hide_window).start()


if __name__ == "__main__":

    app = ttk.Window(
        title="Monitor Censura MQTT",
        themename="superhero",
        resizable=(False, False)
    )
    MainForm(app)

    app.protocol('WM_DELETE_WINDOW', hide_window_threading)

    app.mainloop()
