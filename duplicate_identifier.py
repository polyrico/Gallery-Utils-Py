import os, json, shutil
from imagededup.methods import PHash

ORIGIN_DIR = '/run/media/kevinguzman/USB001/bkp_photos_kevocde/2025'
DEST_DIR = '/run/media/kevinguzman/USB001/duplicates'
IMAGE_EXT = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic', '.webp')

def find_duplicates():
  phasher = PHash()
  #phasher = PHash()
  #encodings = phasher.encode_images(image_dir=ORIGIN_DIR)
  #print(encodings)
  #duplicates = phasher.find_duplicates(encoding_map=encodings)
  #print(duplicates);
  encodings = {}
  mapped_files = {}
  for baseroute, _, files in os.walk(ORIGIN_DIR):
    if files:
      mapped_files = {**mapped_files, **{filename:os.path.join(baseroute, filename) for filename in files}}
      localencoding = phasher.encode_images(image_dir=baseroute)
      encodings = {**encodings, **localencoding}

  duplicates = phasher.find_duplicates(encoding_map=encodings)
  added = []
  output = []

  for key, value in duplicates.items():
    if value and key not in added:
      output.append([mapped_files[filename] for filename in [key, *value]])
      added.append(key)
      added.extend(value)

  with open('duplicates.json', 'w') as f:
    json.dump(output, f, indent=2)


def move_duplicates():
  duplicates = []
  with open("duplicates.json") as file:
    duplicates = json.load(file)

  os.makedirs(DEST_DIR, exist_ok=True)

  increment = 0
  for group in duplicates:
    increment +=1
    destdir = os.path.join(DEST_DIR, str(increment))
    os.makedirs(destdir, exist_ok=True)
    for filename in group:
      print(filename)
      shutil.copy2(filename, os.path.join(destdir, filename.split('/')[-1]))


if __name__ == "__main__":
  find_duplicates()
  move_duplicates()
