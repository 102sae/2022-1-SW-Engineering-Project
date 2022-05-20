
from flask import Flask,redirect,render_template,url_for, request, flash, session

from DB_handler import DBModule

app = Flask(__name__)
app.secret_key = "skjdbfbaskbdjbff"
DB = DBModule()

@app.route("/") #홈
def index():
    if "uid" in session: #로그인 된 상태일 경우 
        user = session["uid"]
    else:
        user = "Login" #로그아웃 된 상태일 경우
    return render_template("index.html",user =user)

#회원가입
@app.route("/signin")
def signin():
   return render_template("signin.html")

@app.route("/signin_done", methods =["get"])
def signin_done():
    email  = request.args.get("email") 
    uid  = request.args.get("id")
    pwd = request.args.get("pwd")
    name  = request.args.get("name")
    if DB.signin(uid,pwd,name,email): #중복 정보 없을 때
        return redirect(url_for("index"))
    else: #중복 정보 있을 때
        flash("이미 존재하는 아이디입니다.")
        return redirect(url_for("signin"))

#로그인 
@app.route("/login")
def login():
    if "uid" in session: #로그인 된 상테에서 로그인 창에 들어오면
        return redirect(url_for("index")) #홈으로 
    return render_template("login.html")
    
@app.route("/login_done", methods =["get"])
def login_done():
    uid  = request.args.get("id")
    pwd = request.args.get("pwd")
    if DB.login(uid,pwd): #로그인 정보가 일치하면
        session["uid"] = uid #로그인 세션 열어줌
        return redirect(url_for("index"))
    else: #로그인 정보가 일치하지 않을 경우
        flash("아이디가 존재하지 않거나 비밀번호가 다릅니다.")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "uid" in session: #로그인 상태
        session.pop("uid") 
        return redirect(url_for("index"))
    else: #로그아웃 상태
        return redirect(url_for("login"))


#글 작성
@app.route("/write")
def write():
    if "uid" in session:
        return render_template("write_post.html")
    else:
        return redirect(url_for("login"))
    

@app.route("/write_done",methods=["get"])
def write_done():
    title  = request.args.get("title") 
    contents  = request.args.get("contents")
    cost = request.args.get("cost")
    uid = session.get("uid")
    
    DB.write_post(title,contents,cost,uid)
    return redirect(url_for("index"))

#글 목록 보기
@app.route("/user/<string:uid>")
def user_posts(uid):
    user_post = DB.get_user(uid)
    if user_post == None:
        length = 0
    else :
        length = len(user_post)
    
    return render_template("user_detail.html",post_list = user_post, length = length,uid = uid)



@app.route("/list")
def post_list():
    post_list = DB.post_list()
    if post_list == None :
        length = 0
    else:
        length = len(post_list)

    return render_template('product_list.html',post_list = post_list,length = length)


@app.route("/post/<string:pid>")
def post(pid):
    post = DB.post_detail(pid)
    return render_template("product_detail.html",post = post)

@app.route("/user/<uid>")
def user(uid):
    pass

if __name__ == "__main__":
    app.run(debug=True)