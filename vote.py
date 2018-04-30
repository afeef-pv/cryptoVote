from block import *
"""
Simple blockchain based voting program for understanding how blockchain based implementation works :)
Not so perfect ,cuncurrency issues and not fully wrote ,just did it for this CV

"""
class BlockChain(object):
    def __init__(self):
        self.blocks = []
        #self.blocks[-1].mine()
        self.difficulty = 6

    def addBlock(self,block):
        if block.hash[:self.difficulty] == "0"*self.difficulty and block.index == len(self.blocks):
                self.blocks.append(block)
    
    def getLatestBlock(self):
        return self.blocks[-1]
    def __str__(self): 
        for block in self.blocks:
            print str(block.index) + " : " + str(block.hash) + '\n'
        return ""

class Node(object):
    def __init__(self,bc):
        self.bc = bc
        self.votes = []
        #self.currentBlock = Block(votes = [],index = len(self.bc.blocks),prvs_hash = self.bc.blocks[-1].hash,diff = bc.difficulty)
        self.currentBlock = Block.gensis_block()
        self.miner = Miner(self,self.currentBlock) #Thread for mining
        self.voter = Voter(self)                   #Thread for transactions(Voting)
        self.voter.start()
        self.mine()

    def mine(self): #Mininig
        if self.miner.mineBlock(self.currentBlock):
            self.bc.addBlock(self.currentBlock)
            newBlock = Block(votes = self.votes,index = len(self.bc.blocks),prvs_hash = self.currentBlock.hash,diff = self.bc.difficulty)
            self.currentBlock = newBlock
            self.votes = []
            self.mine()

    def validateVote(self,vote):
        if hashlib.sha256(str(vote.pubkey+vote.vote).encode()).hexdigest() == vote.getHash():
            #self.currentBlock.addVote(vote)
            self.votes.append(vote)
            return True
        else:
            print "Invalid"
            return False

    def getCurrentBlock(self):
        return self.currentBlock

    def updateVotes(self,votes):
            return
    def validateBlock(self,block):
            return
            

class Miner(Thread):
        def __init__(self,node,currentBlock):
                Thread.__init__(self,name = "MinerThread")
                self.cb = currentBlock
                self.node = node
        def run(self):
                self.mineBlock(self.cb)

        def mineBlock(self,cb):
            if cb.mine():
                return True

class Voter(Thread):
        def __init__(self,node):
                Thread.__init__(self,name = "Voter")
                self.node = node

        def vote(self,vote):
                
                self.validateVote(vote)
        def validateVote(self,vote):
                if hashlib.sha256(str(vote.pubkey+vote.vote).encode()).hexdigest() == vote.getHash():
                    self.node.validateVote(vote)
                    return True
                else:
                    print "Invalid"
                    return False
                
        def run(self):
                print "Voter"
                while True:
                    command = input("1.vote\n2.exit\n")
                    if command == 1:
                        vote = raw_input("Enter your vote")
                        vote = vote.split(':')
                        vote = Vote(vote[0],vote[1])
                        self.vote(vote) 
                    elif command == 2:
                        for block in self.node.bc.blocks:
                                print str(block)
                    else:
                        break
            

    

node = Node(BlockChain())


