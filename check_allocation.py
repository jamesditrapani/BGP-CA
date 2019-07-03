#!/usr/bin/python

import json
import requests
import ipaddress
from argparse import ArgumentParser

class BGP_CA():

	def main(self):
		parser = ArgumentParser(
			description = 'Display information on the current allocation of a sub aggregate address'
		)
		parser.add_argument(
			'ip',
			type = str,
			help = 'IPv4 or IPv6 sub aggregate address you wish to recieve information on'
		)
		arguments = parser.parse_args()
		self.grab_information(arguments.ip)

	def grab_information(self, query):
		api_url = 'https://api.bgpview.io/ip/{0}'.format(query)
		session = requests.session()
		get_data = session.get(api_url)
		json_data = get_data.json()
		self.parse_data(json_data, query)

	def parse_data(self, json_data, query):
		return_status = json_data.get('status')
		if return_status.lower() != 'ok':
			print('{0}, please try again'.format(json_data.get('status_message')))
		
		ip_data = json_data.get('data')
		ptr_record = ip_data.get('ptr_record')
		
		prefix_data = ip_data.get('prefixes')
		prefix_list = []
		for prefix in prefix_data:
			prefix_list.append(prefix.get('prefix'))
		
		most_specific = self.most_specific_subnet(prefix_list)
		
		total_advertisements = 0
		for prefix in prefix_data:
			total_advertisements = total_advertisements + 1
			if ipaddress.ip_network(prefix.get('prefix')) == ipaddress.ip_network(most_specific):
				prefix_data = prefix
		
		subnet = prefix_data.get('prefix')
		allocation_company = prefix_data.get('description')
		allocation_country = prefix_data.get('country_code')
		as_data = prefix_data.get('asn')
		advertisement_as = 'AS{0}'.format(as_data.get('asn'))
		advertisement_company = as_data.get('description')

		allocation_data = ip_data.get('rir_allocation')
		routing_information_registry = allocation_data.get('rir_name')
		allocation_date = allocation_data.get('date_allocated')
		
		self.print_output(ptr_record, query, subnet, allocation_company, advertisement_as, advertisement_company, routing_information_registry, allocation_date, allocation_country, total_advertisements)
		
	def most_specific_subnet(self, prefix_list):
		current_specific = ipaddress.ip_network('0.0.0.0/0') 
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
			raise TypeError('Unable to test subnet containment between {0} and {1}'.fromat(a, b))

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
	current_allocation.main()
