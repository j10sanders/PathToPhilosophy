from bs4 import BeautifulSoup
import requests
import re

#/wiki/Philippines
def visit(url="https://en.wikipedia.org", topic="/wiki/Philippines",
visited=None):
    if visited == None:
        visited = {}
    print(topic)
    if topic in visited:
        return "Ran into a cycle -- %s came up twice" % (topic)
    else:
        visited[topic] = 1
    r = requests.get(url + topic)
    #print(r.text)
    text = remove_parens(r.text)
    # BeautifulSoup(text, "html.parser").select('#mw-content-text li > a') + 
    soup = BeautifulSoup(text,  "html.parser").select('#mw-content-text p > a')
    try:
        topic = valid_url(soup)[0]
    except ValueError:
        return "No valid links on %s" %(topic)
    if topic != "/wiki/Philosophy":
        return visit(url, topic, visited)
    return topic

#and ":" not in href
def valid_url(soup):
    ''' Check if the first link meets certain criteria. If no links in the first 
    'paragraph' meet the criteria ('paragraph' is probably a tbody of images), 
    try the next paragraph.'''
    links = []
    while len(links) == 0:
        for link in soup:
            #print(link)
            href = link.get("href")
            dont = ["/wiki/Help", "/wiki/File", "/wiki/User"]
            if not link.find(class_='image') and href.startswith("/wiki/") and not href.startswith(tuple(dont)):
                links.append(link.get("href"))
                #print(link.get("href"))
        if len(links) == 0:
            raise ValueError
    return links
    
    
def remove_parens(text):
    '''Parentheses, and anything inside of them, should be removed if they are
    not inside of '<>'s'''
    hrefs, paren, bracket, tbody = [], 0, 0, 0
    '''To cut down on time, only look at first quarter of text.  This could 
    clearly be optimized further'''
    #print(len(text))
    for i in range(len(text)):
        if bracket == 0 and tbody == 0 and text[i] == '(':
            paren += 1
        elif bracket == 0 and tbody == 0 and text[i] == ')':
            paren -= 1
        elif text[i] == '<':
            if text[i:i+6] == '<tbody':
                tbody += 1
                bracket += 1
                #print("9hiusadhsa")
            elif text[i:i+8] == '</tbody>':
                tbody -= 1
            elif paren == 0:
                bracket += 1
        elif text[i] == '>':
            if text[i-6:i] == '/tbody':
                #print("YUP")
                pass
            elif paren == 0:
                bracket -= 1
        #print(i, text[i], paren, bracket, tr)
        if paren == 0 and tbody == 0:
            # and (bracket == 1 or text[i] == '>')
            hrefs.append(text[i])
            #print(hrefs)
    links = "".join(hrefs)
    #print(links)
    return links

print(visit())
