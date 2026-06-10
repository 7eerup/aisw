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


-- 테스트용 주문 생성
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

-- 확인
SELECT *
FROM orders
ORDER BY id DESC;

-- 테스트용 주문 삭제
DELETE FROM orders
WHERE id = 11;

-- 초기화
ALTER TABLE member AUTO_INCREMENT = 1;