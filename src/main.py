import sys
from datetime import datetime
import ipaddress

def read_input(s):
    d, a, r = s.split(",")
    date = datetime.strptime(d, "%Y%m%d%H%M%S")
    addr = ipaddress.ip_interface(a)
    resp = int(r) if r != '-' else None
    return date, addr, resp

def print_downtime(ip, time_from, time_to="now"):
    print(f"{ip} has been down from {time_from} to {time_to}")

class ServerWatcher():
    def __init__(self, torelance):
        self.torelance = torelance
        self.timeouts = {}
    def ping_response(self, date, addr, latency):
        if addr in self.timeouts:
            count, start = self.timeouts[addr]
            if count >= self.torelance:
                print_downtime(addr, start, date)
            del self.timeouts[addr]
    def ping_no_response(self, date, addr):
        if addr not in self.timeouts:
            self.timeouts[addr] = (1, date)
        else:
            count, start = self.timeouts[addr]
            count += 1
            self.timeouts[addr] = count, start
    def finalize(self):
        for addr in self.timeouts:
            count, start = self.timeouts[addr]
            if count >= self.torelance:
                print_downtime(addr, start)

def main(argv):
    _, n = argv
    torelance = int(n)
    watcher = ServerWatcher(torelance)
    for line in sys.stdin:
        date, addr, resp = read_input(line.strip())
        if resp:
            watcher.ping_response(date, addr, resp)
        else:
            watcher.ping_no_response(date, addr)
    watcher.finalize()

if __name__ == '__main__':
    main(sys.argv)
