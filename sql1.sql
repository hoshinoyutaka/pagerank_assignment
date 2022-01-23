SELECT COUNT(from_id), to_id 
     FROM Links 
     GROUP BY to_id 
     ORDER BY 1 DESC