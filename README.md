
# BGP-CA
## Description
Check current allocation & BGP prefix advertisement of an address

## Usage
usage: check_allocation.py [-h] ip

Display information on the current allocation of a sub aggregate address

positional arguments:
  ip          IPv4 or IPv6 sub aggregate address you wish to recieve
              information on

optional arguments:
  -h, --help  show this help message and exit

## Sample Output
```
[james@web1.ditrapani.com.au][~/Github/BGP-CA]$ python3.4 check_allocation.py 8.8.8.8

IP: 8.8.8.8
PTR Record: dns.google

Total Advertisements: 3
Advertised Prefix: 8.8.8.0/24
Advertised by: AS15169 - Google LLC

Allocation RIR: ARIN
Allocation Country: US
Allocation Company: Google LLC
Allocated Date: 1992-12-01 00:00:00
```

## To do
- Allow subnets to be parsed
- Move to RIS live BGP feed
- Add argument to show all advertisements

## Authors
* **James Di Trapani** - [Github](https://github.com/jamesditrapani)
