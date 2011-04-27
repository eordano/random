# coding: utf-8

import urllib
import urllib2
import cookielib
import re

from cPickle import dumps

from BeautifulSoup import BeautifulSoup

from area import Area
from filenode import FileNode
from foldernode import FolderNode
from news import News

iol_domain = "http://iol2.itba.edu.ar:27521"

class IOL2Service:
    def __init__(self, auth_cookie_value):
        ''' Start up. ''' 
        cookiejar = cookielib.CookieJar()
        cookiejar.set_cookie(cookielib.Cookie(
            version=0, name='.ASPXAUTH',
            value=auth_cookie_value,
            port=None, port_specified=False, domain='iol2.itba.edu.ar',
            domain_specified=False, domain_initial_dot=False, path='/',
            path_specified=True, secure=False,
            expires=1805039183, # Way ahead in the future (as of 2011)
            discard=False, comment=None, comment_url=None, rest={}, rfc2109=False
        ))
        self.cookies = cookiejar._cookies

        data = self._read_url(iol_domain)

        if data.find('ctl00_PlaceHolderMain_login_UserName') != -1:
            raise Exception('Invalid Cookie')

        # A lot of cleanup needs to get done to get the users name
        bs = BeautifulSoup(data)

        self.username = bs.findAll(name="table",
            attrs={"class": "ms-globalright"})[0].findAll(name="td")[0].text\
                .strip().split('&nbsp;')[0].strip()

        self.areas = self.fetch_areas(bs)

    def _read_url(self, url):
        ''' Open a url prefixing the IOL domain
        '''
        cookiejar = cookielib.CookieJar()
        cookiejar._cookies = self.cookies
        opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(cookiejar)
        )
        opener.addheaders = [
            ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                           'Windows NT 5.2; .NET CLR 1.1.4322)'))
        ]
        return opener.open(url).read()
            
    def get_areas(self):
        return self.areas

    def fetch_areas(self, bs):
        ''' This method parses te home page and returns the areas the user has
        access to. They are "Area" objects as described in area.py.

        The return value is a plain old python list.
        '''
        areas = []

        # The identifier for menues is a Anchor element that has a certain 
        # style (this is very UGLY)
        for anchor in bs.findAll(name="a",
                attrs={"style":"border-style:none;font-size:1em;"}):

            name = anchor.text
            url = anchor.attrMap['href']
            if not url.startswith('/grado'):
                continue

            new_area = Area(name, url, None)
            areas.append(new_area)

        return areas

    def __repr__(self):
        return 'IOL2Service instance'


if __name__ == '__main__':
    import getpass 

    value = raw_input('Enter your ASPXAUTH cookie: ')

    test = IOL2Service(value)

    print test.username
    areas = test.get_areas()

    print(areas)

    print(areas[-4].get_root(test).get_files(test))

    news = areas[-4].get_news(test)
    for new in news.values():
        print new

    dumps(test)
    dumps(news)
    dumps(areas)
