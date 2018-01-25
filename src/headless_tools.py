# -*- coding: UTF-8 -*-

import os, random, urllib2
from ua_headers import user_agents_pool


def create_opener(proxy_value, create_headers):
	'''Create urllib opener.'''

	# Set proxy
	proxy = urllib2.ProxyHandler({'https':proxy_value, 'http':proxy_value, 'ftp':proxy_value, 'sock5':proxy_value})
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)

	# Set headers
	if create_headers == True:
	
		header_index = random.randint(0, len(user_agents_pool) - 1)
		
		user_agent_header = user_agents_pool[header_index]
	
		i_headers = [
			('User-Agent', user_agent_header),
			("Referer", 'https://duckduckgo.com/'),
			("Accept", "text/html,​application/xhtml+xml,​application/xml;q=0.9,​image/webp,​image/apng,​*/*;q=0.8"),
			("Accept-Encoding", "gzip, deflate"),
			("Accept-Language", "en-US,en;q=0.8"),
			("Cache-Control", "max-age=0"),
			("Connection", "keep-alive"),
			("Upgrade-Insecure-Requests", "1"),
		]
		opener.addheaders = i_headers
	return opener

