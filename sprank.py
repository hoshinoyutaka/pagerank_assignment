import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

# Getting the ids(from_ids) that send out page rank. 
cur.execute('SELECT DISTINCT from_id FROM Links')
from_ids = list()
for row in cur:
    from_ids.append(row[0])

#print('FROM IDS:', from_ids, end = ', ')

# Getting the ids(to_ids) that receive page rank - we only are intrested in pages
# that have inbound and outbound links to ensure an algorithm works properly.
# In result we get a strongly connected oriented graph.
cur.execute('SELECT DISTINCT from_id, to_id FROM Links')
to_ids = list()
links = list()
for row in cur:
    from_id = row[0]
    to_id = row[1]
    if from_id == to_id: continue
    if from_id not in from_ids: continue
    if to_id not in from_ids: continue
    links.append(row)
    if to_id not in to_ids: to_ids.append(to_id)

#print('TO IDS:', to_ids)

# Set up the previous ranks
prev_ranks = {}
for page in from_ids:
    cur.execute('SELECT new_rank FROM Pages WHERE id = ?', ( page, ) )
    prev_ranks[page] = cur.fetchone()[0]

#print('PREV_RANKS: ', list(prev_ranks.items())[:10])

sval = input('How many iterations? ')
many = 1
if ( len(sval) > 0 ): many = int(sval)

# Sanity check
if ( len(prev_ranks) < 1 ) : 
    print('Nothing to PageRank. Check data.')
    many = 0
    quit()

# Compute a page rank in memory so it really runs fast
for i in range(many):
    # Set up new ranks but not actually computing them. We also compute the sum of all old_ranks.
    new_ranks = {}
    total = 0.0
    for page, old_rank in list(prev_ranks.items()):
        total = total + old_rank
        new_ranks[page] = 0.0
    #print('TOTAL:', total)
    
    # Find the number of outbound links and sent the page rank down each
    for page, old_rank in list(prev_ranks.items()):
        give_ids = list()
        for from_id, to_id in links:
            if from_id != page: continue
            #print(from_id, to_id)
            if to_id not in to_ids: continue #double guardian
            give_ids.append(to_id)
        if ( len(give_ids) < 1) : continue
        
        amount = old_rank / len(give_ids)
        #print(page, old_rank, amount, give_ids)

        for id in give_ids:
            new_ranks[id] =  new_ranks[id] + amount
        
    #print('NEW_RANKS: ', list(new_ranks.items())[:10])

    newtotal = sum(list(new_ranks.values()))
    #print('NEW TOTAL: ', newtotal)

    d = (total - newtotal) / len(new_ranks)
    #print('d: ', d)

    # Make amortization with d coefficient so the algorithm converges.
    for page in new_ranks:
        new_ranks[page] = new_ranks[page] + d

    #print('NEW_RANKS AFTER AMORTIZATION: ', new_ranks)

    # Compute the per-page average change from old rank to new rank
    # as an indication of convergence of the algorithm.
    totdiff = 0
    for page, old_rank in list(prev_ranks.items()):
        new_rank = new_ranks[page]
        diff = abs(old_rank - new_rank)
        totdiff = totdiff + diff

    avetotdiff = totdiff / len(prev_ranks)
    print(str(i+1)+') Average per-page difference: ', avetotdiff)

    # Rotate
    prev_ranks = new_ranks

# Put the final ranks back into the table
print('FINAL NEW_RANKS: ', list(new_ranks.items())[:10])
cur.execute('UPDATE Pages SET old_rank = new_rank')
for page, new_rank in list(new_ranks.items()):
    cur.execute('UPDATE Pages SET new_rank = ? WHERE id = ?', ( new_rank, page) )
conn.commit()
    
cur.close()
conn.close()