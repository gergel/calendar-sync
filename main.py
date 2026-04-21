import time
from sync import run_sync

while True:
    try:
        print("SYNC START")
        run_sync()
        print("SYNC DONE")
    except Exception as e:
        print("ERROR:", e)

    time.sleep(180)
