import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

print('Creating JSON output on spider.js...')
howmany = int(input('How many nodes to put in a graph?'))

cur.execute('''SELECT COUNT(from_id) AS inbound, old_rank, new_rank, id, url 
     FROM Pages JOIN Links ON Pages.id = Links.to_id
     WHERE html IS NOT NULL AND error IS NULL
     GROUP BY id ORDER BY id, inbound DESC''')

fname = 'spider.js'
fhand = open(fname, 'w', encoding = 'utf-8')
pages = list()
maxrank = None
minrank = None
for row in cur:
    pages.append(row)
    rank = row[2]
    if (maxrank is None) or (rank > maxrank) : maxrank = rank
    if (minrank is None) or (rank < minrank) : minrank = rank
    if len(pages) >= howmany : break

if maxrank == minrank or maxrank is None or minrank is None:
    print('Error occured. Please run sprank.py to compute page rank or check the database')
    quit()

print(pages[:10])

print('MAXRANK:',maxrank,' MINRANK:', minrank)

fhand.write('spiderJson = {"nodes":[\n')
count = 0
json_map = dict()  #connecting "nodes" list with "links" list in our JSON(see the contents of spider.js)
ranks = dict()
for row in pages:
    if count > 0 : fhand.write(',\n')
    #print(row)
    rank = row[2]
    rank = 19 * (rank - minrank) / (maxrank - minrank)
    fhand.write('{'+'"weight":'+str(row[0])+',"rank":'+str(rank)+',')
    fhand.write(' "id":'+str(row[3])+', "url":"'+row[4]+'"}')
    json_map[row[3]] = count
    ranks[row[3]] = rank
    count = count + 1
fhand.write('],\n')

print(list(json_map.items())[:10])
print(list(ranks.items())[:10])

cur.execute('''SELECT DISTINCT from_id, to_id FROM Links''')
fhand.write('"links":[\n')

count = 0
for row in cur:
    if (row[0] not in json_map) or (row[1] not in json_map): continue
    if count > 0 : fhand.write(',\n')
    rank = ranks[row[0]]
    srank = 19 * (rank - minrank) / (maxrank - minrank)
    fhand.write('{"source":'+str(json_map[row[0]])+',"target":'+str(json_map[row[1]])+',"value":3}')
    count = count + 1
fhand.write(']};')
fhand.close()

cur.close()
conn.close()

print("Open force.html in a browser to view the visualization")
