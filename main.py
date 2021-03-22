from flask import Flask, Response, stream_with_context, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
import time, psycopg2


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK MODIFICATIONS']=False
db=SQLAlchemy(app)

con = psycopg2.connect(dbname="Kalder", user="postgres", password="root")
cur = con.cursor()

class Loans(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    type=db.Column(db.String(100))
    amount=db.Column(db.Integer)
    timeframe=db.Column(db.Integer)
    communication=db.Column(db.String(100))
    add_com=db.Column(db.String(200))

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template('register.html')

@app.route("/register_new", methods=["POST"])
def create_new_user():
    #get id
    cur.execute("select MAX(id) from users")
    maxid=cur.fetchall()
    id=maxid[0][0]+1
    name=request.form.get("username")
    password=request.form.get("psw")
    balance=request.form.get("balance")
    debt=0
    sql="insert into users values (%s, %s, %s, %s, %s)"
    values=[id, name, password, balance, debt]
    cur.execute(sql, values)
    con.commit()
    return redirect(url_for("home"))

@app.route("/request_latest/<int:rowcount>", methods=["GET"])
def hello1(rowcount):
    def f():
        sql="select * from transactions order by id desc limit %s"
        cur.execute(sql, [rowcount,])
        latest=cur.fetchall()
        return f'{latest}'
    return Response(stream_with_context(f()))

@app.route("/request_userinfo/<int:rowcount>", methods=["GET"])
def hello2(rowcount):
    def f2():
        sql="select * from users where id = %s "
        cur.execute(sql, [rowcount,])
        user_info=cur.fetchall()
        a=user_info[0][0]
        sql="select * from transactions where from_user = %s"
        cur.execute(sql, [a,])
        user_transactions=cur.fetchall()
        sql="select * from transactions where to_user = %s"
        cur.execute(sql, [a,])
        user_transactions2=cur.fetchall()
        return f'{user_info} \n \n \n {user_transactions} \n \n \n {user_transactions2}'
    return Response(stream_with_context(f2()))

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template('login.html')

@app.route("/profile", methods=["GET", "POST"])
def profile():
    return render_template('profile.html')

@app.route("/loans", methods=["GET", "POST"])
def loans():
    abc=Loans.query.all()
    return render_template('Loaning_services.html', a=abc)

@app.route("/add", methods=["POST"])
def add():
    #new loan
    type=request.form.get("req")
    amount=request.form.get("amnt")
    payback=request.form.get("pbk")
    communication_details=request.form.get("cd")
    additional_comments=request.form.get("ac")
    new_loan=Loans(type=type, amount=amount, timeframe=payback, communication=communication_details, add_com=additional_comments)
    db.session.add(new_loan)
    db.session.commit()
    return redirect(url_for("loans"))

@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    return render_template('transfer_funds.html')

@app.route("/mk_transaction", methods=["POST"])
def make_transaction():
    #get the data
    from_user=request.form.get("fname")
    to_user=request.form.get("Receiverid")
    amount=request.form.get("amnt")
    #execute the queries
    sql1="UPDATE users SET balance = balance - %s WHERE id = %s"
    sql2="UPDATE users SET balance = balance + %s WHERE id = %s"
    sql3="INSERT INTO transactions values (%s, %s, %s, NOW())"
    cur.execute(sql1, [amount, from_user,])
    cur.execute(sql2, [amount, to_user,])
    cur.execute(sql3, [from_user, to_user, amount])
    con.commit()
    return redirect(url_for("home"))

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method=="POST":
        return redirect(url_for('home_page.html'))
    return render_template('home_page.html')

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)





