import gevent.monkey
gevent.monkey.patch_all()

import random
import time
import urllib2

import gevent


grc = 0  # global request counter
faliures = 0


def worker(urls, delay=.00001, loops=10):
    global grc, faliures
    urls = list(urls)  # rnadom.shuffle mutates the list
    while loops:
        loops -= 1
        random.shuffle(urls)
        for url in urls:
            resp = urllib2.urlopen(url)
            # print resp.code, url
            if resp.code != 200:
                faliures += 1
            grc += 1
            gevent.sleep(delay)


def main(filename, pool_size=10):
    pool_size = int(pool_size)
    with open(filename) as f:
        urls = f.readlines()
    workers = [gevent.Greenlet(worker, urls) for _ in xrange(pool_size)]
    for w in workers:
        w.start()
    then = time.time()
    old_count = grc
    while any(not(w.ready()) for w in workers):
        gevent.sleep(5)
        now = time.time()
        print (grc - old_count) / (now - then)
        print "failed:", faliures
        then = now
        old_count = grc


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
