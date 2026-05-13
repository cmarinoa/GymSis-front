from tkinter import messagebox

from view.login_view import LoginView
from view.register_view import RegisterView
from view.menu_view import MenuView
from view.sessions_view import SessionsView
from view.exercises_view import ExercisesView
from controller.validation_helpers import validate_cardio_exercise, validate_measurements, validate_password, validate_username, validate_weight_exercise
from model.gym_model import clear_session_token, delete_exercise, delete_saved_exercise, delete_session, get_exercises, get_measurements, get_saved_exercises, get_saved_session, get_sessions, load_session_token, login_user, register_exercise, register_measurements, register_saved_exercise, register_session, register_user, save_session_token, update_exercise, update_saved_exercise, update_session

class AppController:
    def __init__(self, root):
        self.root = root
        self.current_view = None
        self.current_user = None
        self.current_token = None
        # Stores the sessions currently loaded for the logged in user
        self.sessions = []
        # Groups exercises by session number
        self.exercises_by_session = {}
        # Keeps a reference to the exercises screen currently being shown
        self.current_exercises_view = None
        # Stores the latest profile measurements loaded from the backend
        self.measurements = {}
        # Stores the user's saved exercises
        self.saved_exercises = []

        self.restore_saved_session()

    def clear_view(self):
        if self.current_view:
            self.current_view.destroy()

    def show_login(self):
        self.clear_view()
        # Reset local state when returning to the login screen
        self.current_user = None
        self.current_token = None
        self.sessions = []
        self.exercises_by_session = {}
        self.current_exercises_view = None
        self.measurements = {}
        self.saved_exercises = []
        view = LoginView(self.root)

        view.signup_label.bind("<Button-1>", lambda e: self.show_register())
        view.signin_button.configure(command=lambda: self.handle_login(view))

        self.current_view = view
        view.pack(fill="both", expand=True)

    def restore_saved_session(self):
        # Try to keep the user logged in with the token saved on disk
        saved_token = load_session_token()

        if not saved_token:
            self.show_login()
            return

        response = get_saved_session(saved_token)

        if "error" in response:
            clear_session_token()
            self.show_login()
            return

        self.current_token = saved_token
        self.sessions = []
        self.exercises_by_session = {}
        self.saved_exercises = []
        self.load_sessions()
        self.load_measurements()
        self.load_saved_exercises()
        self.show_menu(response["name"])

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

        # Connect each menu action with the matching controller method
        view.on_logout = self.handle_logout
        view.on_open_sessions = lambda: view.show_sessions(
            self.handle_session_selected,
            self.handle_add_session,
            self.sessions,
            self.handle_edit_session,
            self.handle_delete_session
        )
        view.on_open_profile = lambda: view.show_profile(
            self.handle_save_measurements,
            self.measurements
        )
        view.on_open_saved_exercises = lambda: view.show_saved_exercises(
            self.saved_exercises,
            self.handle_add_saved_exercise,
            self.handle_edit_saved_exercise,
            self.handle_delete_saved_exercise
        )

        self.current_view = view
        view.pack(fill="both", expand=True)

        # Show the sessions screen first after login
        view.show_sessions(
            self.handle_session_selected,
            self.handle_add_session,
            self.sessions,
            self.handle_edit_session,
            self.handle_delete_session
        )

    def show_sessions(self):
        self.clear_view()
        view = SessionsView(self.root, self.current_user)
        view.on_session_selected = self.handle_session_selected
        view.on_add_session = self.handle_add_session
        view.on_edit_session = self.handle_edit_session
        view.on_delete_session = self.handle_delete_session
        view.display_sessions(self.sessions)

        self.current_view = view
        view.pack(fill="both", expand=True)

    def handle_add_session(self, session_date):
        if not self.current_token:
            messagebox.showerror("Session error", "You must log in first")
            return

        # Ask the model to create the new session in the backend
        response = register_session(session_date, self.current_token)

        if "error" in response:
            messagebox.showerror("Session error", response["error"])
            return

        # Reload sessions so the visible numbering stays correct for this user
        self.load_sessions()

        self.current_view.show_sessions(
            self.handle_session_selected,
            self.handle_add_session,
            self.sessions,
            self.handle_edit_session,
            self.handle_delete_session
        )

    def handle_edit_session(self, session_data, new_date):
        if not self.current_token:
            messagebox.showerror("Session error", "You must log in first")
            return

        response = update_session(session_data["session_id"], new_date, self.current_token)

        if "error" in response:
            messagebox.showerror("Session error", response["error"])
            return

        # Reload sessions because changing the date may change the visible order
        self.load_sessions()

        self.current_view.show_sessions(
            self.handle_session_selected,
            self.handle_add_session,
            self.sessions,
            self.handle_edit_session,
            self.handle_delete_session
        )

    def handle_delete_session(self, session_data):
        confirm = messagebox.askyesno(
            "Delete session",
            "Are you sure you want to delete this session?"
        )

        if not confirm:
            return

        session_id = session_data["session_id"]
        if not self.current_token:
            messagebox.showerror("Session error", "You must log in first")
            return

        response = delete_session(session_id, self.current_token)

        if "error" in response:
            messagebox.showerror("Session error", response["error"])
            return

        self.exercises_by_session.pop(session_id, None)
        # Reload sessions because deleting one changes the visible numbering
        self.load_sessions()

        self.current_view.show_sessions(
            self.handle_session_selected,
            self.handle_add_session,
            self.sessions,
            self.handle_edit_session,
            self.handle_delete_session
        )

    def show_profile(self):
        self.current_view.show_profile(
            self.handle_save_measurements,
            self.measurements
        )

    def show_saved_exercises(self):
        self.current_view.show_saved_exercises(
            self.saved_exercises,
            self.handle_add_saved_exercise,
            self.handle_edit_saved_exercise,
            self.handle_delete_saved_exercise
        )

    def handle_save_measurements(self, measurements):
        if not self.current_token:
            messagebox.showerror("Profile error", "You must log in first")
            return None

        validation_error = validate_measurements(measurements)

        if validation_error:
            messagebox.showerror("Profile error", validation_error)
            return None

        # Send the edited profile values to the backend
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
        # Load the latest exercises before opening the exercises screen
        self.load_exercises(session_data["session_id"])
        exercises = self.exercises_by_session.get(session_data["session_id"], [])
        self.current_exercises_view = self.current_view.show_exercises(
            session_data,
            exercises,
            self.saved_exercises,
            lambda exercise: self.handle_add_exercise(session_data, exercise),
            lambda old_exercise, new_exercise: self.handle_edit_exercise(session_data, old_exercise, new_exercise),
            lambda exercise: self.handle_delete_exercise(session_data, exercise)
        )

    def handle_add_exercise(self, session_data, exercise):
        if not self.current_token:
            messagebox.showerror("Exercise error", "You must log in first")
            return False

        validation_error = self.validate_exercise(exercise)

        if validation_error:
            messagebox.showerror("Exercise error", validation_error)
            return False

        # Add the session id so the backend knows where this exercise belongs
        exercise["session_id"] = session_data["session_id"]
        response = register_exercise(exercise, self.current_token)

        if "error" in response:
            messagebox.showerror("Exercise error", response["error"])
            return False

        session_id = session_data["session_id"]
        self.exercises_by_session.setdefault(session_id, [])
        # Keep the created exercise in local memory too
        self.exercises_by_session[session_id].append(response)
        self.current_exercises_view.display_exercises(self.exercises_by_session[session_id])
        return True

    def handle_logout(self):
        # Logging out removes the saved token so the next app start shows login
        clear_session_token()
        self.show_login()

    def handle_add_saved_exercise(self, exercise_name):
        if not self.current_token:
            messagebox.showerror("Exercise error", "You must log in first")
            return False

        response = register_saved_exercise(exercise_name, self.current_token)

        if "error" in response:
            messagebox.showerror("Exercise error", response["error"])
            return False

        self.saved_exercises.append({
            "exercise_id": response["exercise_id"],
            "name": response["name"]
        })
        self.saved_exercises.sort(key=lambda exercise: (exercise["name"].lower(), exercise["exercise_id"]))

        self.show_saved_exercises()
        return True

    def handle_edit_saved_exercise(self, exercise_data, new_name):
        if not self.current_token:
            messagebox.showerror("Exercise error", "You must log in first")
            return False

        response = update_saved_exercise(exercise_data["exercise_id"], new_name, self.current_token)

        if "error" in response:
            messagebox.showerror("Exercise error", response["error"])
            return False

        for saved_exercise in self.saved_exercises:
            if saved_exercise["exercise_id"] == exercise_data["exercise_id"]:
                saved_exercise["name"] = response["name"]
                break

        self.saved_exercises.sort(key=lambda exercise: (exercise["name"].lower(), exercise["exercise_id"]))

        self.show_saved_exercises()
        return True

    def handle_delete_saved_exercise(self, exercise_data):
        confirm = messagebox.askyesno(
            "Delete exercise",
            "Are you sure you want to delete this exercise?"
        )

        if not confirm:
            return

        if not self.current_token:
            messagebox.showerror("Exercise error", "You must log in first")
            return

        response = delete_saved_exercise(exercise_data["exercise_id"], self.current_token)

        if "error" in response:
            messagebox.showerror("Exercise error", response["error"])
            return

        self.saved_exercises = [
            exercise for exercise in self.saved_exercises
            if exercise["exercise_id"] != exercise_data["exercise_id"]
        ]

        self.show_saved_exercises()

    def handle_edit_exercise(self, session_data, old_exercise, new_exercise):
        session_id = session_data["session_id"]
        if not self.current_token:
            messagebox.showerror("Exercise error", "You must log in first")
            return None

        validation_error = self.validate_exercise(new_exercise)

        if validation_error:
            messagebox.showerror("Exercise error", validation_error)
            return None

        response = update_exercise(old_exercise.get("exercise_id"), new_exercise, self.current_token)

        if "error" in response:
            messagebox.showerror("Exercise error", response["error"])
            return None

        exercises = self.exercises_by_session.get(session_id, [])

        for index, exercise in enumerate(exercises):
            if exercise.get("exercise_id") == old_exercise.get("exercise_id"):
                exercises[index] = response

        return response

    def handle_delete_exercise(self, session_data, exercise_data):
        confirm = messagebox.askyesno(
            "Delete exercise",
            "Are you sure you want to delete this exercise?"
        )

        if not confirm:
            return

        session_id = session_data["session_id"]
        if not self.current_token:
            messagebox.showerror("Exercise error", "You must log in first")
            return

        response = delete_exercise(exercise_data.get("exercise_id"), self.current_token)

        if "error" in response:
            messagebox.showerror("Exercise error", response["error"])
            return

        self.exercises_by_session[session_id] = [
            exercise for exercise in self.exercises_by_session.get(session_id, [])
            if exercise.get("exercise_id") != exercise_data.get("exercise_id")
        ]

        self.current_exercises_view.display_exercises(self.exercises_by_session[session_id])

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
        save_session_token(self.current_token)
        # Load the user's saved data before opening the main menu
        self.sessions = []
        self.exercises_by_session = {}
        self.saved_exercises = []
        self.load_sessions()
        self.load_measurements()
        self.load_saved_exercises()
        self.show_menu(response["name"])

    def load_sessions(self):
        # Requests every session that belongs to the logged in user
        response = get_sessions(self.current_token)

        if "error" in response:
            messagebox.showerror("Session error", response["error"])
            return

        self.sessions = response["sessions"]

        for session in self.sessions:
            # Create the local slot where that session's exercises will be stored
            self.exercises_by_session.setdefault(session["session_id"], [])

    def load_exercises(self, session_id):
        # Requests all exercises from one selected session
        response = get_exercises(session_id, self.current_token)

        if "error" in response:
            messagebox.showerror("Exercise error", response["error"])
            return

        self.exercises_by_session[session_id] = response["exercises"]

    def load_measurements(self):
        # Requests the latest saved body measurements for the current user
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

    def load_saved_exercises(self):
        # Requests the saved exercises that belong to the logged in user
        response = get_saved_exercises(self.current_token)

        if "error" in response:
            messagebox.showerror("Exercise error", response["error"])
            return

        self.saved_exercises = response["exercises"]

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

        username_error = validate_username(username)

        if username_error:
            messagebox.showerror("Register error", username_error)
            return

        password_error = validate_password(password)

        if password_error:
            messagebox.showerror("Register error", password_error)
            return

        response = register_user(username, password)

        if "error" in response:
            messagebox.showerror("Register error", response["error"])
            return

        messagebox.showinfo("Register", "User registered successfully")
        self.show_login()

    def validate_exercise(self, exercise):
        # Validate the correct fields depending on the exercise type
        if exercise.get("exercise_type") == "cardio":
            return validate_cardio_exercise(exercise)

        return validate_weight_exercise(exercise)
