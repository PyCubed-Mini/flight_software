import time

def collect():
    """
    To emulate the gc.collect() function, we just sleep for a bit.
    """
    time.sleep(0.02)

def mem_free():
    """
    Just return a constant value for memory free for now.
    """
    return 1024 * 24  # 24 KB
