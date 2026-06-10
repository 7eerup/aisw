-- JOIN 방식 SQL
SELECT
    o.id AS order_id,
    m.name AS member_name,
    o.total_amount
FROM orders o
JOIN member m
ON o.member_id = m.id;


-- 서브쿼리 방식 SQL
SELECT
    o.id AS order_id,
    (
        SELECT m.name
        FROM member m
        WHERE m.id = o.member_id
    ) AS member_name,
    o.total_amount
FROM orders o;