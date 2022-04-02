import hashlib
from fastapi import FastAPI
app = FastAPI()
class Block:
    def __init__(self, previousBlockHash, transactionsList):
        self.previousBlockHash = previousBlockHash
        self.transactionList = transactionsList
        self.BlockData = str(self.previousBlockHash)+"--".join(transactionsList)
        self.BlockHash = hashlib.sha256(bytes(self.BlockData, 'utf-8')).hexdigest()
        f = open('AkatsukiBlockChain.txt', 'a')
        f.writelines(self.BlockHash+'\n')

    def getBlockData(self):
        return self.BlockData
    
    def getBlockHash(self):
        return self.BlockHash

BlockChain = []
f = open('AkatsukiBlockChain.txt', 'w')
f.write("-----------Akatsuki Block Chain-------------\n")
f.close()
baseBlock = Block('aaa', [])
BlockChain.append(baseBlock)

def addBlock(transactions):
    newBlock = Block(BlockChain[-1].getBlockHash(), transactions)
    BlockChain.append(newBlock)
    print('New Block Created Successfully!')
    print("block hash: ")
    print(BlockChain[-1].getBlockHash())
    return BlockChain[-1].getBlockHash()
def viewBlockData(blockHash):
    output = {}
    for i in BlockChain:
        if i.getBlockHash() == baseBlock.getBlockHash():
            return {"message":"You have reached the base block!"}
        elif i.getBlockHash() == blockHash:
            datastring = i.getBlockData()
            previousHash = datastring[:65]
            _out = datastring[64:].split("--")
            output["Previous"] = previousHash
            for i in _out:
                x, y = map(str, i.split(':'))
                output[x] = y

    if output == {}:
        return "Invalid Block Hash \n no such block exists in the Akatsuki BlockChain"
    else:
        return output


@app.get('/viewBlockData/{apiKey}/{blockHash}')
async def apiViewBlockData(apiKey:str, blockHash: str):
    if apiKey == "tostoptrainpullchain":
        output = viewBlockData(blockHash)
        return output
    else:
        return {'message':'invalid api key'}

@app.get('/createBlock/{apiKey}/{transactions}')
async def apiCreateBlock(apiKey: str, transactions: str):
    if apiKey == "tostoptrainpullchain":
        _transactions = transactions.split(",")
        output = addBlock(_transactions)
        return output
    else:
        return {'message':'invalid api key'}