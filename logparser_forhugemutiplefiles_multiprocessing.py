##Log Parser for processing 1000 of files with some 100GB file using all the process of CPU##

import os
import multiprocessing
import time

def listener_process(queue, output_file):
    """
    The 'Sink': Runs on its own core.
    Listens to the Queue and writes alerts to a central file.
    """
    with open(output_file, 'w') as f:
        while True:
            message = queue.get()
            # The "Poison Pill" pattern to stop the listener safely
            if message == "KILL":
                break
            f.write(message + '\n')
            f.flush() # Ensure data hits the disk immediately

def worker_process(filepath, queue, buffer_size=1024*1024):
    """
    The 'Source': Runs on many cores.
    Reads logs and pushes 'ERROR' lines to the Queue immediately.
    """
    try:
        with open(filepath, 'r', buffering=buffer_size, encoding='utf-8', errors='replace') as file:
            for line in file:
                if "ERROR" in line:
                    # PRINCIPAL MOVE: We don't keep it. We push it.
                    # This keeps Worker RAM usage flat/constant.
                    queue.put(f"From {filepath}: {line.strip()}")
    except Exception as e:
        queue.put(f"CRITICAL FAILURE in {filepath}: {e}")

   listener.join()
    print("✅ Aggregation Complete.")
def main():
    # Simulated log files
    log_files = [f"/var/log/node_{i}.log" for i in range(100)]
    output_file = "central_alerts.log"

    # 1. Start the Manager to handle the Shared Queue
    manager = multiprocessing.Manager()
    queue = manager.Queue()

    # 2. Start the Listener (The "Sink")
    # We use a separate Process, not a Pool worker, because it stays alive forever.
    listener = multiprocessing.Process(target=listener_process, args=(queue, output_file))
    listener.start()

    # 3. Start the Workers (The "Beast Mode" Pool)
    num_workers = multiprocessing.cpu_count() - 1 # Leave 1 core for the listener!
    print(f"🔥 Starting {num_workers} Workers + 1 Listener...")
    
    with multiprocessing.Pool(processes=num_workers) as pool:
        # We use starmap to pass multiple arguments (file + queue) to workers
        # Create a list of arguments: [('file1', q), ('file2', q), ...]
        work_items = [(f, queue) for f in log_files]
        
        # This blocks until all files are processed
        pool.starmap(worker_process, work_items)

    # 4. Clean Shutdown
    # Send the "Poison Pill" to tell the listener to stop
    queue.put("KILL")
    listener.join()
    print("✅ Aggregation Complete.")

if __name__ == "__main__":
    main()

