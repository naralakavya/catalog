from flask import Flask,redirect,url_for,render_template,request,flash
from flask_mail import Mail,Message
from random import randint
from project_database import Register,Base,User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_login import LoginManager,login_user,current_user,logout_user,login_required,UserMixin

engine=create_engine('sqlite:///iiit.db')
engine=create_engine('sqlite:///iiit.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()


app=Flask(__name__)

login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='naralakavya26@gmail.com'
app.config['MAIL_PASSWORD']='harithra@123'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

app.secret_key = 'abc'
mail=Mail(app)
otp=randint(000000,999999)

@app.route("/sample")
def demo():
    return "hello world"

@app.route("/demo")
def d():
 	return "<h1>Hello demo page</h1>"

@app.route("/info/details")
def details():
    return "hello details"

@app.route("/details/<name>/<int:age>/<float:salary>")
def info(name,age,salary):
	return "<h2>hello {} age {} and salary {} <h2>".format(name,age,salary) #{} or {{}}-deliminator 

@app.route("/admin")
def admin():
	return "Hello Admin"

@app.route("/student")
def student():
	return "Hello Student"

@app.route("/staff")
def staff():
	return "Hello Staff"

@app.route("/info/<name>")
def admin_info(name):
	if name=='admin':
		return redirect(url_for('admin'))
	elif name=='student':
		return redirect(url_for('student'))
	elif name=='staff':
		return redirect(url_for('staff'))
	else:
		return "NO URL"

 
@app.route("/data/<name>/<int:age>/<float:salary>")
def demo_html(name,age,salary):
	return render_template('sample.html',n=name,k=age,l=salary)

@app.route("/tableformat")
def table():
	s_no=10
	name='kavya'
	branch='cse'
	dept='student'
	return render_template('tableform.html',k=s_no,l=name,m=branch,n=dept)

data=[{'sno':123,'name':'kavya','branch':'cse','dept':'studesnt'},{'sno':22,'name':'narala','branch':'ece','dept':'employ'},{'sno':111,'name':'keerthi','branch':'mech','dept':'devoloper'}]
@app.route("/dummy_data")
def dummy(): 
	return render_template("dictionary.html",dummy_data=data)
@app.route("/table/<int:number>")
def table1(number):
	 return render_template("multipletab.html",n=number)

@app.route("/file_Upload",methods=['GET','POST'])
def file_upload():
	 return render_template("file_upload.html")

@app.route("/success",methods=['GET','POST'])
def success():
	if request.method=="POST":
		f=request.files["file"]
		f.save(f.filename)
		return render_template("success.html",f_name=f.filename)

@app.route("/email",methods=['POST','GET'])
def email_send():
	return render_template("email.html")

@app.route("/email_verify",methods=['POST','GET'])
def verify_email():
    email=request.form['email']
    msg=Message('One time password',sender='naralakavya26@gmail.com',recipients=[email])
    msg.body=str(otp)
    mail.send(msg)
    return render_template('v_email.html')

@app.route("/email_success",methods=['POST','GET'])
def success_email():
	user_otp=request.form['otp']
	if otp==int(user_otp):
		return render_template("email_success.html")
	return "invaild otp"

@app.route("/show")
def showData():
	register=session.query(Register).all()
	return render_template('show.html',reg=register)
@app.route("/login",methods=['POST','GET'])
def loginPage():
	if current_user.is_authenticated:
		return redirect(url_for('showData'))

	try:
		if request.method=='POST':
		   user=session.query(User).filter_by(email=request.form['email'],password=request.form['password']).first()
		   
		   if user:

                login_user(user)
                return redirect(url_for('showData'))
           else:
		   	    flash("Invalid login...")
		else:
            return render_template('login.html',title='login')
    except Exception as e:
    	flash("login failed...")
    else:
    	return render_template("login.html",title='login')

   @app.route("/logout")
   def.logout():
   		logout_user()
   		return.redriect(url_for('nav'))


   @login_manager.user_loader
   def load_user(user_id):
   		return session.query(User).get(int(user_id))




@app.route("/reg",methods=['POST','GET'])
def regpage():
	if request.method=='POST':
		newData=Register(name=request.form['name'],
			surname=request.form['surname'],
			mobile=request.form['mobile'],
			email=request.form['email'],
			branch=request.form['branch'],
			role=request.form['role'])
		session.add(newData)
		session.commit()
		flash("New dta added...")

		return redirect(url_for('showData'))
	else:
         return render_template('register.html')

@app.route("/bootstrap")
def boot():
	 return render_template('bootstrapcheck.html') 
@app.route("/")
def nav():
	return render_template('navigation.html')

@app.route("/edit/<int:register_id>",methods=['POST','GET'])
def editData(register_id):
    editedData=session.query(Register).filter_by(id=register_id).one()
    if request.method=='POST':
       editedData.name=request.form['name']
       editedData.surname=request.form['surname']
       editedData.mobile=request.form['mobile']
       editedData.email=request.form['email']
       editedData.branch=request.form['branch']
       editedData.role=request.form['role']
       session.add(editedData)
       session.commit()
       flash("edited data added...")
       return redirect(url_for('showData'))
    else:
       return render_template('edit.html',register=editedData)

@app.route("/delete/<int:register_id>",methods=['POst','GET'])
def deleteData(register_id):
    deletedData=session.query(Register).filter_by(id=register_id).one()
    if request.method=='POST':
       deletedData.name=request.form['name']
       session.delete(deletedData)
       session.commit()
       flash("data deleted successfully...{}".format(deletedData.name))
       return redirect(url_for('showData'))
    else:
       return render_template('delete.html',register=deletedData)

@app.route("/account",methods=['POST','GET'])
def account():
	return render_template("account.html")



if __name__=='__main__':
      app.run(debug=True)