import glob
import json
import os
import requests
import shutil
import zipfile

from pydub import AudioSegment


TEMP_DIR = "./temp"
MUSIC_DIR = "./musics"


def get_bsr_music(bsr_id: str, name: str, zip_url: str):
    sanitized_name = f"{bsr_id}_{name.replace(' ', '_').replace('/', '_')[:20]}"
    mp3_file_name = f"{sanitized_name}.mp3"
    mp3_file_path = os.path.join(MUSIC_DIR, mp3_file_name)

    # Check if the mp3 file already exists in MUSIC_DIR
    if os.path.exists(mp3_file_path):
        print(f"  {mp3_file_name} already exists in {MUSIC_DIR}. Skipping download and conversion.")
        return

    # Create a unique directory for each bsr_id
    bsr_dir = os.path.join(TEMP_DIR, bsr_id)
    if not os.path.exists(bsr_dir):
        os.makedirs(bsr_dir)

    zip_file_path = os.path.join(bsr_dir, f"{bsr_id}.zip")

    # Download the ZIP file
    response = requests.get(zip_url)
    if response.status_code == 200:
        with open(zip_file_path, 'wb') as file:
            file.write(response.content)
        print(f"  Downloaded {bsr_id} to {zip_file_path}")

        # Unzip the file into the bsr_id directory
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(bsr_dir)
        print(f"  Extracted {bsr_id} in {bsr_dir}")

        # Rename the .egg file to {bsr_id}.ogg
        egg_files = glob.glob(os.path.join(bsr_dir, "*.egg"))
        if egg_files:
            ogg_file_path = os.path.join(bsr_dir, f"{bsr_id}.ogg")
            os.rename(egg_files[0], ogg_file_path)
            print(f"  Renamed {egg_files[0]} to {bsr_id}.ogg")

            AudioSegment.from_ogg(ogg_file_path).export(mp3_file_path, format="mp3")
            print(f"  Converted {bsr_id}.ogg to {mp3_file_name} and moved to {MUSIC_DIR}")
    else:
        print(f"! Failed to download {bsr_id} from {zip_url}")

    # Remove the bsr_id directory and its contents
    shutil.rmtree(bsr_dir)
    print(f"  Removed directory and contents: {bsr_dir}")


def main():
    # Create MUSIC_DIR if it doesn't exist
    if not os.path.exists(MUSIC_DIR):
        os.makedirs(MUSIC_DIR)

    bsrs_json_files = ["bsrs_ranking.json", "bsrs_mapper_misterlihao.json"]

    for bsrs_json_file in bsrs_json_files:
        if not os.path.exists(bsrs_json_file):
            print(f"! File not found: {bsrs_json_file}")
            continue

        with open(bsrs_json_file, "r", encoding="utf-8") as json_file:
            bsrs = json.load(json_file)

        # Ensure the TEMP_DIR exists
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)

        for i, bsr in enumerate(bsrs):
            print(f"{i} {bsr['id']} {bsr['versions'][0]['downloadURL']}")
            get_bsr_music(bsr_id=bsr["id"], name=bsr["name"], zip_url=bsr["versions"][0]["downloadURL"])
            #break
            #if i > 10:
            #    break

    # List all files in the MUSIC_DIR and write to musics.txt
    with open("musics.txt", "w", encoding="utf-8") as f:
        for file_name in os.listdir(MUSIC_DIR):
            f.write(f"{file_name}\n")
        print("Written file names to musics.txt")


if __name__ == "__main__":
    main()
