import os, sys, datetime, MySQLdb, dbconn2
from flask import Flask, render_template, request, redirect, url_for, flash
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
    
    if company!="": #if nonempty, then fetch row from database
      curs.execute('select name from companies where name like %s', ('%'+company+'%',))
      row = curs.fetchone()
      print row
      if row is not None: #Returns redirect if nonempty
      	return redirect(url_for('display', company_name = row['name']))
      flash("Sorry, reviews for this company do not yet exist in IDeal.") #Flashes error if no such title
    #flash ("Please enter a search term in category.") #Flashes error if empty search
    elif identity !="":
      curs.execute('select identity from identities where identity = %s', ('%'+identity+'%',))
      row = curs.fetchone()
      if row is not None:
        return redirect(url_for('display', identity = row['identity']))
      flash("Sorry, reviews for this identity do not yet exist in IDeal.")
    else:
      curs.execute('select term from terms where term = %s', ('%'+tag+'%',))
      row = curs.fetchone()
      if row is not None:
        return redirect(url_for('display', terms = row['term']))
      flash("Sorry, reviews for this tag do not yet exist in IDeal.")
    flash ("Please enter a search term in category.")
  return render_template('index.html',pageTitle='IDeal')

@app.route('/display/<company_name>', methods=['POST','GET'])
#@app.route('/display/<term>', methods=['POST','GET'])
#@app.route('/display/<identity>', methods=['POST','GET'])
def display(company_name=None, terms=None, identity=None):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  print company_name
  print terms
  print identity
  if company_name:
    rows = getCompanyReviews(company_name)
  elif terms:
    rows = getTermReviews(terms)
  else:
    rows =getIdentityReviews(identity)
  
  return render_template("display.html", info = rows)
  
def getCompanyReviews(company):
  curs = getConn().cursor(MySQLdb.cursors.DictCursor)
  curs.execute('select * from reviews join (select reviewID from companies where name like %s) as currCompany on reviews.reviewID = currCompany.reviewID', ('%'+company+'%',))
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
  
# @app.route('/display/<term>', methods=['POST','GET'])
# def display_review(term):
#   curs = getConn().cursor(MySQLdb.cursors.DictCursor)
#   curs.execute('select * from reviews join (select term from terms where name like %s) as currCompany on reviews.reviewID = currCompany.reviewID', ('%'+term+'%',))
#   row = curs.fetchall()
  
# @app.route('/display/<identity>', methods=['POST','GET'])
# def display_review(identity):
#   curs = getConn().cursor(MySQLdb.cursors.DictCursor)
#   curs.execute('select * from reviews join (select identity from companies where name like %s) as currCompany on reviews.reviewID = currCompany.reviewID', ('%'+identity+'%',))
#   row = curs.fetchall()

if __name__ == '__main__':
    app.debug = True
    port = os.getuid()
    # Flask will print the port anyhow, but let's do so too
    print('Running on port '+str(port))
    app.run('0.0.0.0',port)
      
  

