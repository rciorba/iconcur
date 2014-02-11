import sys
import threading
from Queue import Queue

from PIL import Image


SIZE = 1023
MAX_ITER = 100
WORKERS = 8


img = Image.new("RGB", (SIZE+1, SIZE+1))


def carthesiza_2_complex(point):
    """maps the 0-SIZE range to -2 1 (x axis) and -1.5 1.5 (y axis)"""
    x, y = point
    size = float(SIZE)
    x = (-2 + (x/size)*3)
    y = (-1.5 + (y/size)*3)
    return complex(x, y)

def complex_2_carthesian(point):
    x = int((point.real+2)/3 * SIZE)
    y = int((point.imag+1.5)/3 * SIZE)
    return x, y


def render(x, y):
    # if (0 <= x < SIZE) and (0 <= y < SIZE):
    # x, y = complex_2_carthesian(point)
    # pixel_value = img.getpixel((x, y))[0] + 1
    img.putpixel((x, y), (255, 255, 255))


def brot_orbit(point):
    iterations = 0
    z = point
    while (iterations < MAX_ITER) and ((z.imag**2 + z.real**2) < 4):
        z = z**2 + point
        iterations += 1
    return iterations


def subregion(region_x, region_y, size):
    for x in xrange(region_x, region_x+size):
        for y in xrange(region_y, region_y+size):
            point = carthesiza_2_complex((x, y))
            iterations = brot_orbit(point)
            if iterations == MAX_ITER:
                render(x, y)

class Worker(threading.Thread):
    def __init__(self, job_q):
        super(Worker, self).__init__()
        self.job_q = job_q

    def run(self):
        while True:
            job = self.job_q.get()
            if job is None:
                return
            x, y, region_size = job
            subregion(x, y, region_size)


def main():
    job_q = Queue()
    workers = [Worker(job_q) for _ in xrange(WORKERS)]
    [w.start() for w in workers]
    region_size = 64
    for x in xrange(0, SIZE+1, region_size):
        for y in xrange(0, SIZE+1, region_size):
            # subregion(x, y, region_size)
            job_q.put((x, y, region_size))
    for _ in xrange(WORKERS):
        job_q.put(None)
    for worker in workers:
        worker.join()
    img.save("brot.bmp", "BMP")


if __name__ == "__main__":
    main()
