# coding: utf-8

import urllib2
import re

from BeautifulSoup import BeautifulSoup

from news import News
from foldernode import FolderNode

iol_domain = "http://iol2.itba.edu.ar:27521"
iol_news_grado = "/Lists/Noticias_n/VistaNoticias.aspx"
iol_news = "/Lists/Noticias/AllItems.aspx"
iol_files_grado = "/Material%20Didctico/Forms/Vista%20Material%20Didactico.aspx"
iol_files = "/Archivos/Forms/Vista%20Material%20Didactico.aspx"

class Area:
    def __init__(self, name="", url="", parent=None):
        ''' An area is a category or subcategory that contains files
        and news and information.
        '''
        self.name = name
        self.url = url

        assert(not parent or parent.__class__ == Area)
        self.parent = parent

        self.children = []

    def add_child(self, new_child):
        ''' Receives another Area and saves a reference to it.
        '''
        assert(new_child.__class__ == Area)
        self.children.append(new_child)

    def get_news(self, service):
        ''' Returns a array of News related to this area. The keys are
        the IDs of the news

        Needs a IOL2Service instance to fetch the htmls.
        '''
        if self.__dict__.has_key('news'):
            news = self.news
        else:
            news = {}
            self.news = news

        try:
            url = iol_domain + self.url
            if "GRADO" in url or "grado" in url:
                url += iol_news_grado
            else:
                url += iol_news
            bs = BeautifulSoup(service._read_url(url))

        except:
            raise Exception('Could not read/parse news')

        #UGLY
        if not bs.findAll(name='td', attrs={'id': 'MSOZoneCell_WebPartWPQ2'}):
            raise Exception('No news listing found')

        all_ids = []

        #UGLY
        for entry in bs.findAll(name='td', attrs={'class': 'ms-vb'}):
            try:
                url = entry.a.get('href')
            except:
                break

            # Check if it has my url as a prefix
            if url.find(self.url) == 0:
                id = re.findall('ID=(\d+)', url)[0]
                all_ids.append(id)

                if news.has_key(id):
                    pass
                else:
                    newitem = News(service, url)
                    news.update({newitem.id: newitem})

        # Erase old news
        for item in news.keys():
            if not item in all_ids:
                news.pop(item)

        return news

    def get_root(self, service):
        ''' Returns a FolderNode with all files requested
        '''
        url = iol_domain + self.url
        if "GRADO" in url or "grado" in url:
            url += iol_files_grado
        else:
            url += iol_files
        return FolderNode(url)

    def __unicode__(self):
        return u"area '%s' at '%s', parent=(%s)"%(self.name, self.url,
            self.parent.name if self.parent else None)

    def __repr__(self):
        return self.__unicode__().encode('iso-8859-1')

