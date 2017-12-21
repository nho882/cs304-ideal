import os, sys, datetime, MySQLdb, dbconn2, imghdr
from werkzeug import secure_filename

def getConn():
  DSN = dbconn2.read_cnf()
  DSN['db'] = 'weddit_db'     # the database we want to connect to
  return dbconn2.connect(DSN)

def login(account, password):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute("SELECT * FROM account WHERE accountName = %s", (account,))
  row = curs.fetchone()
  return row

def insertReview(account, company, review, sentiment, salary):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute("SELECT * FROM companies WHERE companyName = %s", (company,))
  if not curs.fetchone():
      curs.execute("insert into companies values (%s)", (company,))
  curs.execute("insert into reviews values (Null, %s, %s, %s, %s, %s, 0)", (account, review, sentiment, salary, company))

def getIdentities():
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute("show columns FROM identities WHERE field = 'identity'")
  return curs.fetchall()

def getCompanyReviews(company):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute('SELECT * FROM reviews WHERE companyName like %s', ('%'+company+'%',))
  row = curs.fetchall() 
  return row 

def getTermReviews(term):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute("SELECT * FROM reviews WHERE reviewID in (SELECT reviewID FROM terms WHERE term = %s)", (term,))
  row = curs.fetchall()
  return row 

def getIdentityReviews(identity):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute('SELECT * FROM reviews WHERE accountName in (SELECT accountName FROM identities WHERE identity = %s)', (identity,))
  row = curs.fetchall()
  return row

def getAccountReviews(accountName):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute('SELECT * FROM reviews WHERE accountName = %s', (accountName,))
  row = curs.fetchall()
  return row

def getAccountInfo(accountName):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute("SELECT * FROM account WHERE accountName = %s",
    (accountName,))
  return curs.fetchone()

def get_useful_count(reviewID):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute('SELECT useful FROM reviews WHERE reviewID= %s', (reviewID,))
  return curs.fetchone()

def update_useful_count(reviewID):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  update_count = int(get_useful_count(reviewID)['useful'])+1
  curs.execute('UPDATE reviews set useful=%s WHERE reviewID = %s',
      (update_count, reviewID ))
  return get_useful_count(reviewID)

def updateAccount(oldName,newPassword, newJobTitle):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute('UPDATE account set password=%s,jobtitle=%s WHERE accountName=%s',
    (newPassword, newJobTitle, oldName))

def deleteReview(reviewID):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute("DELETE FROM reviews WHERE reviewID=%s", (reviewID,))

def getFile(accountName):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute("SELECT resume FROM account WHERE accountName=%s", (accountName,))
  row = curs.fetchone()
  data = row[0]
  return data







