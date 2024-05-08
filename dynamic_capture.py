import os
import glob
import time
from datetime import datetime
from mss import mss
from screeninfo import get_monitors
from PIL import Image

def get_monitor_id(monitor):
    """
    Generate a unique identifier for a monitor based on its size and position.
    """
    return f"{monitor.width}x{monitor.height}_{monitor.x}_{monitor.y}"

def create_black_image(directory, monitor, count, existing_timestamps):
    """
    Create a black image for each missing interval with the correct resolution and synchronized timestamps.
    """
    width, height = monitor.width, monitor.height
    for i in range(count):
        img = Image.new('RGB', (width, height), color='black')
        img.save(f'{directory}/{existing_timestamps[i]}_black.png')
    print(f'Filled {count} black images in {directory}.')

def backfill_with_black_images(directory, monitor, up_to_count, existing_timestamps):
    """
    Create black images to backfill new monitor directories to synchronize with the timestamps of existing captures.
    """
    width, height = monitor.width, monitor.height
    for i in range(up_to_count):
        img = Image.new('RGB', (width, height), color='black')
        img.save(f'{directory}/{existing_timestamps[i]}_black.png')
    print(f'Backfilled {up_to_count} black images in {directory}.')

def update_max_images_count_and_timestamps():
    """
    Update the maximum image count based on the number of files in the directories and collect all existing timestamps.
    """
    current_max = 0
    timestamps = []
    # Assume directories follow the 'screen_ID' format and are in the same root directory
    for directory in glob.glob('screen_*'):
        files = glob.glob(f'{directory}/*.png')
        current_max = max(current_max, len(files))
        if not timestamps:
            timestamps = sorted([os.path.basename(f).split('_')[0] for f in files])
    return current_max, timestamps

def capture_screenshots(interval=5):
    """
    Capture screenshots from all screens every 'interval' seconds, adjusting for monitor additions or removals.
    """
    last_monitors = {get_monitor_id(m): m for m in get_monitors()}
    max_images_count, existing_timestamps = update_max_images_count_and_timestamps()

    try:
        while True:
            current_monitors = {get_monitor_id(m): m for m in get_monitors()}
            removed_monitors = set(last_monitors) - set(current_monitors)
            added_monitors = set(current_monitors) - set(last_monitors)

            # Handle removed monitors by creating black images
            for id in removed_monitors:
                monitor = last_monitors[id]
                monitor_dir = f'screen_{id}'
                create_black_image(monitor_dir, monitor, max_images_count - len(existing_timestamps), existing_timestamps)

            # Capture and save screenshots
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            with mss() as sct:
                for id, monitor in current_monitors.items():
                    directory = f'screen_{id}'
                    os.makedirs(directory, exist_ok=True)
                    filename = f'{directory}/{timestamp}.png'
                    if id in added_monitors:
                        # Backfill with black images if new monitor
                        backfill_with_black_images(directory, monitor, max_images_count, existing_timestamps)

                    # Define monitor capture area
                    monitor_area = {
                        "top": monitor.y,
                        "left": monitor.x,
                        "width": monitor.width,
                        "height": monitor.height
                    }

                    # Capture the actual screenshot using monitor dimensions and position
                    sct_img = sct.grab(monitor_area)
                    Image.frombytes('RGB', (sct_img.width, sct_img.height), sct_img.rgb).save(filename)
                    print(f'Captured {filename}')

            # Update last_monitors and max_images_count
            last_monitors = current_monitors
            max_images_count, existing_timestamps = update_max_images_count_and_timestamps()

            time.sleep(interval)
    except KeyboardInterrupt:
        print("Stopped screenshot capture.")

if __name__ == "__main__":
    capture_screenshots(interval=5)  # Set your desired interval (in seconds) here.
