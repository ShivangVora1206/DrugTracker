import datetime as _dt
import hashlib as _hs
import json as _json

class Blockchain:
    def __init__(self):
        self.chain = list()
        baseBlock = self.createBlock(data="genesis block", proof=1, previousHash="0", index=1)
        self.chain.append(baseBlock)

    def getPreviousBlock(self):
        return self.chain[-1]

    def createBlock(self, data:str, proof:int, previousHash:str, index:int):
        block = {
            "index": index,
            "timestamp": str(_dt.datetime.now()),
            "data":data,
            "proof":proof,
            "previousHash": previousHash
        }
        return block

    def toDigest(self, newProof:int, previousProof:int, index:int, data:str):
        todigest = str(newProof ** 7 + previousProof * 13 + index) + data
        return todigest.encode()
    
    def proofOfWork(self, previousProof:int, index:int, data:str):
        newProof = 1
        flag = False

        while not flag:
            to_digest = self.toDigest(newProof, previousProof, index, data)
            hash_operation = _hs.sha256(to_digest).hexdigest()
            if hash_operation[:3] == "000":
                flag = True
            else:
                newProof += 1
        
        return newProof

    def hash(self, block:dict):
        encoded_block = _json.dumps(block, sort_keys=True).encode()
        return _hs.sha256(encoded_block).hexdigest()

    def mineBlock(self, data:str):
        previousBlock = self.getPreviousBlock()
        previousProof = previousBlock["proof"]
        index = len(self.chain)+1
        proof = self.proofOfWork(previousProof, index, data)
        previousHash = self.hash(block=previousBlock)
        block = self.createBlock(data, proof, previousHash, index)
        self.chain.append(block)
        return block
    
    def is_chain_valid(self) -> bool:
            previous_block = self.chain[0]
            block_index = 1
            while block_index < len(self.chain):
                block = self.chain[block_index]
                if block["previousHash"] != self.hash(previous_block):
                    return False
                previous_proof = previous_block["proof"]
                index, data, proof = block["index"], block["data"], block["proof"]
                hash_operation = _hs.sha256(
                    self.toDigest(
                        newProof=proof,
                        previousProof=previous_proof,
                        index=index,
                        data=data,
                    )
                ).hexdigest()
                if hash_operation[:3] != "000":
                    return False
                previous_block = block
                block_index += 1

            return True


