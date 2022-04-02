import fastapi as _fastapi
import newBlockChain as _blockchain
import requests
import uvicorn
from hashlib import sha256

blockChains = {}
primary_unique_id = "abcdef"
blockchain = _blockchain.Blockchain()
blockChains[primary_unique_id] = blockchain
app = _fastapi.FastAPI()

connectedNodes  = {
    1:'127.0.0.1:8000',
    }

self_node = 1

@app.get(f"/{self_node}"+"/{blockChainUniqueKey}/mine_block/{data}")
def mine_block(blockChainUniqueKey:str, data: str):
    if not blockChains[blockChainUniqueKey].is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    block = blockChains[blockChainUniqueKey].mineBlock(data=data)
    for i in connectedNodes.keys():
        if i != self_node:
            requests.get("http://"+str(connectedNodes[i]+"/"+str(i)+f"/{blockChainUniqueKey}/mine_block/"+data))
    return block


@app.get(f"/{self_node}"+"/{blockChainUniqueKey}/blockchain/")
def get_blockchain(blockChainUniqueKey:str):
    if not blockChains[blockChainUniqueKey].is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    chain = blockChains[blockChainUniqueKey].chain
    return chain


@app.get(f"/{self_node}"+"/{blockChainUniqueKey}/blockchain/last/")
def last_block(blockChainUniqueKey:str):
    if not blockChains[blockChainUniqueKey].is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
        
    return blockChains[blockChainUniqueKey].getPreviousBlock()

@app.post(f"/{self_node}"+"/{blockChainUniqueKey}/viewblock/")
def viewBlockData(blockChainUniqueKey:str, index:int):
    _chain = blockChains[blockChainUniqueKey].chain
    flag = False
    for i in _chain:
        if i["index"] == index:
            flag = True
            return i
    if not flag:
        return {"message":"no block exists on provided index"}

@app.get(f'/{self_node}/createNewBlockChain/')
def createNewBlockChain():
    newBlockChain = _blockchain.Blockchain()
    index = len(blockChains)
    todigest = str(index).encode()
    blockchain_unique_key = sha256(todigest).hexdigest()
    blockChains[blockchain_unique_key] = newBlockChain
    return {"new blockchain index":blockchain_unique_key}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)