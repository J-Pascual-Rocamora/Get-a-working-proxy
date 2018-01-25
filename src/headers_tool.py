import os, time, random, re, urlparse, ssl
import urllib2
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def find_proxy_hints(headers_used, my_ip):
	'''Receives the list header:value used by the proxy and
	returns a pool of headers which my hint that a proxy is in used'''


	proxy_headers_pool = [	'Forwarded',
							'Via',
							'X-Forwarded-For',
							'Client-ip',
							'HTTP_X_FORWARDED_FOR',
							'HTTP_CLIENT_IP',
							'X-Client-IP',
							'HTTP_X_REAL_IP',
							]

	suspicious_headers = []
							
	for i in range(0, len(headers_used)):
		split_header = headers_used[i].split(':')
		header_title = split_header[0]
		header_value = split_header[1]
		# Collect headers that are in proxy_headers_pool
		if (header_title in proxy_headers_pool) and (header_title not in suspicious_headers):
			suspicious_headers.append(header_title)
		# Collect headers which have the ip in their value
		if re.search(str(my_ip), str(header_value)) and (header_title not in suspicious_headers):
			suspicious_headers.append(header_title)
		# Collect headers which have the proxy word in their value
		if re.search('proxy', str(header_value)) and (header_title not in suspicious_headers):
			suspicious_headers.append(header_title)

	print '*'*35
	print '\tSuspicious headers'
	print '*'*35
	for i in range(0, len(suspicious_headers)):
		print suspicious_headers[i]
	print ''

	return suspicious_headers


def print_headers(headers_used):
	'''Receives a list header:value and prints it.'''
	
	print '*'*35
	print '\tProxy Headers'
	print '*'*35
	
	for i in range(0, len(headers_used)):
		print headers_used[i]
	print ''

	return

def is_proxy(my_ip, headers_used):
	'''Checks the headers to see if there is any
	which tells a proxy is in use.'''

	proxy_headers_pool = [	'Forwarded',
							'Via',
							'X-Forwarded-For',
							'Client-ip',
							'HTTP_X_FORWARDED_FOR',
							'HTTP_CLIENT_IP',
							'X-Client-IP',
							'HTTP_X_REAL_IP',
							]

	is_proxy_flag = False
							
	for i in range(0, len(headers_used)):
		split_header = headers_used[i].split(':')
		header_title = split_header[0]
		header_value = split_header[1]
		# Collect headers that are in proxy_headers_pool
		if (header_title in proxy_headers_pool):
			is_proxy_flag = True
		# Collect headers which have the ip in their value
		if re.search(str(my_ip), str(header_value)):
			is_proxy_flag = True
		# Collect headers which have the proxy word in their value
		if re.search('proxy', str(header_value)):
			is_proxy_flag = True

	print '*'*35
	print 'Is a proxy? ' + str(is_proxy_flag)
	print '*'*35
	print ''

	return is_proxy_flag

def is_ip_leaked(my_ip, headers_used):
	'''Checks the headers looking for original IP.'''

	leaked_flag = True

	if not re.search(str(my_ip), str(headers_used)):
		leaked_flag = False

	print '*'*35
	print 'Is IP leaked? ' + str(leaked_flag)
	print '*'*35
	print''

	return leaked_flag

if __name__ == "__main__":

	print 'Hello from headers_tool.py'