# Making a simple Search Engine
This is a set of programs that emulate some of the key functions of a search engine. We basically want to crawl a web site,  
compute the ranks of the collected pages and visualize the network on a graph. 

More specifically:  
1. The first step is to construct a web-crawler(see **spider.py**). The program crawls a site, pulls the series of pages and their hyperlinks into the database(named '**spider.sqlite**') and records the links between pages. The process is restartable, so you can collect more and more pages of different sites without re-crawling already existing ones.  
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
    332 https://www.tinymixtapes.com/news/charli-xcx-announces-new-netflix-series (46757) 45
    How many pages?
    ```  
    We can run **spdump.py** to look at the contents of the database. It prints out the number of *incoming links*, *the old page rank*, *the new page rank*, the *id* of the page, and the *url* of the page. The **spdump.py** program only shows pages that have at least one incoming link to them:  

    ```
    (988, None, 1.0, 1, 'https://www.tinymixtapes.com')
    (988, None, 1.0, 5, 'https://www.tinymixtapes.com/chocolate-grinder')
    ...
    (12, None, 1.0, 556, 'https://www.tinymixtapes.com/artists/mount-eerie')
    988 rows.
    ```  
2. Once we crawl some pages, we can compute their ranks via [PageRank algorithm](https://en.wikipedia.org/wiki/PageRank). The importance of the page is based on the number and quality of inbound links to this page. For each iteration of the algorithm **sprank.py** prints the average change per page of the page rank. The network initially is quite unbalanced and so the individual page ranks are changing wildly. But in a few short iterations, the PageRank converges.  
Here is a sample run of **sprank.py**. You simply tell it how many PageRank iterations to run:
    ```
    How many iterations? 100
    1) Average per-page difference:  1.7059848925641143
    2) Average per-page difference:  0.4187217355892373
    ...
    99) Average per-page difference:  1.8805530158313896e-15
    100) Average per-page difference:  1.4470556012717222e-15
    ```
    You could also reset the PageRank calculations and set ranks of all spidered pages to default using the **spreset.py** program.
3. The last step is to visualize the network of pages in terms of PageRank, which is more natural with an oriented graph. First, we write the pages and links between them out in a JSON format(see **spider.js** file), that's what the **spjson.py** does:
    ```
    Creating JSON output on spider.js...
    How many nodes to put in a graph? 30
    (988, 1.0, 54.8714150365245, 1, 'https://www.tinymixtapes.com'), 
    (988, 1.0, 55.406224149940925, 5, 'https://www.tinymixtapes.com/chocolate-grinder'),
    ...
    (17, 1.0, 2.258073835052772, 29, 'https://www.tinymixtapes.com/writer/leah+b.+levinson')]
    MAXRANK: 55.406224149940925  MINRANK: 0.089815062340995
    Open force.html in a browser to view the visualization
    ```
    Secondly, we use D3.js, some HTML and CSS to put the vertices and edges from **spider.js** on an actual graph. You can view the result by opening the file **index.html** in your web browser or directly on this page: https://hoshinoyutaka.github.io/pagerank_assignment/    
    
    You can click and drag any node and you can also double click on a node to find the URL that is represented by the node.  
    
    Also, the whole process is additive and restartable. You can spider more pages(**spider.py**), compute their ranks(**sprank.py**), write out the data(**spjson.py**) and then just hit the refresh button in a browser(**index.html**) to view an updated version of a graph.
