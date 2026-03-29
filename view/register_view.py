import customtkinter as ctk

class RegisterView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Callbacks (controller will assign these)
        self.on_back = None
        self.on_signup = None
        self.on_login = None

        self.build_ui()

    def build_ui(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(padx=40, pady=40, fill="both", expand=True)

        # Back button
        self.back_button = ctk.CTkButton(
            self.main_frame,
            text="← Back",
            command=self.handle_back
        )
        self.back_button.pack(anchor="w", padx=10, pady=(10, 0))

        # Username
        self.username_label = ctk.CTkLabel(self.main_frame, text="Username:")
        self.username_label.pack(anchor="w", padx=60, pady=(20, 0))

        self.username_entry = ctk.CTkEntry(self.main_frame)
        self.username_entry.pack(padx=60, pady=10, fill="x")

        # Password
        self.password_label = ctk.CTkLabel(self.main_frame, text="Password:")
        self.password_label.pack(anchor="w", padx=60, pady=(10, 0))

        self.password_entry = ctk.CTkEntry(self.main_frame, show="*")
        self.password_entry.pack(padx=60, pady=10, fill="x")

        # Confirm Password
        self.confirm_password_label = ctk.CTkLabel(self.main_frame, text="Confirm Password:")
        self.confirm_password_label.pack(anchor="w", padx=60, pady=(10, 0))

        self.confirm_password_entry = ctk.CTkEntry(self.main_frame, show="*")
        self.confirm_password_entry.pack(padx=60, pady=10, fill="x")

        # Signup button
        self.signup_button = ctk.CTkButton(
            self.main_frame,
            text="SIGN UP",
            command=self.handle_signup
        )
        self.signup_button.pack(pady=20)

        # Login link
        self.login_label = ctk.CTkLabel(
            self.main_frame,
            text="Sign in",
            text_color="blue",
            cursor="hand2"
        )
        self.login_label.pack()
        self.login_label.bind("<Button-1>", lambda e: self.handle_login())


    # EVENT HANDLERS

    def handle_back(self):
        if self.on_back:
            self.on_back()

    def handle_signup(self):
        if self.on_signup:
            self.on_signup()

    def handle_login(self):
        if self.on_login:
            self.on_login()