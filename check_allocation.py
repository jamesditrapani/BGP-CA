#!/usr/bin/python

import json
import requests
import ipaddress
from argparse import ArgumentParser

class BGP_CA():

	@classmethod
	def grab_information(self, query):
		api_url = 'https://api.bgpview.io/ip/{0}'.format(query)
		session = requests.session()
		get_data = session.get(api_url)
		json_data = get_data.json()
                return json_data

	def parse_data(self, json_data, query):
		if json_data['status'].lower() != 'ok':
			print('{0}, please try again'.format(json_data['status_message']))
	
                prefix_data = json_data['data']['prefixes']
		prefix_list = []
		for prefix in prefix_data:
			prefix_list.append(prefix['prefix'])
	    
		most_specific = self.most_specific_subnet(prefix_list)
	    
		for prefix in prefix_data:
			if ipaddress.ip_network(prefix['prefix']) == ipaddress.ip_network(most_specific):
				prefix_data = prefix
		
		advertisement_as = 'AS{0}'.format(prefix_data['asn']['asn'])
		
		self.print_output(json_data['data']['ptr_record'], query, prefix_data['prefix'], prefix_data['description'], advertisement_as, prefix_data['asn']['description'], json_data['data']['rir_allocation']['rir_name'], json_data['data']['rir_allocation']['date_allocated'], prefix_data['country_code'], len(prefix_data))
		
	def most_specific_subnet(self, prefix_list):
		current_specific = ipaddress.ip_network(u'0.0.0.0/0') 
		for prefix in prefix_list:
			prefix = ipaddress.ip_network(prefix)
			subnet_of = self.is_subnet_of(prefix, current_specific)
			if subnet_of:
				current_specific = prefix
		return current_specific
			
	def is_subnet_of(self, a, b):
		# Taken from https://github.com/python/cpython/blob/v3.7.0/Lib/ipaddress.py#L976
		# Python 3.4 does not support subnet_of, have taken the source function from 3.6
		try:
			if a.version != b.version:
				raise TypeError('{0} and {1} are not of the same version'.format(a, b))
			return (b.network_address <= a.network_address and b.broadcast_address >= a.broadcast_address)
		except AttributeError:
			raise TypeError('Unable to test subnet containment between {0} and {1}'.format(a, b))

	def print_output(self, ptr_record, query, subnet, allocation_company, advertisement_as, advertisement_company, routing_information_registry, allocation_date, allocation_country, total_advertisements):
		print('\nIP: {0}'.format(query))
		print('PTR Record: {0}\n'.format(ptr_record))
		print('Total Advertisements: {0}'.format(total_advertisements))
		print('Advertised Prefix: {0}'.format(subnet))
		print('Advertised by: {0} - {1}\n'.format(advertisement_as, advertisement_company))
		print('Allocation RIR: {0}'.format(routing_information_registry))
		print('Allocation Country: {0}'.format(allocation_country))
		print('Allocation Company: {0}'.format(allocation_company))
		print('Allocated Date: {0}\n'.format(allocation_date))


if __name__ == "__main__":
	current_allocation = BGP_CA()
	parser = ArgumentParser(
		description = 'Display information on the current allocation of a sub aggregate address'
	)
	parser.add_argument(
		'ip',
		type = str,
		help = 'IPv4 or IPv6 sub aggregate address you wish to recieve information on'
	)
	arguments = parser.parse_args()
	json_data = current_allocation.grab_information(arguments.ip)
	current_allocation.parse_data(json_data, arguments.ip)
