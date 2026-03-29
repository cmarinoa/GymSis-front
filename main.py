import customtkinter as ctk
from controller.gym_controller import AppController


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GymSis")
        self.geometry("500x600")

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Start controller
        self.controller = AppController(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()