import customtkinter as ctk


class LoginView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Main container
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(padx=40, pady=40, fill="both", expand=True)

        # Logo (circle)
        self.logo_frame = ctk.CTkFrame(
            self.main_frame,
            width=150,
            height=150,
            corner_radius=75
        )
        self.logo_frame.pack(pady=(30, 20))
        self.logo_frame.pack_propagate(False)

        self.logo_label = ctk.CTkLabel(
            self.logo_frame,
            text="LOGO",
            font=("Arial", 18)
        )
        self.logo_label.pack(expand=True)

        # Username
        self.username_label = ctk.CTkLabel(
            self.main_frame,
            text="Username",
            anchor="w"
        )
        self.username_label.pack(padx=60, pady=(10, 5), fill="x")

        self.username_entry = ctk.CTkEntry(self.main_frame, height=35)
        self.username_entry.pack(padx=60, fill="x")

        # Password
        self.password_label = ctk.CTkLabel(
            self.main_frame,
            text="Password",
            anchor="w"
        )
        self.password_label.pack(padx=60, pady=(15, 5), fill="x")

        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            height=35,
            show="*"
        )
        self.password_entry.pack(padx=60, fill="x")

        # Button
        self.signin_button = ctk.CTkButton(
            self.main_frame,
            text="SIGN IN",
            width=120
        )
        self.signin_button.pack(pady=25)

        # Bottom text
        self.bottom_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.bottom_frame.pack(side="bottom", pady=20)

        self.text_label = ctk.CTkLabel(
            self.bottom_frame,
            text="Don't have an account?"
        )
        self.text_label.pack(side="left")

        self.signup_label = ctk.CTkLabel(
            self.bottom_frame,
            text=" Sign up",
            text_color="blue",
            cursor="hand2"
        )
        self.signup_label.pack(side="left")