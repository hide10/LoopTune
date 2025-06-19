import requests
from bs4 import BeautifulSoup
from datetime import datetime, date

def get_latest_babymetal_city(cutoff_date: date | None = None) -> tuple[str, date] | None:
    """
    Setlist.fm から BABYMETAL の直近（cutoff_date より前）の
    ライブ開催地と日付を返す。

    Parameters
    ----------
    cutoff_date : datetime.date | None
        ・None の場合 : 今日を基準とする
        ・指定した場合 : その日付より前のライブを対象とする

    Returns
    -------
    (都市名, 開催日) のタプル。例: ("Atlanta, GA, USA", date(2025, 6, 18))
    見つからない場合は None
    """
    url = "https://www.setlist.fm/setlists/babymetal-5bd19f80.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache"
    }

    if cutoff_date is None:
        cutoff_date = datetime.today().date()

    response = requests.get(url, headers=headers, timeout=15)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    blocks = soup.select(".col-xs-12.setlistPreview.vevent")

    latest_city = None
    latest_date = datetime.min.date()

    for block in blocks:
        date_tag = block.select_one(".dateBlock .value-title[title]")
        if not date_tag:
            continue

        try:
            date_obj = datetime.strptime(date_tag["title"], "%Y-%m-%d").date()
        except ValueError:
            continue

        if cutoff_date and date_obj >= cutoff_date:
            continue

        # 開催地の抽出（地域がなくても city + country でOKにする）
        locality = block.select_one(".locality")
        region = block.select_one(".region")
        country = block.select_one(".country-name")

        if locality and country:
            if region:
                city_name = f"{locality.text.strip()}, {region.text.strip()}, {country.text.strip()}"
            else:
                city_name = f"{locality.text.strip()}, {country.text.strip()}"
        else:
            continue  # 地域情報があまりに不足していたらスキップ

        if date_obj > latest_date:
            latest_date = date_obj
            latest_city = city_name

    return (latest_city, latest_date) if latest_city else None
