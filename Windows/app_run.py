import sys
import ctypes
from ctypes import c_uint, c_char_p, create_string_buffer
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, 
                               QMenu, QMenuBar)
from PySide6.QtCore import Qt, QThread, Signal
import os

class TrialThread(QThread):
    # Define a signal to send messages to the main thread
    trial_completed = Signal(str)
    trial_error = Signal(str)

    def __init__(self, window_handle, library_key):
        super().__init__()
        self.window_handle = window_handle
        self.library_key = library_key

    def run(self):
        try:
            print("Debug Information-Product Starting")

            base_path = os.path.dirname(os.path.abspath(__file__))
            dll_path = os.path.join(base_path, "Trial.dll")

            # Load the Trial DLL
            trial_dll = ctypes.CDLL(dll_path)


            # Define function signatures
            init_trial_func = trial_dll.ReadSettingsStr
            init_trial_func.argtypes = [c_char_p, ctypes.c_void_p]
            init_trial_func.restype = c_uint

            get_property_func = trial_dll.GetPropertyValue
            get_property_func.argtypes = [c_char_p, ctypes.c_void_p, ctypes.POINTER(c_uint)]
            get_property_func.restype = c_uint

            # Initialize trial
            result = init_trial_func(
                self.library_key.encode('ascii'),
                self.window_handle
            )

            # Read trial name property
            buffer_size = c_uint(256)
            trial_name = create_string_buffer(buffer_size.value)

            result = get_property_func(
                b"TrialName",
                trial_name,
                ctypes.byref(buffer_size)
            )

            if result == 234:  # Need larger buffer
                trial_name = create_string_buffer(buffer_size.value)
                get_property_func(b"TrialName", trial_name, ctypes.byref(buffer_size))

            # Emit the result to the main thread
            self.trial_completed.emit(f"TrialName={trial_name.value.decode()}")

        except OSError:
            self.trial_error.emit("Trial.dll is missing. Application will close.")
        except Exception as e:
            self.trial_error.emit(str(e))


class MainWindow(QMainWindow):
    # The library key to prevent unauthorized use
    LIBRARY_KEY = "D36D04DC7BBB2F2D8F4E9A601F11483825C4BA"

    # Get the directory of the current executable or script


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trial Test Example")
        self.setup_ui()

        # Start trial initialization in a QThread
        self.trial_thread = TrialThread(ctypes.c_void_p(int(self.winId())), self.LIBRARY_KEY)
        self.trial_thread.trial_completed.connect(self.on_trial_completed)
        self.trial_thread.trial_error.connect(self.on_trial_error)
        self.trial_thread.start()

    def setup_ui(self):
        # Create menu bar
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)

        # File menu
        file_menu = QMenu("&File", self)
        menu_bar.addMenu(file_menu)

        # Exit action
        exit_action = file_menu.addAction("E&xit")
        exit_action.triggered.connect(self.close)

        # Help menu
        help_menu = QMenu("&Help", self)
        menu_bar.addMenu(help_menu)

        # Register action
        register_action = help_menu.addAction("&Register")
        register_action.triggered.connect(self.show_registration)

        # Set window size and center it
        self.resize(800, 600)
        self.center_window()

    def center_window(self):
        # Get the screen geometry
        screen = QApplication.primaryScreen().geometry()
        # Calculate center position
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        # Move window to center
        self.move(x, y)

    def on_trial_completed(self, message):
        print(message)

    def on_trial_error(self, error_message):
        QMessageBox.critical(self, "Error", error_message)
        self.close()

    def show_registration(self):
        try:
            trial_dll = ctypes.CDLL("Trial.dll")

            # Define function signature
            display_reg_func = trial_dll.DisplayRegistrationStr
            display_reg_func.argtypes = [c_char_p, ctypes.c_void_p]
            display_reg_func.restype = c_uint

            # Get window handle
            window_handle = ctypes.c_void_p(int(self.winId()))

            # Show registration dialog
            display_reg_func(
                self.LIBRARY_KEY.encode('ascii'),
                window_handle
            )

        except OSError:
            QMessageBox.critical(self, "Error",
                                 "Trial.dll is missing. Application will close.")
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
