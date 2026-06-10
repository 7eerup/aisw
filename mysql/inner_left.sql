-- INNER JOIN 공통 데이터(주문이 있는 회원)만 조회
SELECT
    m.id,
    m.name,
    o.id AS order_id
FROM member m
INNER JOIN orders o
ON m.id = o.member_id;


-- LEFT JOIN 왼쪽 테이블(member) 전체 조회 주문이 없는 회원은 order_id가 NULL로 표시
SELECT
    m.id,
    m.name,
    o.id AS order_id
FROM member m
LEFT JOIN orders o
ON m.id = o.member_id;


-- 주문이 없는 회원 추가
INSERT INTO member (
    name,
    email,
    phone
)
VALUES (
    '홍길동',
    'hong@example.com',
    '010-1234-5678'
);


-- 추가 결과 확인
SELECT *
FROM member
WHERE name = '홍길동';


-- LEFT JOIN 재실행 주문이 없는 회원까지 조회
SELECT
    m.id,
    m.name,
    o.id AS order_id
FROM member m
LEFT JOIN orders o
ON m.id = o.member_id;


-- INNER JOIN 재실행 주문이 없는 회원은 조회되지 않음
SELECT
    m.id,
    m.name,
    o.id AS order_id
FROM member m
INNER JOIN orders o
ON m.id = o.member_id;


-- 실습 후 원상 복구
DELETE FROM member
WHERE email = 'hong@example.com';

-- AUTO_INCREMENT 초기화
ALTER TABLE member AUTO_INCREMENT = 11;