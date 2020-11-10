#!/usr/bin/python
import json, requests, ipaddress
from argparse import ArgumentParser

__author__ 'James Di Trapani <james@ditrapani.com.au>'

class BGPCheckAdvertisement():
	"""
		Wrapper for bgptoolkit.net that provides quick & useful information to console for a given IP. 
		
		Essential for any Network Engineers toolkit.

	"""
	def __init__(self, ip):
		self.ip = ip
		self.data = self.grab_information(self.ip)

	def grab_information(self, query):
		api_url = 'https://bgptoolkit.net/api/ca/{0}'.format(query)
		session = requests.session()
		get_data = session.get(api_url)
		json_data = get_data.json()
		return json_data

	def parse_data(self):
		if self.data['status'].lower() != 'ok':
			print('{0}, please try again'.format(json_data['status_message']))

		prefix_data = json_data['data']['prefixes']
		prefix_list = []
		for prefix in prefix_data:
			prefix_list.append(prefix['prefix'])
			
		most_specific = self.most_specific_subnet(prefix_list)
			
		for prefix in prefix_data:
			if ipaddress.ip_network(prefix['prefix']) == ipaddress.ip_network(most_specific):
				prefix_data = prefix
		
		prefix_data['asn']['asn'] = f'AS{prefix_data["asn"]["asn"]}'
		
		self.print_output(self.ip, json_data['data']['ptr_record'], prefix_data, len(prefix_data))
		
	def most_specific_subnet(self, prefix_list):
		current_specific = ipaddress.ip_network(u'0.0.0.0/0') 
		for prefix in prefix_list:
			prefix = ipaddress.ip_network(prefix)
			subnet_of = ipaddress.subnet_of(prefix, current_specific)
			if subnet_of:
				current_specific = prefix
		return current_specific

	def print_output(self, query, ptr, pd, ta):
		print(f'\nIP: {query}')
		print(f'PTR Record: {ptr}\n')
		print(f'Total Advertisements: {ta}')
		print(f'Advertised Prefix: {pd["prefix"]}')
		print(f'Advertised by: {pd["asn"]["asn"]} - {pd["asn"]["description"]}\n')
		print(f'Allocation RIR: {pd["data"]["rir_allocation"]["rir_name"]}')
		print(f'Allocation Country: {pd["country_code"]}')
		print(f'Allocation Company: {pd["description"]}')
		print(f'Allocated Date: {pd["data"]["rir_allocation"]["data_allocated"]}\n')


if __name__ == "__main__":
	parser = ArgumentParser(
		description = 'Display information on the current allocation of a sub aggregate address'
	)
	parser.add_argument(
		'ip',
		type = str,
		help = 'IPv4 or IPv6 sub aggregate address you wish to recieve information on'
	)
	arguments = parser.parse_args()
	current_allocation = BGPCheckAdvertisement(arguments.ip)
	current_allocation.parse_data()
