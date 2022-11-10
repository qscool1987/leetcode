create table user_lc_daily_info (
	id int auto_increment,
	user varchar(128) not null default '',
	total_solve int not null default 0,
	code_submit int not null default 0,
	problem_submit int not null default 0,
	rating_score int not null default 0,
	continue_days int not null default 0,
	new_solve int not null default 0,
	date_time datetime not null,
	primary key(id),
	index idx_date_time(date_time),
	index idx_user(user)
) engine=innoDB default charset=utf8;


create table account_info (
	id int auto_increment,
	user varchar(128) not null default '',
	git_account varchar(128) not null default '',
	medal int not null default 0,
	primary key(id),
	unique (user),
	unique (git_account)
) engine=innoDB default charset=utf8;

create table feedback_info (
	id int auto_increment,
	content varchar(2048) not null default '',
	date_time datetime not null,
	primary key(id)
) engine=innoDB default charset=utf8;

create table user_target_info (
	id int auto_increment,
	user varchar(128) not null default '',
	target_type int not null default 0,
	target_value int not null default 0,
	opponent varchar(128) not null default '',
	status int not null default 0,
	create_date datetime not null,
	dead_line datetime not null,
	primary key(id)
) engine=innoDB default charset=utf8;