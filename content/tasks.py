import subprocess

import os



def convert_to_hls_480p(source_video_path, video_id):

    _convert(source_video_path, video_id, "480p", "hd480")



def convert_to_hls_720p(source_video_path, video_id):

    _convert(source_video_path, video_id, "720p", "hd720")



def convert_to_hls_1080p(source_video_path, video_id):

    _convert(source_video_path, video_id, "1080p", "hd1080")



def _convert(source_video_path, video_id, res_name, scale):

    base_dir = os.path.dirname(source_video_path)

    target_folder = os.path.join(base_dir, str(video_id), res_name)

    os.makedirs(target_folder, exist_ok=True)

    

    playlist_path = os.path.join(target_folder, "index.m3u8")

    

    cmd = (

        f'ffmpeg -i "{source_video_path}" '

        f'-s {scale} -c:v libx264 -crf 23 -c:a aac -strict -2 '

        f'-start_number 0 -hls_time 10 -hls_list_size 0 '

        f'-hls_playlist_type vod "{playlist_path}"'

    )

    

    print(f"Starte Konvertierung fuer Video {video_id} nach {res_name}...")

    subprocess.run(cmd, shell=True, check=True)

    print(f"Fertig mit {res_name}!")


def generate_thumbnail(source_video_path, video_id):
    from content.models import Video
    from django.core.files import File
    try:
        video = Video.objects.get(id=video_id)
        if not video.thumbnail_url and video.video_file:
            base_dir = os.path.dirname(source_video_path)
            thumb_name = f"thumb_{video_id}.jpg"
            thumb_path = os.path.join(base_dir, thumb_name)

            cmd = f'ffmpeg -y -i "{source_video_path}" -vframes 1 -q:v 2 "{thumb_path}"'
            print(f"Starte Thumbnail-Generierung für Video {video_id}...")
            subprocess.run(cmd, shell=True, check=True)

            if os.path.exists(thumb_path):
                with open(thumb_path, 'rb') as f:
                    video.thumbnail_url.save(thumb_name, File(f), save=True)
                os.remove(thumb_path)
                print(f"Thumbnail für Video {video_id} erfolgreich generiert!")
    except Exception as e:
        print(f"Fehler bei Thumbnail-Generierung für Video {video_id}: {e}")

