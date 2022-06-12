
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
        if users :
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
    
    def is_following(self,uid,fid):

        if uid == fid :
            return True #본인은 본인을 팔로우 못해
        followed = self.db.child("users").child(uid).child("followed").get().val()
        if followed:
            for key in followed:
                if key == fid: #이미 팔로우 됨
                    return True
        else:
            print("팔로우 하는 사람이 없음")
        return False #팔로우 안된 사람이면
        

    def follow(self,uid,fid):
        if self.is_following(uid,fid):
            print("이미 팔로우하고 있습니다")
            return True
        else:
            followed_ref = self.db.child("users").child(uid).child("followed") #follow 하는 사람 추가
            information = { 
                fid :fid
            }     
            followed_ref.update(information)

            follower_ref = self.db.child("users").child(fid).child("follower") #follow 당한 사람에게는 follower 추가
            information = { 
                uid :uid
            }     
            follower_ref.update(information)
            return True #팔로우 함

    def unfollow(self,uid,fid): 

        followed_ref = self.db.child("users").child(uid).child("followed") #follow 하는 사람 추가 
        followed_ref.child(fid).remove()

        follower_ref = self.db.child("users").child(fid).child("follower") #follow 당한 사람에게는 follower 추가  
        follower_ref.child(uid).remove()
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

    def delete_post(self,pid):
        users_post = self.db.child("posts").get().val()
        if users_post != None:
             for post in users_post.items():
                print(post[0])
                if post[0] == pid:
                    print(pid,'삭제함')
                    self.db.child("posts").child(pid).remove()
        
    
    def post_list(self): #전체 포스트
        post_lists = self.db.child("posts").get().val()
        return post_lists

    def post_detail(self,pid): #포스트 한개 보기
        post = self.db.child("posts").get().val()[pid]
        return post

    def get_user(self,uid): #유저의 마이페이지
        post_list = []
        users_post = self.db.child("posts").get().val()
        if users_post != None:
             for post in users_post.items():
                if post[1]["uid"] == uid:
                    post_list.append(post)
             return post_list

    def get_follower(self,uid): #유저의 마이페이지
        follower_list = []
        follower = self.db.child("users").child(uid).child("followed").get().val()
        if follower != None:
             for f in follower.items():
                print( f[1])
                follower_list.append(f[1])
        
        post_list = []
        for f in follower_list:
            post_list.append(self.get_user(f))
        return post_list
        
    def edit_post(self,pid,title,contents,cost,keyword,uid):
        infomation = {
            "title" : title,
            "contents" : contents,
            "cost" : cost,
            "keyword":keyword,
            "uid" : uid
        }
        self.db.child("posts").child(pid).set(infomation)

    def search(self):
        pass


   