'''
Created on 28. des. 2013

@author: frankda
'''
import urllib2
from bs4 import BeautifulSoup
import json


class ParseSpeakerNo(object):
    '''
    classdocs
    '''
    outputFileName = ""
    #http://idrett.speaker.no/07/organisation.aspx?id=609143&HideKO=y
    #base_link = "http://idrett.speaker.no/07/organisation.aspx?id=%(ID_String)s&HideKO=y"
    
    def __init__(self, outfile, base_link):
        '''
        Constructor
        '''
        self.outfile = outfile
        self.base_link = base_link
    
    def parse(self, startID):
        local = False #Set to false in order to get content from live site
        
        link = self.base_link % {"ID_String":startID}
        
        req = urllib2.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        myfile = urllib2.urlopen(req).read()
        soup = BeautifulSoup(myfile)
        
        #Get all org-ids for Ull/Kisa teams
        selectSection = soup.find("select", {"name":"lstOrganisation"})
        #selsec = soup.select
        st = []
        
        for child in selectSection('option'):
            keyval = []
            print child.get('value')+","+child.string
        
            st.append((child.get('value'), child.string))
            #st.append((child.string, (child.get('value'))))
             
        #Now getting all the team fixtures
        fixtures = []
        tblFixtures = []
        local = False
        for s in st:
            #print s
            #link = base_link % {"ID_String":str(s[0])}
            link = self.base_link % {"ID_String":s[0]}
            if not local:
                req = urllib2.Request(link, headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/5.0)'})
                myfile = urllib2.urlopen(req).read()
                #myfile = f.read()
            else:
                with open("../fixtureshtml.txt", "r") as f:
                    myfile = f.read()       
        
            soup = BeautifulSoup(myfile)
           
            fixtures = soup.find(id='listNext')
            dates = fixtures.findAll("tr","odd")
            games = fixtures.findAll("tr","even")
            tblTeamFixtures = []
            count = 0
            for nst in dates:
                tblTeamFixtures.append((nst.text, games[count]("td")[0].text,games[count]("td")[1].text,games[count].find("a")["href"]))
                print nst.text
                print games[count]("td")[0].text
                print games[count]("td")[1].text
                print games[count].find("a")["href"]
                count +=1
            tblFixtures.append((s[0], s[1], tblTeamFixtures))
        return ((("Teams",st),("Fixtures",tblFixtures)))