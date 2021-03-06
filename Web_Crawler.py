index=[] # We create an nested list where the associated url's are stored against each keyword

def get_page(url): # Here we acquire the source code of the page. This is an in built function. 
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

def add_to_index(index, keyword, url):
    for entry in index:
        if entry[0] == keyword:
            entry[1].append(url)
    return index.append([keyword, [url]])
    

def lookup(index, keyword): 
    for entry in index:
        if entry[0] == keyword:
            return entry[1]
    


def add_page_to_index(index, url, content): # We add the content of the page to the the index. The words in this page serve as keywords
                                            # for the associated url
    words = content.split()
    for word in words:
        add_to_index(index, word, url)


def get_target_link(page):
    startpos = page.find('<a href=') # Most hyperlinks begin with '<a href'
    if startpos == -1:
        return None, 0
    startquote = page.index('"', startpos)
    endquote = page.index('"', startquote+1)
    return page[startquote+1:endquote], endquote


def get_all_links(page): # Gets all the links on a given page
    links = []
    while True:
        url,endpos = get_target_link(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break;
    return links


def union(p, q): # To append crawled pages in order to prevent recrawling of the same page
    for e in q:
        if e not in p:
            p.append(e)

def crawl_web(seed): 
    tocrawl = [seed]
    index = []
    
    crawled = []
    for e in range(20): 
        page = tocrawl.pop()
        if not page in crawled :
            content = get_page(page)
            add_page_to_index(index, page, content)
            union(tocrawl, get_all_links(content))
            crawled.append(page)
    return index
    

print('\n\n\tWELCOME TO MAYUR\'S SEARCH ENGINE!!')
user_url = input('Enter the seed page\'s url: ')
srch = input('Enter the key word to look up: ')
print lookup(crawl_web(user_url), srch)
