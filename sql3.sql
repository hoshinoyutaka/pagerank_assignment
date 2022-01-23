SELECT P1.url, P1.id, Links.from_id, Links.to_id, P2.id, P2.url 
     FROM Pages AS P1 JOIN Links JOIN Pages as P2 ON P1.id = Links.from_id
     AND Links.to_id = P2.id
     WHERE P1.html IS NOT NULL AND P2.html is not NULL