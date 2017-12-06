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
	identity ENUM("East Asian", "Southeast Asian", "Cis-woman",
		"Cis-man", "Non-binary","Genderfluid", "Trans", "Trans-Woman", "Trans-Man",
		"White", "Black", "Latinx", "South Asian", "Pacific Islander", "Low income",
		"First Generation College Student", "Immigrant", "Disabled", "Able-bodied", "Undocumented",
		"Fat", "Indigenous", "Gay", "Heterosexual", "Lesbian", "Bisexual", "Queer",
		"Asexual", "Aromantic", "Multi-racial"),
	accountName varchar(20) not null,
	primary key (identity, accountName),
	foreign key (accountName) references account(accountName) on delete restrict
	)

ENGINE = InnoDB;

create table reviews (
	reviewID int not null AUTO_INCREMENT,
	accountName varchar(20),
	reviewText LONGBLOB not null,
	sentiment ENUM("Positive", "Negative", "Neutral") not null,
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