import urllib.request, urllib.parse, urllib.error
import sqlite3
from bs4 import BeautifulSoup
import ssl
import os

# Certificat errors handling for https sites
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#if os.path.exists('spider.sqlite'):
#    os.remove('spider.sqlite')

conn = sqlite3.connect('spider.sqlite')

cur = conn.cursor()
#cur.executescript('''DROP TABLE IF EXISTS Pages;
#                     DROP TABLE IF EXISTS Links;
#                     DROP TABLE IF EXISTS Webs   ''')

cur.execute('''CREATE TABLE IF NOT EXISTS Pages
            (id INTEGER PRIMARY KEY, url TEXT UNIQUE, html TEXT,
             error INTEGER, old_rank REAL, new_rank REAL)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Links 
            (from_id INTEGER, to_id INTEGER, UNIQUE(from_id, to_id))''')

cur.execute('''CREATE TABLE IF NOT EXISTS Webs(url TEXT UNIQUE)''')

# Check to see if we are already in progress...
cur.execute('SELECT id, url FROM Pages WHERE html IS NULL AND error IS NULL LIMIT 1')
row = cur.fetchone()
if row is not None:
    print("Restarting existing crawl. Remove spider.sqlite to restart the crawl.")
else:
    starturl = input('Enter web url or press Enter: ')
    if ( len(starturl) < 1 ): starturl = 'http://www.dr-chuck.com/'       #Set up a default starting host
    if ( starturl.endswith('/') ): starturl = starturl[:-1]
    web = starturl
    if ( starturl.endswith('.htm') ) or ( starturl.endswith('.html') ):
        pos = starturl.rfind('/')
        web = starturl[:pos]

    if ( len(web) > 1 ):
        cur.execute('INSERT OR IGNORE INTO Webs(url) VALUES ( ? )', (web,))
        cur.execute('INSERT OR IGNORE INTO Pages(url, html, new_rank) VALUES( ?, NULL, 1.0)', (starturl,))
        conn.commit()

# Get the current webs
webs = [ str(row[0]) for row in cur.execute('SELECT url FROM Webs') ]   
print(webs)

many = 0
while True:
    if ( many < 1 ):
        sval = input('How many pages?')
        if ( len(sval) < 1 ): break
        many = int(sval)
    many = many - 1
    
    cur.execute('SELECT id, url FROM Pages WHERE html is NULL AND error is NULL ORDER BY RANDOM() LIMIT 1')
    try:
        row = cur.fetchone()
        fromid = row[0]
        url = row[1]
    except:
        print('No unretrieved HTML pages found')
        many = 0
        break
    
    print(fromid, url, end = ' ')
    
    # If we are retrieving this page, there should be no links from it
    cur.execute('DELETE FROM Links WHERE from_id = ?', (fromid,))
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        req = urllib.request.Request(url, headers = {'User-Agent': user_agent.encode()})
        document = urllib.request.urlopen(req, context=ctx)
        
        html = document.read()
        #print(html[:100])
        if document.getcode() != 200:
            print('Error on page: ', document.getcode())
            cur.execute('UPDATE Pages SET error = ? WHERE url = ?', (document.getcode(), url) )
        
        if 'text/html' != document.info().get_content_type() :
            print('Ignore non text/html page')
            cur.execute('DELETE FROM Pages WHERE url = ?', (url,) )
            conn.commit()
            continue
        
        print('('+str(len(html))+')', end = ' ')
        
        soup = BeautifulSoup(html, 'html.parser')
    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user')
        break
    except:
        print('Unable to retrieve or parse a page')
        cur.execute('UPDATE Pages SET error = -1 WHERE url = ?', (url, ) )
        conn.commit()
        continue
    
    cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0)', (url, ) )
    cur.execute('UPDATE Pages SET html = ? WHERE url = ?', (memoryview(html), url ) )
    conn.commit()

    # Retrieve all of the anchor tags
    tags = soup('a')
    count = 0
    for tag in tags:
        href = tag.get('href', None)
        if ( href is None ) : continue
        # Resolve relative references like href="/contact"
        up = urllib.parse.urlparse(href)
        if ( len(up.scheme) < 1 ):
            href = urllib.parse.urljoin(url, href)
        ipos = href.find('#')
        if ( ipos > 1 ) : href = href[:ipos]
        if ( href.endswith('.png') ) or ( href.endswith('.jpg') ) or ( href.endswith('.gif') ): continue
        if ( href.endswith('/') ) : href = href[:-1]
        #print(href)
        if ( len(href) < 1 ) : continue
            
        # Check if the URL is in any of the webs. Webs are for pretty visualization so we only search 
        # for tags within a couple of our webs(implying sites we crawl)
        
        found = False
        for web in webs:
            if href.startswith(web) : 
                found = True
                break
        if not found: continue   #skip the tag outside of our network
        
        cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0  )', ( href, ) )
        count = count + 1 
        conn.commit()
        
        cur.execute('SELECT id FROM Pages WHERE url = ? LIMIT 1', ( href, ) )
        try:
            row = cur.fetchone()
            toid = row[0]
        except:
            print('Could not retrieve id')
            continue
        
        #print('\n',url, fromid, toid, href)
        
        cur.execute('INSERT OR IGNORE INTO Links (from_id, to_id) VALUES ( ?, ? )', ( fromid, toid ) ) 
        
    print(count)

cur.close()
conn.close()
