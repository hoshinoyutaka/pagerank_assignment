# Making a simple Search Engine
This is the set of programs that emulate some of the key functions of the search engine. We basically want to crawl a web site,  
compute the ranks of the collected pages and visualize the network on a graph. 

More specifically:  
1. The first step is to construct a web-crawler(see **spider.py**). The program crawls a site, pulls the series of pages and their hyperlinks into the database(named 'spider.sqlite') and records the links between pages. The process is restartable, so you can collect more and more pages of different sites without re-crawling already existing ones.  
Here is a sample run, with each iteration we choose randomly amongst non-visited pages:
```
Enter web url or press Enter: https://www.tinymixtapes.com
How many pages? 30
1 https://www.tinymixtapes.com (57415) 115
51 https://www.tinymixtapes.com/live-blog/perfume (46357) 41
25 https://www.tinymixtapes.com/writer/shane+mack (43529) 81
12 https://www.tinymixtapes.com/mix-tapes (47800) 63
...
269 https://www.tinymixtapes.com/features/favorite-100-songs-of-the-decade?page=10 (56790) 57
332 https://www.tinymixtapes.com/news/charli-xcx-announces-new-netflix-series-im-band-nasty-cherry (46757) 45
How many pages?
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We can run **spdump.py** to look at the contents of the database. It prints out the number of *incoming links*, *the old page rank*, *the new &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;page rank*, the *id* of the page, and the *url* of the page. The **spdump.py** program only shows pages that have at least one incoming &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;link to them:
```
(988, None, 1.0, 1, 'https://www.tinymixtapes.com')
(988, None, 1.0, 5, 'https://www.tinymixtapes.com/chocolate-grinder')
...
(12, None, 1.0, 556, 'https://www.tinymixtapes.com/artists/mount-eerie')
988 rows.
```
2. Once we crawl some pages, we can compute their ranks via [PageRank algorithm](https://en.wikipedia.org/wiki/PageRank). The importance of the page is based on the number and quality of inbound links to this page.   
Here is a sample run of **sprank.py**. You simply tell it how many PageRank iterations to run:
```
dfsfdfs
```
