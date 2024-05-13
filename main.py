from flask import Flask,redirect,render_template,Blueprint
from conf import app,auth,db,generate_password_hash,Sign,Login,User,current_user,login_user,load_user,login_required,logout_user,check_password_hash

with app.app_context():
    db.create_all()
# @app.route("/")
# def home_page():
#     return render_template('index.html')
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect("/dashboard")
    else:
        return render_template("index.html")

@auth.route("/signin")
def signin():
    form = Sign()
    return render_template("sign.html",form=form)
@auth.route("/signing",methods=['post'])
def signing():

        with app.app_context():
            form = Sign()

            print(form.username.data,form.password.data)
            user = User(name=form.username.data,password=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            login_user(user,True)
        return redirect("/dashboard")

@auth.route("/signup")
def signup():
    form = Login()
    return render_template("login.html",form=form)

@app.route("/login",methods=['post'])
def login_2():
    form = Login()
    print(form.username.data,form.password.data)
    usr = User.query.filter_by(name=form.username.data).first()
    if usr:
        print(form.username.data,form.password.data)
        if check_password_hash(usr.password,form.password.data):
            login_user(usr)
            return redirect("/dashboard")
        else:
            return "Parol Xato"
    else:
        return "Foydalanuvchi mavjud emas"
@app.route("/profile/edit")
def profile_edit():
    return render_template("profile.html")    


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "log out susses"
@app.route("/dashboard")
def dashboard():
     print(current_user.name)
     return str(current_user.name) 
    #  return render_template("dashboard.html")
app.register_blueprint(auth)
app.run()