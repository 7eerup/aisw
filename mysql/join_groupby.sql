USE online_shop_db;

-- 1. JOIN: 회원 이름과 주문 금액을 함께 조회
SELECT m.name, o.total_amount
FROM member m
JOIN orders o
ON m.id = o.member_id;

-- 2. GROUP BY: 회원 ID별 주문 개수 집계
SELECT member_id, COUNT(*) AS order_count
FROM orders
GROUP BY member_id;

-- 3. JOIN + GROUP BY: 회원 이름과 함께 회원별 주문 수 집계
SELECT m.id, m.name, COUNT(o.id) AS order_count
FROM member m
JOIN orders o
ON m.id = o.member_id
GROUP BY m.id, m.name;