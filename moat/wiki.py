from bs4 import BeautifulSoup
import requests
import re




def visit(url="https://en.wikipedia.org/wiki/", topic="78rpm_record",
visited=None, current=None, cache=None, iters=0, fails=0, p_lens=None):
    if iters == 10:
        return analyze(fails, p_lens)
    else:
        if visited is None:
            visited = []
        if current is None:
            current = {}
        if cache is None:
            cache = {'Science': 4, 'Knowledge': 3, 'Awareness': 2, 'Quality_(philosophy)': 1, 'Property_(philosophy)': 0}
        if p_lens is None:
            p_lens = []
        r = requests.get(url + topic)
        text = remove_parens(r.text)
            # BeautifulSoup(text, "html.parser").select('#mw-content-text li > a') + 
        soup = BeautifulSoup(text,  "html.parser").select('#mw-content-text p > a')
        try:
            topic = valid_url(soup)[0][6:]  # [6:] because 'wiki/'
        except ValueError:
            iters += 1
            fails += 1
            print(fails, topic)
            return visit(cache=cache, iters=iters, fails=fails, p_lens=p_lens)
        print(topic)
        if topic == "Philosophy":
            visited.append('Philosophy')
            if len(current) > 0:
                p_lens.append(max(current.values()))
            else:
                p_lens.append(0)
            iters += 1
            print("CACHE -:", len(cache), iters, p_lens)
            return visit(cache=cache, iters=iters, fails=fails, p_lens=p_lens)
        elif topic in current:
            visited.append(topic)
            iters += 1
            fails += 1
            return visit(cache=cache, iters=iters, fails=fails, p_lens=p_lens)
        elif topic in cache:
            for x in current:
                current[x] += cache[topic]
            print("current: ", current, "cache:", cache)
            cache.update(current)
            p_lens.append(max(current.values()))
            iters += 1
            print("CACHE -:", len(cache), iters, p_lens)
            return visit(cache=cache, iters=iters, fails=fails, p_lens=p_lens)
        else:
            visited.append(topic)
            if len(current) == 0:
                current[topic] = 1
            else:
                for words in current:
                    current[words] += 1
                current[topic] = 1
            print(current)
            return visit(url, topic, visited, current, cache=cache, fails=fails, iters=iters, p_lens=p_lens)


def valid_url(soup):
    ''' Check if the first link meets certain criteria. If no links in the first 
    'paragraph' meet the criteria ('paragraph' is probably a table of images), 
    try the next paragraph.'''
    links = []
    for link in soup:
        href = link.get("href")
        dont = ["/wiki/Help", "/wiki/File", "/wiki/User"] 
        if not link.find(class_='image') and href.startswith("/wiki/") and not href.startswith(tuple(dont)):
            links.append(link.get("href"))
    if len(links) == 0:
        raise ValueError
    return links


def remove_parens(text):
    '''Parentheses, and anything inside of them, should be removed if they are
    not inside of '<>'s'''
    hrefs, paren, bracket, tbody = [], 0, 0, 0
    '''To cut down on time, only look at first quarter of text.  This could 
    clearly be optimized further'''
    for i in range(len(text)):
        if bracket == 0 and tbody == 0 and text[i] == '(':
            paren += 1
        elif bracket == 0 and tbody == 0 and text[i] == ')':
            paren -= 1
        elif text[i] == '<':
            if text[i:i+6] == '<tbody':
                tbody += 1
                bracket += 1
            elif text[i:i+8] == '</tbody>':
                tbody -= 1
            elif paren == 0:
                bracket += 1
        elif text[i] == '>':
            if text[i-6:i] == '/tbody':
                pass
            elif paren == 0:
                bracket -= 1
        if paren == 0 and tbody == 0:
            hrefs.append(text[i])
    links = "".join(hrefs)
    #print(links)
    return links


def analyze(fails, p_lens):
    percent_valid = len(p_lens)/fails
    distribution = {}
    for i in p_lens:
        if i in distribution:
            distribution[i] += 1
        else:
            distribution[i] = 1

    return percent_valid, sorted(distribution.items())

print(visit())
