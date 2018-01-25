import os, time, random, re, urlparse, ssl
import urllib2
import requests
from bs4 import BeautifulSoup

def get_headers(web_html):
	'''Get headers from lagado website.'''

	headers_pool = []
	
	headers_table = web_html.find('table', attrs={'id':'request-headers-table'})
	rows_html = headers_table.find_all('tr')
	for item in rows_html:
		columns_html = item.find_all('td')
		row_title = columns_html[0].text.strip()
		row_value = columns_html[1].text.strip()
		header_line = str(row_title) + ':' + str(row_value.encode('utf-8', 'ignore'))
		headers_pool.append(header_line)

	return headers_pool
	
def is_my_ip_there(web_html, my_ip):
	'''Look for local ip on headers.'''

	detected_flag = True
	
	web_data = re.search(my_ip, str(web_html))
	if web_data:
		print 'Your ip has been found'
		print web_data.group()
	else:
		print 'Your ip has not been found'
		detected_flag = False
	
	return detected_flag

def proxy_or_not(web_html):
	'''Check for proxy hints on headers.'''

	no_proxy_text = re.search(r"This request appears NOT to have come via a proxy.", str(web_html))
	
	# Proxy identifier
	proxy_text = re.search(r"This request appears to have come via a proxy.", str(web_html))
	
	if no_proxy_text:
		print no_proxy_text.group(1)
		proxy_flag = False
	
	if proxy_text:
		print proxy_text.group()
		proxy_text = True
	
	print proxy_text
	
	return

def proxy_header_hint(web_html):
	'''Receives the html code from lagado website and looks for any proxy header'''

	# Get headers table
	headers_table = web_html.find('table', attrs={'id':'request-headers-table'})
	rows_html = headers_table.find_all('tr')
	for item in rows_html:
		columns_html = item.find_all('td')
		row_title = columns_html[0].text.strip()
		row_value = columns_html[1].text.strip()
		# Look for proxy headers
		if row_title == "Via":
			print "Found Via header"
		if row_title == "Forwarded":
			print "Found Forwarded header"
		if row_title == "X-Forwarded-For":
			print "Found X-Forwarded-For header"
		if row_title == "Client-ip":
			print "Found Client-ip header"

	return

def print_headers(headers_pool):
	'''Receives the pool of headers and prints it.'''
	
	print "*"*30
	print "\tHEADERS"
	print "*"*30
	
	for i in range(0, len(headers_pool)):
		print headers_pool[i]
	
	print "*"*30
	print ""
	
	return