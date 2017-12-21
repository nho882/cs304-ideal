import os, sys, datetime, MySQLdb, dbconn2, helper, imghdr, re
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session, jsonify
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
  rows = helper.getTermReviews(term)
  return render_template("display-terms.html", term=term, info = rows)


@app.route('/insert/', methods=['POST', 'GET'])
def insert():
  if request.method == 'POST':
    account = session['user_name']
    companyName = request.form['companyName']
    review = request.form['review']
    sentiment = request.form['sentiment']
    salary = request.form['salary']
    helper.insertReview(account, companyName, review, sentiment, salary)
    flash("Thank you for submitting your review!")
    return render_template('insert.html')

  user = session.pop('user_name', None)
  if user: 
    session['user_name'] = user
    return render_template('insert.html', account=user)
  else: 
    return redirect(url_for('signon'))
  

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
      session['logged_in'] = True
      session['user_name'] = account
      return redirect(url_for('displayAccount', accountName = account))
    else:
      flash("Sorry, we do not recognize this username and password.")
      return render_template('sign_on.html')
  
  return render_template('sign_on.html')

@app.route('/account/<accountName>', methods = ['POST', 'GET'])
def displayAccount(accountName):
  if request.method == 'GET':
    if accountName == session["user_name"]:
      rows = helper.getAccountReviews(accountName)
      row = helper.getAccountInfo(accountName)
      return render_template("account_display.html", accountName=accountName, reviews=rows, info=row)
    else:
      # No accountName specified 
      #OR the user is attempting to look at an account that is not theirs.
      return redirect(url_for('searchBar'))
  # On updating account information
  elif request.method == 'POST':
    accountName = session["user_name"]
    new_password = request.form["password"]
    new_job = request.form["jobTitle"]
    helper.updateAccount(accountName, new_password, new_job)
    flash("Your account has been updated")
    rows = helper.getAccountReviews(new_user_name)
    row = helper.getAccountInfo(new_user_name)
    return render_template("account_display.html", accountName=accountName, reviews=rows, info=row)
     

@app.route('/register', methods = ['POST', 'GET'])
def register():
  if request.method == 'POST':
    account = request.form['accountName']
    password = request.form['password']
    jobTitle = request.form['jobTitle']
    identities = request.form.getlist('identities')
    resume = request.files['resume']

    if account and password and jobTitle and identities:
      curs = helper.getConn().cursor(MySQLdb.cursors.DictCursor)
      curs.execute("select * from account where accountName = %s", (account,))
      row = curs.fetchall()
      if row:
        flash("Account name already exists. Please choose another one.")
        return render_template('register.html')
      else:
        flash("Successfully created account!")
        session["user_name"] = account
        session["logged_in"] = True
        curs.execute("insert into account values (%s, %s, %s, %s)", (account, password, jobTitle, resume))
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

@app.route('/signout/', methods = ['GET'])
def signout():
  session["logged_in"] = False
  session.pop('user_name', None)
  return redirect(url_for('searchBar'))

@app.route('/get_useful_count/', methods=['POST', 'GET'])
def get_useful_count():
  if request.method == 'GET':
    reviewID = request.args.get('review_ID')

  #hardcoded for the first review always, for now
  return jsonify(useful = helper.get_useful_count(reviewID)['useful'])

@app.route('/update_useful_count/', methods=['GET'])
def update_useful_count():
  if request.method == 'GET':
    reviewID = request.args.get('review_ID');
  return jsonify(usefulUpdate = helper.update_useful_count(reviewID)['useful'])

@app.route('/delete-review/', methods=["GET"])
def delete_review(account_name=None, reviewID=None):
  print "in here!"
  print "hello"
  account_name = request.args.get("account_name")
  reviewID = request.args.get("reviewID")
  helper.deleteReview(reviewID)
  return redirect(url_for("displayAccount", accountName=account_name))

    
  
if __name__ == '__main__':
    app.debug = True
    port = os.getuid()
    # Flask will print the port anyhow, but let's do so too
    print('Running on port '+str(port))
    app.run('0.0.0.0',port)
      