USE online_shop_db;

-- 1. 전체 회원 조회
SELECT * FROM member;
SELECT * FROM product;
SELECT * FROM orders;
SELECT * FROM order_item;

-- 2. 전자기기 상품만 조회
SELECT * FROM product
WHERE category = '전자기기';

-- 3. 가격이 높은 상품 순으로 조회
SELECT * FROM product
ORDER BY price DESC;

-- 4. 주문 금액이 높은 상위 5개 주문 조회
SELECT * FROM orders
ORDER BY total_amount DESC
LIMIT 5;

-- 5. 회원 이름과 주문 정보 조회: INNER JOIN
SELECT m.name, o.id AS order_id, o.status
FROM member m
INNER JOIN orders o ON m.id = o.member_id;

-- 6. 주문 상세와 상품명 조회: INNER JOIN
SELECT oi.id, p.name AS product_name, oi.quantity, oi.unit_price
FROM order_item oi
INNER JOIN product p ON oi.product_id = p.id;

-- 7. 주문, 회원, 상품 상세 조회
SELECT 
    o.id AS order_id,
    m.name AS member_name,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price,
    oi.quantity * oi.unit_price AS item_total
FROM orders o
INNER JOIN member m ON o.member_id = m.id
INNER JOIN order_item oi ON o.id = oi.order_id
INNER JOIN product p ON oi.product_id = p.id;

-- 8. 주문이 없는 회원까지 포함해 조회: LEFT JOIN
SELECT m.id, m.name, o.id AS order_id, o.status
FROM member m
LEFT JOIN orders o ON m.id = o.member_id;

-- 9. 회원별 주문 수 집계: COUNT + GROUP BY
SELECT m.name, COUNT(o.id) AS order_count
FROM member m
LEFT JOIN orders o ON m.id = o.member_id
GROUP BY m.id, m.name;

-- 10. 주문 상태별 총 주문 금액 집계: SUM + GROUP BY
SELECT status, SUM(total_amount) AS total_sales
FROM orders
GROUP BY status;

-- 11. 카테고리별 평균 상품 가격: AVG + GROUP BY
SELECT category, AVG(price) AS avg_price
FROM product
GROUP BY category;

-- 12. 평균 주문 금액보다 큰 주문 조회: 서브쿼리
SELECT *
FROM orders
WHERE total_amount > (
    SELECT AVG(total_amount)
    FROM orders
);

-- 13. 주문 상태 수정: UPDATE
UPDATE orders
SET status = 'DELIVERED'
WHERE id = 1;

-- 수정 결과 확인
SELECT * FROM orders WHERE id = 1;

-- 14. 상품 재고 수정: UPDATE
UPDATE product
SET stock = stock - 2
WHERE id = 1;

-- 수정 결과 확인
SELECT * FROM product WHERE id = 1;

-- 15. 삭제 예시: DELETE
SELECT * FROM order_item WHERE id = 10;

DELETE FROM order_item WHERE id = 10;

SELECT * FROM order_item WHERE id = 10;


-- 16. 주문 날짜 검색 속도 향상을 위한 인덱스 생성
-- 주문 날짜(order_date)를 기준으로 검색/정렬하는 경우가 많기 때문에 인덱스를 생성
CREATE INDEX idx_orders_order_date
ON orders(order_date);

-- 인덱스 생성 확인
SHOW INDEX FROM orders;

-- 주문일 기준 내림차순 정렬 조회
SELECT *
FROM orders
ORDER BY order_date DESC;

-- 특정 날짜 이후 주문 조회
SELECT *
FROM orders
WHERE order_date >= '2026-01-01';

-- 실행 계획 확인
EXPLAIN
SELECT *
FROM orders
WHERE order_date >= '2026-01-01';

-- 인덱스 제거
DROP INDEX idx_orders_order_date ON orders;