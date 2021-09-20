import sys
import utils

class ServerWatcher():
    def __init__(self, timeout_torelance, overload_torelance):
        self.timeout_torelance = timeout_torelance
        self.overload_torelance = overload_torelance
        self.servers = {}
    def print_status(self, addr, date='now'):
        srv = self.servers[addr]
        time_from = srv.date
        time_to = date
        if srv.status == 'timeout' and srv.count >= self.timeout_torelance:
            print(f"{addr} has been down; from {time_from} to {time_to}")
        elif srv.status == 'overload' and srv.count >= self.overload_torelance:
            print(f"{addr} has been overloaded; from {time_from} to {time_to}")
    def ping_response(self, date, addr):
        if addr in self.servers:
            self.print_status(addr, date)
            del self.servers[addr]
    def ping_abnormal(self, date, addr, status):
        if addr not in self.servers:
            srv = utils.StatusCounter(date, status)
            self.servers[addr] = srv
        else:
            srv = self.servers[addr]
            if srv.status != status:
                self.print_status(addr, date)
            srv.send(status)
    def finalize(self):
        for addr in self.servers:
            self.print_status(addr)

def main(argv):
    _, n, m, t = argv
    timeout_torelance = int(n)
    overload_torelance = int(m)
    overload_threashold = int(t)
    watcher = ServerWatcher(timeout_torelance, overload_torelance)
    for line in sys.stdin:
        date, addr, resp = utils.read_input(line.strip())
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
