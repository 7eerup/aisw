USE online_shop_db;

-- 1. 검색 (WHERE): 특정 조건 데이터 찾기
-- 전자기기 카테고리 상품 조회
SELECT *
FROM product
WHERE category = '전자기기';

-- 2. 정렬 (ORDER BY): 가격순, 최신순 등으로 정렬
-- 상품을 가격 높은 순으로 조회
SELECT *
FROM product
ORDER BY price DESC;

-- 3. 집계 COUNT: 전체 주문 개수 계산
SELECT COUNT(*) AS order_count
FROM orders;

-- 4. 집계 SUM: 전체 주문 금액 합계 계산
SELECT SUM(total_amount) AS total_sales
FROM orders;

-- 5. 집계 AVG: 평균 주문 금액 계산
SELECT AVG(total_amount) AS avg_order_amount
FROM orders;

-- 6. 그룹 통계 (GROUP BY): 카테고리별 상품 개수 계산
SELECT category, COUNT(*) AS product_count
FROM product
GROUP BY category;

-- 7. 랭킹 (ORDER BY + LIMIT): 주문 금액 TOP 5 조회
SELECT *
FROM orders
ORDER BY total_amount DESC
LIMIT 5;