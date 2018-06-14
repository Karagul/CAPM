from flask import Flask, render_template, request,json
from Portfolio import portfolio

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/name",methods=['POST'])
def name():
    name = request.form['name']
    port = portfolio(name)
    port.read()
    port.write()
    curr = open('curr.txt', 'w')
    curr.write(name)
    curr.close()
    return render_template("name.html",user=port.getName())

@app.route("/topup",methods=['POST'])
def topup():
    amount = request.form['topup']
    curr = open('curr.txt', 'r')
    name = curr.readline()
    curr.close()
    port = portfolio(name)
    port.read()
    port.topUp(amount)
    port.write()
    return render_template("get.html")

@app.route("/withdraw",methods=['POST'])
def withdraw():
    amount = request.form['withdraw']
    curr = open('curr.txt', 'r')
    name = curr.readline()
    curr.close()
    port = portfolio(name)
    port.read()
    port.withdraw(amount)
    port.write()
    return render_template("get.html")

@app.route("/buy",methods=['POST'])
def buy():
    stock = request.form['buystock']
    amount = request.form['buyamount']
    curr = open('curr.txt', 'r')
    name = curr.readline()
    curr.close()
    port = portfolio(name)
    port.read()
    port.buy(stock,amount)
    port.write()
    return render_template("get.html")

@app.route("/sell",methods=['POST'])
def sell():
    stock = request.form['sellstock']
    amount = request.form['sellamount']
    curr = open('curr.txt', 'r')
    name = curr.readline()
    curr.close()
    port = portfolio(name)
    port.read()
    port.sell(stock,amount)
    port.write()
    return render_template("get.html")

@app.route("/get",methods=['GET'])
def get():
    curr = open('curr.txt', 'r')
    name = curr.readline()
    curr.close()
    port = portfolio(name)
    port.read()
    port.write()
    return render_template("get.html",user=port.getName(),name=port.getName(),account=port.getAccount(),value=port.getValue(),result=port.getPortfolio())

if __name__ == "__main__":
    app.run()


