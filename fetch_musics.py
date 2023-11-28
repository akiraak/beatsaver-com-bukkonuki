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
    # 最終的なファイル名は {bsr_id} + 曲名の先頭20文字 + .mp3 とする
    sanitized_name = f"{bsr_id}_{name.replace(' ', '_').replace('/', '_')[:20]}"
    mp3_file_name = f"{sanitized_name}.mp3"
    mp3_file_path = os.path.join(MUSIC_DIR, mp3_file_name)

    # 既にmp3ファイルが存在する場合はダウンロードと変換をスキップする
    if os.path.exists(mp3_file_path):
        print(f"  {mp3_file_name} already exists in {MUSIC_DIR}. Skipping download and conversion.")
        return

    # bsr用の一時作業ディレクトリを作成
    bsr_dir = os.path.join(TEMP_DIR, bsr_id)
    if not os.path.exists(bsr_dir):
        os.makedirs(bsr_dir)

    zip_file_path = os.path.join(bsr_dir, f"{bsr_id}.zip")

    # zipファイルをダウンロード
    response = requests.get(zip_url)
    if response.status_code == 200:
        # zipファイルを保存
        with open(zip_file_path, 'wb') as file:
            file.write(response.content)
        print(f"  Downloaded {bsr_id} to {zip_file_path}")

        # zipファイルを解凍
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(bsr_dir)
        print(f"  Extracted {bsr_id} in {bsr_dir}")

        egg_files = glob.glob(os.path.join(bsr_dir, "*.egg"))
        if egg_files:
            #　eggファイルをoggファイルにリネーム
            ogg_file_path = os.path.join(bsr_dir, f"{bsr_id}.ogg")
            os.rename(egg_files[0], ogg_file_path)
            print(f"  Renamed {egg_files[0]} to {bsr_id}.ogg")

            # oggファイルをmp3ファイルに変換
            AudioSegment.from_ogg(ogg_file_path).export(mp3_file_path, format="mp3")
            print(f"  Converted {bsr_id}.ogg to {mp3_file_name} and moved to {MUSIC_DIR}")
    else:
        print(f"! Failed to download {bsr_id} from {zip_url}")

    # 一時作業ディレクトリを削除
    shutil.rmtree(bsr_dir)
    print(f"  Removed directory and contents: {bsr_dir}")


def main():
    # 一時作業ディレクトリを作成
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    # 音楽ファイルを保存するディレクトリを作成
    if not os.path.exists(MUSIC_DIR):
        os.makedirs(MUSIC_DIR)

    bsrs_json_files = ["bsrs_ranking.json", "bsrs_mapper_misterlihao.json"]

    for bsrs_json_file in bsrs_json_files:
        if not os.path.exists(bsrs_json_file):
            print(f"! File not found: {bsrs_json_file}")
            continue

        with open(bsrs_json_file, "r", encoding="utf-8") as json_file:
            bsrs = json.load(json_file)

        for i, bsr in enumerate(bsrs):
            print(f"{i} {bsr['id']} {bsr['versions'][0]['downloadURL']}")
            get_bsr_music(bsr_id=bsr["id"], name=bsr["name"], zip_url=bsr["versions"][0]["downloadURL"])

    # musics ディレクトリにあるファイル名を musics.txt に書き出す
    with open("musics.txt", "w", encoding="utf-8") as f:
        for file_name in os.listdir(MUSIC_DIR):
            f.write(f"{file_name}\n")
        print("Written file names to musics.txt")


if __name__ == "__main__":
    main()
