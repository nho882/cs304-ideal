use nho_db;
drop table if exists terms;
drop table if exists companies;
drop table if exists reviews;
drop table if exists identities;
drop table if exists account;

create table account(
	accountName varchar(20) primary key,
	position varchar(20)
	)

ENGINE = InnoDB;

create table identities(
	identity varchar(20),
	accountName varchar(20) not null,
	primary key (identity, accountName),
	foreign key (accountName) references account(accountName) on delete restrict
	)

ENGINE = InnoDB;

create table reviews (
	reviewID int not null AUTO_INCREMENT,
	accountName varchar(20),
	reviewText LONGBLOB not null,
	sentiment boolean not null,
	salary int unsigned,
	primary key (reviewID),
	foreign key (accountName) references account(accountName) on delete restrict
	)

ENGINE = InnoDB;

create table companies (
	name varchar(20) primary key,
	reviewID int not null AUTO_INCREMENT,
	foreign key (reviewID) references reviews(reviewID) on delete restrict
	)

ENGINE = InnoDB;

create table terms (
	term varchar(20) not null,
	reviewID int not null AUTO_INCREMENT,
	primary key (term, reviewID),
	foreign key (reviewID) references reviews(reviewID) on delete restrict
	)

ENGINE = InnoDB;