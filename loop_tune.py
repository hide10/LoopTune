import yt_dlp
import subprocess
import time

# 🔧 設定項目
SEARCH_QUERY = "BABYMETAL"
MIN_DURATION_SECONDS = 180   # 最低1時間（180秒）の動画だけ再生
MAX_RESULTS = 10             # 1回の検索で取得する動画数
PLAYED_URLS_FILE = "played_urls.txt"

def search_videos(query, max_results=10, min_duration=0):
    ydl_opts = {
        'quiet': True,
        'extract_flat': False,
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
        'default_search': 'ytsearch',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"🔍 検索ワード: {query}")
        try:
            results = ydl.extract_info(f"{query}", download=False)
        except Exception as e:
            print(f"⚠️ 検索中にエラー: {e}")
            return []

        filtered = [
            entry for entry in results.get('entries', [])[:max_results]
            if entry.get('duration') and entry['duration'] >= min_duration
        ]
        return filtered

def play_video(url):
    try:
        subprocess.run(["mpv", "--no-terminal", url])
    except FileNotFoundError:
        print("❌ mpv が見つかりません。インストールされているか確認してください。")

def load_played_urls():
    try:
        with open(PLAYED_URLS_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_played_url(url):
    with open(PLAYED_URLS_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")

def filter_unplayed_urls(url_list):
    played = load_played_urls()
    return [url for url in url_list if url not in played]

def main():
    print("🎧 LoopTune 起動しました。Ctrl+C で終了できます。\n")
    while True:
        videos = search_videos(SEARCH_QUERY, MAX_RESULTS, MIN_DURATION_SECONDS)
        if not videos:
            print("⏳ 条件に合う動画が見つかりませんでした。10秒待機して再試行します。")
            time.sleep(10)
            continue

        unplayed_videos = filter_unplayed_urls([video['webpage_url'] for video in videos])
        if not unplayed_videos:
            print("✅ すべての動画を再生済みです。10秒待機して再試行します。")
            time.sleep(10)
            continue

        for video in videos:
            if video['webpage_url'] in unplayed_videos:
                print(f"\n▶️ 再生中: {video['title']}\nURL: {video['webpage_url']}\n")
                play_video(video['webpage_url'])
                save_played_url(video['webpage_url'])

if __name__ == "__main__":
    main()
