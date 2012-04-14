from bs4 import BeautifulSoup

def multi_lookup(index, query):
    urls = []
    url_query_positions = []

    for i in range(len(query)):
        url_positions = lookup(index, query[i])
        if not url_positions:
            return urls
        for url_position in url_positions:
            if not len(url_query_positions):
                position = [None for x in range(len(query) + 1)]
                position[0] = url_position[0]
                position[i + 1] = url_position[1]
                url_query_positions.append(position)
            else:
                found = False
                new_url_query_positions = []
                for j in range(len(url_query_positions)):
                    if url_query_positions[j][0] == url_position[0]:
                        found = True
                        if url_query_positions[j][i + 1] is None:
                            url_query_positions[j][i + 1] = url_position[1]
                        else:
                            new_position = list(url_query_positions[j])
                            new_position[i + 1] = url_position[1]
                            new_url_query_positions.append(new_position)
                url_query_positions.extend(new_url_query_positions)
                if not found:
                    new_position = [None for x in range(len(query) + 1)]
                    new_position[0] = url_position[0]
                    new_position[i + 1] = url_position[1]
                    url_query_positions.append(new_position)

    for url_query_position in url_query_positions:
        prev_position = -999
        consecutive = True
        position_list = []
        for i in range(1, len(query) + 1):
            position_list.append(url_query_position[i])
            #position_list.sort()
        for position in position_list:
            if prev_position is -999:
                prev_position = position
            else:
                if position is None:
                    consecutive = False
                    break
                #elif abs(position - prev_position) != 1:
                elif position - prev_position != 1:
                    consecutive = False
                    break
                else:
                    prev_position = position
        if consecutive and (url_query_position[0] not in urls):
            urls.append(url_query_position[0])

    return urls


def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph


def get_all_links(page):
    soup = BeautifulSoup(page)
    links = []
    for string in soup.stripped_strings:
        print(repr(string))
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links


def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)


def add_page_to_index(index, url, content):
    words = content.split()
    for position in range(len(words)):
        add_to_index(index, words[position], url, position)


def add_to_index(index, keyword, url, position):
    if keyword in index:
        index[keyword].append([url, position])
    else:
        index[keyword] = [[url, position]]


def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None


cache = {
    'http://www.udacity.com/cs101x/final/multi.html': """<html>
<body>

<a href="http://www.udacity.com/cs101x/final/a.html">A</a><br>
<a href="http://www.udacity.com/cs101x/final/b.html">B</a><br>

</body>
""",
    'http://www.udacity.com/cs101x/final/b.html': """<html>
<body>

Monty likes the Python programming language
Thomas Jefferson founded the University of Virginia
When Mandela was in London, he visited Nelson's Column.

</body>
</html>
""",
    'http://www.udacity.com/cs101x/final/a.html': """<html>
<body>

Monty Python is not about a programming language
Udacity was not founded by Thomas Jefferson
Nelson Mandela said "Education is the most powerful weapon which you can
use to change the world."
</body>
</html>
""",
    }


def get_page(url):
    if url in cache:
        return cache[url]
    else:
        print "Page not in cache: " + url
        return None


index, graph = crawl_web('http://www.udacity.com/cs101x/final/multi.html')
#print index

print multi_lookup(index, ['Thomas', 'Jefferson'])
#>>> ['http://www.udacity.com/cs101x/final/b.html', 'http://www.udacity.com/cs101x/final/a.html']

