#!/usr/bin/env python3
import argparse
import time
import psutil
import logging
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Initialize variables to store min, max, and average values
min_cpu_usage = None
max_cpu_usage = None
min_memory_usage = None
max_memory_usage = None

min_memory_used = None
max_memory_used = None
min_memory_free = None
max_memory_free = None

cpu_usages = []
memory_usages = []
memory_used_list = []
memory_free_list = []
timestamps = []
t_objects = []

def log_performance(log_file):
    global min_cpu_usage, max_cpu_usage, min_memory_usage, max_memory_usage
    global min_memory_used, max_memory_used, min_memory_free, max_memory_free
    global cpu_usages, memory_usages, memory_used_list, memory_free_list, timestamps, t_objects
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    t_object = datetime.now()
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    memory_total = memory_info.total // (1024 * 1024)
    memory_used = memory_info.used // (1024 * 1024)
    memory_free = memory_info.available // (1024 * 1024)

    # Update min and max CPU usage, excluding 0 and 100
    if 0 < cpu_usage < 100:
        if min_cpu_usage is None or cpu_usage < min_cpu_usage:
            min_cpu_usage = cpu_usage
        if max_cpu_usage is None or cpu_usage > max_cpu_usage:
            max_cpu_usage = cpu_usage

    # Update min and max memory usage, excluding 0 and 100
    if 0 < memory_usage < 100:
        if min_memory_usage is None or memory_usage < min_memory_usage:
            min_memory_usage = memory_usage
        if max_memory_usage is None or memory_usage > max_memory_usage:
            max_memory_usage = memory_usage

    # Update min and max memory used and free
    if min_memory_used is None or memory_used < min_memory_used:
        min_memory_used = memory_used
    if max_memory_used is None or memory_used > max_memory_used:
        max_memory_used = memory_used

    if min_memory_free is None or memory_free < min_memory_free:
        min_memory_free = memory_free
    if max_memory_free is None or memory_free > max_memory_free:
        max_memory_free = memory_free

    # Append current usage to lists for aggregate statistics
    cpu_usages.append(cpu_usage)
    memory_usages.append(memory_usage)
    memory_used_list.append(memory_used)
    memory_free_list.append(memory_free)
    timestamps.append(timestamp)
    t_objects.append(t_object)

    log_message = (f"{timestamp} - CPU Usage: {cpu_usage}% "
                   f"- Memory Usage: {memory_usage}% (Total: {memory_total}MB, Used: {memory_used}MB, Free: {memory_free}MB)")
    logging.info(log_message)
    with open(log_file, "a") as f:
        f.write(log_message + "\n")

def plot_metrics():
    plt.figure(figsize=(14, 8))
    
    # Generate relative timestamps in seconds for plotting
    start_time = t_objects[0]
    relative_time = [(t - start_time).total_seconds() for t in t_objects]

    plt.subplot(2, 2, 1)
    plt.plot(relative_time, cpu_usages, label='CPU Usage (%)', color='r')
    plt.xlabel('Time (seconds)')
    plt.ylabel('CPU Usage (%)')
    plt.title('CPU Usage Over Time')
    plt.xticks(rotation=45)
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.plot(relative_time, memory_usages, label='Memory Usage (%)', color='b')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Memory Usage (%)')
    plt.title('Memory Usage Over Time')
    plt.xticks(rotation=45)
    plt.legend()

    plt.subplot(2, 2, 3)
    plt.plot(relative_time, memory_used_list, label='Memory Used (MB)', color='g')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Memory Used (MB)')
    plt.title('Memory Used Over Time')
    plt.xticks(rotation=45)
    plt.legend()

    plt.subplot(2, 2, 4)
    plt.plot(relative_time, memory_free_list, label='Memory Free (MB)', color='m')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Memory Free (MB)')
    plt.title('Memory Free Over Time')
    plt.xticks(rotation=45)
    plt.legend()

    plt.tight_layout()
    plot_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    plt.savefig(f'metrics_{plot_time}.png')

def main(timeout):
    log_file = "server_performance.log"
    start_time = time.time()

    while True:
        log_performance(log_file)
        time.sleep(1)

        if time.time() - start_time >= timeout:
            break

    # Calculate min, max, and average CPU and memory usage
    if cpu_usages:
        min_cpu = min(cpu_usages)
        max_cpu = max(cpu_usages)
        avg_cpu = round(sum(cpu_usages) / len(cpu_usages), 2)
    else:
        min_cpu, max_cpu, avg_cpu = None, None, None

    if memory_usages:
        min_memory = min(memory_usages)
        max_memory = max(memory_usages)
        avg_memory = round(sum(memory_usages) / len(memory_usages), 2)
    else:
        min_memory, max_memory, avg_memory = None, None, None

    if memory_used_list:
        min_memory_used_val = min(memory_used_list)
        max_memory_used_val = max(memory_used_list)
        avg_memory_used = round(sum(memory_used_list) / len(memory_used_list), 2)
    else:
        min_memory_used_val, max_memory_used_val, avg_memory_used = None, None, None

    if memory_free_list:
        min_memory_free_val = min(memory_free_list)
        max_memory_free_val = max(memory_free_list)
        avg_memory_free = round(sum(memory_free_list) / len(memory_free_list), 2)
    else:
        min_memory_free_val, max_memory_free_val, avg_memory_free = None, None, None

    # Write aggregate statistics to log file
    logging.info("\nAggregate Statistics:")
    logging.info(f"Min CPU Usage: {min_cpu}%\tMax CPU Usage: {max_cpu}%\tAvg CPU Usage: {avg_cpu}%")
    logging.info(f"Min Memory Usage: {min_memory}%\tMax Memory Usage: {max_memory}%\tAvg Memory Usage: {avg_memory}%")
    logging.info(f"Min Memory Used: {min_memory_used_val}MB\tMax Memory Used: {max_memory_used_val}MB\tAvg Memory Used: {avg_memory_used}MB")
    logging.info(f"Min Memory Free: {min_memory_free_val}MB\tMax Memory Free: {max_memory_free_val}MB\tAvg Memory Free: {avg_memory_free}MB")


    plot_metrics()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor server performance.")
    parser.add_argument("timeout", type=int, help="Timeout in seconds")
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.INFO,
                        format="%(message)s",
                        handlers=[
                            logging.FileHandler("server_performance.log"),
                            logging.StreamHandler()
                        ])

    main(args.timeout)
