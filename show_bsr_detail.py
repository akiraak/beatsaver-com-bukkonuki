import argparse
import json
import os


def get_bsr(bar_id: str):
    bsrs_json_files = ["bsrs_ranking.json", "bsrs_mapper_misterlihao.json"]

    for bsrs_json_file in bsrs_json_files:
        if not os.path.exists(bsrs_json_file):
            print(f"! File not found: {bsrs_json_file}")
            continue

        with open(bsrs_json_file, "r", encoding="utf-8") as json_file:
            bsrs = json.load(json_file)
        for bsr in bsrs:
            if bsr["id"] == bar_id:
                return bsr

    return None


def show_detail(bar_id: str):
    bsr = get_bsr(bar_id)
    if not bsr:
        print(f"bsr not found: {bar_id}")
        return

    print(f"ID: {bsr['id']}")
    print(f"Name: {bsr['name']}")
    print(f"Description: {bsr['description']}")
    print(f"Mapper: {bsr['uploader']['name']}")
    print(f"BPM: {bsr['metadata']['bpm']}")
    minutes, seconds = divmod(bsr['metadata']['duration'], 60)
    print(f"Duration: {minutes:02d}:{seconds:02d}")
    print(f"👍Upvotes: {bsr['stats']['upvotes']}")
    print(f"👎Downvotes: {bsr['stats']['downvotes']}")
    print(f"Score: {bsr['stats']['score']}")
    print(f"tags: {bsr['tags'] if 'tags' in bsr else ''}")
    print(f"downloadURL: {bsr['versions'][0]['downloadURL']}")
    print(f"coverURL: {bsr['versions'][0]['coverURL']}")
    print(f"previewURL: {bsr['versions'][0]['previewURL']}")
    print(f"bsaber.com: https://bsaber.com/songs/{bar_id}/")
    print(f"beatsaver.com: https://beatsaver.com/maps/{bar_id}")
    print(f"Viewer: https://allpoland.github.io/ArcViewer/?id={bar_id}")
    if 'curatedAt' in bsr:
        print(f"curatedAt: {bsr['curatedAt']}")
    print(f"createdAt: {bsr['createdAt']}")
    print(f"updatedAt: {bsr['updatedAt']}")
    print(f"lastPublishedAt: {bsr['lastPublishedAt']}")
    print("")

    print("--- Maps ---")
    for bsr_map in bsr['versions'][0]['diffs']:
        print(f"{bsr_map['difficulty']}:")
        print(f"  Offset: {bsr_map['offset']}")
        print(f"  NJS: {bsr_map['njs']}")
        print(f"  Notes: {bsr_map['notes']}")
        print(f"  Bombs: {bsr_map['bombs']}")
        print(f"  Obstacles: {bsr_map['obstacles']}")
        print(f"  NPS: {bsr_map['nps']}")
        print(f"  Length: {bsr_map['length']}")
        print(f"  Characteristic: {bsr_map['characteristic']}")
        print(f"  Events: {bsr_map['events']}")
        print(f"  Chroma: {bsr_map['chroma']}")
        print(f"  Me: {bsr_map['me']}")
        print(f"  Ne: {bsr_map['ne']}")
        print(f"  Cinema: {bsr_map['cinema']}")
        print(f"  Seconds: {bsr_map['seconds']}")
        print(f"  MaxScore: {bsr_map['maxScore']}")


def main():
    parser = argparse.ArgumentParser(description="譜面の詳細を表示する")
    parser.add_argument("--bsr", type=str, help="bsr ID")
    args = parser.parse_args()

    show_detail(bar_id=args.bsr)


if __name__ == "__main__":
    main()