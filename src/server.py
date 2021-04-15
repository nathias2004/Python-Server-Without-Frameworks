# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 13:54:26 2021

@author: SAINATH THOTA
"""

from http.server import BaseHTTPRequestHandler
import json
import cgi
from urllib.parse import urlparse, parse_qsl
from src.GAME import game

obj = game()

def User_login(UserId):
    print(UserId)
    result = obj.login(UserId)
    return json.dumps({"USER": result})

def Find_High_Score(LevelId):
    print(LevelId)
    result = obj.get_high_score(LevelId)
    return json.dumps(result)

def Post_Score(score,LevelId,sessionkey):
    print(score,LevelId,sessionkey)
    result = obj.post_score(int(score),LevelId,sessionkey)
    return json.dumps(result)

class Server(BaseHTTPRequestHandler):
    def _set_headers(self,status):
        self.send_response(status)
        if(status == 200):           
            self.send_header('Content-type', 'application/json')
        self.end_headers()
        return
        
        
    def do_HEAD(self):
        return

    def do_GET(self):
        print(self.path)
        self.respond("GET")
        return

    def do_POST(self):
        print(self.path)
        self.respond("POST")
        return
        
    def handle_http(self,Request_Type):
        if(Request_Type == "GET"):            
            key = self.path.split("/")
            print(key)
            if(len(key) == 3 and key[-2].isalnum() and key[-1] == "login"):
                json_result = User_login(key[-2])
            elif(len(key) == 3 and key[-2].isnumeric() and int(key[-2])>0 and key[-1] == "highscorelist"):
                json_result = Find_High_Score(key[-2])
            else:
                self._set_headers(404)
                return
            self._set_headers(200)
            return bytes(json_result, "UTF-8")
        elif(Request_Type == "POST"):
            key = self.path.split("/")
            print(key)
            if(len(key) == 3 and key[-2].isnumeric() and int(key[-2])>0 and key[-1].count("?") == 1 and key[-1].split("?")[0] == "score"):
                LevelId = key[1]            
                params = dict(parse_qsl(urlparse(self.path).query))
                print(params)
                if len(params) == 1 and "sessionkey" in params.keys():
                    sessionkey = params["sessionkey"]
                    ctype, pdict = cgi.parse_header(self.headers.get('Content-type'))
                    # refuse to receive non-json content
                    if ctype != 'application/json':
                        self._set_headers(400)
                        return
                
                    # read the message and convert it into a python dictionary
                    length = int(self.headers.get('Content-Length'))
                    message = json.loads(self.rfile.read(length))
                    if("score" in message.keys()):
                        score = message["score"]            
                        json_result = Post_Score(score, LevelId, sessionkey)
                        # send the message back
                        self._set_headers(200)
                        return bytes(json_result, "UTF-8")
            self._set_headers(404)
            return
            

    def respond(self,Request_Type):
        content = self.handle_http(Request_Type)
        self.wfile.write(content)
        return