import sys
from datetime import datetime
import ipaddress

from serverwatcher import ServerWatcher

def read_input(s):
    d, a, r = s.split(",")
    date = datetime.strptime(d, "%Y%m%d%H%M%S")
    addr = ipaddress.ip_interface(a)
    resp = int(r) if r != '-' else None
    return date, addr, resp

def main(argv):
    _, n, m, t = argv
    timeout_torelance = int(n)
    overload_torelance = int(m)
    overload_threashold = int(t)
    watcher = ServerWatcher(timeout_torelance, overload_torelance)
    for line in sys.stdin:
        date, addr, resp = read_input(line.strip())
        if resp:
            if resp > overload_threashold:
                watcher.ping_abnormal(date, addr, 'overload')
            else:
                watcher.ping_response(date, addr)
        else:
            watcher.ping_abnormal(date, addr, 'timeout')
    watcher.finalize()

if __name__ == '__main__':
    main(sys.argv)
