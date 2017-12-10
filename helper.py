import os, sys, datetime, MySQLdb, dbconn2

# helper module (that wil be utilized later)
def login(account, password):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute("select * from account where accountName = %s", (account,))
  row = curs.fetchone()
  return row

def insertReview(account, company, review, sentiment, salary):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute("insert into reviews values (Null, %s, %s,%s, %s, %s)", (account, review, sentiment, salary, company))

def getIdentities():
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute("show columns from identities where field = 'identity'")
  return curs.fetchall()

def getCompanyReviews(company):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute('select * from reviews where companyName like %s', ('%'+company+'%',))
  row = curs.fetchall()
  #formatting 
  return row 
  
def getTermReviews(term):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute('select * from reviews join (select term from terms where name like %s) as currCompany on reviews.reviewID = currCompany.reviewID', ('%'+term+'%',))
  row = curs.fetchall()
  #formatting 
  return row 

def getIdentityReviews(identity):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute('select * from reviews join (select identity from companies where name like %s) as currCompany on reviews.reviewID = currCompany.reviewID', ('%'+identity+'%',))
  row = curs.fetchall()
  #formatting 
  return row 

def getAccountInfo(accountName):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute('select * from reviews where accountName = %s', (accountName,))
  row = curs.fetchall()
  return row