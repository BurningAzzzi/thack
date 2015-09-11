create table message(
	id int(4) not null primary key auto_increment,
	user_id int(4) not null,
	content varchar(255) not null,
	audio_url varchar(255),
	picture_url varchar(255),
	latitude double(9,6) not null,
	longitude double(9,6) not null,	
	create_on datetime not null,
	with_sku_type int(4),
	with_sku_id int(4)
);

create table user(
	id int(4) not null primary key auto_increment,
	username varchar(32) not null unique,
	password char(32) not null
);

