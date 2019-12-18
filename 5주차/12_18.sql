show databases;
use mysql;

# webdb user 생성
create user 'webdb'@'localhost' identified by 'webdb';

# DB 생성
create database webdb;

# 권한 부여
grant all privileges on webdb.* to 'webdb'@'localhost';

show databases;

use webdb;

show tables;

select * from table2;

insert into table2
values (null, '안', '대혁', 'aaaa@gmail.com');

insert into table2
values (null, '둘', '리', 'abbbb@gmail.com');

select * from table2;

-- delete
delete from table2 where no = 4;

-- update
update table2 set first_name = '박', last_name = '재혁', email ='acc@gmail.com' where no = 7;









