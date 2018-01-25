# -*- coding: UTF-8 -*-

import os, time, random, re, urlparse, urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import proxy_request as proxy_request
from ua_headers import user_agents_pool

def initiate_browser(proxy_type):	
	
	working_proxy = False

	while working_proxy == False:
		# Get new proxy
		proxy_ip = proxy_request.get_new_proxy(proxy_type)
		try:
			print '\nTrying the new proxy...'
			# Check that proxy works
			# Open browser with the new ip
			browser = open_browser(proxy_ip, False)
			time.sleep(random.uniform(0.3, 0.5))
			print 'Browser opened sucessfuly'
			browser.get('https://www.bing.com/')
			time.sleep(random.uniform(2.3, 4.2))
			browser.get('https://www.bing.com/')
			time.sleep(random.uniform(1.7, 2.1))
			browser.get('http://www.lagado.com/proxy-test')
			time.sleep(random.uniform(0.3, 0.5))
			working_proxy = True
		except Exception, e:
			print 'This proxy is not valid'
			print str(e)
			print ''
			time.sleep(5)
			browser.quit()

	return browser

def open_browser(proxy_ip, my_pc):
	'''Opens browser with the desired proxy'''
	
	cwd = os.getcwd()
	firebug_path = str(cwd) + r'\extensions\firebug-2.0.19-fx.xpi'
	
	# Create Mozilla profile
	profile = webdriver.FirefoxProfile()
	# Use proxy if requiered
	if my_pc == False:
		proxy_params = proxy_ip.split(':')
		proxy = str(proxy_params[0])
		port = proxy_params[1]
		print 'Proxy parameters: '
		print '\tProxy: ' + str(proxy)
		print '\tPort:  ' + str(port)
		# Set up the proxy
		profile.set_preference('network.proxy.ssl_port', int(port))
		profile.set_preference('network.proxy.ssl', proxy)
		profile.set_preference('network.proxy.http_port', int(port))
		profile.set_preference('network.proxy.http', proxy)
		profile.set_preference('network.proxy.type', 1)	
	# random Mozilla
	profile.set_preference("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0")
	profile.set_preference("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
	profile.set_preference("Accept-Language", "en-GB,en;q=0.5")
	profile.set_preference("Accept-Encoding", "gzip, deflate, br")
	profile.update_preferences()
	# Open browser with predifined headers
	browser = webdriver.Firefox(firefox_profile=profile)
	return browser
	
def get_the_soup(browser):
	'''Gets the html code from the open website.'''
	
	# Gets the html from the url				
	soup = BeautifulSoup(browser.page_source, 'lxml')
	return soup
