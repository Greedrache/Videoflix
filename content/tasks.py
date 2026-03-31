import subprocess
import os

def convert_to_hls_480p(source_video_path, video_id):
    """
    Nimmt das Originalvideo und zerlegt es in 480p HLS Segmente (.m3u8 und .ts Dateien)
    """
    base_dir = os.path.dirname(source_video_path)
    
    target_folder = os.path.join(base_dir, str(video_id), "480p")
    
    os.makedirs(target_folder, exist_ok=True)
    
    playlist_path = os.path.join(target_folder, "index.m3u8")
    
    cmd = (
        f'ffmpeg -i "{source_video_path}" '
        f'-s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 '
        f'-start_number 0 -hls_time 10 -hls_list_size 0 '
        f'-hls_playlist_type vod "{playlist_path}"'
    )
    
    print(f"Starte Konvertierung für Video {video_id} nach 480p...")
    subprocess.run(cmd, shell=True, check=True)
    print("Fertig!")
