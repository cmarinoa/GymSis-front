from tkinter import messagebox

from view.login_view import LoginView
from view.register_view import RegisterView
from view.menu_view import MenuView
from view.sessions_view import SessionsView
from view.exercises_view import ExercisesView
from model.gym_model import get_exercises, get_measurements, get_sessions, login_user, register_exercise, register_measurements, register_session, register_user

class AppController:
    def __init__(self, root):
        self.root = root
        self.current_view = None
        self.current_user = None
        self.current_token = None
        self.sessions = []
        self.exercises_by_session = {}
        self.current_exercises_view = None
        self.measurements = {}

        self.show_login()

    def clear_view(self):
        if self.current_view:
            self.current_view.destroy()

    def show_login(self):
        self.clear_view()
        self.current_user = None
        self.current_token = None
        self.sessions = []
        self.exercises_by_session = {}
        self.current_exercises_view = None
        self.measurements = {}
        view = LoginView(self.root)

        view.signup_label.bind("<Button-1>", lambda e: self.show_register())
        view.signin_button.configure(command=lambda: self.handle_login(view))

        self.current_view = view
        view.pack(fill="both", expand=True)

    def show_register(self):
        self.clear_view()
        view = RegisterView(self.root)

        view.on_back = self.show_login
        view.on_signup = lambda: self.handle_register(view)
        view.on_login = self.show_login

        self.current_view = view
        view.pack(fill="both", expand=True)

    def show_menu(self, username):
        self.clear_view()
        view = MenuView(self.root, username)
        self.current_user = username
        self.current_exercises_view = None

        # navigation callbacks
        view.on_logout = self.show_login
        view.on_open_sessions = lambda: view.show_sessions(
            self.handle_session_selected,
            self.handle_add_session,
            self.sessions
        )
        view.on_open_profile = lambda: view.show_profile(
            self.handle_save_measurements,
            self.measurements
        )

        self.current_view = view
        view.pack(fill="both", expand=True)

        # Show sessions upon login
        view.show_sessions(
            self.handle_session_selected,
            self.handle_add_session,
            self.sessions
        )

    def show_sessions(self):
        self.clear_view()
        view = SessionsView(self.root, self.current_user)
        view.on_session_selected = self.handle_session_selected
        view.on_add_session = self.handle_add_session
        view.display_sessions(self.sessions)

        self.current_view = view
        view.pack(fill="both", expand=True)

    def handle_add_session(self, session_date):
        if not self.current_token:
            messagebox.showerror("Session error", "You must log in first")
            return

        response = register_session(session_date, self.current_token)

        if "error" in response:
            messagebox.showerror("Session error", response["error"])
            return

        self.sessions.append({
            "session_number": response["session_number"],
            "date": response["date"]
        })
        self.exercises_by_session[response["session_number"]] = []

        self.current_view.show_sessions(
            self.handle_session_selected,
            self.handle_add_session,
            self.sessions
        )

    def show_profile(self):
        self.current_view.show_profile(
            self.handle_save_measurements,
            self.measurements
        )

    def handle_save_measurements(self, measurements):
        if not self.current_token:
            messagebox.showerror("Profile error", "You must log in first")
            return None

        response = register_measurements(measurements, self.current_token)

        if "error" in response:
            messagebox.showerror("Profile error", response["error"])
            return None

        self.measurements = {
            "height": response["height"],
            "weight": response["weight"],
            "chest": response["chest"],
            "thighs": response["thighs"],
            "waist": response["waist"],
            "hips": response["hips"]
        }

        return self.measurements

    def handle_session_selected(self, session_data):
        # Navigate to ExercisesView inside the menu content area
        self.load_exercises(session_data["session_number"])
        exercises = self.exercises_by_session.get(session_data["session_number"], [])
        self.current_exercises_view = self.current_view.show_exercises(
            session_data,
            exercises,
            lambda exercise: self.handle_add_exercise(session_data, exercise)
        )

    def handle_add_exercise(self, session_data, exercise):
        if not self.current_token:
            messagebox.showerror("Exercise error", "You must log in first")
            return

        exercise["session_id"] = session_data["session_number"]
        response = register_exercise(exercise, self.current_token)

        if "error" in response:
            messagebox.showerror("Exercise error", response["error"])
            return

        session_number = session_data["session_number"]
        self.exercises_by_session.setdefault(session_number, [])
        self.exercises_by_session[session_number].append(response)
        self.current_exercises_view.display_exercises(self.exercises_by_session[session_number])

    def handle_login(self, view):
        username = view.username_entry.get()
        password = view.password_entry.get()

        if not username or not password:
            messagebox.showerror("Login error", "Username and password are required")
            return

        response = login_user(username, password)

        if "error" in response:
            messagebox.showerror("Login error", response["error"])
            return

        self.current_token = response["token"]
        self.sessions = []
        self.exercises_by_session = {}
        self.load_sessions()
        self.load_measurements()
        self.show_menu(response["name"])

    def load_sessions(self):
        response = get_sessions(self.current_token)

        if "error" in response:
            messagebox.showerror("Session error", response["error"])
            return

        self.sessions = response["sessions"]

        for session in self.sessions:
            self.exercises_by_session.setdefault(session["session_number"], [])

    def load_exercises(self, session_number):
        response = get_exercises(session_number, self.current_token)

        if "error" in response:
            messagebox.showerror("Exercise error", response["error"])
            return

        self.exercises_by_session[session_number] = response["exercises"]

    def load_measurements(self):
        response = get_measurements(self.current_token)

        if "error" in response:
            messagebox.showerror("Profile error", response["error"])
            return

        self.measurements = {
            "height": response["height"],
            "weight": response["weight"],
            "chest": response["chest"],
            "thighs": response["thighs"],
            "waist": response["waist"],
            "hips": response["hips"]
        }

    def handle_register(self, view):
        username = view.username_entry.get()
        password = view.password_entry.get()
        confirm_password = view.confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Register error", "All fields are required")
            return

        if password != confirm_password:
            messagebox.showerror("Register error", "Passwords do not match")
            return

        response = register_user(username, password)

        if "error" in response:
            messagebox.showerror("Register error", response["error"])
            return

        messagebox.showinfo("Register", "User registered successfully")
        self.show_login()
