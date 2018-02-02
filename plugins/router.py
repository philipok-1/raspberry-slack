'''utility to scan BTHomehub IP address assignment'''


import re, time, sys

import urllib2

from bs4 import BeautifulSoup

import pprint

def scan_router(url, known_devices, rename=False):

    try:
        html=urllib2.urlopen(url)
    except urllib2.URLError, e:
        print "Error "+str(e)
        sys.exit(1)

    file=html.read()

    soup=BeautifulSoup(file, 'html.parser')

    refined=soup.find_all('td', class_='bt_border')

    mac = re.findall(r'(?:[0-9a-fA-F]:?){12}', str(refined))
    ip= re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', str(refined))

    data={}

    for i in range(0, len(mac)):
	
            if mac[i] in known_devices.keys() and rename:
                mac[i]=known_devices[str(mac[i])]
   	    data.update({str(mac[i]):str(ip[i])})
	
    return data

def check_device(url, mac):

    scan=scan_router(url)
    if mac in scan:
        return True
    else: return False

