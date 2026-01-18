import subprocess
import os

class VideoUtil:
    process = None

    @staticmethod
    def start_recording(name):
        os.makedirs("videos", exist_ok=True)
        file = f"videos/{name}.mp4"
        VideoUtil.process = subprocess.Popen([
            "ffmpeg",
            "-y",
            "-f", "gdigrab",
            "-i", "desktop",
            file
        ])
        return file

    @staticmethod
    def stop_recording():
        if VideoUtil.process:
            VideoUtil.process.terminate()
