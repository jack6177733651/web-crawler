import sys
import requests
from bs4 import BeautifulSoup
from collections import deque
import time


# get all links from a page and return it in an array
def get_neighbors(soup):
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    # for link in soup.find_all('a'):
    #     print(link.get('href'))
    # example code that I used to extract all links
    links = soup.find_all('a')
    neighbors = []
    for link in links:
        link_text = link.get('href')
        # to avoid NoneType link_text
        if isinstance(link_text, str):
            # /wiki/ ensures only wikipedia links, ':' filters wikipedia help links, and also avoid the main page
            if str.startswith(link_text, '/wiki/') and ':' not in link_text and not str.startswith(link_text, '/wiki/Main_Page'):
                # if there's a '#' then only take the link text before it, filter links to sections of the same page
                if '#' in link_text:
                    split = link_text.split('#')
                    link_text = split[0]
                neighbors.append(link_text)
    return neighbors


# main crawl function using bfs
def bfs_crawl(seed, phrase):
    # maintain a set of all visited links
    visited = set()
    # maintain a set of all visited links that actually contain the keyphrase
    crawled = set()
    # maintain a queue structure as the frontier for bfs
    frontier = deque()
    frontier.append(seed)
    # a dictionary to track the depth of pages, where the seed is 1
    url_depth = {seed: 1}
    # while the queue is not empty
    while frontier:
        # if there are 1000 or more pages with the keyphrase then break
        if len(crawled) >= 1000:
            break
        # politeness policy
        time.sleep(1)
        # pop the oldest link added
        popped_link = frontier.popleft()
        http_link = 'https://en.wikipedia.org' + popped_link
        # make a connection to that link
        request = requests.get(http_link)
        # get the page
        page = request.text
        # use beautifulsoup to parse the text
        soup = BeautifulSoup(page, 'lxml')
        # the page of the link has now been visited
        visited.add(popped_link)
        # check if the keyphrase (regardless of case) is in the relevant text of the page, skip this loop if not
        if phrase not in soup.text.lower():
            continue
        # since the page contains the keyphrase add it to the list of crawled links
        crawled.add(popped_link)
        # get all links from the soup of the page
        neighbors = get_neighbors(soup)
        # print statement for human verification that program is working properly
        print(popped_link + " " + str(len(crawled)) + " depth=" + str(url_depth[popped_link]))
        # for every link in the page
        for neighbor in neighbors:
            # check if the link has already been visited
            if neighbor not in visited:
                # if not then get the depth of the current page
                # every neighboring link has that depth + 1
                depth = url_depth[popped_link]+1
                # if the depth of the neighboring link is less or equal to 5
                if depth <= 5:
                    # check if the neighbor's depth has already been assigned before
                    depth_exists = neighbor in url_depth.keys()
                    # if it hasn't that means that this is the first time that link has been encountered
                    if not depth_exists:
                        # append the neighboring link to the queue
                        frontier.append(neighbor)
                        # record the depth of the neighbor
                        url_depth[neighbor] = depth
    return crawled


def main(argv):
    len_arg = len(argv) - 1
    # number of arguments must be either 1 or 2
    if len_arg not in [1, 2]:
        raise TypeError('Wrong number of command line arguments')
    # check if the first argument is a wikipedia link
    if 'https://en.wikipedia.org' not in argv[1]:
        raise TypeError('The first argument must be a wikipedia link')
    # parse only the /wiki/name-of-page part of the link
    initial_seed = argv[1][24:]
    # set the keyphrase depending whether there's a second argument, turn it to lower case
    if len_arg == 1:
        key = ''
    else:
        key = argv[2].lower()
    # get all crawled links
    crawled_urls = bfs_crawl(initial_seed, key)
    # write the links to a txt file
    f = open("crawled_urls.txt", "w+", encoding="utf-8")
    for url in crawled_urls:
        f.write('https://en.wikipedia.org' + url + "\n")
    f.close()


if __name__ == "__main__":
    main(sys.argv)
