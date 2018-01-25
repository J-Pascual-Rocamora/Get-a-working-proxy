import os
import sys
import requests

def get_new_proxy(proxy_type):

	proxy_types = [ 'german',
					'level_one',
					'google',
					'any']
	
	if proxy_type.lower() not in proxy_types:
		print 'A NO VALID VALUE WAS PASSED TO get_new_proxy'
		print str(proxy_type) + ' is not a valid value for variable proxy_type'
		print 'VALID VALUES ARE:'
		print proxy_types
		sys.exit(-1)
	
	if proxy_type.lower() == 'german':
		print 'Looking for a german proxy...'
		url = 'http://gimmeproxy.com/api/getProxy?country=DE'
	if proxy_type.lower() == 'level_one':
		print 'Looking for a level one proxy...'
		url = 'http://gimmeproxy.com/api/getProxy?anonymityLevel=1'
	if proxy_type.lower() == 'google':
		print 'Looking for a google proxy...'
		url = 'http://gimmeproxy.com/api/getProxy?websites=google'
	if proxy_type.lower() == 'any':
		print 'Looking for any proxy...'
		url = 'https://gimmeproxy.com/api/getProxy'
	
	got_a_proxy = False

	while got_a_proxy == False:
	
		try:
		
			proxies = {
						"http": None,
						"https": None,
						}
			
			# Create headers
			headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}
			# Request proxy from url
			r = requests.get(url, headers=headers, proxies=proxies)
			# Open content as json
			contents = r.json()
			# Close url connection
			r.close()
			
			string_proxy = contents['ipPort']
			print '\tFound a proxy: ' + string_proxy

			got_a_proxy = True

		except Exception as e:
			print 'Error requesting proxy'
			print e
		
	return string_proxy

	
def load_proxy():
	'''Loads proxy file'''
	cwd = os.getcwd()
	proxy_file = str(cwd) + r'\proxy_data\proxy_file.txt'	
	f = open(proxy_file, 'r')
	proxy_ip = f.read()
	f.close()
	if len(proxy_ip) <= 1: # Not a valid IP
		print ''
		print '\tOld proxy is not valid'
		print '\tExiting...'
		sys.exit()
	return proxy_ip
	
if __name__=="__main__":

	get_new_proxy()