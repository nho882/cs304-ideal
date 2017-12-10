import os, sys, datetime, MySQLdb, dbconn2
from flask import Flask, render_template, request, redirect, url_for, flash
import re
app = Flask(__name__)
app.secret_key = 'nancyhohoho'

def getConn():
  DSN = dbconn2.read_cnf()
  DSN['db'] = 'weddit_db'     # the database we want to connect to
  return dbconn2.connect(DSN)

@app.route('/', methods=['POST','GET']) #Renders search page
def searchBar():
  if request.method == 'POST': 
    #Assume user is only searching for one of these items for now
    curs = getConn().cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    company = request.form['searchCompany']
    identity = request.form['searchIdentity']
    tag = request.form['searchTags']
    
    if company: #if nonempty, then fetch row from database
      curs.execute('select companyName from companies where companyName like %s', ('%'+company+'%',))
      row = curs.fetchone()
      print row
      if row is not None: #Returns redirect if nonempty
      	return redirect(url_for('display_company', company_name = row['companyName']))
      flash("Sorry, reviews for this company do not yet exist in IDeal.") #Flashes error if no such title
    #flash ("Please enter a search term in category.") #Flashes error if empty search
    elif identity:
      print identity
      curs.execute('select identity from identities where identity like %s', ('%'+identity+'%',))
      row = curs.fetchone()
      if row is not None:
        return redirect(url_for('display_identity', identity=row['identity']))
      flash("Sorry, reviews for this identity do not yet exist in IDeal.")
    else:
      curs.execute('select term from terms where term like %s', ('%'+tag+'%',))
      row = curs.fetchone()
      if row is not None:
        return redirect(url_for('display_term', term = row['term']))
      flash("Sorry, reviews for this tag do not yet exist in IDeal.")
    flash ("Please enter a search term in category.")
  return render_template('index.html',pageTitle='IDeal')

@app.route('/display-identity/<identity>', methods=['POST','GET'])
def display_identity(identity):
  print "in the else"
  rows = getIdentityReviews(identity)
  print rows
  return render_template("display-identity.html", identity=identity, info = rows)


@app.route('/display-company/<company_name>', methods=['POST','GET'])
def display_company(company_name):
  print "in the if"
  rows = getCompanyReviews(company_name)
  return render_template("display.html", company=company_name, info = rows)

@app.route('/display-term/<term>', methods=['POST','GET'])
def display_term(term):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute("select * from reviews where reviewID in (select reviewID from terms where term = %s)", (term,))
  rows = curs.fetchall()
  return render_template("display-terms.html", term=term, info = rows)


@app.route('/insert/', methods=['POST', 'GET'])
def insert():
  if request.method == 'POST':
    account = request.form['accountName']
    companyName = request.form['companyName']
    review = request.form['review']
    sentiment = request.form['sentiment']
    salary = request.form['salary']
    identities = request.form['identities']
    print request.form.getlist('identities')
    insertReview(account, companyName, review, sentiment, salary)
    flash("Thank you for submitting your reivew!")
  
  identities = getIdentities()[0]['Type']
  identities = re.sub('[(){}<>]', '', identities)
  identities = identities.replace('enum','').replace("'", '').split(',')
  return render_template('insert.html', identities= identities)

@app.route('/sign_on', methods = ['POST', 'GET'])
def signon():
  if request.method == 'POST':
    account = request.form['accountName']
    password = request.form['accountPassword']
    row = login(account, password)
    if row is None:
      flash("Sorry, we do not recognize this username and password.")
      return render_template('sign_on.html')

    if row['password'] == password:
      flash("Successfully logged in.")
      # return render_template('account_display.html')
      return redirect(url_for('displayAccount', accountName = account))
      #Redirect to an account page
    else:
      flash("Sorry, we do not recognize this username and password.")
      return render_template('sign_on.html')
  
  return render_template('sign_on.html')

@app.route('/account/<accountName>', methods = ['POST', 'GET'])
def displayAccount(accountName):
  rows = getAccountInfo(accountName)
  return render_template("account_display.html", accountName = accountName, info = rows)


@app.route('/register', methods = ['POST', 'GET'])
def register():
  if request.method == 'POST':
    account = request.form['accountName']
    password = request.form['password']
    jobTitle = request.form['jobTitle']

    if account and password and jobTitle:
      curs = getConn().cursor(MySQLdb.cursors.DictCursor)
      curs.execute("select * from account where accountName = %s", (account,))
      row = curs.fetchall()
      if row:
        flash("Account name already exists. Please choose another one.")
        return render_template('register.html')
      else:
        flash("Successfully created account!")
        curs.execute("insert into account values (%s, %s, %s)", (account, password, jobTitle))
        return redirect(url_for('displayAccount', accountName = account))
  return render_template('register.html')

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
  curs.execute('select * from reviews where accountName in (select accountName from identities where identity = %s)', (identity,))
  row = curs.fetchall()
  #formatting 
  return row 

def getAccountInfo(accountName):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute('select * from reviews where accountName = %s', (accountName,))
  row = curs.fetchall()
  return row
  
if __name__ == '__main__':
    app.debug = True
    port = os.getuid()
    # Flask will print the port anyhow, but let's do so too
    print('Running on port '+str(port))
    app.run('0.0.0.0',port)
      
  

