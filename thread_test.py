import threading
import time
import queue
import sys

# Queue to hold counter values sent between threads
counter_queue = queue.Queue()
# Event object to signal threads to stop
stop_event = threading.Event()

# Function for the producer thread to increment the counter and send it to the other thread
def producer():
    counter = 0
    while not stop_event.is_set():
        counter += 1
        counter_queue.put(counter)  # Put the counter value in the queue
        time.sleep(0.5)  # Simulate some work in the producer thread

# Function for the consumer thread to wait for a new counter value and print it
def consumer():
    while not stop_event.is_set():
        try:
            counter_value = counter_queue.get(timeout=1)  # Wait for a new counter value
            print(f"Received counter value: {counter_value}")
            counter_queue.task_done()  # Mark the task as done
        except queue.Empty:
            # If the queue is empty, check if we should stop
            continue

# Create and start the producer and consumer threads
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()

try:
    # Keep the main thread running to catch Ctrl+C
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Main thread received shutdown signal.")
    stop_event.set()  # Signal both threads to stop

# Wait for both threads to exit
producer_thread.join()
consumer_thread.join()
sys.exit(0)
