# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 15:11:01 2021

@author: SAINATH THOTA
"""

1->Run app.py to start the server

**********Assumptions**********
1->When a user logins again with in the previous session time, the previous session logsout and new session is created
2->It is possible that a user can play any level at any point of time irrespective of the previous level completion i.e levels are independent
3->User account is created firts time when he/she logs in to the system
4->Priority and Login time can be changed in the config file i.e src/config.py
5->Multi Threading is not implemented
6->Priority calcultion is implemete naively...can be optimised using priority queues for each level