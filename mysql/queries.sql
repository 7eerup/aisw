USE online_shop_db;

-- 1. 전체 회원 조회
SELECT * FROM member;

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
SELECT m.name, o.id AS order_id, o.status, o.total_amount
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
DELETE FROM order_item
WHERE id = 10;

-- 삭제 결과 확인
SELECT * FROM order_item;

-- 인덱스 생성: 주문 날짜 검색과 정렬을 빠르게 하기 위해 생성
CREATE INDEX idx_orders_order_date
ON orders(order_date);


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


| 항목    | JOIN     | 서브쿼리               |
| ----- | -------- | ------------------ |
| 방식    | 테이블 연결   | SELECT 안에 SELECT   |
| 가독성   | 관계 표현 명확 | 단순 조회 시 이해 쉬움      |
| 성능    | 일반적으로 유리 | 데이터가 많아지면 불리할 수 있음 |
| 실무 사용 | 매우 많음    | 보조적으로 사용           |



-- 데이터 정합성 FK 에러 발생 테스트
INSERT INTO orders (
    member_id,
    status,
    total_amount
)
VALUES (
    999,
    'ORDERED',
    10000
);

/*
예상 결과:
ERROR 1452 (23000)
Cannot add or update a child row:
a foreign key constraint fails

원인:
orders.member_id는 member.id를 참조하는 FK이다.
하지만 member 테이블에 id=999인 회원이 없기 때문에
데이터 정합성을 깨뜨리는 입력으로 판단되어 DB가 막는다.

해결 방법:
존재하는 member.id를 사용하거나,
먼저 member 테이블에 회원 데이터를 추가한 뒤 orders에 입력한다.
*/

-- 정상 입력 예시
INSERT INTO orders (
    member_id,
    status,
    total_amount
)
VALUES (
    1,
    'ORDERED',
    10000
);



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