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

def main():
    down = {}
    for line in sys.stdin:
        date, addr, resp = read_input(line.strip())
        if not resp:
            if addr not in down:
                down[addr] = date
        else:
            if addr in down:
                start = down[addr]
                print_downtime(addr, start, date)
                del down[addr]
    for addr in down:
        start = down[addr]
        print_downtime(addr, start)

if __name__ == '__main__':
    main()
