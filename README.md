
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

## Importing class
When importing the class, run using the `import_from()` function. This will currently only take an IP address and return the raw JSON data

### Code example
```python
from check_allocation import BGP_CA

code = BGP_CA
returned_json = code.import_from('8.8.8.8')
print(returned_json)
```

### JSON return example
```json
{'status': 'ok', 'status_message': 'Query was successful', 'data': {'maxmind': {'city': None, 'country_code': 'US'}, 'iana_assignment': {'description': 'Administered by ARIN', 'date_assigned': None, 'assignment_status': 'legacy', 'whois_server': 'whois.arin.net'}, 'rir_allocation': {'country_code': 'US', 'ip': '8.0.0.0', 'allocation_status': 'allocated', 'date_allocated': '1992-12-01 00:00:00', 'prefix': '8.0.0.0/9', 'cidr': 9, 'rir_name': 'ARIN'}, 'ip': '8.8.8.8', 'prefixes': [{'asn': {'asn': 15169, 'description': 'Google LLC', 'country_code': 'US', 'name': 'GOOGLE'}, 'country_code': 'US', 'name': 'LVLT-GOGL-8-8-8', 'ip': '8.8.8.0', 'description': 'Google LLC', 'prefix': '8.8.8.0/24', 'cidr': 24}, {'asn': {'asn': 3356, 'description': 'Level 3 Parent, LLC', 'country_code': 'US', 'name': 'LEVEL3'}, 'country_code': 'US', 'name': 'LVLT-ORG-8-8', 'ip': '8.0.0.0', 'description': 'Level 3 Parent, LLC', 'prefix': '8.0.0.0/12', 'cidr': 12}, {'asn': {'asn': 3356, 'description': 'Level 3 Parent, LLC', 'country_code': 'US', 'name': 'LEVEL3'}, 'country_code': 'US', 'name': 'LVLT-ORG-8-8', 'ip': '8.0.0.0', 'description': 'Level 3 Parent, LLC', 'prefix': '8.0.0.0/9', 'cidr': 9}], 'ptr_record': 'dns.google'}, '@meta': {'api_version': 1, 'time_zone': 'UTC', 'execution_time': '117.72 ms'}}
```

## To do
- Allow subnets to be parsed
- Move to RIS live BGP feed
- Add argument to show all advertisements

## Authors
* **James Di Trapani** - [Github](https://github.com/jamesditrapani)
