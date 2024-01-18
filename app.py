from flask import Flask ,render_template , request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///auth.db"

app.app_context()
db =SQLAlchemy(app)

class db_model(db.Model):
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
    mn=[["Iron Man 1","https://firebasestorage.googleapis.com/v0/b/ticket-booking-system-a0a8a.appspot.com/o/Image%20Movies%2Fhanu-man-et00311673-1704954533.avif?alt=media&token=2548719d-4d32-44fe-adaa-c07601c9ecfc","Hanumanthu gets the powers of Hanuman in a distant village and fights for Anjanadri."],["Iron Man 2","https://assets-in.bmscdn.com/discovery-catalog/events/tr:w-400,h-600,bg-CCCCCC:w-400.0,h-660.0,cm-pad_resize,bg-000000,fo-top:l-image,i-discovery-catalog@@icons@@star-icon-202203010609.png,lx-24,ly-615,w-29,l-end:l-text,ie-Ny44LzEwICAyMS40SyBWb3Rlcw%3D%3D,fs-29,co-FFFFFF,ly-612,lx-70,pa-8_0_0_0,l-end/et00348399-dlwrzqasxw-portrait.jpg","Hanumanthu gets the powers of Hanuman in a distant village and fights for Anjanadri."]]
    return render_template('seeall.html',mn=mn)

@app.route('/admin')
def admin():
    return render_template('dashbaord.html')


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
    