import os, sys, time
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import urllib2
import argparse

import src.proxy_request as proxy_request
import src.proxy_tools as proxy_tools
import src.headers_tool as headers_tool
import src.headless_tools as headless_tools
import src.headers_parser as headers_parser

def commandLineArgs():
    '''
    Handles the arguments
    '''
    
    parser = argparse.ArgumentParser(
									formatter_class=argparse.RawTextHelpFormatter,
									prog = "Get_a_working_proxy",    
									description="""Search for a working proxy and checks for original IP and headers""",
									)
    
    parser.add_argument('--version', action = 'version', version = 'Get_a_working_proxy.py 1.0.0')
    parser.add_argument('-v',        action = 'version', version = 'Get_a_working_proxy.py 1.0.0')
    

    parser.add_argument("-F", action='store_true', dest='firefox_flag', default=False,
						help='''Uses visible Firefox browser. Default=False''')
	
    parser.add_argument("-s", action='store', type=str, dest='proxy_type', required=True,
						help='''Type of proxy to be searched.''')

	
    return parser.parse_args()


def get_my_ip():

	r = requests.get('https://wtfismyip.com/json')

	contents = r.content
	contents = contents.split(',')
	IP_line  = contents[0]
	IP_broken = IP_line.split(':')
	IP_text = IP_broken[1]
	no_spaces = IP_text.replace(' ', '')
	clean_ip = no_spaces.replace('"', '')
	
	return clean_ip

def firefox_app(proxy_type):

	# Get computer IP
	my_ip = get_my_ip()

	# Find a working proxy
	browser = proxy_tools.initiate_browser(proxy_type)

	# Get the headers
	browser.get('http://www.lagado.com/proxy-test')
	print '\nA succesful proxy has been found'
	
	# Check for proxy info on headers
	web_html = proxy_tools.get_the_soup(browser)
	# Get headers
	headers_pool = headers_parser.get_headers(web_html)
	# Print headers
	headers_parser.print_headers(headers_pool)
	# Check if original IP is whitin headers
	headers_parser.is_my_ip_there(web_html, my_ip)
	headers_tool.is_ip_leaked(my_ip, headers_pool)
	# Check if there are 'proxy' headers
	headers_parser.proxy_header_hint(web_html)
	headers_tool.is_proxy(my_ip, headers_pool)

	return

def headless_app(proxy_type):

	valid_proxy_flag = False
	
	# Get computer IP
	my_ip = get_my_ip()

	while valid_proxy_flag == False:
	
		try:
			
			# Gets a proxy
			proxy_value = proxy_request.get_new_proxy(proxy_type)

			# Set up proxy for requests
			forwared_ip = proxy_value
			proxy_broken = proxy_value.split(':')
			proxy_ip = proxy_broken[0]

			os.environ['http_proxy']  = proxy_ip
			os.environ['https_proxy'] = proxy_ip

			# Create requests opener
			opener = headless_tools.create_opener(proxy_value, True)
			site = urllib2.urlopen('http://www.lagado.com/proxy-test')
			time.sleep(15)
			doc = site.read()
			
			valid_proxy_flag = True
	
		except Exception as e:
			print '\t' + str(e)
			print '\tThe proxy is not valid'
			print ''
			time.sleep(60)
	
	web_html = BeautifulSoup(str(doc), "html.parser")
	
	# Get headers
	headers_pool = headers_parser.get_headers(web_html)
	# Print headers
	headers_parser.print_headers(headers_pool)
	# Check if original IP is whitin headers
	headers_parser.is_my_ip_there(web_html, my_ip)
	headers_tool.is_ip_leaked(my_ip, headers_pool)
	# Check if there are 'proxy' headers
	headers_parser.proxy_header_hint(web_html)
	headers_tool.is_proxy(my_ip, headers_pool)

	return

if __name__=="__main__":

	args = commandLineArgs()
	firefox_flag = args.firefox_flag
	proxy_type   = args.proxy_type
	proxy_type   = proxy_type.lower()
	
	proxy_types = [ 'german',
					'level_one',
					'google',
					'any']
					
	if proxy_type not in proxy_types:
		print 'The type of proxy inserted is not covered'
		print 'Types of proxies covered are:'
		for i in range(0, len(proxy_types)):
			print '\t' + str(proxy_types[i])
		sys.exit()
	
	if firefox_flag == True:
		firefox_app(proxy_type)
	else:
		headless_app(proxy_type)