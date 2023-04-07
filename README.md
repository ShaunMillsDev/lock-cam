This script implements a face detection application that locks the computer screen when a face is not detected in the webcam feed for a specified number of seconds.

Imports:

    - cv2: OpenCV library for computer vision tasks.
    - ctypes: For interacting with the Windows API to lock the computer screen.
    - keyboard: For listening to keyboard events, like the F8 keypress to stop the application.
    - threading: For running the keyboard listener in a separate thread.

Classes:

    - App: Main class for the application.
        - init: Initializes attributes for the class.
        - lock_screen: Locks the computer screen using the Windows API.
        - unlock_screen: Marks the screen as unlocked.
        - detect_faces: Main function to detect faces in the webcam feed and lock the screen if no face is detected.

    - KeyboardListener: Threaded class to listen for the F8 keypress to stop the application.
        - init: Initializes attributes for the class.
        - run: Main function that runs in a separate thread, listens for the F8 keypress and stops the application when it's pressed.
        - stop_program: Sets the stop_flag, releases the VideoCapture object, and closes all OpenCV windows.
        
Functions:

    - main: Main function that creates an instance of the App class, starts the keyboard listener thread, and calls the detect_faces method.

Execution:

    - The script starts by calling the main function when run as a standalone script.


Class App:

    - __init__ (continued): Initializes the necessary attributes for the class.
        - self.cap: Creates a VideoCapture object to access the webcam.
        - self.count_since_last_seen: Keeps track of the time since the last face was detected.
        - self.locked_screen: Flag to indicate whether the screen is locked or not.
        - self.user32: Loads the user32.dll library for interacting with the Windows API.
        - self.VK_LWIN, self.VK_L: Define the key codes for locking and unlocking the screen.
        - self.stop_flag: Flag to indicate whether the application should stop or not.
    - lock_screen: Locks the computer screen using the Windows API and sets the self.locked_screen flag to True.
    - unlock_screen: Sets the self.locked_screen flag to False.
    - detect_faces: Main function for face detection and screen locking logic.
        - Takes three arguments: number_of_seconds, refresh_rate, and stop_flag.
        - Sets self.count_since_last_seen to 0.
        - Initializes increment_amount for counting the elapsed time.
        - Continuously reads frames from the webcam and processes them.
        - Converts the frame to grayscale and detects faces using the Haar Cascade.
        - If faces are detected, resets the counter and unlocks the screen.
        - If no faces are detected and the screen is not locked, increments the counter.
        - If the counter reaches the specified number_of_seconds and the screen is not locked, locks the screen.
        - Waits for the specified refresh_rate before processing the next frame.
        - Breaks the loop if the stop_flag is set.
        - Releases the VideoCapture object at the end.

Class KeyboardListener:

    - Inherits from threading.Thread to run as a separate thread.
    - __init__: Initializes the necessary attributes for the class.
        - self.daemon: Sets the thread as a daemon thread to automatically exit when the main program finishes.
        - self.app: Reference to the App instance.
        - self.stop_flag: Reference to the shared stop_flag.
    - run: Main function that runs in a separate thread.
        - Adds a hotkey for the F8 key, which calls the stop_program method when pressed.
        - Waits for key events until the stop_flag is set or an exception occurs.
        - Catches and prints exceptions if they occur.
    - stop_program: Method to stop the application.
        - Sets the stop_flag to True.
        - Releases the VideoCapture object.
        - Closes all OpenCV windows.

Function main:

    - Creates an instance of the App class.
    - Creates a threading.Event object for the stop_flag.
    - Starts the KeyboardListener thread.
    - Calls the detect_faces method on the App instance with the specified arguments and shared stop_flag.
    - Releases the VideoCapture object and closes all OpenCV windows.

Execution:

    - If the script is run as a standalone program, the main function is called to start the application.
