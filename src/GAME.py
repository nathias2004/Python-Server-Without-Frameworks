# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 13:58:55 2021

@author: SAINATH THOTA
"""
import uuid
from datetime import datetime,timedelta   
from src.config import CONFIG


  
class game():
    def __init__(self):
        self.users = {}
        self.sessionKeys = {}
        self.config = CONFIG
    def getscores(self, level_id):
        scores = []
        for user in self.users.keys():
            if(level_id in self.users[user].keys()):
                scores.append([user,self.users[user][level_id]])
        
        return scores
    
    def login(self,user_id):
        #generate unique session key
        #add the end time to the session key
        #assumption is user will not do multiple logins with in the time span if done old sessionkey gets dectivated and new one gets generated
        id = str(uuid.uuid1())
        print(id,user_id)
        if user_id not in self.users.keys():
             self.users[user_id] = {}
        self.users[user_id]["session_key"] = id
        self.sessionKeys[id] = user_id
        now = datetime.now()
        now_plus_10 = now + timedelta(minutes = self.config["logintime"])
        self.users[user_id]["end_time"] = now_plus_10
        return id
    
    
    def post_score(self,score,level_id,session_key):
        print(session_key)
        if session_key not in self.sessionKeys.keys():
            return {"error": "Session Key invalid"}
        user_id = self.sessionKeys[session_key]
        now = datetime.now()
        if(now<self.users[user_id]["end_time"]):
            #success
            print("Session Key Active\n")
            if(level_id in self.users[user_id].keys()):
                #level_id present
                if(score <= self.users[user_id][level_id]):
                    #no update
                    print(score,self.users[user_id][level_id])
                    print("Update not required\n")
                    return {"status": "Update Not Required"}
                else:
                    scores = self.getscores(level_id)
                    if len(scores) == 0:
                        self.users[user_id][level_id] = score
                        return {"status": "Score Updated"}
                    scores = sorted(scores,reverse=True, key = lambda x: x[1])                        
                    if((len(scores)>=self.config["TopCount"] and score>=scores[self.config["TopCount"]-1][1]) or len(scores)<self.config["TopCount"]):
                        #update
                        self.users[user_id][level_id] = score
                        return {"status": "Score Updated"}
                    print("yes")
                    return {"status": "Update Not Required"}
                    
            else:
                scores = self.getscores(level_id)
                if len(scores) == 0:
                        self.users[user_id][level_id] = score
                        return {"status": "Score Updated"}              
                scores = sorted(scores,reverse=True, key = lambda x: x[1])
                if((len(scores)>=self.config["TopCount"] and score>=scores[self.config["TopCount"]-1][1]) or len(scores)<self.config["TopCount"]):
                    self.users[user_id][level_id] = score
                    return {"status": "Score Updated"}
                return {"status": "Update Not Required"}
            
                
        return {"error": "Session Key not active"}
    
    
    
    def get_high_score(self,level_id):
        scores = self.getscores(level_id)
        if len(scores) == 0:
            return []
        scores = sorted(scores,reverse=True, key = lambda x: x[1])
        if(len(scores)>self.config["TopCount"]):
            scores = scores[0:self.config["TopCount"]-1]
        for i in range(0,len(scores)-1):
            if((scores[i][1] == scores[i+1][1]) and scores[i][0]>scores[i+1][0]):
                temp = scores[i][0]
                scores[i][0] = scores[i+1][0]
                scores[i+1][0] = temp
        New_Scores = []
        for user,score in scores:
            dic = {}
            dic["user"] = user
            dic["score"] = score
            New_Scores.append(dic)
        return New_Scores
            
        
    
    
        
        
        
    
            
        