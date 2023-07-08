from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask.globals import request
from datetime import datetime


from flask_mail import Mail
import json

# import pymysql
# pymysql.install_as_MySQLdb()
local_server=True

with open('config.json','r') as c:
    params=json.load(c)['params']
    


app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['username'],
    MAIL_PASSWORD=params['password'],
)
mail=Mail(app)


if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
    

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
        
    

db = SQLAlchemy(app)

# id , name,phone_num,msg,date,email

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    phone_num = db.Column(db.String(13), unique=True, nullable=False)
    msg = db.Column(db.String(120), unique=False, nullable=False)
    date = db.Column(db.String(12),  nullable=True)
    email = db.Column(db.String(20), unique=True, nullable=False)

#  ====================== Post Class ==============
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    slug = db.Column(db.String(21), unique=True, nullable=False)
    content = db.Column(db.String(500), unique=False, nullable=False)
    tagline = db.Column(db.String(500), unique=False, nullable=False)
    date = db.Column(db.String(12),  nullable=True)





@app.route("/")
def home():
    posts=Posts.query.filter_by().all()[0:params['no_of_post']]
    return render_template('index.html',params=params,posts=posts)


@app.route("/post/<string:post_slug>",methods=['GET'])
def post_route(post_slug):
    post1 = Posts.query.filter_by(slug=post_slug).first()
    
    
    return render_template('post.html',params=params,post1=post1)




@app.route("/about")
def about():
    return render_template('about.html',params=params)


@app.route("/dashboard",  methods = ['GET','POST'])
def dashboard():
    if request.method=='POST':
        pass
    else:
        return render_template('login.html',params=params)
        
    
    






@app.route("/contact", methods = ['GET','POST'])
def contact():
    if(request.method=='POST'):
        
 
        name = request.form.get('name');
        email = request.form.get('email');
        phone = request.form.get('phone_num');
        message = request.form.get('message');
        
        entry=Contact(name=name,phone_num=phone,msg=message, date=datetime.now() ,email=email);
        db.session.add(entry)
        db.session.commit()
        # ====================== Mail Start ========================
        mail.send_message('New Message From '+name,
                          sender=email,
                          recipients=[params['username']],
                          body=message + "\n"+ phone
                          )
    #  =========================== mail End ======================
    return render_template('contact.html',params=params)

app.run(debug=True)