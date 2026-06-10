USE online_shop_db;

-- SELECT : 조회(Read)
SELECT * FROM member;

-- INSERT : 추가(Create)
INSERT INTO member (name, email)
VALUES ('jenson', 'hwang@example.com');

-- UPDATE : 수정(Update)
UPDATE member
SET phone = `010-1234-5678`
WHERE id = 11;

-- DELETE : 삭제(Delete)
DELETE FROM member
WHERE id = 11;



-- 전체 데이터 삭제
TRUNCATE TABLE member;

-- 특정 데이터 삭제
DELETE FROM member
WHERE id = 11;

-- AUTO_INCREMENT 초기화
ALTER TABLE member
AUTO_INCREMENT = 1;