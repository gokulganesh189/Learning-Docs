
with RECURSIVE CategoryCTE AS (
    SELECT category_id, category_name, level
    FROM Category
    WHERE category_name = 'Electronics'
    
    UNION ALL
    
    SELECT c.category_id, c.category_name, c.level
    FROM Category c
    INNER JOIN CategoryCTE cte ON cte.category_id = c.parent_category_id
);  

select * from CategoryCTE order by level, category_id;