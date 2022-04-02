from flask import Flask, render_template, request, url_for,redirect
import requests
import hashlib
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
user="root",
password="",
database="testDB1",
)

mycursor =mydb.cursor(buffered=True)

app = Flask(__name__)

@app.route('/register')
def register():
    return render_template("page-register.html")


@app.route("/registerParticipant", methods=["POST", "GET"])
def registerPart():
    name = request.form['name']
    email = request.form['email']
    pwd = request.form['pwd']
    password = hashlib.md5(str(pwd).encode('utf-8')).digest()
    for i in range(200):
        try:
            query = "INSERT INTO credentials VALUES(%s, %s, %s, %s)"
            mycursor.execute(query, (i,name, email, str(password)))
            mydb.commit()
            break
        except:
            print(i)
    return redirect(url_for("index"))

@app.route("/login", methods=['POST','GET'])
def index():
    if request.method == "POST":
        _name = ''
        _id = str(request.form['id']).encode('utf-8')
        pwd = request.form['password']
        _password = hashlib.md5(str(pwd).encode('utf-8')).digest()
        print(_password)
        query = f"select name from credentials where email=%s and pwd=%s"
        # try:
        mycursor.execute(query, (_id, str(_password)))
        mydb.commit()
        results = mycursor.fetchall()
        print(results)
        _name = results[0][0]
        # except:
        #     print("invalid creds")
        return redirect(url_for("homePage"))
    else:
        return render_template("index.html")

@app.route('/homePage')
def homePage():
    return render_template("form-basic.html")

@app.route('/homePage/viewBlockChain', methods=['POST', 'GET'])
def viewBlockChain():
    if request.method == "POST":
        uniqueKey = request.form['uniqueKey']
        print(uniqueKey)
        self_node = 1
        blockChain = requests.get(f"http://127.0.0.1:8000/{self_node}"+f"/{uniqueKey}/blockchain/").json()
        return render_template('viewBlockChain.html', blockchain=blockChain)
    else:
        return render_template('index.html')

@app.route('/homePage/viewBlock', methods=['POST', 'GET'])
def viewBlock():
    if request.method == "POST":
        uniqueKey = request.form['uniqueKey']
        index = request.form['index']
        self_node = 1
        block = requests.post(f"http://127.0.0.1:8000/{self_node}/{uniqueKey}/viewblock/?index={index}").json()
        data = block['data']
        return render_template('viewBlock.html', block=block, data=data)
    else:
        return render_template('index.html')

@app.route('/homePage/viewLastBlock', methods=['POST', 'GET'])
def viewLastBlock():
    if request.method == "POST":
        uniqueKey = request.form['uniqueKey']
        print(uniqueKey)
        self_node = 1
        _lastBlock = requests.get(f"http://127.0.0.1:8000/{self_node}/{uniqueKey}/blockchain/last").json()
        data = _lastBlock['data']
        return render_template('viewLastBlock.html', lastBlock=_lastBlock, data=data)
    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8091)
