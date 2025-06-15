import time

def wait_until(condition_fn, timeout=30, interval=0.5):
    start = time.time()
    while time.time() - start < timeout:
        if condition_fn():
            return True
        time.sleep(interval)
    return False


def retry(fn, retries=3, delay=1):
    for i in range(retries):
        try:
            return fn()
        except Exception as e:
            if i == retries - 1:
                raise
            time.sleep(delay)
