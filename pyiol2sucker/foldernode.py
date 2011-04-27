# coding: utf-8

import urllib2
import re

from BeautifulSoup import BeautifulSoup

from filenode import FileNode

iol_domain = "http://iol2.itba.edu.ar:27521"

class FolderNode:

    def __init__(self, url, path="", name="/", parent=None):
        '''
        '''
        self.name = name
        self.url = url
        self.parent = parent
        self.path = path


    def get_files(self, service):
        if self.__dict__.has_key('children'):
            return self.children

        bs = BeautifulSoup(service._read_url(self.url))
        try:
            pass
        except:
            raise Exception('Could not list directory '+url)

        #UGLY
        table = bs.findAll(name='table', attrs={'id': 'onetidDoclibViewTbl0'})
        if not table:
            raise Exception('No files found.')

        # Pick the first (and hopefully only) table
        table = table[0]

        children = {}
        # [1:] to skip the header
        for entry in table.findAll(name='tr', recursive=False)[1:]:
            tds = entry.findAll(name='td', recursive=False)
            icon_td = tds[0]

            folder = icon_td.a.get('href').find('Folder') != -1

            childurl = icon_td.a.get('href')
            childname = tds[1].text

            if folder:
                children.update({childname: 
                    FolderNode(url=childurl, path=self.path+"/"+childname, 
                        name=childname, parent=self)
                })

            else:
                children.update({childname: 
                    FileNode(name=childname, path=self.path+"/"+childname,
                        url=iol_domain+childurl, parent=self)
                })

        self.children = children
        return children

    def __unicode__(self):
        return u'folder "%s" with path %s'%(self.name, self.path)

    def __repr__(self):
        return self.__unicode__().encode('iso-8859-1')

