#!/usr/bin/python3

import tqdm
import subprocess 
import os
import time

def main():
    # For all the running processes with CMD gem5.opt, create a list with PIDs
    ps = subprocess.Popen(('ps', '-ef'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('grep', 'gem5.opt'), stdin=ps.stdout)
    ps.wait()
    pids = [int(x.split()[1]) for x in output.splitlines()][:-1]
    print(pids)
    iter = tqdm.trange(len(pids))
    while pids:
        for pid in pids:
            if not os.path.exists('/proc/%d' % pid):
                iter.update(1)
                pids.remove(pid)
        time.sleep(1)


if __name__ == '__main__':
    main()