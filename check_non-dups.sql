SELECT *
FROM name_count
WHERE NOT EXISTS(SELECT * FROM name WHERE name.address = name_count.address)