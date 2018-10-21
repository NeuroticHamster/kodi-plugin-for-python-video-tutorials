
'''
https://kodi.wiki/view/HOW-TO:Write_python_scripts
'''
from urlparse import parse_qsl
import sys
import xbmc, xbmcgui, urllib3
import requests
import re
from collections import OrderedDict, Counter



action_enter = 7
action_escape = 10

class main_layout(xbmcgui.Window):
    def __init__(self):
        self.addControl(xbmcgui.ControlImage(275,100,800,600, '/usr/share/kodi/addons/firstplugin/python.jpg'))
        self.strActionInfo = xbmcgui.ControlLabel(400, 50, 400, 400, 'font13', '#ffffff')
        self.addControl(self.strActionInfo)
        self.strActionInfo.setLabel(str('intro to python videos'))
        
        self.initializedbutton()
        
        
    def onAction(self, action):
      
        if action == action_enter:             
            self.popup('Nothing selected')
            
        if action == action_escape:
            self.close()
    def initializedbutton(self):
        titlelist = []
        self.dict_pos = {}
        newlist = []
        self.keyvalue = {}
        #I removed the playlist from the url look up. I'd at least like to ask before i post a kodi plugin of someone elses videos.
        url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=<add youtube api playlist here>'
        urls = requests.get(url)
        values = urls.text
        npage = re.findall(r'nextPageToken": ".+"', values)

        for item in npage:
            nextpage = item.split('nextPageToken": "')[-1]
        nextpage = nextpage.replace('"', '')
        
        
        
        serchterm = re.findall(r'videoId".+', values)
        for item in serchterm:
            change = item.split('Id": "')[-1]
            newlist.append(change.replace('"', ''))
    
        results = re.findall(r'title":.+', values)
        for item in results:
            titlelist.append(item.split('title": ')[-1 ])
            
           
        self.list = xbmcgui.ControlList(25,150,800,900)
        self.addControl(self.list)
        for item in titlelist:
            self.list.addItem(str(item))
            self.setFocus(self.list)
        for item, items in zip(titlelist, newlist):
            self.keyvalue[str(item)]= str(items)
        
        
        self.pagbutton(nextpage, newlist, titlelist)
        
    def pagbutton(self, nextpage, newl=None, titlel=None):
        newlist = []
        titlelist = []
        url2 = requests.get('https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&pageToken=' + str(nextpage) + '<youtube playlist remove for github upload>')
        values = url2.text
        serchterm = re.findall(r'videoId".+', values)
        for item in serchterm:
            change = item.split('Id": "')[-1]
            newlist.append(change.replace('"', ''))
    
        results = re.findall(r'title":.+', values)
        for item in results:
            titlelist.append(item.split('title": ')[-1 ])
        for item in titlelist:
            self.list.addItem(str(item))
        for item, items in zip(titlelist, newlist):
            self.keyvalue[str(item)]= str(items)
        self.new = newlist + newl
        self.title = titlelist + titlel
        return self.new, self.title
    def popup(self, message):
        pops = xbmcgui.Dialog()
        pops.ok('This is the name', message)
            
    def onControl(self, control, vid=0):
        self.first_chunk = 'plugin://plugin.video.youtube?action=play_video&videoid='
        
        if control == self.list:
            
            item = self.list.getSelectedItem()
            vid = self.keyvalue.get(str(item.getLabel()))
            self.vid = self.first_chunk + str(vid)
            self.nexttrack()
            #self.popup(str(item.getLabel()))
            
            
            
            
    def nexttrack(self, labvalue=0):
        
##        h = h.keys()
       
        item = self.list.getSelectedItem()
        labvalue = int(self.title.index(str(item.getLabel())))
        labvalue += 1
        self.playvid(labvalue)
   
        
        
            
            
            
            
            
            
        
        
                
        
        
        
        

    
    def playvid(self, labvalue):
        nextvid = self.first_chunk + str(self.new[labvalue])
        #self.popup(str(self.new[labvalue]))
        self.vidplay = xbmc.Player()
        self.playlist= xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        self.playlist.add(str(self.vid))
        self.playlist.add(str(nextvid))
        self.vidplay.play(self.playlist)
        
        
main = main_layout()
main .doModal()
del main