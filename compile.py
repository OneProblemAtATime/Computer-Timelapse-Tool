import os
import glob
from moviepy.editor import ImageSequenceClip, VideoFileClip, clips_array

def create_timelapse(screen_folder, image_duration_ms):
    try:
        fps = 1000.0 / image_duration_ms if image_duration_ms > 0 else 24  # Default to 24 FPS if duration is invalid
    except TypeError:
        print("Invalid image_duration_ms value. Please ensure it's a number greater than 0.")
        return None

    image_files = sorted(glob.glob(os.path.join(screen_folder, '*.png')))
    
    if not image_files:
        print(f"No images found in {screen_folder}. Skipping...")
        return None

    clip = ImageSequenceClip(image_files, fps=fps)
    output_file = f"{screen_folder}_timelapse.mp4"
    clip.write_videofile(output_file, fps=fps)
    print(f"Timelapse video created: {output_file}")
    return output_file  # Returning the output file path for further use

def compile_videos(video_clips):
    if not video_clips:
        print("No video clips provided for compilation.")
        return

    min_height = min(clip.size[1] for clip in video_clips)
    resized_clips = [clip.resize(height=min_height) for clip in video_clips]

    final_clip = clips_array([resized_clips])  # Correctly pass the list of lists
    final_output = "compiled_timelapse.mp4"
    final_clip.write_videofile(final_output, codec="libx264", fps=24)
    print(f"Compiled video created: {final_output}")

def main(image_duration_ms=100):
    video_clips = []
    for folder_name in sorted(os.listdir('.')):
        if os.path.isdir(folder_name) and folder_name.startswith('screen_'):
            video_path = create_timelapse(folder_name, image_duration_ms)
            if video_path:
                video_clips.append(VideoFileClip(video_path))  # Correctly load the video file

    compile_videos(video_clips)

if __name__ == "__main__":
    main(image_duration_ms=50)
