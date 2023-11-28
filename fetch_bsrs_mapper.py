import json
import requests
import time


# マッパーさんの譜面を取得する
def user_bsr_ids(user_id: str):
    url = f"https://api.beatsaver.com/users/id/{user_id}/playlist"
    bsr_ids = []

    response = requests.get(url)
    if response.status_code == 200:
        response_json = response.json()
        for song in response_json["songs"]:
            bsr_ids.append(song["key"])
    else:
        print(f"Error fetching data for {url}")

    return bsr_ids


def main():
    BSRS_PER_ONCE = 50
    USER_ID = "4284977"  # misterlihao

    bsr_ids = user_bsr_ids(USER_ID)
    bsrs = []

    # 譜面データを取得する
    for i in range(0, len(bsr_ids), BSRS_PER_ONCE):
        fetch_ber_ids = bsr_ids[i : i + BSRS_PER_ONCE]

        ids_param = ",".join(fetch_ber_ids)
        url = f"https://api.beatsaver.com/maps/ids/{ids_param}"
        response = requests.get(url)
        if response.status_code == 200:
            response_json = response.json()
            print(
                f"Fetching {len(response_json)} bsrs: {i + 1} - {i + len(response_json)} / {len(bsr_ids)}"
            )
            for id, bsr in response_json.items():
                bsrs.append(bsr)
        else:
            print(f"Error fetching data for {url}")

        time.sleep(5)

    # id, タイトルなどをファイルに保存
    with open("bsrs_mapper_misterlihao_summary.txt", "w", encoding="utf-8") as list_file:
        for i, bsr in enumerate(bsrs):
            print(
                f"{i + 1}: {bsr['id']} [+{bsr['stats']['upvotes']} {bsr['stats']['score']}]: {bsr['name']}"
            )
            list_file.write(
                f"{i + 1}: {bsr['id']} [+{bsr['stats']['upvotes']} {bsr['stats']['score']}]: {bsr['name']}\n"
            )

    # 全ての情報をファイルに保存
    with open("bsrs_mapper_misterlihao.json", "w", encoding="utf-8") as json_file:
        json.dump(bsrs, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
