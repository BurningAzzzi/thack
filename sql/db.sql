-- -- 消息
-- drop table message;
-- create table message(
-- 	id int(4) not null primary key auto_increment,
-- 	user_id int(4) not null,
-- 	content varchar(255) not null,
-- 	latitude double(9,6) not null,
-- 	longitude double(9,6) not null,	
-- 	create_on datetime not null,
-- 	tags varchar(255) not null,
-- 	category_id int(4) not null,
-- 	with_sku_type int(4) not null,
-- 	with_sku_id int(4) not null
-- )default charset=utf8;

-- drop table message_resources;
-- create table message_resources(
-- 	id int(4) not null primary key auto_increment,
-- 	message_id int(4) not null,
-- 	resource_id int(4) not null
-- )default charset=utf8;

-- drop table message_routes;
-- create table message_routes(
-- 	id int(4) not null primary key auto_increment,
-- 	message_id int(4) not null,
-- 	route_id int(4) not null
-- )default charset=utf8;

-- -- 用户
-- drop table user;
-- create table user(
-- 	id int(4) not null primary key auto_increment,
-- 	username varchar(32) not null unique,
-- 	password char(32) not null
-- )default charset=utf8;

-- insert into user(username,password) values("eleven","123456");
-- insert into user(username,password) values("user_1","123456");
-- insert into user(username,password) values("user_2","123456");
-- insert into user(username,password) values("user_3","123456");
-- insert into user(username,password) values("user_4","123456");
-- insert into user(username,password) values("user_5","123456");
-- insert into user(username,password) values("user_6","123456");
-- insert into user(username,password) values("user_7","123456");
-- insert into user(username,password) values("user_8","123456");
-- insert into user(username,password) values("user_9","123456");

-- -- 消息分类
-- drop table category;
-- create table category(
-- 	id int(4) not null primary key auto_increment,
-- 	name varchar(32) not null
-- )default charset=utf8;
-- insert into category(id,name) values(1,"吃");
-- insert into category(id,name) values(2,"行");
-- insert into category(id,name) values(3,"玩");
-- insert into category(id,name) values(4,"住");

-- -- sku 分类
-- drop table sku_type;
-- create table sku_type(
-- 	id int(4) not null primary key auto_increment,
-- 	name varchar(32) not null
-- )default charset=utf8;
-- insert into sku_type(id,name) values(1,"景点");
-- insert into sku_type(id,name) values(2,"酒店");

-- 签到
drop table mark;
create table mark(
	id int(4) not null primary key auto_increment,
	user_id int(4) not null,
	sight_id int(4) not null,
	latitude double(9,6) not null,
	longitude double(9,6) not null,	
	create_on datetime not null,
	mark_order int(4) not null
)default charset=utf8;

create unique index UK_USER_SIGHT on mark (user_id, sight_id); 
-- -- 即时通信
-- drop table im;
-- create table im(
-- 	id int(4) not null primary key auto_increment,
-- 	from_user_id int(4) not null,
-- 	to_user_id int(4) not null,
-- 	content text not null,
-- 	create_on datetime not null
-- )default charset=utf8;

-- -- 图片
-- drop table resource;
-- create table resource(
-- 	id int(4) not null primary key auto_increment,
-- 	url char(255) not null,
-- 	resource_type int(4) not null,
-- 	create_on datetime not null,
-- 	latitude double(9,6) not null,
-- 	longitude double(9,6) not null,
-- 	user_id int(4) not null
-- )default charset=utf8; 

-- drop table route;
-- create table route(
-- 	id int(4) not null primary key auto_increment,
-- 	user_id int(4) not null,
-- 	latitude double(9,6) not null,
-- 	longitude double(9,6) not null,
-- 	create_on datetime not null
-- )default charset=utf8;

-- drop table route_resources;
-- create table route_resources(
-- 	id int(4) not null primary key auto_increment,
-- 	route_id int(4) not null,
-- 	resource_id int(4) not null
-- )default charset=utf8;

-- drop table pushing;
-- create table pushing(
-- 	id int(4) not null primary key auto_increment,
-- 	from_user_id int(4) not null,
-- 	to_user_id int(4) not null,
-- 	message_id int(4) not null,
-- 	enable int(4) not null default 1,
-- 	create_on datetime not null
-- )default charset=utf8;
