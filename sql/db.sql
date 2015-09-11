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
)default charset=utf8;;

drop table user;
create table user(
	id int(4) not null primary key auto_increment,
	username varchar(32) not null unique,
	password char(32) not null
)default charset=utf8;;

-- 分类
drop table category;
create table category(
	id int(4) not null primary key auto_increment,
	name varchar(32) not null
)default charset=utf8;;
insert into category(id,name) values(1,"吃");
insert into category(id,name) values(2,"喝");
insert into category(id,name) values(3,"玩");
insert into category(id,name) values(4,"住");
insert into category(id,name) values(5,"行");