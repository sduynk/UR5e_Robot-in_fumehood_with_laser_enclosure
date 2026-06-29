import time
import subprocess
import threading
from datetime import datetime
import pandas as pd
from collections import deque

# Load schedule from CSV
def load_schedule(csv_path):
    df = pd.read_csv(csv_path)
    schedule = {}
    for _, row in df.iterrows():
        t = row['time']
        rack = int(row['rack_number'])
        if t not in schedule:
            schedule[t] = []
        schedule[t].append(rack)
    return schedule

# Initialize
schedule = load_schedule("schedule/rack_schedule_Rack1and2and3.csv") #rack_schedule_onlyrack1.csv rack_schedule_Rack1and2.csv rack_schedule_Rack1and2and3.csv
executed_times = set()
task_queue = deque()
last_day = datetime.now().day
current_task_running = False

# Robot runner function (runs in background thread)
def robot_runner(rack_numbers):
    global current_task_running
    args = ["python3", "Execution_rack.py"]
    for rack in rack_numbers:
        args += ["--rack_number", str(rack)]
    args += ["--loop", "1"]

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running:", ' '.join(args))
    subprocess.run(args)

    # After subprocess is done
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Finished running racks: {rack_numbers}")
    current_task_running = False

# Main loop
while True:
    now = datetime.now()
    time_str = now.strftime("%H:%M")

    # Reset at new day
    if now.day != last_day:
        executed_times.clear()
        last_day = now.day
        print(f"[{now.strftime('%Y-%m-%d')}] New day, schedule reset.")

    for sched_time in schedule:
        sched_dt = datetime.strptime(sched_time, "%H:%M")
        sched_datetime = now.replace(hour=sched_dt.hour, minute=sched_dt.minute, second=0, microsecond=0)
        delta_seconds = (sched_datetime - now).total_seconds()

        # Only add task if scheduled time is "now" or in next 10 seconds
        if 0 <= delta_seconds < 10 and sched_time not in executed_times:
            print(f"[{now.strftime('%H:%M:%S')}] Adding task for time {sched_time} to queue.")
            task_queue.append(schedule[sched_time])
            executed_times.add(sched_time)

    if not current_task_running and task_queue:
        current_task_running = True
        next_rack_numbers = task_queue.popleft()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting robot thread for racks: {next_rack_numbers}")
        threading.Thread(target=robot_runner, args=(next_rack_numbers,)).start()
        
    time.sleep(10)  # Check every 10 seconds
