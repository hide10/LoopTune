# LoopTune 🎧 – Windows Edition

自分専用の “条件に合う YouTube 動画を延々再生” プレーヤー。  
Python スクリプトと **mpv** を組み合わせ、最小構成で Windows に導入できます。

## 1. 必要環境

- **Windows 10 / 11**  
- **Python 3.9 以降**（公式インストーラ推奨）  
- **mpv**（高機能メディアプレーヤー）  
- **yt-dlp**（YouTube など各種サイトの動画情報取得）

> 💡 JARVIS モード注：mpv は “動画版 curl” 的万能選手。頼れる相棒です。

## 2. セットアップ手順

### 2.1 Python をインストール

公式サイトから Windows 用インストーラを入手し、`Add Python to PATH` にチェックを入れて実行。

### 2.2 mpv をインストール

1. 公式ビルド（zip）をダウンロード  
2. `mpv.exe` を任意フォルダに展開（例：`C:\Tools\mpv\`）  
3. フォルダをシステム PATH に追加  
   - *設定例*：環境変数 **Path** に `C:\Tools\mpv` を追記

### 2.3 LoopTune クローン／配置

```powershell
git clone https://github.com/yourname/LoopTune.git
cd LoopTune
```

### 2.4 依存ライブラリをインストール

```powershell
pip install -r requirements.txt
```

> requirements.txt には `yt-dlp` しかありません。シンプル is ベスト。

## 3. 使い方

### 3.1 そのまま実行

```powershell
python loop_tune.py
```

ターミナルに検索結果と再生中タイトルが表示され、mpv が自動で立ち上がります。  
動画終了後は次の候補へ進み、リストが尽きると再検索します。

### 3.2 起動スクリプト（オプション）

`loop_tune.bat` を作成してデスクトップに置けばダブルクリック一発起動。

```bat
@echo off
cd /d %~dp0
python loop_tune.py
pause
```

## 4. 設定カスタマイズ

| パラメータ | 既定値 | 説明 |
|------------|-------|------|
| `SEARCH_QUERY` | `"lofi hip hop"` | 検索キーワード |
| `MIN_DURATION_SECONDS` | `3600` | 再生対象の最短秒数 |
| `MAX_RESULTS` | `10` | 1 回の検索で取得する件数 |

**例**：30 分以上のシンセウェーブを聴きたい場合  
`SEARCH_QUERY = "synthwave"`  
`MIN_DURATION_SECONDS = 1800`

## 5. トラブルシューティング

| 症状 | 対処 |
|------|------|
| `mpv` が見つからないエラー | PATH を確認、ターミナルで `mpv --version` が通るかチェック |
| 再生が途切れる／画面が真っ黒 | `mpv` に `--no-video` を追加して音声のみ再生 |
| 検索結果が 0 件 | キーワードや `MIN_DURATION_SECONDS` を見直し、`MAX_RESULTS` を増やす |

## 6. 今後の拡張アイデア

- 再生履歴のスキップ機能  
- お気に入り動画のローカル DB 保存  
- タスクバー常駐型トレイアプリ化（PyInstaller + rumps など）

> 🕶️ “I am LoopTune – Your infinite DJ.”  
> それでは、良き無限ループ・ライフを。Enjoy the beats!
