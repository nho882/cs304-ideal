import os, sys, datetime, MySQLdb, dbconn2, helper, imghdr, re
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from werkzeug import secure_filename
app = Flask(__name__)
app.secret_key = 'nancyhohoho'

@app.route('/', methods=['POST','GET']) #Renders search page
def searchBar():
  if request.method == 'POST': 
    #Assume user is only searching for one of these items for now
    curs = helper.getConn().cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
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
  rows = helper.getIdentityReviews(identity)
  print rows
  return render_template("display-identity.html", identity=identity, info = rows)


@app.route('/display-company/<company_name>', methods=['POST','GET'])
def display_company(company_name):
  rows = helper.getCompanyReviews(company_name)
  return render_template("display.html", company=company_name, info = rows)

@app.route('/display-term/<term>', methods=['POST','GET'])
def display_term(term):
  rows = helper.getTermReviews(terms)
  return render_template("display-terms.html", term=term, info = rows)


@app.route('/insert/', methods=['POST', 'GET'])
def insert():
  if request.method == 'POST':
    account = request.form['accountName']
    companyName = request.form['companyName']
    review = request.form['review']
    sentiment = request.form['sentiment']
    salary = request.form['salary']
    helper.insertReview(account, companyName, review, sentiment, salary)
    flash("Thank you for submitting your reivew!")
    return render_template('insert.html')

  cookie = request.cookies.get('username')
  if cookie: 
    return render_template('insert.html', account=cookie)
  else: 
    flash("You must be logged in to add a review!")
    return render_template('insert.html', account="NO ACCOUNT!")
  

@app.route('/sign_on', methods = ['POST', 'GET'])
def signon():
  if request.method == 'POST':
    account = request.form['accountName']
    password = request.form['accountPassword']
    row = helper.login(account, password)
    if row is None:
      flash("Sorry, we do not recognize this username and password.")
      return render_template('sign_on.html')
    if row['password'] == password:
      flash("Successfully logged in.")
      resp = make_response(render_template('account_display.html',
                                           accountName = account))
      resp.set_cookie('username', request.form['accountName'])
      # return render_template('account_display.html')
      # return redirect(url_for('displayAccount', accountName = account))
      return resp
      #Redirect to an account page
    else:
      flash("Sorry, we do not recognize this username and password.")
      return render_template('sign_on.html')
  
  return render_template('sign_on.html')

@app.route('/account/<accountName>', methods = ['POST', 'GET'])
def displayAccount(accountName):
  rows = helper.getAccountInfo(accountName)
  return render_template("account_display.html", accountName = accountName, info = rows)


@app.route('/register', methods = ['POST', 'GET'])
def register():
  if request.method == 'POST':
    account = request.form['accountName']
    password = request.form['password']
    jobTitle = request.form['jobTitle']
    identities = request.form.getlist('identities')

    if account and password and jobTitle and identities:
      curs = helper.getConn().cursor(MySQLdb.cursors.DictCursor)
      curs.execute("select * from account where accountName = %s", (account,))
      row = curs.fetchall()
      if row:
        flash("Account name already exists. Please choose another one.")
        return render_template('register.html')
      else:
        flash("Successfully created account!")
        curs.execute("insert into account values (%s, %s, %s)", (account, password, jobTitle))
        for identity in identities:
          curs.execute("insert into identities values(%s, %s)", (identity, account))
        return redirect(url_for('displayAccount', accountName = account))
  identities = helper.getIdentities()[0]['Type']
  identities = re.sub('[(){}<>]', '', identities)
  identities = identities.replace('enum','').replace("'", '').split(',')
  return render_template('register.html', identities= identities)

@app.route('/about/', methods = ['POST', 'GET'])
def about():
  return render_template('about.html')

@app.route('/contact/', methods = ['POST', 'GET'])
def contact():
  return render_template('contact.html')
  
if __name__ == '__main__':
    app.debug = True
    port = os.getuid()
    # Flask will print the port anyhow, but let's do so too
    print('Running on port '+str(port))
    app.run('0.0.0.0',port)
      
  

