import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_latest_babymetal_city():
    """
    Setlist.fmからBABYMETALの最新（過去）ライブの開催地を返す。
    戻り値：例 "Atlanta, GA, USA"
    """
    url = "https://www.setlist.fm/setlists/babymetal-5bd19f80.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    blocks = soup.select(".col-xs-12.setlistPreview.vevent")

    latest_city = None
    latest_date = datetime.min
    today = datetime.today()

    for block in blocks:
        date_tag = block.select_one(".dateBlock .value-title[title]")
        if not date_tag:
            continue

        date_str = date_tag["title"]  # YYYY-MM-DD
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            continue

        if date_obj >= today:
            continue  # 未来のライブは無視

        # 開催地の抽出
        locality = block.select_one(".locality")
        region = block.select_one(".region")
        country = block.select_one(".country-name")

        if locality and region and country:
            city_name = f"{locality.text.strip()}, {region.text.strip()}, {country.text.strip()}"
        else:
            city_name = "不明"

        # 最新の過去日付で更新
        if date_obj > latest_date:
            latest_date = date_obj
            latest_city = city_name

    return latest_city
