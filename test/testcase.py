import datetime
import ipaddress

def server_log(sec, ip, resp=None):
    now = datetime.datetime.now()
    dt = datetime.timedelta(seconds=sec)
    date = now + dt
    datestring = datetime.datetime.strftime(date, "%Y%m%d%H%M%S")
    resp = str(resp) if resp else "-"
    return f"{datestring},{ip},{resp}"

def server(ip, sec):
    s = 0
    for _ in range(4):
        print(server_log(s, ip, 10))
        s += sec
    for _ in range(3):
        print(server_log(s, ip))
        s += sec
    for _ in range(4):
        print(server_log(s, ip, 10))
        s += sec
    
def main():
    logs = []
    server(ipaddress.ip_interface('192.168.11.1/24'), 20)
    server(ipaddress.ip_interface('192.168.11.2/24'), 50)
    server(ipaddress.ip_interface('192.168.11.3/24'), 70)
    
main()
