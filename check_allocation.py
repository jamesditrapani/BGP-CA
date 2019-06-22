#!/usr/bin/python

import json
import requests
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
		for prefix in prefix_data:
			larger_subnet = prefix.get('prefix')
			allocation_company = prefix.get('description')
			allocation_country = prefix.get('country_code')
			as_data = prefix.get('asn')
			advertisement_as = 'AS{0}'.format(as_data.get('asn'))
			advertisement_company = as_data.get('description')

		allocation_data = ip_data.get('rir_allocation')
		routing_information_registry = allocation_data.get('rir_name')
		allocation_date = allocation_data.get('date_allocated')
		
		self.print_output(ptr_record, query, larger_subnet, allocation_company, advertisement_as, advertisement_company, routing_information_registry, allocation_date, allocation_country)
		
	def print_output(self, ptr_record, query, larger_subnet, allocation_company, advertisement_as, advertisement_company, routing_information_registry, allocation_date, allocation_country):
		print('\nIP: {0}'.format(query))
		print('PTR Record: {0}\n'.format(ptr_record))
		print('Advertised Prefix: {0}'.format(larger_subnet))
		print('Advertised by: {0} - {1}\n'.format(advertisement_as, advertisement_company))
		print('Allocation RIR: {0}'.format(routing_information_registry))
		print('Allocation Country: {0}'.format(allocation_country))
		print('Allocation Company: {0}'.format(allocation_company))
		print('Allocated Date: {0}\n'.format(allocation_date))


if __name__ == "__main__":
	current_allocation = BGP_CA()
	current_allocation.main()
