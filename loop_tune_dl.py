import subprocess
import yt_dlp
from pathlib import Path
from yt_dlp import YoutubeDL
from babymetal_city import get_latest_babymetal_city
from datetime import datetime, timedelta

def search_videos(query, max_results=10, min_duration=0, max_duration=None):
    ydl_opts = {
        'quiet': True,
        'extract_flat': False,
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
        'default_search': f'ytsearch{max_results}',
        'socket_timeout': 10,
    }

    one_year_ago = datetime.now() - timedelta(days=365)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"🔍 検索ワード: {query}")
        try:
            results = ydl.extract_info(query, download=False)
        except Exception as e:
            print(f"⚠️ 検索中にエラー: {e}")
            return []

        filtered = []
        for entry in results.get('entries', [])[:max_results]:
            duration = entry.get('duration')
            upload_date_str = entry.get('upload_date')  # e.g. '20240615'
            if not duration or duration < min_duration:
                continue
            if upload_date_str:
                try:
                    upload_date = datetime.strptime(upload_date_str, "%Y%m%d")
                    if upload_date < one_year_ago:
                        continue
                except ValueError:
                    continue
            filtered.append(entry)

        return filtered


def download(video_id, out_dir: Path):
    """指定動画IDをyt-dlpでダウンロードする。"""
    url = f"https://www.youtube.com/watch?v={video_id}"
    cmd = [
        "yt-dlp", url,
        "--output", str(out_dir / "%(upload_date)s_%(title)s.%(ext)s"),
        "--restrict-filenames",
        "--format", "bv*+ba/best",
        "--no-playlist"
    ]
    print(f"⬇️ ダウンロード: {url}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ ダウンロード失敗: {e}")


if __name__ == "__main__":
    city = get_latest_babymetal_city()
    if not city:
        print("❌ 最新都市が取得できませんでした。")
        exit(1)

    print(f"📍 最新ライブ都市: {city}")

    query = f'BABYMETAL {city.split(",")[0]}'  # Atlanta, GA, USA → Atlanta
    save_dir = Path("downloads") / city
    save_dir.mkdir(parents=True, exist_ok=True)

    min_sec = 15
    max_sec = 240

    videos = search_videos(query, max_results=10, min_duration=min_sec, max_duration=max_sec)

    if not videos:
        print("⚠️ 該当動画が見つかりませんでした。")
    else:
        for v in videos:
            download(v["id"], save_dir)

    print("✅ 全処理完了")
