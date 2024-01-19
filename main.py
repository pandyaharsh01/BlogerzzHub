from flask import Flask ,render_template,request, session
from flask_sqlalchemy import SQLAlchemy
# from flask_mail import Mail 
import json
from datetime import datetime



'''$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--building connection--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'''



with open('config.json','r') as c:
	para = json.load(c)["para"]

local_server= True
app= Flask(__name__)
app.secret_key = "Your_secret_string"


'''$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--getting email(optional)--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'''

# app.config.update(
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = '465',
#     MAIL_USE_SSL = True,
#     MAIL_USERNAME = para['gmail-user'],
#     MAIL_PASSWORD = para['gmail-password']
# )
# mail = Mail(app)

'''$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--getting email(optional)--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'''



if (local_server):
	app.config['SQLALCHEMY_DATABASE_URI'] = para['local_uri']
else:
	app.config['SQLALCHEMY_DATABASE_URI'] = para['prod_uri']

db = SQLAlchemy(app)

class Contacts(db.Model):
    sr_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    ph_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)
 
class Post(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    tagline = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)
    
# class Login(db.Model):
#     sr = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), nullable=False)
#     password = db.Column(db.String(80), nullable=False)
    
 
'''$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--home--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'''	
	

@app.route('/')
def home ():
	posts=Post.query.filter_by().all()
	return render_template('index.html', para=para, post=posts)



'''$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--about--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'''	



@app.route('/about')
def about():
	return render_template('about.html', para=para)

@app.route("/login",methods = ['GET' ,'POST'])
def dashboard():

	if ('user' in session and session['user'] == para['admin_user']):
		post=Post.query.all()
		return render_template('dashboard.html',para=para,post=post)

	if(request.method=='POST'):
		username=request.form.get('uname')
		userpass=request.form.get('pass')
		if (username==para['admin_user'] and userpass==para['admin_pass']):
			#set the session varioble
			session['user']=username
			post=Post.query.all()
			return render_template('dashboard.html',para=para,post=post)

		else:
			return render_template('not logged in.html')

	else:
		return render_template('login.html',para=para)

'''$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--contact--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'''	



@app.route("/contact",methods = ['GET' ,'POST'])
def contact():
	if(request.method=='POST'):
		name=request.form.get('name')
		email=request.form.get('email')
		phone=request.form.get('phone')
		message=request.form.get('message')
		entry=Contacts(name=name , ph_num=phone , msg=message , date = datetime.now() , email=email)
		db.session.add(entry)
		db.session.commit()
		
		# mail.send_message('New message from ' + name,
        #                   sender=email,
        #                   recipients = [para['gmail-user']],
        #                   body = message + "\n" + phone
        #                   )
	return render_template('contact.html', para=para)
	


'''$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$--sample post--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'''	


@app.route('/post/<string:post_slug>',methods=['GET'])
def post_route(post_slug):
	post = Post.query.filter_by(slug=post_slug).first()
	return render_template('post.html', para=para, post = post)

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')


