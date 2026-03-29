import subprocess


def convert_480p(video_path):
    cmd = f"ffmpeg -i \"{video_path}\" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 \"{video_path}_480p.mp4\""
    subprocess.run(cmd, shell=True, check=True)
