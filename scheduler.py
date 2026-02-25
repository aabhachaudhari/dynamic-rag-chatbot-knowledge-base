import schedule
import time
import os

def run_update():
    os.system("python update.py")

# Run every 24 hours (you can change this)
schedule.every(24).hours.do(run_update)

print("⏰ Scheduler started. Updating knowledge base every 24 hours...")

while True:
    schedule.run_pending()
    time.sleep(60)