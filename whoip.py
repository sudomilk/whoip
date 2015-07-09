from requests.exceptions import ConnectionError
from multiprocessing import Pool
import argparse
import requests
import sys


#Functions
def ip_banned_alert():
    r = requests.get('http://curlmyip.com/')
    banned_ip = r.text.rstrip('\n').encode('UTF-8')
    return 'It looks like your IP might be banned. Go to http://ip-api.com/docs/unban and try to unban {ip}.'.format(ip=banned_ip)

def getgeo(ip):
    """Give this a string of an IPv4 or IPv6 address
    Returns a dict with geographical data about the ip
    """
    headers = {'User-Agent': 'whoip v2'}
    try:
        r = requests.get('http://ip-api.com/json/{ip}'.format(ip=ip))
    except ConnectionError:
        return {'error': 'I had a connection issue'}
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
            formatted[key] = geodict[key].encode('UTF-8')
        elif key == 'error':
            return ip_banned_alert()
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

if len(ip_list) > 250:
    print('Cannot process more than 250 IPs per minute. Quitting.')
    sys.exit(1)

#call getgeo on the list of strings, use mp if the string is a list > 1
if len(ip_list) > 1:
    if len(ip_list) in range(2,8):
        pool = Pool(len(ip_list))
    else:
        pool = Pool(8)
        result = pool.map(getgeo, ip_list)
    for line in result:
        if line is not None:
            print(format_geodict(line))
else:
    answer = getgeo(ip_list[0])
    if answer is not None:
        print(format_geodict(answer))
