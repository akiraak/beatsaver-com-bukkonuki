import argparse
import json
import os


def get_bsrs(min_nps: float, max_nps:float):
    bsrs_json_files = ["bsrs_ranking.json", "bsrs_mapper_misterlihao.json"]

    bsrs = []

    for bsrs_json_file in bsrs_json_files:
        if not os.path.exists(bsrs_json_file):
            print(f"! File not found: {bsrs_json_file}")
            continue

        with open(bsrs_json_file, "r", encoding="utf-8") as json_file:
            bsrs_json = json.load(json_file)
        for bsr_json in bsrs_json:
            for bsr_map in bsr_json['versions'][0]['diffs']:
                if min_nps <= bsr_map['nps'] and bsr_map['nps'] <= max_nps:
                    bsrs.append(bsr_json)
                    break

    return bsrs


def show_bsrs(min_nps: float, max_nps:float):
    print(f"min_nps: {min_nps} max_nps: {max_nps}")
    print("")

    bsrs = get_bsrs(min_nps=min_nps, max_nps=max_nps)

    # bsr['stats']['score'] で降順にソート
    bsrs = sorted(bsrs, key=lambda bsr: bsr['stats']['score'], reverse=True)

    SHOW_BSRS = 10

    for bsr in bsrs[:SHOW_BSRS]:
        hit = False
        for bsr_map in bsr['versions'][0]['diffs']:
            if min_nps <= bsr_map['nps'] and bsr_map['nps'] <= max_nps:
                hit = True
                break

        if hit:
            print(f"{bsr['id']} [+{bsr['stats']['upvotes']} {bsr['stats']['score']}] {bsr['name']}")
            minutes, seconds = divmod(bsr['metadata']['duration'], 60)
            print(f"  ", end="")
            for bsr_map in bsr['versions'][0]['diffs']:
                if min_nps <= bsr_map['nps'] and bsr_map['nps'] <= max_nps:
                    print(f"[{bsr_map['difficulty']} NPS: {bsr_map['nps']}]", end=" ")
            print(f"Duration: {minutes:02d}:{seconds:02d} BPM: {bsr['metadata']['bpm']}\n")

    print(f"Showed {SHOW_BSRS} / {len(bsrs)} bsrs")


def main():
    parser = argparse.ArgumentParser(description="NPSで絞り込んだ譜面を表示する")
    parser.add_argument("--min-nps", type=float, help="Min NPS")
    parser.add_argument("--max-nps", type=float, help="Max NPS")
    args = parser.parse_args()

    show_bsrs(min_nps=args.min_nps, max_nps=args.max_nps)


if __name__ == "__main__":
    main()