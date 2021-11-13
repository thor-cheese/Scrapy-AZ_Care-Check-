SELECT a.*
	FROM name_count a
	JOIN (SELECT address, COUNT(*)
	FROM name_count 
	GROUP BY address
	HAVING count(*) > 1 ) b
	ON a.address = b.address
	ORDER BY a.address