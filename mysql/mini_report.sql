-- MINI REPORT: 총 매출
SELECT
    SUM(total_amount) AS total_sales
FROM orders;


-- MINI REPORT: 상품별 판매 수량 TOP 5
SELECT
    p.name AS product_name,
    SUM(oi.quantity) AS total_quantity
FROM order_item oi
JOIN product p
ON oi.product_id = p.id
GROUP BY p.id, p.name
ORDER BY total_quantity DESC
LIMIT 5;


-- MINI REPORT: 회원별 주문 금액 TOP 5
SELECT
    m.name AS member_name,
    SUM(o.total_amount) AS total_order_amount
FROM member m
JOIN orders o
ON m.id = o.member_id
GROUP BY m.id, m.name
ORDER BY total_order_amount DESC
LIMIT 5;