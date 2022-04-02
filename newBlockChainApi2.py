import fastapi as _fastapi
import newBlockChain as _blockchain
import uvicorn
blockchain = _blockchain.Blockchain()
app = _fastapi.FastAPI()


self_node = 2

@app.post(f"/{self_node}/mine_block/")
def mine_block(data: str):
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    block = blockchain.mineBlock(data=data)
    return block


@app.get(f"/{self_node}/blockchain/")
def get_blockchain():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    chain = blockchain.chain
    return chain


@app.get(f"/{self_node}/blockchain/last/")
def previous_block():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    return blockchain.getPreviousBlock()

@app.post(f"/{self_node}/viewblock/")
def viewBlockData(index:int):
    _chain = blockchain.chain
    flag = False
    for i in _chain:
        if i["index"] == index:
            flag = True
            return i
    if not flag:
        return {"message":"no block exists on provided index"}
        
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)