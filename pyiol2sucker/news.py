# coding: utf-8

import urllib2
import re

from BeautifulSoup import BeautifulSoup

iol_domain = "http://iol2.itba.edu.ar:27521"

class News:
    def __init__(self, service, url):
        ''' Build a news instance from a URL.
        '''

        self.url = url
        self.id = re.findall('ID=(\d+)', url)[0]

        try:
            bs = BeautifulSoup(service._read_url(iol_domain + url))
        except:
            raise Exception('Could not fetch news from %s'%url)

        title = bs.findAll(id='SPFieldText')[0].text
        #UGLY
        title = title[78:-6]
        content = str(bs.findAll(id='SPFieldNote')[0].div.div)

        # Extracto info about the author and timestamp
        info = bs.findAll(id='onetidinfoblock1')[0].span.text
        info_pattern = re.compile('Creado  el ([^&]+)&nbsp; por([^&]+)&nbsp;')
        match = info_pattern.findall(info)[0]
        author = match[1]
        date_created = match[0]

        self.title = title
        self.author = author
        self.content = content
        self.date_created = date_created

    def __repr__(self):
        return self.__unicode__().encode('iso-8859-1')

    def __unicode__(self):
        return u"news titled '%s' at '%s'"%(self.title, self.url)

