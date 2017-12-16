use weddit_db;
drop table if exists terms;
drop table if exists reviews;
drop table if exists identities;
drop table if exists companies;
drop table if exists account;

create table account (
       accountName varchar(20) primary key,
       password varchar(20) not null,
       jobTitle varchar(20),
       resume BLOB
       )

ENGINE = InnoDB;

create table companies (
       companyName varchar(20) primary key
       )

ENGINE = InnoDB;

create table identities (
       identity ENUM ("East Asian", "Southeast Asian", "Cis-woman",
       		"Cis-man", "Non-binary","Genderfluid", "Trans", "Trans-Woman", "Trans-Man",
			   "White", "Black", "Latinx", "South Asian", "Pacific Islander", "Low income",
			   	    "First Generation College Student", "Immigrant", "Disabled", "Able-bodied", "Undocumented",
				    	   "Fat", "Indigenous", "Gay", "Heterosexual", "Lesbian", "Bisexual", "Queer",
					   	  "Asexual", "Aromantic", "Multi-racial") not null,
						  accountName varchar(20),
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
       companyName varchar(20),
       useful int unsigned  DEFAULT 0,
       primary key (reviewID),
       foreign key (accountName) references account(accountName) on delete restrict,
       foreign key (companyName) references companies(companyName) on delete restrict
       )

ENGINE = InnoDB;


create table terms (
       term varchar(20) not null,
       reviewID int not null AUTO_INCREMENT,
       primary key (term, reviewID),
       foreign key (reviewID) references reviews(reviewID) on delete restrict
       )

ENGINE = InnoDB;