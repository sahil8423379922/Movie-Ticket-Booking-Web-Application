import json
from flask import Flask ,render_template , request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)



# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///auth.db"
app.config['SQLALCHEMY_BINDS']={
   'default':"sqlite:///auth.db",
   'db2':"sqlite:///movie.db",
   'db3':"sqlite:///bookedticket.db"
}





app.app_context()
db =SQLAlchemy(app)




#Model for Authentication
class db_model(db.Model):
    __bind_key__ = 'default'
    sno =db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(500),nullable = False)
    


    def __repr__(self) -> str:
        return "{self.sno}-{self.title}"
    

#Model for Movie
class db_movie(db.Model):
    __bind_key__ = 'db2'
    sno =db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    url=db.Column(db.String(500),nullable = False)
    desc=db.Column(db.String(500),nullable = False)
    tid=db.Column(db.String(500),nullable = False)
    city=db.Column(db.String(500),nullable = False)
    


    def __repr__(self) -> str:
        return "{self.sno}-{self.title}"
    

#Model for Booked ticket
class db_booked_tickets(db.Model):
    __bind_key__ = 'db3'
    sno =db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(500),nullable = False)
    


    def __repr__(self) -> str:
        return "{self.sno}-{self.title}"
    





@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/login',methods =['GET','POST'])
def login():
    email=""
    password=""
    if request.method =='POST':
        email= request.form['email']
        password=request.form['pass']

    
    authdetails = db_model.query.all()
    
    for x in authdetails:
        print('Loop Executing = {} and  {}'.format(type(x.email),type(x.password)))
        print('Form Data = {} and  {}'.format((email),(password)))
        if x.password ==str(password):
            print("User Authenticated")
            return render_template('dashboard.html')

    return render_template('login.html')



@app.route('/seeall')
def seeall():
    moviename = db_movie.query.all()
    mn=[]
    for x in moviename:
        lst=[]
        lst.append(x.name)
        lst.append(x.url)
        lst.append(x.desc)
        mn.append(lst)
    
    return render_template('seeall.html',mn=mn)

@app.route('/admin')
def admin():
    return render_template('dashbaord.html')

@app.route('/movie/<string:mname>')
def movie(mname):
   
    minstance=""
    tn=""
    tid=""
    

    tname={1:["Inox","Delhi"],2:["PVR","Delhi"]}
    fetchmovie = db_movie.query.all()
    
    for x in fetchmovie:
        for m,n in tname.items():
            if int(x.tid)==m and x.city==n[1]:
               minstance = x
               tn=n[0]
               tid=m
                

    return render_template('movie_booking.html',mname=mname,minstance=minstance,tn=tn,tid=tid)



@app.route('/dashboard',methods =['GET','POST'])
def dashboard():
    if request.method =='POST':

        mname=request.form['name']
        murl=request.form['url']
        desc=request.form['desc']
        tid=request.form['tid']
        city=request.form['city']

        task =db_movie(name = mname, url=murl,desc = desc,tid=tid,city=city)
        db.session.add(task)
        db.session.commit()
        redirect('/dashboard')

    return render_template('dashboard.html')




@app.route('/register',methods =['GET','POST'])
def Register():
    if request.method == "POST":
        email= request.form['email']
        password=request.form['pass']

        email=email.replace('.','')
        password = password.replace('.','')
        
        task =db_model(email = email, password=password)
        db.session.add(task)
        db.session.commit()
        redirect('register.html')


    return render_template('register.html')



if __name__ =="__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
    
