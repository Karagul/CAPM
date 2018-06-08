import urllib.request

#Portfolio Class Take Data From Yahoo
class portfolio:
    def __init__(self,name_):
        self.name = name_ #name of the account
        self.stock = [] #name of each stock in account, format: Apple As "AAPL"
        self.amount = [] #amount of each stock in account
        self.value = 0 #value of the total stock at price
        self.account = 0 #amount of money in account

    #Public:

    #buy stocks
    def buy(self,stock_,amount_):
        if stock_ in self.stock:
            idx = self.stock.index(stock_)
        else:
            self.stock.append(stock_)
            self.amount.append(amount_)
        self.account -= self.checkYahooAsk(stock_) * amount_
        if self.account < 0:
            print("Warning, top up your account, current amount =" + str(self.account))

    #sell stocks
    def sell(self,stock_,amount_):
        if stock_ in self.stock:
            idx = self.stock.index(stock_)
            self.amount[idx] -= amount_
            if self.amount[idx] < 0:
                print("Warning, shorting selling, current amount = " + str(self.amount[idx]))
            self.account += self.checkYahooBid(stock_) * amount_
        else:
            print("Error Stock Not Found")

    #top up the money in the account
    def topUp(self,amount_):
        self.account += amount_

    #withdraw money from the account
    def withdraw(self,amount_):
        self.account -= amount_

    #getter for value
    def getValue(self):
        self.value = 0
        for i in range(len(self.stock)):
            self.value += self.checkYahooPrice(self.stock[i]) * self.amount[i]
        return self.value

    #getter for account
    def getAccount(self):
        return self.account

    #getter for [(stock,amount)]
    def getPortfolio(self):
        return [(self.stock[i],self.amount[i]) for i in range(len(self.stock))]

    #Private:

    #return stock price from yahoo
    def checkYahooPrice(self,stock_):
        link = "https://finance.yahoo.com/quote/" + stock_
        #link = "http://finance.yahoo.com/q/ks?s=" + stock_ + "+Key+Statistics"
        resp = urllib.request.urlopen(link).read()
        keyword = '<span class="Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)" data-reactid="21">'
        idxstart = str(resp).find(keyword)
        idxend = str(resp).find("<",idxstart+len(keyword))
        return float(str(resp)[idxstart+len(keyword):idxend].replace(',' , ''))

    # return bid price from yahoo
    def checkYahooBid(self,stock_):
        link = "https://finance.yahoo.com/quote/" + stock_
        #link = "http://finance.yahoo.com/q/ks?s=" + stock_ + "+Key+Statistics"
        resp = urllib.request.urlopen(link).read()
        keyword = '<span class="Trsdu(0.3s) " data-reactid="25">'
        idxstart = str(resp).find(keyword)
        idxend = str(resp).find(" ", idxstart + len(keyword))
        return float(str(resp)[idxstart+len(keyword):idxend].replace(',' , ''))

    # return ask price from yahoo
    def checkYahooAsk(self,stock_):
        link = "https://finance.yahoo.com/quote/" + stock_
        #link = "http://finance.yahoo.com/q/ks?s=" + stock_ + "+Key+Statistics"
        resp = urllib.request.urlopen(link).read()
        keyword = '<span class="Trsdu(0.3s) " data-reactid="30">'
        idxstart = str(resp).find(keyword)
        idxend = str(resp).find(" ",idxstart+len(keyword))
        return float(str(resp)[idxstart+len(keyword):idxend].replace(',' , ''))
