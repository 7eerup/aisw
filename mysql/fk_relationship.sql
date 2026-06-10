USE online_shop_db;

-- orders 테이블 구조 확인
DESC orders;

-- order_item 테이블 구조 확인
DESC order_item;

-- CREATE TABLE 문으로 FK 확인
SHOW CREATE TABLE orders;

SHOW CREATE TABLE order_item;

-- 현재 DB의 모든 FK 관계 조회
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'online_shop_db'
  AND REFERENCED_TABLE_NAME IS NOT NULL;


-- 부모 테이블 데이터 확인
SELECT * FROM member;
SELECT * FROM product;

-- 자식 테이블 데이터 확인
SELECT * FROM orders;
SELECT * FROM order_item;

-- 1:N 관계 확인 (회원 10명 모두 주문을 1건 갖고 있다)
SELECT
    m.id,
    m.name,
    o.id AS order_id
FROM member m
LEFT JOIN orders o
ON m.id = o.member_id;

-- 