import unicodedata
import argparse
import requests
import sys


#Functions
def getgeo(ip):
    """Give this a string of an IPv4 or IPv6 address
    Returns a dict with geographical data about the ip
    """
    headers = {
        'User-Agent': 'whoip v2'
        }
    r = requests.get('http://ip-api.com/json/{ip}'.format(ip=ip))
    info = r.json()
    if r.status_code == 200:
        return info


def format_geodict(geodict):
    """Give this a dictionary of geo data
    Returns a pipe-formatted string of the data
    """
    keys = ['query', 'country', 'regionName', 'city', 'isp']
    formatted = {'query': '-', 'country': '-', 'regionName': '-', 'city': '-', 'isp': '-'}
    for key in geodict:
        if key in keys:
            formatted[key] = geodict[key]
    result = '{query}|{country}|{regionName}|{city}|{isp}'.format(**formatted)
    return result


#Parse the arguments
parser = argparse.ArgumentParser(description='provides geo information for IPs', prog='geoip')
parser.add_argument('ip', nargs='?', default=sys.stdin, help='the ip to check; \
    this can also come from stdin as a single IP or a newline-separated series of IPs.')
args = parser.parse_args()

#Format input into a list of strings
if type(args.ip) == type('string'):
    ip_list = [args.ip]
else:
    ip_list = [item.rstrip('\n') for item in args.ip.readlines()]

for ip in ip_list:
    answer = format_geodict(getgeo(ip))
    print(answer)
