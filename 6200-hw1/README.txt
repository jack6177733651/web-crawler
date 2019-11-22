Environment: python 3
External Libraries: requests, bs4, lxml

My code is in a python file called crawler.py. It takes in two command line arguments, the first is necessary and must be a valid English 
Wikipedia link, the second is optional and is a keyphrase that must be present in every crawled page. To run this script type 
python crawler.py command-1 command-2(optional) into the machine terminal. 

During runtime the script will output a printed line for every page that it crawls in the format as follows "link number-of-crawled-pages-so-far
depth-of-the-page-from-seed-page". This is to provide some form of visual information that the script is running properly and not stuck in a
loop, as the total runtime is quite long. When the program finishes execution it will write the 1000 (or less) crawled links to a text file
called "crawled_urls.txt". The order of links is random due to my storage of links in a hashed set.

Using my count.py script I calculated the prevalence of 'retrieval'. Out of the 1000 paged retrieved by the full crawl without a keyphrase, 
27 of them were also retrieved by the focused crawl for 'retrieval'. This equates to a 2.7% prevalence of 'retrieval' on wikipedia 
(which is almost certainly a vast overestimate). 