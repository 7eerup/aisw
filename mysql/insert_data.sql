USE online_shop_db;

INSERT INTO member (name, email, phone) VALUES
('김민준', 'minjun.kim@example.com', '010-1111-1111'),
('이서연', 'seoyeon.lee@example.com', '010-2222-2222'),
('박지호', 'jiho.park@example.com', '010-3333-3333'),
('최하은', 'haeun.choi@example.com', '010-4444-4444'),
('정도윤', 'doyoon.jung@example.com', '010-5555-5555'),
('강서준', 'seojun.kang@example.com', '010-6666-6666'),
('조유나', 'yuna.cho@example.com', '010-7777-7777'),
('윤지민', 'jimin.yoon@example.com', '010-8888-8888'),
('장현우', 'hyunwoo.jang@example.com', '010-9999-9999'),
('임수아', 'sua.lim@example.com', '010-0000-0000');

INSERT INTO product (name, price, stock, category) VALUES
('무선 마우스', 25000, 50, '전자기기'),
('기계식 키보드', 89000, 30, '전자기기'),
('USB-C 충전기', 19000, 80, '전자기기'),
('노트북 거치대', 32000, 40, '사무용품'),
('텀블러', 15000, 100, '생활용품'),
('에코백', 12000, 70, '패션잡화'),
('블루투스 이어폰', 59000, 25, '전자기기'),
('마우스패드', 8000, 120, '사무용품'),
('LED 스탠드', 27000, 35, '생활용품'),
('휴대용 선풍기', 22000, 60, '생활용품');

INSERT INTO orders (member_id, order_date, status, total_amount) VALUES
(1, '2026-05-01 10:15:00', 'ORDERED', 50000),
(2, '2026-05-02 11:20:00', 'PAID', 89000),
(3, '2026-05-03 14:30:00', 'SHIPPED', 38000),
(4, '2026-05-04 09:10:00', 'DELIVERED', 32000),
(5, '2026-05-05 16:45:00', 'PAID', 15000),
(6, '2026-05-06 13:00:00', 'ORDERED', 12000),
(7, '2026-05-07 18:20:00', 'SHIPPED', 59000),
(8, '2026-05-08 20:10:00', 'DELIVERED', 16000),
(9, '2026-05-09 08:50:00', 'PAID', 27000),
(10, '2026-05-10 12:25:00', 'ORDERED', 22000);

INSERT INTO order_item (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 2, 25000),
(2, 2, 1, 89000),
(3, 3, 2, 19000),
(4, 4, 1, 32000),
(5, 5, 1, 15000),
(6, 6, 1, 12000),
(7, 7, 1, 59000),
(8, 8, 2, 8000),
(9, 9, 1, 27000),
(10, 10, 1, 22000);