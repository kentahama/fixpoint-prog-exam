class StatusCounter:
    def __init__(self, date, status):
        self.date = date
        self.status = status
        self.count = 1
    def send(self, date, status):
        if self.status == status:
            self.count += 1
        else:
            self.status = status
            self.date = date
            self.count = 1

class ServerWatcher():
    def __init__(self, timeout_torelance, overload_torelance):
        self.timeout_torelance = timeout_torelance
        self.overload_torelance = overload_torelance
        self.known_servers = {}
        self.watch_targets = {}
        self.down_networks = {}
    def is_timeout(self, addr):
        if addr in self.watch_targets:
            srv = self.watch_targets[addr]
            return srv.status == 'timeout' and srv.count >= self.timeout_torelance
        else:
            return False
    def is_overload(self, addr):
        if addr in self.watch_targets:
            srv = self.watch_targets[addr]
            return srv.status == 'overload' and srv.count >= self.overload_torelance
        else:
            return False
    def is_down(self, net):
        return all(self.is_timeout(addr) for addr in self.known_servers[net])
    def print_status(self, addr, date_to='now'):
        srv = self.watch_targets[addr]
        date_from = srv.date
        if self.is_timeout(addr):
            print(f"{addr} has been timeout; from {date_from} to {date_to}")
        elif self.is_overload(addr):
            print(f"{addr} has been overloaded; from {date_from} to {date_to}")
    def print_network(self, net, date_to='now'):
        date_from = self.down_networks[net]
        print(f"Network {net} has been down from {date_from} to {date_to}")
    def check_network(self, addr, date):
        net = addr.network
        if net in self.known_servers:
            self.known_servers[net].add(addr)
        else:
            self.known_servers[net] = {addr}
        if self.is_down(net):
            if net not in self.down_networks:
                self.down_networks[net] = date
        else:
            if net in self.down_networks:
                self.print_network(net, date)
                del self.down_networks[net]
    def ping_response(self, date, addr):
        if addr in self.watch_targets:
            self.print_status(addr, date)
            del self.watch_targets[addr]
        self.check_network(addr, date)
    def ping_abnormal(self, date, addr, status):
        if addr not in self.watch_targets:
            srv = StatusCounter(date, status)
            self.watch_targets[addr] = srv
        else:
            srv = self.watch_targets[addr]
            if srv.status != status:
                self.print_status(addr, date)
            srv.send(date, status)
        self.check_network(addr, date)
    def finalize(self):
        for addr in self.watch_targets:
            self.print_status(addr)
        for net in self.down_networks:
            self.print_network(net)
