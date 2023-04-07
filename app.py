import cv2
import ctypes
import keyboard
import threading

# The App class handles the face detection and screen locking/unlocking functionality.
class App:
    def __init__(self):
        self.face_detected = False
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.cap = cv2.VideoCapture(1)
        self.count_since_last_seen = 0
        self.locked_screen = False

        # Load the user32.dll library for screen locking functionality
        self.user32 = ctypes.WinDLL('user32')

    # Locks the screen and marks it as locked
    def lock_screen(self):
        ctypes.windll.user32.LockWorkStation()
        self.locked_screen = True

    # Unlocks the screen and marks it as unlocked
    def unlock_screen(self):
        self.locked_screen = False

    # Scans for faces in the webcam, locks the screen when no face is detected for a specified time
    def detect_faces(self, number_of_seconds, refresh_rate, stop_flag):
        self.count_since_last_seen = 0
        increment_amount = refresh_rate / 1000

        while not stop_flag.is_set():
            _, frame = self.cap.read()

            if frame is None:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            if len(faces):
                self.count_since_last_seen = 0
                self.unlock_screen()
            elif not self.locked_screen:
                self.count_since_last_seen += increment_amount

            if self.count_since_last_seen >= number_of_seconds and not self.locked_screen:
                self.lock_screen()

            cv2.waitKey(refresh_rate)

            if stop_flag.is_set():
                break

        self.cap.release()

# The KeyboardListener class listens for the F8 key press to stop the program
class KeyboardListener(threading.Thread):
    def __init__(self, app, stop_flag):
        super().__init__()
        self.daemon = True
        self.app = app
        self.stop_flag = stop_flag

    # Listens for the F8 key press and calls the stop_program method when detected
    def run(self):
        try:
            keyboard.add_hotkey('f8', self.stop_program)
            while not self.stop_flag.is_set():
                keyboard.wait()
        except Exception as e:
            print(f"An error occurred in the KeyboardListener thread: {e}")

    # Stops the program by setting the stop_flag and releasing resources
    def stop_program(self):
        self.stop_flag.set()
        self.app.cap.release()
        cv2.destroyAllWindows()

# The main function creates an instance of the App class and starts the KeyboardListener thread
def main():
    app = App()
    stop_flag = threading.Event()

    keyboard_listener = KeyboardListener(app, stop_flag)
    keyboard_listener.start()

    app.detect_faces(10, 100, stop_flag)

    app.cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
