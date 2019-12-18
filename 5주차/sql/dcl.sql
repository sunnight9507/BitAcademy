show databases;
use mysql;
show tables;
create user 'webdb'@'localhost' identified by 'webdb';
create database webdb;
grant all privileges on webdb.* to 'webdb'@'localhost';
