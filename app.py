from flask import Flask, render_template, request
from Portfolio import portfolio
import CAPM
from binomial import Binomial

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main.html")

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
    return render_template("name.html",user=port.getName())

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
    return render_template("name.html",user=port.getName())

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
    return render_template("name.html",user=port.getName())

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
    return render_template("name.html",user=port.getName())

@app.route("/get",methods=['GET'])
def get():
    curr = open('curr.txt', 'r')
    name = curr.readline()
    curr.close()
    port = portfolio(name)
    port.read()
    port.write()
    return render_template("get.html",user=port.getName(),name=port.getName(),account=port.getAccount(),value=port.getValue(),result=port.getPortfolio(),diversity=round(port.getDiversity()*100,1))

@app.route('/capmin.html', methods=['GET', 'POST'])
def capmin():
    return render_template("capmin.html")

@app.route('/index.html', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/binomial.html', methods=['GET', 'POST'])
def binomial():
    return render_template("binomial.html")

@app.route('/main.html', methods=['GET', 'POST'])
def tomain():
    return render_template("main.html")

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    return render_template("capmin.html")

@app.route("/generate",methods=['POST','GET'])
def generate():
    dow30 = ["MMM", "AXP", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DWDP", "XOM", "GE", "GS", "HD", "IBM", "INTC",
             "JNJ", "JPM", "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UNH", "UTX", "VZ", "V", "WMT", "DIS"]
    iq100 = ["MMM", "ABT", "A", "ALGN", "AMZN", "AMAT", "AAPL", "BHGE", "BAC", "BAX", "BDX", "AVGO", "CA", "BA",
             "ELY", "CAT", "CBS", "CVX", "C", "CLX", "KO", "CTSH", "CREE", "DE", "DXCM", "DOV", "DWDP", "DXC", "EMN",
             "ETN",
             "EW",  "ESRX", "XOM", "GRMN", "GE", "GM", "HAL", "HRS", "HIG", "HON", "HPQ", "IBM", "ITW",
             "INTC",
             "IP", "JNJ", "JPM", "KMB", "LMT", "MA", "MAT", "MDT", "MET", "MU", "MSFT", "MDLZ", "MSI", "NCR", "NKE",
             "NOC",
             "ORCL", "PFE", "PX", "PG", "PGR", "PRU", "QCOM", "RTN", "ROK", "SLB", "STX", "SEE", "SON",  "SYK",
             "TGT",
             "TEL", "TER", "TXN", "TXT", "BKNG", "UTX", "UNH", "VRX", "VZ", "V", "WRK", "WY", "WHR", "XRX",
             "XLNX"]
    nasdaq100 = ["AAL", "ADBE", "ADI", "ADP", "ADSK", "AAPL", "ALGN", "ALXN", "AMAT", "AMGN", "AMZN", "ATVI",
                 "AVGO", "BHGE", "BIDU", "BIIB", "BMRN", "CA", "CELG", "CERN", "CHKP", "CHTR", "CTAS", "CSCO",
                 "CTXS", "CMCSA", "COST", "CTSH", "DISCA", "DISCK", "DISH", "DLTR", "EA", "EBAY", "ESRX", "EXPE",
                 "FAST",
                 "FB", "FISV", "FOX", "FOXA", "GILD", "GOOG", "GOOGL", "HAS", "HSIC", "HOLX", "ILMN", "INCY", "INTC",
                 "INTU",
                 "ISRG", "IDXX", "JBHT", "KLAC", "KHC", "LBTYA", "LRCX", "MAR", "MAT", "MCHP",
                 "MDLZ", "MU", "MXIM", "MYL", "MSFT", "NCLH", "NFLX", "NVDA", "ORLY", "PAYX", "PCAR", "BKNG",
                 "PYPL", "QCOM", "REGN", "ROST", "STX",  "SIRI", "SWKS", "SBUX", "SYMC", "TSCO", "TSLA",
                 "TXN", "TMUS", "ULTA", "VIAB", "VOD", "VRSK", "VRTX", "WBA", "WDC", "XLNX", "XRAY", "PCAR",
                 "WYNN"]
    snp500=['AAPL', 'ABT', 'ABBV', 'ACN', 'ACE', 'ADBE', 'ADT', 'AAP', 'AES', 'AET', 'AFL', 'AMG', 'A', 'GAS', 'ARE',
          'APD', 'AKAM', 'AA', 'AGN', 'ALXN', 'ALLE', 'ADS', 'ALL', 'ALTR', 'MO', 'AMZN', 'AEE', 'AAL', 'AEP', 'AXP',
          'AIG', 'AMT', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'APC', 'ADI', 'AON', 'APA', 'AIV', 'AMAT', 'ADM', 'AIZ',
          'T', 'ADSK', 'ADP', 'AN', 'AZO', 'AVGO', 'AVB', 'AVY', 'BHI', 'BLL', 'BAC', 'BK', 'BCR', 'BXLT', 'BAX', 'BBT',
          'BDX', 'BBBY', 'BBY', 'BLX', 'HRB', 'BA', 'BWA', 'BXP', 'BSX', 'BMY', 'BRCM', 'CHRW', 'CA',
          'CVC', 'COG', 'CAM', 'CPB', 'COF', 'CAH', 'HSIC', 'KMX', 'CCL', 'CAT', 'CBG', 'CBS', 'CELG', 'CNP', 'CTL',
          'CERN', 'CF', 'SCHW', 'CHK', 'CVX', 'CMG', 'CB', 'CI', 'XEC', 'CINF', 'CTAS', 'CSCO', 'C', 'CTXS', 'CLX',
          'CME', 'CMS', 'COH', 'KO', 'CCE', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CSC', 'CAG', 'COP', 'CNX', 'ED', 'STZ',
          'GLW', 'COST', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DLPH', 'DAL', 'XRAY', 'DVN',
          'DO', 'DTV', 'DFS', 'DISCA', 'DISCK', 'DG', 'DLTR', 'D', 'DOV', 'DOW', 'DPS', 'DTE', 'DD', 'DUK', 'DNB',
          'ETFC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMC', 'EMR', 'ENDP', 'ESV', 'ETR', 'EOG', 'EQT',
          'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ES', 'EXC', 'EXPE', 'EXPD', 'ESRX', 'XOM', 'FFIV', 'FB', 'FAST', 'FDX',
          'FIS', 'FITB', 'FSLR', 'FE', 'FISV', 'FLIR', 'FLS', 'FLR', 'FMC', 'FTI', 'F', 'FOSL', 'BEN', 'FCX', 'FTR',
          'GME', 'GPS', 'GRMN', 'GD', 'GE', 'GGP', 'GIS', 'GM', 'GPC', 'GNW', 'GILD', 'GS', 'GT', 'GOOGL', 'GOOG',
          'GWW', 'HAL', 'HBI', 'HOG', 'HAR', 'HRS', 'HIG', 'HAS', 'HCA', 'HCP', 'HCN', 'HP', 'HES', 'HPQ', 'HD', 'HON',
          'HRL', 'HSP', 'HST', 'HCBK', 'HUM', 'HBAN', 'ITW', 'IR', 'INTC', 'ICE', 'IBM', 'IP', 'IPG', 'IFF', 'INTU',
          'ISRG', 'IVZ', 'IRM', 'JEC', 'JBHT', 'JNJ', 'JCI', 'JOY', 'JPM', 'JNPR', 'KSU', 'K', 'KEY', 'GMCR', 'KMB',
          'KIM', 'KMI', 'KLAC', 'KSS', 'KRFT', 'KR', 'LB', 'LLL', 'LH', 'LRCX', 'LM', 'LEG', 'LEN', 'LVLT', 'LUK',
          'LLY', 'LNC', 'LLTC', 'LMT', 'L', 'LOW', 'LYB', 'MTB', 'MAC', 'M', 'MNK', 'MRO', 'MPC', 'MAR', 'MMC', 'MLM',
          'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK', 'MJN', 'MDT', 'MRK', 'MET', 'KORS', 'MCHP', 'MU', 'MSFT',
          'MHK', 'TAP', 'MDLZ', 'MON', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MUR', 'MYL', 'NDAQ', 'NOV', 'NAVI', 'NTAP',
          'NFLX', 'NWL', 'NFX', 'NEM', 'NWSA', 'NEE', 'NLSN', 'NKE', 'NI', 'NE', 'NBL', 'JWN', 'NSC', 'NTRS', 'NOC',
          'NRG', 'NUE', 'NVDA', 'ORLY', 'OXY', 'OMC', 'OKE', 'ORCL', 'OI', 'PCAR', 'PLL', 'PH', 'PDCO', 'PAYX', 'PNR',
          'PBCT', 'POM', 'PEP', 'PKI', 'PRGO', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PBI', 'PCL', 'PNC', 'RL',
          'PPG', 'PPL', 'PX', 'PCP', 'PCLN', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM', 'PVH', 'QRVO',
          'PWR', 'QCOM', 'DGX', 'RRC', 'RTN', 'O', 'RHT', 'REGN', 'RF', 'RSG', 'RAI', 'RHI', 'ROK', 'COL', 'ROP',
          'ROST', 'RLD', 'R', 'CRM', 'SNDK', 'SCG', 'SLB', 'SNI', 'STX', 'SEE', 'SRE', 'SHW', 'SPG', 'SWKS', 'SLG',
          'SJM', 'SNA', 'SO', 'LUV', 'SWN', 'SE', 'STJ', 'SWK', 'SPLS', 'SBUX', 'HOT', 'STT', 'SRCL', 'SYK', 'STI',
          'SYMC', 'SYY', 'TROW', 'TGT', 'TEL', 'TE', 'TGNA', 'THC', 'TDC', 'TSO', 'TXN', 'TXT', 'HSY', 'TRV', 'TMO',
          'TIF', 'TWX', 'TWC', 'TJX', 'TMK', 'TSS', 'TSCO', 'RIG', 'TRIP', 'FOXA', 'TSN', 'TYC', 'UA', 'UNP', 'UNH',
          'UPS', 'URI', 'UTX', 'UHS', 'UNM', 'URBN', 'VFC', 'VLO', 'VAR', 'VTR', 'VRSN', 'VZ', 'VRTX', 'VIAB', 'V',
          'VNO', 'VMC', 'WMT', 'WBA', 'DIS', 'WM', 'WAT', 'ANTM', 'WFC', 'WDC', 'WU', 'WY', 'WHR', 'WFM', 'WMB', 'WEC',
          'WYN', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XL', 'XYL', 'YHOO', 'YUM', 'ZBH', 'ZION', 'ZTS']
    quandl_key = "KAVVW6RCPX2WWvgJNigd"
    amount = float(request.form['amount'])
    number_of_stocks = int(request.form['number'])
    is_short_sell = len(request.form.getlist('short')) != 0
    exp_port_ret = float(request.form['ret'])/100.0
    if request.form['range'].lower() == "dow30":
        stocks = dow30
    elif request.form['range'].lower() == "iq100":
        stocks = iq100
    elif request.form['range'].lower() == "nasdaq100":
        stocks = nasdaq100
    elif request.form['range'].lower() == "snp500":
        stocks = snp500
    else:
        stocks = request.form['stock'].split(',')
    start = request.form['start']
    end = request.form['end']
    capm = CAPM.main(number_of_stocks, is_short_sell, exp_port_ret, quandl_key, stocks, start, end)
    port = portfolio("getresult")
    result = []
    for i in range(len(capm[0])):
        ask = port.checkYahooAsk(capm[0][i])
        if ask > 0:
            result.append((capm[0][i],int(capm[1][i]*amount/ask)))
    ret = round(capm[2]*100,2)
    return render_template("capmout.html",result = result, ret = ret)

@app.route("/redo",methods=['POST','GET'])
def redo():
    return render_template("capmin.html")

@app.route("/estimate",methods=['POST','GET'])
def estimate():
    K = float(request.form['k'])
    T = float(request.form['t'])
    S0 = float(request.form['s0'])
    sigma = float(request.form['sigma'])
    r = float(request.form['r'])
    q = float(request.form['q'])
    N = int(request.form['n'])
    Option = "P"
    if len(request.form.getlist('option')) != 0:
        Option = "C"
    Exercise = "E"
    if len(request.form.getlist('exercise')) != 0:
        Exercise = "A"
    price = round(Binomial(Option, K, T, S0, sigma, r, q, N, Exercise),2)
    return render_template("options.html",price=price)

@app.route("/reset",methods=['POST','GET'])
def resetBinom():
    return render_template("binomial.html")

if __name__ == "__main__":
    app.run()


