
import pyrebase
import json
import uuid

class DBModule:
    def __init__(self):
        with open("./auth/firebaseAuth.json") as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database() #연결
    
    def signin_verification(self,uid): 
        users = self.db.child("users").get().val() #user에 저장된 모든 정보 불러오기
        for i in users: 
            if uid == i : #user에 해당 id가 있다면
                return False
            
        return True

    def signin(self,_id_,pwd,name,email):
        information = { 
            "pwd":pwd,
            "uname":name,
            "email": email
        }
        
        if self.signin_verification(_id_): #id가 중복되지 않으면
            self.db.child("users").child(_id_).set(information) #DB에 저장
            return True
        else : #중복되면 
            return False
    
    def login(self,uid,pwd): 
        users = self.db.child("users").get().val() #user에 저장된 모든 정보 불러오기
        try :
            userinfo = users[uid] #user id가 존재하면
            if userinfo["pwd"] == pwd: #비밀번호 확인
                return True
            else :
                return False
        except: #user id 존재하지 않을 경우
            return False

   

    
    def write_post(self,title,contents,cost,keyword,uid):
        pid = str(uuid.uuid4())[:10] #랜덤 아이디 저장
        infomation = {
            "title" : title,
            "contents" : contents,
            "cost" : cost,
            "keyword":keyword,
            "uid" : uid
        }
        self.db.child("posts").child(pid).set(infomation)

    def post_list(self): #전체 포스트
        post_lists = self.db.child("posts").get().val()
        return post_lists

    def post_detail(self,pid): #포스트 한개 보기
        post = self.db.child("posts").get().val()[pid]
        return post

    def get_user(self,uid): #특정 유저가 쓴 글만 보기
        post_list = []
        users_post = self.db.child("posts").get().val()
        if users_post != None:
             for post in users_post.items():
                if post[1]["uid"] == uid:
                    post_list.append(post)
             return post_list
    

    def user_id(self,uid): #특정 유저가 쓴 글만 보기
        users_post = self.db.child("posts").get().val()
        if users_post != None:
             for post in users_post.items():
                if post[1]["uid"] == uid:
                    True
                else:
                    False

    def search(self):
        pass

    def following(self):
        pass
