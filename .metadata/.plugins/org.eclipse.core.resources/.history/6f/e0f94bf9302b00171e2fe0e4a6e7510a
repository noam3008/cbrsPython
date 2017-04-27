import signal

import time   # For the demo only

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)


interrupted = False
while True:
    print("Working hard...")
    time.sleep(3)
    print("All done!")

    if interrupted:
        print("Gotta go")
        break