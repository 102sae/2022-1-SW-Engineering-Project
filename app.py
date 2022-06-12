
from sre_parse import State
from flask import Flask,redirect,render_template,url_for, request, flash, session
from werkzeug.utils import secure_filename
from DB_handler import DBModule
import os
import urllib.request
"""
#define FIREBASE_HOST "trade-market-d3fe6-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "BkztFqlcC1wLXlPfFq3AaRt13KoszmqiNVg37kxd"

"""
app = Flask(__name__)
app.secret_key = "skjdbfbaskbdjbff"

DB = DBModule()

UPLOAD_FOLDER = 'static/img/'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_PATH"] = 16*1024*1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 

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

# 팔로우 기능
@app.route("/user/<string:uid>/a")
def following_user(uid):
    fid = request.args.get('fid', default = 'followed', type = str) #follow할 user id가져오기

    user_post = DB.get_user(fid)
    if user_post == None:
        length = 0
    else :
        length = len(user_post)
    
    if "uid" in session: #로그인 된 상태일 경우 
         user = session["uid"]
         test = DB.follow(user,fid)
         return render_template("user_detail.html",post_list = user_post, length = length,uid = fid,user=user,isFollow =test)      
    else:
         user = "Login" #로그아웃 된 상태일 경우
         return render_template("index.html",user=user)   

# 언팔로우 기능
@app.route("/user/<string:uid>/u")
def unfollowing_user(uid):
    fid = request.args.get('fid', default = 'followed', type = str) #follow할 user id가져오기

    user_post = DB.get_user(fid)
    if user_post == None:
        length = 0
    else :
        length = len(user_post)
    
    if "uid" in session: #로그인 된 상태일 경우 
         user = session["uid"]
         test = DB.unfollow(user,fid)
         return render_template("user_detail.html",post_list = user_post, length = length,uid = fid,user=user,isFollow =test)      
    else:
         user = "Login" #로그아웃 된 상태일 경우
         return render_template("index.html",user=user)  
    
#글 작성
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/write")
def write():
    if "uid" in session:
        return render_template("write_post.html")
    else:
        return redirect(url_for("login"))
    

@app.route("/write_done",methods=['GET','POST'])
def write_done():
    title  = request.args.get("title") 
    contents  = request.args.get("contents")
    cost = request.args.get("cost")
    keyword = request.args.get("keyword")
    uid = session.get("uid") # 글 내용
    status = request.args.get("판매상태")
    #image = request.files['image']
    DB.write_post(title,contents,cost,keyword,uid,status)

    return redirect(url_for("index"))

#검색
'''
@app.route("/searching",methods=['GET','POST'])
def searching():
    title  = request.args.get("title") 
    contents  = request.args.get("contents")
    cost = request.args.get("cost")
    keyword = request.args.get("keyword")
    uid = session.get("uid") # 글 내용
    status = request.args.get("판매상태")
    #image = request.files['image']
    DB.write_post(title,contents,cost,keyword,uid,status)

    return redirect(url_for("index"))
'''

#글 삭제
@app.route("/delete_done",methods=['GET','POST'])
def delete_done():
    pid = request.args.get('pid', default = 'pid', type = str)
    DB.delete_post(pid)
    return redirect(url_for("index"))

#유저 글 모아 보기
@app.route("/user/<string:uid>")
def user_posts(uid):
    if "uid" in session: #로그인 된 상태일 경우 
        user = session["uid"]
    else:
        user = "Login" #로그아웃 된 상태일 경우

    user_post = DB.get_user(uid)
    if user_post == None:
        length = 0
    else :
        length = len(user_post)
    
    isFollow = DB.is_following(user,uid) #팔로잉 여부
    
    return render_template("user_detail.html",post_list = user_post, length = length,uid = uid,user=user,isFollow=isFollow)

# 팔로워 글 목록
@app.route("/following/new")
def following_list():
    uid = request.args.get('user', default = 'user', type = str) #user id가져오기
    if "uid" in session: #로그인 된 상태일 경우 
        user = session["uid"]
    else:
        user = "Login" #로그아웃 된 상태일 경우

    follower_post = DB.get_follower(uid)

    if follower_post == None:
        length = 0
    else :
        length = len(follower_post)
    
    return render_template('following_list.html',post_list = follower_post,length = length,user =user)


# 글 목록 보기
@app.route("/list")
def post_list():
    if "uid" in session: #로그인 된 상태일 경우 
        user = session["uid"]
    else:
        user = "Login" #로그아웃 된 상태일 경우

    post_list = DB.post_list()
    if post_list == None :
        length = 0
    else:
        length = len(post_list)

    return render_template('product_list.html',post_list = post_list.items(),length = length,user =user)



@app.route("/post/<string:pid>")
def post(pid):
    post = DB.post_detail(pid)
    return render_template("product_detail.html",post = post)


if __name__ == "__main__":
    app.run(debug=True)
    
# 글 검색
@app.route("/search/new")
def search_list():
    uid = request.args.get('user', default = 'user', type = str) #user id가져오기
    if "uid" in session: #로그인 된 상태일 경우 
        user = session["uid"]
    else:
        user = "Login" #로그아웃 된 상태일 경우

    follower_post = DB.get_follower(uid)

    if follower_post == None:
        length = 0
    else :
        length = len(follower_post)
    
    return render_template('following_list.html',post_list = follower_post,length = length,user =user)