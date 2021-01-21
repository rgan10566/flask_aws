#Flask program for online Asset Reporting System
#Author: Ramesh Ganesan
#email : rganesan@beachbody.com
#Date  : 01/12/2021
#updated: 01/20/2021


from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import logging
from logging import Formatter, FileHandler


app = Flask(__name__)

# Config MySQL - This needs to be eventually segregated
app.config['MYSQL_HOST'] = 'tablette-1.culomlubyiwb.us-west-2.rds.amazonaws.com'
# app.config['MYSQL_PORT'] = '3306'
app.config['MYSQL_USER'] = 'appadmin'
app.config['MYSQL_PASSWORD'] = 'BB_Tabl3tt3'
app.config['MYSQL_DB'] = 'tablette'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.logger.setLevel(logging.INFO)

# init MYSQL
mysql = MySQL(app)

# Home - renders home.html
@app.route('/')
def index():
    return render_template('./home.html')

# About - renders about.html
@app.route('/about')
def about():
    return render_template('./about.html')

# Assets - Fetches all the asses
@app.route('/assets')
def assets():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT IP, DNS, OS, APPLICATION, SUBAPPLICATION, ENVIRONMENT, sfunction, HTYPE, INFRASTATUS, TIER FROM tablette.ASSETS where infrastatus = 'ACTIVE' order by tier,application, environment, subapplication, sfunction, htype, ip")

    # if asset == 'null':
    #     result = cur.execute("SELECT IP, DNS, OS, APPLICATION, SUBAPPLICATION, ENVIRONMENT, sfunction, HTYPE, INFRASTATUS, TIER FROM tablette.ASSETS where infrastatus = 'ACTIVE' order by tier,application, environment, subapplication, sfunction, htype, ip")
    # else:
    #     # Get articles
    #     result = cur.execute("SELECT IP, DNS, OS, APPLICATION, SUBAPPLICATION, ENVIRONMENT, sfunction, HTYPE, INFRASTATUS, TIER FROM tablette.ASSETS where infrastatus = 'ACTIVE' and IP = %s order by tier,application, environment, subapplication, sfunction, htype, ip", [asset])

    assets = cur.fetchall()

    if result > 0:
        return render_template('assets.html', assets=assets)
    else:
        msg = 'Asset not Found'
        return render_template('assets.html', msg=msg)
    # Close connection
    cur.close()

# Environments post report
@app.route('/showenvironment/<env>')
def showenvironment(env):
        # ask an environment
        # Create cursor
        # env = request.args.get('env')
        cur = mysql.connection.cursor()

        if env == 'null':
            result = cur.execute("SELECT IP, DNS, OS, APPLICATION, SUBAPPLICATION, ENVIRONMENT, sfunction, HTYPE, INFRASTATUS, TIER FROM tablette.ASSETS where infrastatus = 'ACTIVE' order by tier,application, environment, subapplication, sfunction, htype, ip")
        else:
            # Get articles
            result = cur.execute("SELECT IP, DNS, OS, APPLICATION, SUBAPPLICATION, ENVIRONMENT, sfunction, HTYPE, INFRASTATUS, TIER FROM tablette.ASSETS where infrastatus = 'ACTIVE' and ENVIRONMENT = %s order by tier,application, environment, subapplication, sfunction, htype, ip", [env])

        environments = cur.fetchall()

        if result > 0:
            return render_template('showenvironment.html', environments=environments)
        else:
            msg = 'Environment not Found'
            return render_template('showenvironment.html', msg=msg)
    # Close connection
        cur.close()

# Environments main - get
@app.route('/environments', methods=['GET', 'POST'])
def environments():
        # ask an environment
        # Create cursor
        if request.method == 'POST':
                env = request.form['env']
                if env == "":
                    env='null'
                return redirect(url_for('showenvironment',env=env))
        else:
            return render_template('environments.html')


# Applications post report
@app.route('/showapplication/<app>')
def showapplication(app):
        # ask an environment
        # Create cursor
        # env = request.args.get('env')
        cur = mysql.connection.cursor()

        if app == 'null':
            result = cur.execute("SELECT IP, DNS, OS, APPLICATION, SUBAPPLICATION, ENVIRONMENT, sfunction, HTYPE, INFRASTATUS, TIER FROM tablette.ASSETS where infrastatus = 'ACTIVE' order by tier,application, environment, subapplication, sfunction, htype, ip")
        else:
            # Get articles
            result = cur.execute("SELECT IP, DNS, OS, APPLICATION, SUBAPPLICATION, ENVIRONMENT, sfunction, HTYPE, INFRASTATUS, TIER FROM tablette.ASSETS where infrastatus = 'ACTIVE' and APPLICATION = %s order by tier,application, environment, subapplication, sfunction, htype, ip", [app])

        applications = cur.fetchall()

        if result > 0:
            return render_template('showapplication.html', applications=applications)
        else:
            msg = 'Application not Found'
            return render_template('showapplication.html', msg=msg)
    # Close connection
        cur.close()

# Applications main - get
@app.route('/applications', methods=['GET', 'POST'])
def applications():
        # ask an environment
        # Create cursor
        if request.method == 'POST':
                app = request.form['app']
                if app == "":
                    app='null'
                return redirect(url_for('showapplication',app=app))
        else:
            return render_template('applications.html')

# Tiers post report
@app.route('/showtier/<tier>')
def showtier(tier):
        # ask an environment
        # Create cursor
        # env = request.args.get('env')
        cur = mysql.connection.cursor()

        if tier == 'null':
            result = cur.execute("SELECT IP, DNS, OS, APPLICATION, SUBAPPLICATION, ENVIRONMENT, sfunction, HTYPE, INFRASTATUS, TIER FROM tablette.ASSETS where infrastatus = 'ACTIVE' order by tier,application, environment, subapplication, sfunction, htype, ip")
        else:
            # Get articles
            result = cur.execute("SELECT IP, DNS, OS, APPLICATION, SUBAPPLICATION, ENVIRONMENT, sfunction, HTYPE, INFRASTATUS, TIER FROM tablette.ASSETS where infrastatus = 'ACTIVE' and TIER = %s order by tier,application, environment, subapplication, sfunction, htype, ip", [tier])

        tiers = cur.fetchall()

        if result > 0:
            return render_template('showtier.html', tiers=tiers)
        else:
            msg = 'Application not Found'
            return render_template('showtier.html', msg=msg)
    # Close connection
        cur.close()

# Tiers main - GET
@app.route('/tiers', methods=['GET', 'POST'])
def tiers():
        # ask an environment
        # Create cursor
        if request.method == 'POST':
                tier = request.form['tier']
                if tier == "":
                    tier='null'
                return redirect(url_for('showtier',tier=tier))
        else:
            return render_template('tiers.html')

# User Register - this needs to be redone
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        #cur = mysql.connection.cursor()

        # Execute query
        #cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        #mysql.connection.commit()

        # Close connection
        #cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# User login - this needs to be redone
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        #cur = mysql.connection.cursor()

        # Get user by username
        #result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        #if result > 0:
            # Get stored hash
            #data = cur.fetchone()
            #password = data['password']

            # Compare Passwords
            #if sha256_crypt.verify(password_candidate, password):
                # Passed
                #session['logged_in'] = True
                #session['username'] = username

                #flash('You are now logged in', 'success')
                #return redirect(url_for('dashboard'))
            #else:
                #error = 'Invalid login'
                #return render_template('login.html', error=error)
            # Close connection
            #cur.close()
        #else:
            #error = 'Username not found'
            #return render_template('login.html', error=error)

    return render_template('login.html')


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
