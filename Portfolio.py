import urllib.request
from html.parser import HTMLParser

#Portfolio Class Take Data From Yahoo
class portfolio:
    def __init__(self,name_):
        self.name = name_ #name of the account
        self.stock = [] #name of each stock in account, format: Apple As "AAPL"
        self.amount = [] #amount of each stock in account
        self.value = 0 #value of the total stock at price
        self.account = 0 #amount of money in account

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

    #Change whole portfolio
    def change(self,name_,stock_,amount_,value_,account_):
        self.name = name_
        self.stock = stock_
        self.amount = amount_
        self.value = value_
        self.account = account_

    #return stock price from yahoo
    def checkYahooPrice(self,stock_):
        link = "https://finance.yahoo.com/quote/" + stock_
        resp = urllib.request.urlopen(link).read()
        parser = MyHTMLParser()
        parser.links = []
        parser.feed(str(resp))
        return parser.links[0]

    # return bid price from yahoo
    def checkYahooBid(self,stock_):
        link = "https://finance.yahoo.com/quote/" + stock_
        resp = urllib.request.urlopen(link).read()
        parser = MyHTMLParser()
        parser.links = []
        parser.feed(str(resp))
        return parser.links[3]

    # return ask price from yahoo
    def checkYahooAsk(self,stock_):
        link = "https://finance.yahoo.com/quote/" + stock_
        resp = urllib.request.urlopen(link).read()
        parser = MyHTMLParser()
        parser.links = []
        parser.feed(str(resp))
        return parser.links[4]

    #read from log
    def read(self):
        exist = False
        log = open('log.txt', 'r')
        lines = log.readlines()

        for i in range(len(lines)):
            if lines[i] == "---" + '\n':
                name_ = lines[i + 1]
                stock_ = lines[i + 2]
                amount_ = lines[i + 3]
                account_ = lines[i + 4]
                if self.name + '\n' == name_:
                    exist = True
                    self.stock = []
                    self.amount = []
                    self.account = float(account_[0:len(account_)-2])
                    i = 0
                    while i < len(stock_):
                        if stock_[i] == "," and i + 1 < len(stock_) and stock_[i + 1] != "\n":
                            j = i + 1
                            while stock_[j] != ",":
                                j += 1
                            self.stock.append(stock_[i+1:j])
                            i = j
                        else:
                            i += 1
                    i = 0
                    while i < len(amount_):
                        if amount_[i] == "," and i + 1 < len(amount_) and amount_[i + 1] != "\n":
                            j = i + 1
                            while amount_[j] != ",":
                                j += 1
                            try:
                                self.amount.append(float(amount_[i+1:j]))
                            except:
                                print("Stock Empty")
                            i = j
                        else:
                            i += 1
        if not exist:
            print("Error, can't read " + self.name + ".")
        log.close()

    #write to log
    def write(self):
        name_ = self.name
        account_ = str(self.account)
        stock_ = ',' + ','.join(map(str, self.stock)) + ','
        amount_ = ',' + ','.join(map(str, self.amount)) + ','
        log = open('log.txt', 'r')
        lines = log.readlines()
        log.close()

        log = open('log.txt','w')
        i = 0
        while i < len(lines):
            if lines[i] == "---" + "\n" and lines[i + 1] == name_ + "\n":
                i += 4
            else:
                log.write(lines[i])
            i += 1
        log.close()

        log = open('log.txt','a')
        log.write('---'+'\n')
        log.write(name_+'\n')
        log.write(stock_+'\n')
        log.write(amount_+'\n')
        log.write(account_ + '\n')
        log.close()



# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        return

    def handle_endtag(self, tag):
        return

    def handle_data(self, data):
        string = data.replace(',',"")
        if " x " in string:
            idx = 0
            while idx < len(string) and string[idx] != " ":
                idx += 1
            string = string[:idx]
        try:
            ret = float(string)
            self.links.append(ret)
        except:
            return

