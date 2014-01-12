'''
Created on 27. des. 2013

@author: frankda
'''

import urllib2
from bs4 import BeautifulSoup
import json

local = False #Set to false in order to get content from live site

'''http://idrett.speaker.no/07/organisation.aspx?id=609143&HideKO=y
'''


base_link = "http://idrett.speaker.no/07/organisation.aspx?id=%(ID_String)s&HideKO=y"
link = base_link % {"ID_String":"542742"}

# COMMENTED OUT FOR DEBUGGING IN ORder to Not hit site too much
if not local:
    req = urllib2.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    myfile = urllib2.urlopen(req).read()
else:
    with open("../teamshtml.txt", "r") as f:           
        myfile = f.read()  

soup = BeautifulSoup(myfile)

#Get all org-ids for Ull/Kisa teams
selectSection = soup.find("select", {"name":"lstOrganisation"})
#selsec = soup.select
st = []

for child in selectSection('option'):
    keyval = []
    print child.get('value')+","+child.string

    st.append((child.get('value'), child.string))
     
print json.dumps(st)
with open('teamlist.txt', 'w') as outfile:
  json.dump(st, outfile)
outfile.close

''' Now getting all the team schedules
'''
fixtures = []
tblFixtures = []
for s in st:
    #print s
    link = base_link % {"ID_String":str(s[0])}
    ''''f = urllib.urlopen(link)
    myfile = f.read()
    '''
    
    if not local:
        req = urllib2.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
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
        count+=1

    tblFixtures.append((s[0], s[1], tblTeamFixtures))
    
with open('../fixtures.txt', 'w') as outfile:
    json.dump(tblFixtures, outfile)
outfile.close    

if __name__ == '__main__':
    pass