import os, sys, datetime, MySQLdb, dbconn2, imghdr
from werkzeug import secure_filename

def getConn():
  DSN = dbconn2.read_cnf()
  DSN['db'] = 'weddit_db'     # the database we want to connect to
  return dbconn2.connect(DSN)

def login(account, password):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute("select * from account where accountName = %s", (account,))
  row = curs.fetchone()
  return row

def insertReview(account, company, review, sentiment, salary):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute("select * from companies where companyName = %s", (company,))
  if not curs.fetchone():
      curs.execute("insert into companies values (%s)", (company,))
  curs.execute("insert into reviews values (Null, %s, %s,%s, %s, %s, 0)", (account, review, sentiment, salary, company))

def getIdentities():
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute("show columns from identities where field = 'identity'")
  return curs.fetchall()

def getCompanyReviews(company):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute('select * from reviews where companyName like %s', ('%'+company+'%',))
  row = curs.fetchall() 
  return row 

def getTermReviews(term):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute("select * from reviews where reviewID in (select reviewID from terms where term = %s)", (term,))
  row = curs.fetchall()
  return row 

def getIdentityReviews(identity):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute('select * from reviews where accountName in (select accountName from identities where identity = %s)', (identity,))
  row = curs.fetchall()
  return row

def getAccountInfo(accountName):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute('select * from reviews where accountName = %s', (accountName,))
  row = curs.fetchall()
  return row

def get_useful_count(reviewID):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute('select useful from reviews where reviewID= %s', (reviewID,))
  return curs.fetchone()

def update_useful_count(reviewID):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  update_count = int(get_useful_count(reviewID)['useful'])+1
  curs.execute('UPDATE reviews set useful=%s WHERE reviewID = %s',
      (update_count, reviewID ))
  return get_useful_count(reviewID)

def get_all_reviews():
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute("SELECT * FROM reviews")
  return curs.fetchall()

def get_all_users():
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute("SELECT * FROM account") # Guaranteed to be distinct
  return curs.fetchall()






