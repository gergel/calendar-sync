import time
from sync import run_sync

INTERVAL = 180  # 3 perc

while True:
    try:
        print("Running sync...")
        run_sync()
    except Exception as e:
        print("ERROR:", e)

    time.sleep(INTERVAL)
