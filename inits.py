from flask import Flask, render_template, request, url_for, flash, redirect, session, g
from flask_socketio import SocketIO, emit
from flask_mail import Mail, Message
import db
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)
#app.config['SERVER_NAME'] = 'myapp.dev:5000'
#session handling for the web pages
@app.route('/getsession')
def getSession():
    if 'user' in session:
        return session['user']
    elif 'doc' in session:
        return session['doc']
    elif 'admin' in session:
        return session['admin']

@app.route('/dropsessiondoc')
def dropSessionDoc():
    session.pop('doc', None)
    return redirect(url_for('doc'))

@app.route('/dropsessionuser')
def dropSessionUser():
    session.pop('user', None)
    return redirect(url_for('user'))

@app.route('/dropsessionadmin')
def dropSessionAdmin():
    session.pop('admin', None)
    return redirect(url_for('admin'))

@app.before_request
def before_request():
    g.user = None
    g.admin = None
    g.doc = None
    if 'user' in session:
        g.user = session['user']
    elif 'admin' in session:
        g.admin = session['admin']
    elif 'doc' in session:
        g.doc = session['doc']

#web pages routes
@app.route('/aboutus')
def about():
    return render_template('aboutus.html')
@app.route('/contactus')
def contact():
    return render_template('contactus.html')
@app.route('/about')
def aboutuser():
    return render_template('aboutuser.html')
@app.route('/contact')
def contactuser():
    return render_template('contactuser.html')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods = ['GET','POST'])
def admin():
    if request.method == 'GET':
        return render_template('admin_login.html')
    else:
        uname = request.form['username']
        pword = request.form['password']
        if uname =='admin' and pword =='admin':
            session['admin'] = uname
            print(session['admin'])
            return redirect(url_for('admin_logged'))

@app.route('/doc', methods = ['GET','POST'])
def doc():
    if request.method == 'GET':
        return render_template('doc_login.html')
    else:
        uname = request.form['fname']
        pword = request.form['pword']
        docs = db.query_login_doc()
        key, value = uname, pword
        if key in docs and value == docs[key]:
            details = "SELECT doc_type FROM register_doc WHERE firstname = '{}';".format(uname)
            db.cur.execute(details)
            x = db.cur.fetchall()
            session['doc'] = uname
            session['doc_type'] = x[0]

            return redirect(url_for('doc_logged'))
        else:
            return redirect(url_for('doc'))


@app.route('/user', methods = ['GET','POST'])
def user():
    if request.method == 'GET':
        return render_template('user_login.html')
    else:
        uname = request.form['fname']
        pword = request.form['pword']
        users = db.query_login_user()
        key, value = uname, pword
        print(key, value)
        print(users)
        if key in users and value == users[key]:
            print(users)
            session['user'] = uname
            return redirect(url_for('user_logged'))
        else:
            return render_template('user_login.html')

@app.route('/admin_logged', methods =['GET','POST'])
def admin_logged():
    if g.admin:
        if request.method == 'GET':
            return render_template('loggedin_admin.html')
    else:
        return redirect(url_for('admin'))

@app.route('/user_logged', methods = ['GET','POST'])
def user_logged():
    if g.user:
        if request.method == 'GET':
            return render_template('loggedin_user.html', username = session['user'])
        else:
            Cough = request.form['Cough']
            Headache = request.form['Headache']
            Fever = request.form['Fever']
            stomachpain = request.form['stomachpain']
            LowerAbdominalPain = request.form['LowerAbdominalPain']
            Vomiting = request.form['Vomiting']
            Diarrhea = request.form['Diarrhea']
            Flue = request.form['Flue']
            Chest_pain = request.form['Chest_pain']
            other_comments = request.form['other_comments']
            doc_type = request.form['type']
            email = "SELECT email FROM register_user WHERE firstname = '{}';".format(session['user'])
            db.cur.execute(email)
            user_mail = db.cur.fetchall()
            db.insert_messages(doc_type = doc_type,Cough = Cough, Headache = Headache, Fever = Fever, Stomachpain = stomachpain, LowerAbdominalPain = LowerAbdominalPain, Vomiting = Vomiting, Diarrhea = Diarrhea, Flue= Flue, Chest_pain = Chest_pain, other_comments = other_comments, email = user_mail)
            return redirect(url_for('user_logged'))
    return redirect(url_for('user'))

@app.route('/doc_logged', methods = ['GET', 'POST'])
def doc_logged():
    if g.doc:
        if request.method == 'GET':
            print(session['doc'])
            details = "SELECT doc_id, firstname, lastname, qualification, telephone, email FROM register_doc WHERE firstname = '{}';".format(session['doc'])
            db.cur.execute(details)
            x = db.cur.fetchall()
            return render_template('loggedin_doc.html',doc_logged = x)
        else:
            email =  request.form['email']
            telephone = request.form['telephone']
            varaible = session['doc']
            db.update_doc_details(telephone,email, varaible)
            return redirect(url_for('doc_logged'))
    else:
        return redirect(url_for('doc'))

@app.route('/register_user', methods = ['POST','GET'])
def register_user():    
    if request.method == "GET":
        return render_template('register_user.html') 
    else:
        fname = request.form['fname']
        lname = request.form['lname']
        pword = request.form['pword']
        tel = request.form['telephone']
        email = request.form['email']
        db.create_table_register_user()
        db.save_registered_user(fname,lname, pword, tel, email)
        flash("information successfully stored", "info")
        return render_template('register_user.html')
@app.route('/register_doc', methods = ['POST','GET'])
def register_doc():
    if g.admin:
        if request.method == "GET":
            return render_template('register_doc.html') 
        else:
            doc_id = request.form['doc_id']
            doc_type = request.form['type_doc']
            fname = request.form['firstname']
            lname = request.form['lastname']
            pword = request.form['password']
            qualification = request.form['qualification']
            tel = request.form['telephone']
            email = request.form['email']
            db.create_table_register_doc()
            db.save_registered_doctor(doc_id, doc_type,fname,lname, pword, qualification, tel, email)
            flash("information successfully stored", "info")
            return render_template('register_doc.html')
    else:
        redirect(url_for('admin'))
@app.route('/view_user', methods = ['GET', 'POST'])
def view_user():
    if g.admin:
        if request.method == 'GET':
            registered = db.query_registered_user()
            return render_template('view_user.html', td = (registered))
@app.route('/view_user_doc', methods = ['GET', 'POST'])
def view_user_doc():
    if g.doc:
        if request.method == 'GET':
            registered = db.query_registered_user()
            print(registered)
            return render_template('view_user_doc.html', td = (registered))
@app.route('/view_doctor', methods = ['GET', 'POST'])
def view_doctor():
    if g.admin:
        if request.method == 'GET':
            registered = db.query_registered_doc()
            return render_template('view_doc.html', td = (registered))
@app.route('/user_information', methods = ['GET', 'POST'])
def user_information():
    if g.user:
        if request.method == 'GET':
            details = "SELECT * FROM register_user WHERE firstname = '{}';".format(session['user'])
            db.cur.execute(details)
            x = db.cur.fetchall()
            return render_template('user_personal_information.html', user_logged = x)
        else:
            password =  request.form['password']
            telephone = request.form['telephone']
            email = request.form['email']
            varaible = session['user']
            print(password, telephone, email, varaible)
            db.update_user_details(password,telephone,email, varaible)
            return redirect(url_for('user_information'))
    else:
        return redirect(url_for('user'))

@app.route('/messages', methods = ['GET','POST'])
def messages():
    if g.doc:
        if request.method == 'GET':
            typo = session['doc_type']
            print(typo[0])
            messages = "SELECT * FROM {};".format(typo[0])
            db.cur.execute(messages)
            retrieved = db.cur.fetchall()
            return render_template('messages.html', x = retrieved)
    else:
        redirect(url_for('doc'))
@app.route('/message_to_admin', methods = ['GET','POST'])
def message_to_admin():
    if g.doc:
        if request.method == 'GET':
            details = "SELECT firstname, lastname, email FROM register_doc WHERE firstname = '{}';".format(session['doc'])
            db.cur.execute(details)
            x = db.cur.fetchall()
            return render_template('message_to_admin.html', details = x)
        else:
            firstname =  request.form['fname']
            lastname = request.form['lname']
            email = request.form['email']
            textarea = request.form['textarea']
            db.insert_message_admin(fname = firstname, lname = lastname,email = email, message = textarea)
            return redirect(url_for('message_to_admin'))
    else:
        redirect(url_for('doc'))
@app.route('/messages_admin', methods = ['GET','POST'])
def messages_admin():
    if g.admin:
        if request.method == 'GET':
            messages = "SELECT * FROM message_admin;"
            db.cur.execute(messages)
            retrieved = db.cur.fetchall()
            return render_template('messages_admin.html', x = retrieved)
    else:
        redirect(url_for('admin'))

@app.route('/email' , methods = ['GET', 'POST'])
def mail():
    if g.doc:
        if request.method == 'POST':
            try:
                email = request.form['email']
                body = request.form['body']

                app.config['TESTING'] = False
                app.config['MAIL_SERVER'] = 'smtp.gmail.com'
                app.config['MAIL_PORT'] = 465
                app.config['MAIL_USE_TLS'] = False
                app.config['MAIL_USE_SSL'] = True
                app.config['MAIL_DEBUG'] = True
                app.config['MAIL_USERNAME'] = 'kinyonyidavid@gmail.com'
                app.config['MAIL_PASSWORD'] = ''
                app.config['MAIL_DEFAULT_SENDER'] = ('E-MED','kinyonyidavid@gmail.com')
                app.config['MAIL_MAX_EMAILS'] = 1
                app.config['MAIL_SUPPRESS_SEND'] = False
                app.config['MAIL_ASCII_ATTACHMENTS'] = False

                mail = Mail(app)

                msg = Message('Hello', recipients = [email])
                msg.body = body
                mail.send(msg)
                return redirect(url_for('messages'))
            except:
                return ("Message not sent!, please try again doctor")
        else:
            return render_template("messages.html")

@app.route( '/chat' )
def chat():
  return render_template('chat.html')
@app.route( '/chatuser' )
def chatuser():
  return render_template('chatuser.html')
def messageRecived():
  print( 'message was received!!!' )

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) )
  socketio.emit( 'my response', json, callback=messageRecived )

if __name__ == '__main__':
    socketio.run( app, host = '127.0.0.1', port = 5000,debug = True )