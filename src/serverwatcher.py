from collections import deque

class Server:
    def __init__(self, addr, timeout_torelance,
                 overload_windowsize, overload_threashold):
        self.addr = addr
        self.timeout_torelance = timeout_torelance
        self.overload_threashold = overload_threashold
        self.delays = deque(maxlen=overload_windowsize)
        self.timeout_count = 0
        self.timeout_from = None
        self.overload_from = None
    @property
    def is_timeout(self):
        return self.timeout_count >= self.timeout_torelance
    @property
    def is_overload(self):
        mean = sum(self.delays) / len(self.delays)
        return mean > self.overload_threashold
    def print_timeout(self, date_to='now'):
        addr = self.addr
        date_from = self.timeout_from
        print(f"{addr} has been timeout; from {date_from} to {date_to}")
    def print_overload(self, date_to='now'):
        addr = self.addr
        date_from = self.overload_from
        print(f"{addr} has been overloaded; from {date_from} to {date_to}")
    def ping_timeout(self, date):
        if self.timeout_count == 0:
            self.timeout_from = date
            self.timeout_count = 1
        else:
            self.timeout_count += 1
    def ping(self, date, delay):
        if self.is_timeout:
            self.print_timeout(date)
        self.timeout_count = 0
        self.timeout_from = None
        self.delays.append(delay)
        if self.is_overload:
            if not self.overload_from:
                self.overload_from = date
        else:
            if self.overload_from:
                self.print_overload()
                self.overload_from = None

class ServerWatcher():
    def __init__(self, timeout_torelance, overload_windowsize, overload_threashold):
        self.servers = {}
        self.new_server = lambda addr: Server(addr, timeout_torelance, overload_windowsize, overload_threashold)
        self.network_down_date = {}
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
        self.check_network(date, addr.network)
    def print_network(self, net, date_to='now'):
        date_from = self.network_down_date[net]
        print(f"Network {net} has been down from {date_from} to {date_to}")
    def check_network(self, date, net):
        srvs_in_net = self.servers[net].values()
        net_is_down = all(srv.is_timeout for srv in srvs_in_net)
        if net_is_down:
            if net not in self.network_down_date:
                self.network_down_date[net] = date
        else:
            if net in self.network_down_date:
                self.print_network(net, date)
                del self.network_down_date[net]
    def finalize(self):
        for net, servers in self.servers.items():
            if net in self.network_down_date:
                self.print_network(net)
            for srv in servers.values():
                if srv.is_timeout:
                    srv.print_timeout()
                if srv.is_overload:
                    srv.print_overload()
