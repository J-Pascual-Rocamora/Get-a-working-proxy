# Get-a-working-proxy
Python 2.7.12

Gets a working proxy and checks for IP leak and headers that point to proxy usage.

Proxies are requested from gimmepoxy web. And the headers are checked at lagado.com.
The code gets a proxy and check if works. If it doesnt, a new proxy is requested.
After a working proxy is found, the headers are checked, looking for proxy leaks and headers pointing to proxy usage.

There is the possibility to look for different proxy types: any proxy, proxy from Germany, level one proxy and google friendly proxy.

To get a working proxy, using a headless browser, run:
$ python get_working_proxy.py -s proxy_type

To get a working proxy using firefox, run:
$ python get_working_proxy.py -s proxy_type -F

proxy_type value is choosen from the list: german, level_one, google, any

Note: to use Firefox the webdriver must be installed.
