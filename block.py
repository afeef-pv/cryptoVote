import hashlib
from threading import Thread,Condition,currentThread
import time,random

class Vote(object):
    def __init__(self,pubkey = 0,vote = ""):
        self.pubkey = pubkey
        self.vote = vote
        self.hash = self.calc_hash(pubkey,vote)

    def calc_hash(self,pk,vt):
        return hashlib.sha256(str(pk)+str(vt).encode()).hexdigest()
    def __str__(self):
        return str(self.pubkey) + ':' +str(self.vote)
    def getPubKey(self):
        return self.pubkey
    def getHash(self):
            return self.hash

class Block(object):
    def __init__(self,index = 0,prvs_hash = "",votes = [],diff = 0):
        self.index = index
        self.prvs_hash = prvs_hash
        self.votes = votes
        self.nonce = 0
        self.hash = self.calc_hash()
        self.condition = Condition()
        self.difficulty = diff
        self.isMinable = True
        self.isMined = False
        

    def calc_hash(self):
        return hashlib.sha256(str(self.index)+str(self.prvs_hash)+str(self.votes).encode() + str(self.nonce)).hexdigest()
        
    def addVote(self,vote):
        self.condition.acquire()
        """while self.isMinable:
                print "Mining"
                self.condition.wait()"""
        print "adding in " + str(self.index)
        self.votes.append(vote)
        self.hash = self.calc_hash()
        """self.condition.notify()
        self.condition.release()
        self.isMinable = True"""
        self.mine()

    def validHash(self):
        if self.hash[:difficulty] == "0"*difficulty:
                return True
        else:
                return False

    def mine(self):
        difficulty = self.difficulty
        print "Fuck Minig"
        self.condition.acquire()
        while not self.isMinable:
                print "not Minig"
                self.condition.wait()
        while self.hash[:difficulty] != "0"*difficulty and self.isMinable == True:
            self.nonce += 1
            self.hash = self.calc_hash()
        self.isMined = True
        self.condition.notify()
        self.condition.release()
        return True

    def pauseMine(self):
        self.isMianble = False
        return True
    def resumeMine(self):
        self.isMianble = True
        return True
    def __str__(self):
            data = "Block " + str(self.index) + " : " + str(self.hash) +" : \n"
            for v in self.votes:
                    data += str(v) + '\n'
            return data

    @classmethod
    def gensis_block(cls):
        return cls()
