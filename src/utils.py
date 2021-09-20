from datetime import datetime
import ipaddress

def read_input(s):
    d, a, r = s.split(",")
    date = datetime.strptime(d, "%Y%m%d%H%M%S")
    addr = ipaddress.ip_interface(a)
    resp = int(r) if r != '-' else None
    return date, addr, resp

class StatusCounter:
    def __init__(self, date, status):
        self.date = date
        self.status = status
        self.count = 1
    def send(self, status):
        if self.status == status:
            self.count += 1
        else:
            self.status = status
            self.count = 1
    def reset(self):
        self.status = 'service'
        self.count = 0
