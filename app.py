#importing necessary modules
from flask import Flask, render_template, request, redirect ,session
from flask_sqlalchemy import SQLAlchemy
from datetime import date , timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import random
from flask_mail import Mail , Message

#important configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///haris.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
app.config['SECRET_KEY'] = '123456'
db = SQLAlchemy(app)

#mail configuration
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hariscodes00@gmail.com'
app.config['MAIL_PASSWORD'] = 'ewiy heoy hhty lpko'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#Making The todo app
#defining class for app table
class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    desc = db.Column(db.String(5000),nullable = False)
    date = db.Column(db.Date, default = date.today)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

#Making user Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20) , nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200) , nullable=False)


#functional aspect of app
@app.route('/' , methods = ['GET','POST'])
def home():
    if 'user_id' not in session:
        return redirect('/signup')

    if request.method == 'POST':
        title = request.form.get("title")
        desc = request.form.get("desc")

        new_todo = Todo(title=title, desc=desc )
        db.session.add(new_todo)
        db.session.commit()

    all_todos = Todo.query.all()
    return render_template('index.html' , allTodo = all_todos)

#signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')


        #Setting up OTP
        otp = str(random.randint(1000,9999))
        session['otp'] = otp


        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
             return 'Username or Email already exists!'

        #Starting sessions
        session['signup_data'] = {
            'username' : username,
            'email' : email,
            'password_1': generate_password_hash(password)
        }

        #sending OTP
        msg = Message('Verify Your Email - Haris Todo App' ,sender = 'hariscodes00@gmail.com' , recipients = [email] )

        msg.body = f'Your OTP is {otp}'
        mail.send(msg)

        return redirect('/otp')
    return render_template('signup.html')

#OTP Route
@app.route('/otp', methods =['GET' , 'POST'] )
def otp ():
    return render_template('otp.html')

#Verifying OTP
@app.route('/verify-otp' , methods = ['GET' , 'POST'])
def verify():
    if request.method =='POST':
        user_otp = request.form.get('otp')
        actual_otp = session.get('otp')
        if user_otp == actual_otp:
            data = session.get('signup_data')
            if data:
                user = User(
                username = data['username'],
                email = data['email'],
                password = data['password_1']

            )
                db.session.add(user)
                db.session.commit()

                return redirect('/login')
    error = "Invalid OTP. Please try again."
    return render_template('otp.html' , error=error)

#Resend OTP
@app.route('/resend-otp', methods = ['POST'])
def resend():
    otp = str(random.randint(1000,9999))
    session['otp'] = otp
    email = session.get('signup_data', {}).get('email')
    if not email:
        return redirect('/signup')

    msg = Message ('Verify Your Email - Haris Todo App' , sender = 'hariscodes00@gmail.com' , recipients = [email])
    msg.body = f'Your OTP is {otp}'

    mail.send(msg)

    return render_template('otp.html' , message = 'OTP Resend Successfully')




#login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session.permanent = True
            session['user_id'] = user.id
            return redirect('/')
        return 'Invalid Credentials'
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

#Defining Delete Action
@app.route("/delete/<int:sno>" )
def delete(sno):
    todo = db.session.get(Todo, sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect ('/')

@app.route("/update/<int:sno>" , methods = ['GET','POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        todo.title = title
        todo.desc = desc
        db.session.commit()
        return redirect ('/')
    return render_template('update.html', todo=todo)



if __name__ == "__main__":
    app.run(debug=True)