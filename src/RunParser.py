'''
Created on 28. des. 2013

@author: frankda
'''
from ParseSpeakerNo import ParseSpeakerNo
import json

parser = ParseSpeakerNo("outtest1.txt", "http://idrett.speaker.no/07/organisation.aspx?id=%(ID_String)s&HideKO=y")

tbl= parser.parse("542742")
with open('../parser_test.txt', 'w') as outfile:
    json.dump(tbl, outfile)
outfile.close 
if __name__ == '__main__':
    pass