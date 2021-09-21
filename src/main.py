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
    n, m, t = map(int, (n, m, t))
    watcher = ServerWatcher(n, m, t)
    for line in sys.stdin:
        date, addr, resp = read_input(line.strip())
        watcher.ping(date, addr, resp)
    watcher.finalize()

if __name__ == '__main__':
    main(sys.argv)
