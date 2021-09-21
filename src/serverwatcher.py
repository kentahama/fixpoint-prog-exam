from collections import deque

def print_timeout(addr, date_from, date_to):
    print(f"{addr} has been timeout; from {date_from} to {date_to}")

class Server:
    def __init__(self, addr, timeout_torelance,
                 overload_windowsize, overload_threashold):
        self.addr = addr
        self.timeout_torelance = timeout_torelance
        self.overload_threashold = overload_threashold
        self.delays = deque(maxlen=overload_windowsize)
        self.timeout_count = 0
        self.timeout_from = None
    @property
    def is_timeout(self):
        return self.timeout_count >= self.timeout_torelance
    def ping_timeout(self, date):
        if self.timeout_count == 0:
            self.timeout_from = date
            self.timeout_count = 1
        else:
            self.timeout_count += 1
    def print_timeout(self, date_to='now'):
        addr = self.addr
        date_from = self.timeout_from
        print(f"{addr} has been timeout; from {date_from} to {date_to}")
    def ping(self, date, delay):
        if self.is_timeout:
            self.print_timeout(date)
        self.timeout_count = 0
        self.timeout_from = None

class ServerWatcher():
    def __init__(self, timeout_torelance, overload_windowsize, overload_threashold):
        self.servers = {}
        self.new_server = lambda addr: Server(addr, timeout_torelance, overload_windowsize, overload_threashold)
    def get_or_new_server(self, addr):
        net = addr.network
        if net not in self.servers:
            srv = self.new_server(addr)
            self.servers[net] = {addr: srv}
        if addr not in self.servers[net]:
            srv = self.new_server(addr)
            self.servers[net][addr] = srv
        return self.servers[net][addr]
    def ping(self, date, addr, resp=None):
        srv = self.get_or_new_server(addr)
        if resp:
            srv.ping(date, resp)
        else:
            srv.ping_timeout(date)
    def finalize(self):
        for network in self.servers.values():
            for srv in network.values():
                if srv.is_timeout:
                    srv.print_timeout()
