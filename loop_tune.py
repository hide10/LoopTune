import yt_dlp
import subprocess
import time
import json
import os
import win32file  # pip install pywin32
import pywintypes

# 🔧 設定項目
SEARCH_QUERY = "BABYMETAL"
MIN_DURATION_SECONDS = 180           # 3分以上
MAX_RESULTS = 5
PLAYED_URLS_FILE = "played_urls.txt"
MPV_IPC_PATH = r'\\.\\pipe\\mpvsocket'  # Windows Named Pipe path

# 🏃‍♂️ mpv IPC サーバ確認
def is_mpv_running() -> bool:
    return os.path.exists(MPV_IPC_PATH)

# 🎮 mpv に JSON コマンド送信（Windows Named Pipe）
def send_to_mpv(command_dict: dict) -> bool:
    message = (json.dumps(command_dict) + '\n').encode('utf-8')
    try:
        handle = win32file.CreateFile(
            MPV_IPC_PATH,
            win32file.GENERIC_WRITE,
            0, None,
            win32file.OPEN_EXISTING,
            0, None
        )
        win32file.WriteFile(handle, message)
        handle.close()
        return True
    except pywintypes.error as e:
        print(f"⚠️ mpv にコマンド送信できませんでした: {e}")
        return False

# 🚀 mpv をバックグラウンドで起動
def launch_mpv_ipc():
    print("📺 mpv をバックグラウンドで起動します...")
    subprocess.Popen([
        "mpv",
        "--idle=yes",
        "--force-window=yes", # ウィンドウを強制的に表示
        f"--input-ipc-server={MPV_IPC_PATH}",
        "--geometry=300:200"
    ])

# 🕑 再生終了イベントを待つ
def wait_for_end():
    try:
        handle = win32file.CreateFile(
            MPV_IPC_PATH,
            win32file.GENERIC_READ,
            0, None,
            win32file.OPEN_EXISTING,
            0, None
        )
        buffer = b""
        while True:
            _, data = win32file.ReadFile(handle, 4096)
            buffer += data
            while b'\n' in buffer:
                line, buffer = buffer.split(b'\n', 1)
                if not line:
                    continue
                try:
                    obj = json.loads(line.decode('utf-8'))
                    if obj.get("event") == "end-file":
                        handle.close()
                        return
                except json.JSONDecodeError:
                    continue
    except pywintypes.error as e:
        print(f"⚠️ mpv イベント受信エラー: {e}")

# 🔍 動画検索
def search_videos(query, max_results=10, min_duration=0):
    ydl_opts = {
        'quiet': True,
        'extract_flat': False,
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
        'default_search': f'ytsearch{max_results}',
        'socket_timeout': 10,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"🔍 検索ワード: {query}")
        try:
            results = ydl.extract_info(query, download=False)
        except Exception as e:
            print(f"⚠️ 検索中にエラー: {e}")
            return []
        return [
            e for e in results.get('entries', [])[:max_results]
            if e.get('duration') and e['duration'] >= min_duration
        ]

# 📜 再生履歴
def load_played_urls():
    try:
        with open(PLAYED_URLS_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_played_url(url):
    with open(PLAYED_URLS_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")

# ▶️ 再生
def play_video(url):
    if send_to_mpv({"command": ["loadfile", url, "replace"]}):
        print("🎵 動画を切り替えました")
    else:
        print("❌ 動画の切り替えに失敗しました。mpv が起動しているか確認してください。")

# 🌀 メインループ
def main():
    print("🎧 LoopTune (IPC モード) 起動しました。Ctrl+C で終了できます。\n")
    if not is_mpv_running():
        launch_mpv_ipc()
        time.sleep(2)  # 起動待ち

    while True:
        videos = search_videos(SEARCH_QUERY, MAX_RESULTS, MIN_DURATION_SECONDS)
        if not videos:
            print("⏳ 条件に合う動画がありません。10秒待機して再試行します。")
            time.sleep(10)
            continue

        played = load_played_urls()
        unplayed = [v for v in videos if v['webpage_url'] not in played]
        if not unplayed:
            print("✅ すべて再生済み。履歴をクリアしてループ再開します。")
            os.remove(PLAYED_URLS_FILE)
            continue

        for v in unplayed:
            url = v['webpage_url']
            print(f"\n▶️ 再生中: {v['title']}\nURL: {url}\n")
            play_video(url)
            save_played_url(url)
            wait_for_end()  # 再生終了を待つ

if __name__ == "__main__":
    main()
