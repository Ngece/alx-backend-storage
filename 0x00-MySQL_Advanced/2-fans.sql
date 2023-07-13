-- Desc: Ranks origins of bands ordered by the number of unique fans

SELECT origin, COUNT(DISTINCT user_id) AS fans