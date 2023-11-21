import json
import requests
import time


def main():
    FROM_DATA = "2021-09-01"
    BARS_PER_PAGE = 20
    FETCH_PAGES = 1000
    PAGES = int(FETCH_PAGES / BARS_PER_PAGE)
    bsrs = []

    for i in range(PAGES):
        page = i
        url = f"https://api.beatsaver.com/search/text/{page}?from={FROM_DATA}&sortOrder=Rating"

        print(f"Fetching page: {page + 1} / {PAGES}")
        response = requests.get(url)
        if response.status_code == 200:
            response_json = response.json()
            for bsr in response_json['docs']:
                bsrs.append(bsr)
        else:
            print(f"Error fetching data for {url}")

        time.sleep(5)

    # id, タイトルなどをファイルに保存
    with open("bsrs_ranking_sumarry.txt", "w", encoding="utf-8") as list_file:
        for i, bsr in enumerate(bsrs):
            print(f"{i + 1}: {bsr['id']} [+{bsr['stats']['upvotes']} {bsr['stats']['score']}]: {bsr['name']}")
            list_file.write(f"{i + 1}: {bsr['id']} [+{bsr['stats']['upvotes']} {bsr['stats']['score']}]: {bsr['name']}\n")

    # 全ての情報をファイルに保存
    with open("bsrs_ranking.json", "w", encoding="utf-8") as json_file:
        json.dump(bsrs, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
