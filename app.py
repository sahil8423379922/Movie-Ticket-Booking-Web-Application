import json
from flask import Flask ,render_template , request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)



# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///auth.db"
app.config['SQLALCHEMY_BINDS']={
   'default':"sqlite:///auth.db",
   'db2':"sqlite:///movie.db",
   'db3':"sqlite:///bookedticket.db",
   'db4':"sqlite:///tdb.db",
   'db5':"sqlite:///ticketrange.db",

}





app.app_context()
db =SQLAlchemy(app)




#Model for Authentication
class db_model(db.Model):
    __bind_key__ = 'default'
    sno =db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(500),nullable = False)


#Model for TicketRange
class db_TicketRange(db.Model):
    __bind_key__ = 'db5'
    sno =db.Column(db.Integer,primary_key=True)
    tid=db.Column(db.String(200),nullable=False)
    totalseats=db.Column(db.String(500),nullable = False)
    


    def __repr__(self) -> str:
        return "{self.sno}-{self.title}"
    

#Model for Movie
class db_movie(db.Model):
    __bind_key__ = 'db2'
    sno =db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    url=db.Column(db.String(500),nullable = False)
    tid=db.Column(db.String(500),nullable = False)
    desc=db.Column(db.String(500),nullable = False)
    mid=db.Column(db.String(500),nullable = False)
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
    

#Model for Theater DB
class db_Theater(db.Model):
    __bind_key__ = 'db4'
    sno =db.Column(db.Integer,primary_key=True)
    tid=db.Column(db.String(200),nullable=False)
    tname=db.Column(db.String(200),nullable=False)
    city=db.Column(db.String(500),nullable = False)
    turl=db.Column(db.String(500),nullable = False)
    


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
        lst.append(x.mid)
        mn.append(lst)
    
    return render_template('seeall.html',mn=mn)

@app.route('/admin')
def admin():
    return render_template('dashbaord.html')


@app.route('/movie/<string:mid>',methods =['GET','POST'])
def movie(mid):

    citylist=["Delhi","Kanpur"]
    td=[]
    moviedetails=""

    if request.method =='POST':
        city = request.form['inputGroupSelect01']
        print(city)
      
        fetchTheather = db_Theater.query.all()
        moviedetails = db_movie.query.filter_by(mid=mid).first()
        for x in fetchTheather:
            if int(x.tid)==int(moviedetails.tid) and citylist[int(city)-1]==x.city:
                print("Name of the Theater =",x.tname)
                td.append(x)

        
        
        

    return render_template('movie_booking.html',mid=mid,citylist=citylist,td=td,moviedetails=moviedetails)



@app.route('/dashboard',methods =['GET','POST'])
def dashboard():
    if request.method =='POST':

        mname=request.form['name']
        murl=request.form['url']
        desc=request.form['desc']
        mid=request.form['mid']
        tid=request.form['tid']
        city=request.form['city']

        task =db_movie(name = mname, url=murl,desc = desc,mid=mid,
                       tid=tid,city=city)
        db.session.add(task)
        db.session.commit()
        redirect('/dashboard')

    return render_template('dashboard.html')


@app.route('/theater',methods =['GET','POST'])
def Theater():
    if request.method=="POST":
        tid=request.form['tid']
        tname=request.form['tname']
        city=request.form['city']
        url=request.form['url']
        totalseats=request.form['ts']
        task =db_Theater(tid = tid, tname=tname,city=city,turl=url)
        task1 = db_TicketRange(tid=tid,totalseats=totalseats)
        db.session.add(task)
        db.session.commit()
        db.session.add(task1)
        db.session.commit()

        return render_template('theaterform.html')
   

    
    return render_template('theaterform.html')



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

@app.route('/confirmticket/<string:tid>/<string:mid>',methods =['GET','POST'])
def confirmticket(tid,mid):
    flag=False
    theater = db_Theater.query.filter_by(tid=tid).first()
    movie = db_movie.query.filter_by(mid=mid).first()

    if request.method =="POST":
        print("Total Ticket Available =",request.form['ts'])
        totalseats =request.form['ts']
        totalseats = db_booked_tickets.query.filter_by(tid=tid).first()
        if int(totalseats.totalseats) >=int(totalseats):
            return render_template('payment.html')
        else:
             flag=True
             return render_template('ticketbooking.html',theater=theater,movie=movie,flag=flag)
    else:
        print("Theater id =",tid)
        print("Movie id =",mid)
        return render_template('ticketbooking.html',theater=theater,movie=movie,flag=flag)





   

@app.route('/payment')
def payment():
    return render_template('payment.html')



if __name__ =="__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
    
