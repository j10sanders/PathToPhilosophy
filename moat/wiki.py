from bs4 import BeautifulSoup as bs4
import requests
import matplotlib.pyplot as plt
import numpy as np


def visit(url="https://en.wikipedia.org/wiki/", topic="Special:Random",
          current=None, cache=None, iters=0, fails=0, p_lens=None,
          max_iters=None):
    if max_iters is None:
        max_iters = 500
    if iters >= max_iters:
        return fails, p_lens
    else:
        print("Currently on %s of %s pages" % (iters, max_iters))
        if current is None:
            current = {}
        if cache is None:
            cache = {'Philosophy': 0}
        if p_lens is None:
            p_lens = []
        while topic not in cache:
            r = requests.get(url + topic)
            text = remove_parens(r.text)
            soup = (bs4(text,  "html.parser")
                    .select('#mw-content-text p > a'))
            try:
                topic = valid_url(soup)[0][6:]  # [6:] because 'wiki/'
            except ValueError:
                iters += 1
                fails += 1
                return visit(cache=cache, iters=iters, fails=fails,
                             p_lens=p_lens, max_iters=max_iters)
            if topic in current:
                iters += 1
                fails += 1
                return visit(cache=cache, iters=iters, fails=fails,
                             p_lens=p_lens, max_iters=max_iters)
            if len(current) == 0:
                current[topic] = 1
            else:
                for words in current:
                    current[words] += 1
                current[topic] = 1
        if topic in cache:
            if len(current) > 0:
                for x in current:
                    current[x] += cache[topic]
                cache.update(current)
                p_lens.append(max(current.values()))
                iters += 1
            else:
                p_lens.append(cache[topic])
            return visit(cache=cache, iters=iters, fails=fails, p_lens=p_lens,
                         max_iters=max_iters)


def valid_url(soup):
    '''Check if the first link meets certain criteria. If no links in the first
    'paragraph' meet the criteria ('paragraph' is probably a table of images),
    try the next paragraph.'''
    links = []
    for link in soup:
        href = link.get("href")
        dont = ["/wiki/Help", "/wiki/File", "/wiki/User"]
        if not (link.find(class_='image') and href.startswith("/wiki/")
                and not href.startswith(tuple(dont))):
            links.append(link.get("href"))
    if len(links) == 0:
        raise ValueError
    return links


def remove_parens(text):
    '''Parentheses, and anything inside of them, should be removed if they are
    not inside of '<>'s'''
    hrefs, paren, bracket, tbody = [], 0, 0, 0
    '''To cut down on time, only look at first half of text.  This could
    clearly be optimized further, although looking at the first half does
    not increase the risk of missing the link.'''
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
    return links


def analyze(fails, p_lens):
    '''plot the distribution of path lengths and return percentage of
    valid paths'''
    if fails > 0:
        percent_valid = 1 - (fails/len(p_lens))
    else:
        percent_valid = 1
    percent_valid *= 100
    y = []
    x = []
    dist = {}
    for i in p_lens:
        if i in dist:
            dist[i] += 1
        else:
            dist[i] = 1
    for w in sorted(dist.items()):
        y.append(w[0])
        x.append(w[1])
    pos = np.arange(len(y))
    width = 1.0
    print(y, x)
    ax = plt.axes()
    ax.set_xticks(pos + (width / 2))
    ax.set_xticklabels(y)
    plt.ylabel('frequency')
    plt.xlabel('path length')
    plt.bar(pos, x, width, color='r')
    plt.show()

    return percent_valid, sorted(dist.items())


def run():
    print(analyze(*visit()))


if __name__ == '__main__':
    run()
