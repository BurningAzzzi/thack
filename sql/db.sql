-- 消息
drop table message;
create table message(
	id int(4) not null primary key auto_increment,
	user_id int(4) not null,
	content varchar(255) not null,
	audio_url varchar(255),
	picture_url varchar(255),
	latitude double(9,6) not null,
	longitude double(9,6) not null,	
	create_on datetime not null,
	tags varchar(255),
	category_id int(4),
	with_sku_type int(4),
	with_sku_id int(4)
)default charset=utf8;

-- 用户
drop table user;
create table user(
	id int(4) not null primary key auto_increment,
	username varchar(32) not null unique,
	password char(32) not null
)default charset=utf8;

-- 消息分类
drop table category;
create table category(
	id int(4) not null primary key auto_increment,
	name varchar(32) not null
)default charset=utf8;
insert into category(id,name) values(1,"吃");
insert into category(id,name) values(2,"喝");
insert into category(id,name) values(3,"玩");
insert into category(id,name) values(4,"住");
insert into category(id,name) values(5,"行");

-- sku 分类
drop table sku_type;
create table sku_type(
	id int(4) not null primary key auto_increment,
	name varchar(32) not null
)default charset=utf8;
insert into sku_type(id,name) values(1,"景点");
insert into sku_type(id,name) values(2,"酒店");

-- 签到
drop table mark;
create table mark(
	id int(4) not null primary key auto_increment,
	user_id int(4) not null,
	sight_id int(4) not null,
	create_on datetime not null
)default charset=utf8;

-- 即时通信
drop table im;
create table im(
	id int(4) not null primary key auto_increment,
	from_user_id int(4) not null,
	to_user_id int(4) not null,
	content text,
	create_on datetime not null
)default charset=utf8;

