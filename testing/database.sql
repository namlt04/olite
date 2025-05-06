DROP SCHEMA IF EXISTS csdl;
CREATE SCHEMA csdl;
USE csdl;

CREATE TABLE users (
    username VARCHAR(255) NOT NULL PRIMARY KEY,
    name varchar(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    birth YEAR NOT NULL,
    gender varchar(255) default("male"),
    public_key text,
    password varchar(255) default("test") not null
);

create table friends (
  relationship_id int UNSIGNED AUTO_INCREMENT primary key, 
  user1 varchar(255) not null, 
  user2 varchar(255) not null, 
  user1_status enum("friend", "pending", "sent"),
  user2_status enum("friend", "pending", "sent"),
  check (user1 < user2), 
  unique(user1, user2),
  foreign key (user1) references users(username) ,
  foreign key (user2) references users(username) 
  
  
);
CREATE TABLE conversations (
    conversation_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    conversation_name VARCHAR(100),
    is_group INT DEFAULT 0
);

CREATE TABLE participants (
    conversation_id BIGINT UNSIGNED,
    username VARCHAR(255),
    primary key (conversation_id, username),
    foreign key (conversation_id) references conversations(conversation_id) on delete cascade
);

CREATE TABLE messages (
    message_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    conversation_id BIGINT UNSIGNED,
    username varchar(255),
    receiver varchar(255),
    content TEXT, -- content đã mã hóa trong trường hợp là tên file thì không mã hóa
    key_enc text,
    time_stamp varchar(255),
    is_read INT default 0,
    has_file INT default 0,
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ,
    FOREIGN KEY (username) REFERENCES users(username)
);

CREATE TABLE files (
    file_id varchar(255),
    message_id BIGINT UNSIGNED,
    file_url TEXT,
    file_type VARCHAR(50),
    file_size INT,
    primary key(file_id, message_id)
);


INSERT INTO users (username, name, email, birth) VALUES
('NV001', 'Trần Thị Mai', 'mai.tran@example.com', 1995),
('NV002', 'Lê Hoàng Nam', 'thanhnam.aus@gmail.com', 1992),
('NV003', 'Phạm Quang Minh', 'minh.pham@example.com', 1998),
('NV004', 'Đỗ Thị Hạnh', 'hanh.do@example.com', 1994),
('NV005', 'Nguyễn Văn Duy', 'duy.nguyen@example.com', 1996),
('NV006', 'Nguyễn Văn Duy', 'duy.nguyen@example.com', 1996),
('NV007', 'Hoàng Đức Anh', 'anh.hoang@example.com', 1993),
('NV008', 'Lương Minh Tuấn', 'tuan.luong@example.com', 1999),
('NV009', 'Nguyễn Văn Duy', 'duy.nguyen@example.com', 1996),
('NV010', 'Bùi Văn Thắng', 'thang.bui@example.com', 1988),
('NV011', 'Đặng Hoàng Sơn', 'son.dang@example.com', 1991),
('NV012', 'Trịnh Thị Thu', 'thu.trinh@example.com', 1993),
('NV014', 'Cao Văn Trường', 'truong.cao@example.com', 1995),
('NV015', 'Tô Thanh Bình', 'binh.to@example.com', 1996),
('NV016', 'Phan Minh Khang', 'khang.phan@example.com', 1992),
('NV017', 'Phan Minh Khang', 'khang.phan@example.com', 1992),
('NV018', 'Đỗ Văn Hoài', 'hoai.do@example.com', 1993),
('NV019', 'Phan Minh Khang', 'khang.phan@example.com', 1992),
('NV020', 'Lý Quốc Huy', 'huy.ly@example.com', 1989);


insert into friends(user1, user2, user1_status, user2_status) values
("NV001", "NV002", "friend", "friend"),
("NV002", "NV003", "pending", "sent"),
("NV002", "NV008", "pending", "sent"),
("NV002", "NV004", "sent", "pending"),
("NV002", "NV005", "sent", "pending"),
("NV002", "NV006", "pending", "sent"),
("NV002", "NV007", "sent", "pending");


insert into conversations ( conversation_name , is_group ) values
('P01', 1),
('P02', 1),
('P03', 1),
('P04', 1),
('P05', 1),
('Test 1', 0),
('Test 2', 0),
('Test 3',0),
('Test 4', 0),
('Test 5', 0),
('Test 6',0),
('Test 7',0 ),
('Test 8', 0 ),
('Test 9', 0);

insert into participants (conversation_id, username ) values
(1, 'NV001'),
(1, 'NV002'),
(1, 'NV003'),
(1, 'NV004'),
(1, 'NV005'),
(1, 'NV006'),
(2, 'NV002'),
(2, 'NV007'),
(2, 'NV008'),
(2, 'NV009'),
(2, 'NV010'),
(2, 'NV011'),
(2, 'NV012');




-- Từ NV001 đến NV020
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyIqkONcHDFY8J5p+b3ae
fSUMcHsO4TibUC3svcqHEO32ylT18V46aZMpwV0hsc0Tvl1moFmQ1UJnQqi9uq+h
F64bsfcIMdtGN74+txhLYY4Ecf+6U8BpGFSJ+O5xHElF2JW8Itt1Nh7Bg1pD4lwk
14cNo91xIHzuCDO0XmIYxSV8UfcxQSwf16QrAFLBNV6+VjHzSutYtXLyVBjLfUVa
/+Ux5hVekIb7Rx5Lydkhjw5SwYQOY1okn36UGaLkDMLxF0aM1j12AeR9dEjSg2sD
hJjD1LDLVa4ic9Pgg4MESfke2FcAisk27CF+XTaafTl29hw92El73YGaEHC0y8xo
GQIDAQAB
-----END PUBLIC KEY-----' WHERE username = 'NV001';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmB7GqtJlyNebNfyZJFWw
U+R0jme2Ne78RB/frA6ZqTrDkR/G9cUoDxDM1CgktVfjy8at9SQRj0DCie2TnCs4
7sW+6Sm89PMrWwjCxpLjA8bjCbKkX6sEnkRQoQdOyV68OKQyTRzULGjYMNPtH9je
aHnlT53fyfzn5YLEEq6orbV+xAGBvAoKuElisu6Rk0SEIotw5FdWmYno+LnSHv42
HW2M84G+o1/u8HHxhHJfcIlXVy4NUWTq6sba/WjKdlzJesb00BWa3JUjoatDwCmV
zMn6wNOSfa3CDmdrstqoYHG4Sc7DyrE4+j9IyAfC4krJhKy61YVa0zPhvvjzPS0Y
OQIDAQAB
-----END PUBLIC KEY-----
' WHERE username = 'NV002';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1i3bIs38Z5ykYGDnM5c7
nEpB036z6EKA5FPQDmiF8s+/ui/PV5ZNyeiDz0GLJx2uIdsc6YVM4I5DCbxWyY7w
Ein2ucwgoaCp1ofTUexBVEL5UoaSTeZDSwJrHhUOHwxPKI0F4MyS8zcXfz5rTp2e
DcEpLMUGYsQz9IfV+BTkH5YlKyWATFvm4A8icQvaBQTzHBQfU8SozIkCxDZ+HvTK
eNfRjbBRQxNQtoRhhDxqhfcw34lmMg+akn/9vgV/FqGO3eRi9P1Q9gmZf2ntONv2
tahBdMtfm2wpLzNax1+c2JGVPboEwtz4HTTzQZRodiAxi+5nTWgug7hRdmkoLLgR
zQIDAQAB
-----END PUBLIC KEY-----
' WHERE username = 'NV003';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqrXKkRnZnFPDgJUtfFrL
7DR8eikktmObjvSa3sgfWT51A/sgp5FIGMDl+WeSV6/GRS2W0meauQ/JXvf/YkUN
1gsZjsQSv+hMG+t4g8gnYBqmyYdftiLsDezU+cAu9JbHoJ97WKnVccuWoxY1fEyb
G/o7nS2UvZIv0/HNUMkToIOMs0rMA7fg8+0thBDh/E4wDD5oUJWExqm6Jj8IruuX
GPqX9hMAzy0Zc1QlERTHppBtAfPtB+Jds1jJM+YdezdNyoumknp95JjWns1q7JnY
7wqrHdHihS0IomctCicIiKgnLhgsHMzzvyCykT7zSYzk358uYSSaUePnsuwIqFkw
uwIDAQAB
-----END PUBLIC KEY-----
' WHERE username = 'NV004';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAklES3mooiZK/Lk05mkGL
+eRC+Nrt7lFiRtFzcZjKl9VP/9kkcy8pDG6LnZrRHQz8fYHIk5+qckVsHbI8VLEy
+jh+p8H7pCL1l4L0jrmoMxFKQMBsjC/dCx6baunDhHHyNzvKmZZaYwE9q+sSdBXZ
MNVy3ozJ+MakAGIxexryggk5QNWbNqA2CzTkB90lsC7hC2bf+a8vy3kgNWBZpCEg
3Cb/57ZiHgdQn3pkAnjnylFB07ChS7VDsW15aeUDWEijev5E2CDDhXsNw3CiwJ6v
YJau7fKW/bTPnMkFqeVHb3O0Crd4l2iqeylt6ikulFYRftxpbl46b71rEwj2dx6+
kQIDAQAB
-----END PUBLIC KEY-----
' WHERE username = 'NV005';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzbyPc3QTHtbQaZNlJaw0
1rG3AMqRqoE1CRxvYjm6iHaGH8N12YgDEvl2sTL30fVuZq/P7Jj/fvyptfS/UBNb
wgaAKUvxUxhmzOm+rWOs5d7TMElIRz62ZavqIkE6X4CJDwkt9ZZO7ute1OGQL0qu
x4TetppNa0VCOXYsYVkrTZ4YW/90LB8CQStTyOC9nX2n+nxaXLPWl3KdGwl6kwhj
iFTwSihOlg7ohJD1vRt6abTG3yfDpCY8mqDdzhBisxEZ9ga9/gvcw6aUNFFb4gVC
sbqlZ7/YB2PQemGw8MFpZd1hCE8bLauZwhFndwckVseV9+Q4oCJnjdi6oRBWWBoi
eQIDAQAB
-----END PUBLIC KEY-----' WHERE username = 'NV006';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArly6yP+EgeuNJ9ADKgFW
oa+NxsfvHvsOnAeu8LWdMepDkTm1+B+B0/IFarIsnEM5YnfQLJjEX/DGz5jc1PIQ
c/tveQyci0tOI/bGoXrSpEnNZM1b97Wzd4we965xDjtzpPhqgu+5bByMq2fD9gq5
RBk5ZK4Tx0Bp45Tlq3K3hlATYT++VGXvqim6KkkM3akjVAxJu4B8zC+kvJbvLxIb
tuSjVgbr9HYvfaHhED2kQDY/s2txJCEzfOjgZKnLyF0ZjpMXNVJl8iu9XiXWlXpF
7fnzSa4PqAf/OntvuXBwihzmB9DTm0FwwFkwEJAX2gObrVD6omf6E5ntrJ5UB2oO
4QIDAQAB
-----END PUBLIC KEY-----' WHERE username = 'NV007';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlin7jYknE7/hTVYPLbKQ
Jm/Beh+Y1VPRjAW86lLWP9IlUlzaPt+M0qVRJSopXxuJ+d8SivvkBMhqOXgQEPEj
fsXo/fXxuDCO4DeFfpM9bG7NozcCr1p8Stdn9cBzQ/uH/bzslwGXuAeDM00LohoG
/2YwSeD3vNpIQLs1E77HbGuu6mqUghfsQHh8QuK9vbaaX59H0xE2I1mEo1XsE6GY
RBaIyBtPBMr+8mTvxYr95cmgori/fKgtD+7KOEN/XxrYDM+FISbheEFPDy9ejA0S
TtFs6a1vys/1aO6me7XZOQDcMvJH3S5ZtPdlzFQtVyg35MahGx4FUzf2X3twMErU
FQIDAQAB
-----END PUBLIC KEY-----
' WHERE username = 'NV008';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtYskUJ9oFkIEGXOT3n/a
TpIqbTJjzQh4x6DmLmRmzD1Z0QS1dFDuCeStxG3513sAWPvPtVoIh00ysRdT5Trk
VuGV7aB4r4gXBnu96IPz8aSBUBRoIvfrYkt5F+jz63TiKQ9s/M4Z4RhBfNY3Bf1f
sesu70x3P06hU+bAU3oKVV+zR/cWmvpY8QImn81cmYHFd6QgtNAeJuCAyUiYSXp/
6zUT7Okj/4a8Rp5mmt9uWF35Mp5mCEw/srZWkEgUf/seMh7KWdfi9LZwNrveK29o
cu5RRxnGz2nba+9IV5Fe7Tt+wCob5Xl7ImePsdh+WkckgU61my38DfRTzn/9Ecih
rQIDAQAB
-----END PUBLIC KEY-----' WHERE username = 'NV009';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAm2/P+xRyWr2804QcL1AK
ei01iNgg4Xvz+x/Lu3xc1dK8LZIxsWc2n3LAPiVbtJ6d5Aep+vJyMrplafvRCZh5
5SDcY92WHnzQiocPUEKqoMQOiW+NqwP2anZb4pTVeOPxpPW6oVEmEoUh5egNRRBQ
hQOSxZtzbhVNH0/e5OPPw+UFkYzZlsVM13Xwweh4iUzmP0PPZqYa14DbM1GoXtNY
avk7f7LCASKVvxgsZf6gVUyuffCyZLvAaWGNykUqI5pCaDN1Oa6AIuoO5o3vjmED
OFsADRF8c0Kdw9CEH8qxTe3t+B+vR7fjwyHwKgwJkRVQq0FJCWW9/Xe0gJec74mJ
6wIDAQAB
-----END PUBLIC KEY-----' WHERE username = 'NV010';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAovG3ESL1jyzCbiLvn87S
cKfOYlmmKu0U0lVgFZ14+HQBeiKGJHmQGslVyKPqJSgerM6GNvDbYUnNXIY+xx5d
1tPQpQjffOvX3hCOFNye+Jo9Ge0ztV5JhGgzFSGoaDWvTEt+hTiAuvxNsGa+vWXU
mAW6BDLFwbM3WO92lUymYOAS0JY/OrfKCi4QI7a/dAG1maN1uXI8F2ewbBToehU6
7xOhW1YyNFG0WxW9y1i/wIRr6LyCZCFx+PNpCed1aD/Y0UvuOxvcX59jzNNgbxgs
qtqgohvsFnOIuEzVzuCxeavPDFXmdiuFCx7+QG1enG/IzOXoGzABNqNtGhmAb6nq
0QIDAQAB
-----END PUBLIC KEY-----' WHERE username = 'NV011';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAx+rPHtUnyzweDNzrBj6m
DCKnfFkFtcMVz8cuLhMGaxbM5YaBhB2PKtwmce8SL748VNYva5p0EWmaPkx3047H
XuFWon5sk7Cvz65v3Ez1sVjeyNxr++1ZJ6CwU5LHDeD8M4RZ4ILE+VI5g76kFJV9
SzScUuOUcWaGf2JjekkNyk4tBzDv83KJYZh6sPXdwhniTkDYjs6fekQJVqEh2mRI
bbt+ij2IQI2zx9IWec6ToI3+WZAiIiFAsfdMRHTT6bUaNiux6T0+3mxzft54YZOM
Uy0Rrq9R0aVO017/cd34/TBHNvemfSAHvL99jx4Xr67njgm2E8n2mKHjt3z4z626
PwIDAQAB
-----END PUBLIC KEY-----' WHERE username = 'NV012';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAojzjSX6Tp68RoRGDr7YC
poIBrYNWJLpxbAhbupTj00WCdl7vwrmDAqD5kgx4bXVq76t33lDhjjriVGO3lc90
kt9/9vWHzPlLNpjC2CXpMyTH1KzD7oz2AO/lqDGOnbRVgaf76al+22J+w/BurFQs
lgFH/tSmeN6Hw8X1X/pAbNHhuzvqDIpDIfdzQnoaVvaKb6MivbSsMTZZVmPHhCEw
BIpBAkcI+MQuNqxETuG6eTJqahzp5MZlcjyTiDnhHGmBFbBOkyMP6huNcxD/bCfn
wOt4I9zpVTypuK11/E6uWmu6HjlMTi1XTxzsQj7i3u1NQWrZzHPAicddLm2XSRFD
9wIDAQAB
-----END PUBLIC KEY-----' WHERE username = 'NV013';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkcfrOFs6AOP16HecaQGy
e3cGo2qKZHqiBfiPJwBY6HklzyROFPVPBQtZeGnl8UwmEEv8VE2FVuGvypRo5iuW
Im+M28UnR6YN2TyMmHEBUPajFIAjtUu080iv5MDrJ5O3JsdS/VbXjVHDcyBeii9N
K/9Ue31PuS6xnb6ISeUrmT5mUj+9xZ6VpEMq+UQJIvOcCbugxs5yNmYEUyphdz3n
A+EjyNeN+Dho4dG0kNda8RpCvE2oNGFTkfFM9q2s6Xd5q15UmMpSiwLqknoyAoKO
TCE+TnyKDzSQorB5hB4+zsFL/GFoYOdfzOFMt3W0tqf13GGD20PnqO1131fufrDF
lwIDAQAB
-----END PUBLIC KEY-----' WHERE username = 'NV014';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1OtsMvr5eNRm8bl+JixH
4lCmPJzODXU3hN92nGopSqqlEQHrF2rIcUtcfmehAydmWnt67tvDOdLMX0KYhuj7
IK+I8fcoTfrx7fqX35Xh2d385EdV7SP/76r7RxFt4ywJ5QeMfoeFBSl2NtFz139M
O014AkOk7oD0IyoTn5dT95A34ULbZggZdOyRSl2aSMSmKD2Omi3i2MwCFXF29QDk
v8uldm+AF/PlsZyKyGEKthqEDMgeJv0y5iXSzf9jJ6OCEM+64R2OfX/HVRjXdIBO
OTLV7TXMZCMRzFJv1EqVkK6EEZbltojtAmNgkdtbQ8+cQwq+uOcnrYTWtw3cYcQE
lQIDAQAB
-----END PUBLIC KEY-----
' WHERE username = 'NV015';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvAdLfREfYN2tpP2rIjfc
d10cQHRqNZpKU1A16gDAgl/WhHDLuClmInc//ARa4GBeFeQiqxmIUQz7FV4d/xED
Q6zXGsda3PZx+QlItCUbJMxmTjDdF2+bYZeYz5JwwbVTIngIAKLg1gdt11hc/456
tGFC6ih2+rsMD8xA9/xImz2lVWMsSHf/BQ+HWhjVZ12558GHLBWSJ0ykZ8JFxW++
QQLU1jQjRd52FB+zYTtfKxPFoytAeB8V8h+Hh3t6FOuscXeyuwjXxJLty60Cj00e
4iau7v8diEiqcJGSIjrDTSBK9Hz839KFQ/Q8gWmJKV0sFvU6sfv3OS8lsFeQvFwn
pQIDAQAB
-----END PUBLIC KEY-----
' WHERE username = 'NV016';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA17LSFBq9Q+ZXclynJ7jo
quasZo7lCdQVWdBhr08VQQGmE4orNkfbCTzdRHHgTlMlvdrUAKUNo0a7rn7NsHyi
91GyTs+mls7Cur9NtPpW9rWAJYyZtM+54iuo9txQCD1cEl3Qq1ByUlXfQADXe/Bb
NeqHmgHvMkFhGtvHJ8WEBKPUy1oKOifS1Vw1AqtXvC0vDaLyFt9ucIez/uz76dzo
mJuoudIo5St0csVb4HprsCIftVkauY1pfLE9YtCcw986ZiHq25M1bOo8VBGvxQkj
M5Nl6mRFQcxEVhBh92MP/zcllJ1+vrw9Ysl5vMox5iKEQ0Y8MOZwEU7fUeMhbv1b
TQIDAQAB
-----END PUBLIC KEY-----
' WHERE username = 'NV017';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwe9oX27/Uhn2owfvGVuy
7Upj1i0LU/0FVT1PvFzvQjV3BK6tiyCZtIDtYna7oTd5T3u+VtqNRLhI+yZuIGOj
v77EqTh4+g9dPE8itRzi6BPastrZvntdwTE5su3YZlZW3ihrvAaH2J/VtZzp9hhk
5MltDnpGFlm9dhrevUUXxJNVsmHchPxJZBt0Ts+wMB34WJefQZGHnbbL03xvjdFz
Dj6ioJYdjzGIYZTfNLYzTuaI1KR5YneGqnLi89oDVUwp+V5OUHRxPUrramDpfs5o
9uIvJep/yAMcBRhje6e7vj0Fs6+CHVy8mlS93aWmsXgMrLNOGIeM8QrTXP8HXW0e
3wIDAQAB
-----END PUBLIC KEY-----
' WHERE username = 'NV018';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3hdS7YE254zqacA4ZjKg
WTMffZ/wGSnNTqICf8MK8yk0T8GldnHBfgbNO6jcxUoFe5I/8MARBxtVdKVmz8xC
h5wIsMrUgUvRpj+G2t+16OCZDhGojhzSH4LlIVjBB3IHmjbScUhx2JVPKZtKGR5R
lTx/feG7SoYFkO30r+RwYezjr6HMZN8nJIhAl3gyjeq+2MBn3JzVqPDXcCIblrVE
GAshlOajMDX+Js2SidEqZQiDqLITG0kUpS2phd0xDLt00ngG/TaENQkmjx0zkNzU
jnAKuHXt+kCJnvfstIvMBN0UNvfKRT1wLctZmNUMqvq0CQyMxHaLJ6FCwcrfOug0
FQIDAQAB
-----END PUBLIC KEY-----
' WHERE username = 'NV019';
UPDATE users SET public_key = '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvBXkBRQ6K+8RBUTGP/NR
RYEvGX/IVRvwltdKUYy0m6ThPRgzCZLQo8eU+bDiVpF37wyUiAow84zasXJVfaWY
gv6wPd8DSdj6e+IXsaYpkFw6u3ujaaV9TQXSpjzs/4rQy0OL2xb8TwIrfSKbD1Ci
aCNDWvdCBpllkpneJl9ugPSmYUlFW9e9aNkFe0WkJDRF8XkcuMvxWXvoOjK4k738
t+7ki5c5xcvE6yHG9Nf1zM2UHy6NvksjZ1DTeWp/1j04tRbjOxViyJti7KWAgnM5
uAwhl5nWbZPSHHHQs06cCbcM30R5fIvShfRodxsPnpewd3lbz+0TIybrjouLPcso
hwIDAQAB
-----END PUBLIC KEY-----' WHERE username = 'NV020';


