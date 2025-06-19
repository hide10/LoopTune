from datetime import datetime
from babymetal_city import get_latest_babymetal_city

cutoff_date = datetime.today().date()
results = []

# 最大10件まで繰り返し取得
for _ in range(10):
    result = get_latest_babymetal_city(cutoff_date)
    if not result:
        break
    city, day = result
    results.append((city, day))
    cutoff_date = day  # 取得済みの日付を次の cutoff として更新

# 結果を表示
for idx, (city, day) in enumerate(results, start=1):
    print(f"{idx}. {city}（{day.isoformat()}）")
