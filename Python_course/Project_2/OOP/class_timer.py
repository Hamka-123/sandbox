import time

class Timer:
    def __init__(self, duration: float = 0.0):
        self._start = None
        self._elapsed = 0.0
        self.running = False
        self.duration = duration

    def start(self):
        if not self.running:
            self._start = time.time()
            self.running = True

    def pause(self):
        if self.running:
            self._elapsed += time.time() - self._start
            self._start = None
            self.running = False

    def reset(self):
        self._start = None
        self._elapsed = 0.0
        self.running = False

    def stop(self):
        self.pause()
        self.reset()

    @property
    def elapsed(self):
        return self._elapsed + (time.time() - self._start) if self.running else self._elapsed

class CountDownTimer(Timer):
    def __init__(self, seconds):
        super().__init__()
        self.seconds = float(seconds)

    @property
    def remaining(self):
        return max(0.0, self.seconds - self.elapsed)

if __name__ == "__main__":
    t = Timer(1)
    t.start()
    time.sleep(t.duration)
    t.pause()
    print("Elapsed after pause:", t.elapsed)
    time.sleep(t.duration)
    t.start()
    time.sleep(t.duration)
    print("Elapsed before stop:", t.elapsed)
    t.stop()
    print("Elapsed:", t.elapsed)

    cd = CountDownTimer(5)
    cd.start()
    time.sleep(cd.duration)
    cd.stop()
    print("Remaining:", cd.remaining)
    
'''
Elapsed after pause: 1.0050570964813232
Elapsed before stop: 2.009031057357788
Elapsed: 0.0
Remaining: 5.0
'''
