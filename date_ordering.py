import os
import shutil
from PIL import Image
from datetime import datetime
from moviepy import VideoFileClip

ORIGIN_DIR = '/home/kevinguzman/Descargas/GooglePhotos'
# ORIGIN_DIR = '/home/kevinguzman/Descargas/Ordered'
DEST_DIR = '/home/kevinguzman/Descargas/bkp_photos_kevocde'
IMAGE_EXT = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic', '.webp')
VIDEO_EXT = ('.mp4', '.mov', '.avi', '.mkv', '.mts', '.m4v', '.3gp')

def get_photo_date(fileroute):
  try:
      with Image.open(fileroute) as img:
        exif_data = img._getexif()
        if exif_data:
          strdate = exif_data.get(36867)
          if strdate:
            return datetime.strptime(strdate, '%Y:%m:%d %H:%M:%S')
  except Exception:
    return None

  return None


def get_video_date(fileroute):
  try:
    with VideoFileClip(fileroute) as video:
      if video.metadata and 'creation_time' in video.metadata:
        return video.metadata['creation_time']
  except Exception:
    pass

  try:
      mod_timestamp = os.path.getmtime(fileroute)
      return datetime.fromtimestamp(mod_timestamp)
  except Exception:
    return None


def short_images():
  os.makedirs(DEST_DIR, exist_ok=True)
  nodate_folder = os.path.join(DEST_DIR, "nodate")
  os.makedirs(nodate_folder, exist_ok=True)

  for baseroute, _, files in os.walk(ORIGIN_DIR):
    for filename in files:
      filename_lower = filename.lower()
      fileroute = os.path.join(baseroute, filename)

      if filename_lower.endswith(IMAGE_EXT):
        filedate = get_photo_date(fileroute)
      elif filename_lower.endswith(VIDEO_EXT):
        filedate = get_video_date(fileroute)
      else:
        continue

      if filedate:
        year = str(filedate.year)
        month = f"{filedate.month:02d}"
        final_folder = os.path.join(DEST_DIR, year, month)
      else:
        final_folder = nodate_folder

      os.makedirs(final_folder, exist_ok=True)
      final_file_route = os.path.join(final_folder, filename)

      counter = 1
      base_name, extention = os.path.splitext(filename)
      while os.path.exists(final_file_route):
        new_filename = f"{base_name}_{counter}{extention}"
        final_file_route = os.path.join(final_folder, new_filename)
        counter += 1

      try:
        if True:
          shutil.move(fileroute, final_file_route)
      except Exception as e:
        print(f"!! Error coping {filename}: {e}")


if __name__ == "__main__":
  short_images()
