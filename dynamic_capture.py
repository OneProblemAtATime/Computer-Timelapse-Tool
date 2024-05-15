# capture_screenshots.py
import os
import time
from datetime import datetime
from mss import mss
from screeninfo import get_monitors

def capture_screenshots(interval=5):
    """
    Capture screenshots from all screens every 'interval' seconds.
    """

    try:
        while True:
            monitors = get_monitors()
            print(f"Detected {len(monitors)} screens.")

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            with mss() as sct:
                for i, monitor in enumerate(monitors, start=1):
                    directory = f'screen_{i}'
                    os.makedirs(directory, exist_ok=True)
                    filename = f'{directory}/{timestamp}.png'
                    sct.shot(mon=i, output=filename)
                    print(f'Captured {filename}')
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Stopped screenshot capture.")


if __name__ == "__main__":
    capture_screenshots(interval=1)  # Set your desired interval (in seconds) here.
