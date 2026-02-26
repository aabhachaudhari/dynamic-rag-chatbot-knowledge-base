# scheduler.py
# Automatically rebuilds the vector database every 24 hours
# Run this ONCE and leave it running in the background:
#     python scheduler.py

import schedule
import time
import subprocess
import os
from datetime import datetime

LOG_FILE = "last_updated.txt"
INTERVAL_HOURS = 24        # change to 1 for testing


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_message + "\n")


def run_ingest():
    log("Starting scheduled knowledge base update...")
    try:
        result = subprocess.run(
            ["python", "ingest.py"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            log("✓ Knowledge base updated successfully.")
        else:
            log(f"✗ Update failed:\n{result.stderr}")
    except Exception as e:
        log(f"✗ Error running ingest.py: {e}")


def main():
    print("=" * 55)
    print("   AUTO KNOWLEDGE BASE SCHEDULER")
    print(f"   Updates every {INTERVAL_HOURS} hour(s)")
    print("   Press Ctrl+C to stop")
    print("=" * 55)

    # Run once immediately on start
    run_ingest()

    # Then schedule to run every X hours
    schedule.every(INTERVAL_HOURS).hours.do(run_ingest)

    log(f"Scheduler running — next update in {INTERVAL_HOURS} hour(s)")

    while True:
        schedule.run_pending()
        time.sleep(60)      # check every minute


if __name__ == "__main__":
    main()