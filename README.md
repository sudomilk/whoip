# whoip
Lookup Geo Info about IPs on the command line

```
whoip -h
usage: whoip [-h] [ip]

provides geo information for IPs

positional arguments:
  ip          the ip to check; this can also come from stdin as a single IP or
              a newline-separated series of IPs.

optional arguments:
  -h, --help  show this help message and exit
```

Do just one IP...

```
$ whoip 101.169.127.252
101.169.127.252|Australia|Queensland|Brisbane|Telstra Internet
```

Or do a lot!

```
$ cut -d ' ' -f 1 /var/log/apache2/site.access.log | sort | uniq | grep -v "100" | head -20 | whoip
101.127.227.217|Singapore||Singapore|StarHub Ltd
101.169.127.252|Australia|Queensland|Brisbane|Telstra Internet
101.169.42.149|Australia|Queensland|Gold Coast|Telstra Internet
101.171.170.150|Australia|New South Wales|Sydney|Telstra Internet
101.176.192.20|Australia|New South Wales|Windsor|Telstra Internet
101.180.99.36|Australia|||Telstra Internet
101.181.153.147|Australia|Victoria|Rowville|Telstra Internet
101.188.99.169|Australia|Victoria|Melbourne|Telstra Internet
101.190.62.130|Australia|New South Wales|Sydney|Telstra Internet
101.190.91.226|Australia|Victoria|Stanhope|Telstra Internet
101.191.107.151|Australia|New South Wales|Sydney|Telstra Internet
101.73.11.6|China|Hebei|Hebei|China Unicom Liaoning
103.246.0.29|Indonesia|Riau Islands|Patam|PT Solnet Indonesia
103.27.236.81|Vietnam|Tinh Binh GJinh|Long Van|Long Van System Solution JSC
103.3.146.177|Australia|Victoria|Cranbourne|Vertical Telecoms Pty
104.128.23.23|United States|Iowa|Iowa City|Telentia
104.132.34.65|United States|New York|New York|Google Incorporated
104.14.141.51|United States|California|Visalia|AT&T U-verse
104.144.61.93|United States|New York|Buffalo|B2 Net Solutions
104.148.164.118|United States|New York|East Hampton|Optimum Online
```

Do normal unix parsing things to get the kind of information you care about too.

```
$ cut -d ' ' -f 1 /var/log/apache2/site.access.log | sort | uniq | head -100 | whoip | cut -d \| -f 2 | sort | uniq -c | sort -nr | head
     71 United States
     11 Australia
      5 South Africa
      4 Denmark
      2 China
      1 Vietnam
      1 Singapore
      1 Pakistan
      1 Indonesia
      1 India
```
