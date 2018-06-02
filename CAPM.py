import numpy as np
from scipy.optimize import minimize
import quandl
from mystic.penalty import quadratic_inequality
from mystic.solvers import diffev2
from mystic.monitors import VerboseMonitor
from mystic.symbolic import generate_constraint, generate_solvers, solve
from mystic.symbolic import generate_penalty, generate_conditions
from gekko import GEKKO
import pandas_datareader as pdr
import pandas as pd

#input
number_of_stocks = 2
is_short_sell = False
exp_port_ret = 0
quandl_key = "KAVVW6RCPX2WWvgJNigd"

def main():
    list_of_stocks_data = []
    list_of_stocks_name = []

    snp500 = ['AAPL', 'ABT', 'ABBV', 'ACN', 'ACE', 'ADBE', 'ADT', 'AAP', 'AES', 'AET', 'AFL','AMG', 'A', 'GAS', 'ARE', 'APD', 'AKAM', 'AA', 'AGN', 'ALXN', 'ALLE', 'ADS', 'ALL', 'ALTR', 'MO', 'AMZN', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'APC', 'ADI', 'AON', 'APA', 'AIV', 'AMAT', 'ADM', 'AIZ', 'T', 'ADSK', 'ADP', 'AN', 'AZO', 'AVGO', 'AVB', 'AVY', 'BHI', 'BLL', 'BAC', 'BK', 'BCR', 'BXLT', 'BAX', 'BBT', 'BDX', 'BBBY', 'BRK-B', 'BBY', 'BLX', 'HRB', 'BA', 'BWA', 'BXP', 'BSX', 'BMY', 'BRCM', 'BF-B', 'CHRW', 'CA', 'CVC', 'COG', 'CAM', 'CPB', 'COF', 'CAH', 'HSIC', 'KMX', 'CCL', 'CAT', 'CBG', 'CBS', 'CELG', 'CNP', 'CTL', 'CERN', 'CF', 'SCHW', 'CHK', 'CVX', 'CMG', 'CB', 'CI', 'XEC', 'CINF', 'CTAS', 'CSCO', 'C', 'CTXS', 'CLX', 'CME', 'CMS', 'COH', 'KO', 'CCE', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CSC', 'CAG', 'COP', 'CNX', 'ED', 'STZ', 'GLW', 'COST', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DLPH', 'DAL', 'XRAY', 'DVN', 'DO', 'DTV', 'DFS', 'DISCA', 'DISCK', 'DG', 'DLTR', 'D', 'DOV', 'DOW', 'DPS', 'DTE', 'DD', 'DUK', 'DNB', 'ETFC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMC', 'EMR', 'ENDP', 'ESV', 'ETR', 'EOG', 'EQT', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ES', 'EXC', 'EXPE', 'EXPD', 'ESRX', 'XOM', 'FFIV', 'FB', 'FAST', 'FDX', 'FIS', 'FITB', 'FSLR', 'FE', 'FISV', 'FLIR', 'FLS', 'FLR', 'FMC', 'FTI', 'F', 'FOSL', 'BEN', 'FCX', 'FTR', 'GME', 'GPS', 'GRMN', 'GD', 'GE', 'GGP', 'GIS', 'GM', 'GPC', 'GNW', 'GILD', 'GS', 'GT', 'GOOGL', 'GOOG', 'GWW', 'HAL', 'HBI', 'HOG', 'HAR', 'HRS', 'HIG', 'HAS', 'HCA', 'HCP', 'HCN', 'HP', 'HES', 'HPQ', 'HD', 'HON', 'HRL', 'HSP', 'HST', 'HCBK', 'HUM', 'HBAN', 'ITW', 'IR', 'INTC', 'ICE', 'IBM', 'IP', 'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IRM', 'JEC', 'JBHT', 'JNJ', 'JCI', 'JOY', 'JPM', 'JNPR', 'KSU', 'K', 'KEY', 'GMCR', 'KMB', 'KIM', 'KMI', 'KLAC', 'KSS', 'KRFT', 'KR', 'LB', 'LLL', 'LH', 'LRCX', 'LM', 'LEG', 'LEN', 'LVLT', 'LUK', 'LLY', 'LNC', 'LLTC', 'LMT', 'L', 'LOW', 'LYB', 'MTB', 'MAC', 'M', 'MNK', 'MRO', 'MPC', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK', 'MJN', 'MMV', 'MDT', 'MRK', 'MET', 'KORS', 'MCHP', 'MU', 'MSFT', 'MHK', 'TAP', 'MDLZ', 'MON', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MUR', 'MYL', 'NDAQ', 'NOV', 'NAVI', 'NTAP', 'NFLX', 'NWL', 'NFX', 'NEM', 'NWSA', 'NEE', 'NLSN', 'NKE', 'NI', 'NE', 'NBL', 'JWN', 'NSC', 'NTRS', 'NOC', 'NRG', 'NUE', 'NVDA', 'ORLY', 'OXY', 'OMC', 'OKE', 'ORCL', 'OI', 'PCAR', 'PLL', 'PH', 'PDCO', 'PAYX', 'PNR', 'PBCT', 'POM', 'PEP', 'PKI', 'PRGO', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PBI', 'PCL', 'PNC', 'RL', 'PPG', 'PPL', 'PX', 'PCP', 'PCLN', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM', 'PVH', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RRC', 'RTN', 'O', 'RHT', 'REGN', 'RF', 'RSG', 'RAI', 'RHI', 'ROK', 'COL', 'ROP', 'ROST', 'RLD', 'R', 'CRM', 'SNDK', 'SCG', 'SLB', 'SNI', 'STX', 'SEE', 'SRE', 'SHW', 'SPG', 'SWKS', 'SLG', 'SJM', 'SNA', 'SO', 'LUV', 'SWN', 'SE', 'STJ', 'SWK', 'SPLS', 'SBUX', 'HOT', 'STT', 'SRCL', 'SYK', 'STI', 'SYMC', 'SYY', 'TROW', 'TGT', 'TEL', 'TE', 'TGNA', 'THC', 'TDC', 'TSO', 'TXN', 'TXT', 'HSY', 'TRV', 'TMO', 'TIF', 'TWX', 'TWC', 'TJX', 'TMK', 'TSS', 'TSCO', 'RIG', 'TRIP', 'FOXA', 'TSN', 'TYC', 'UA', 'UNP', 'UNH', 'UPS', 'URI', 'UTX', 'UHS', 'UNM', 'URBN', 'VFC', 'VLO', 'VAR', 'VTR', 'VRSN', 'VZ', 'VRTX', 'VIAB', 'V', 'VNO', 'VMC', 'WMT', 'WBA', 'DIS', 'WM', 'WAT', 'ANTM', 'WFC', 'WDC', 'WU', 'WY', 'WHR', 'WFM', 'WMB', 'WEC', 'WYN', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XL', 'XYL', 'YHOO', 'YUM', 'ZBH', 'ZION', 'ZTS']
    testsmall = ['AAPL', 'AMZN','BAC','AMD','GE','MU','INTC','CSCO','FB','CVS']
    testlarge = ['AAPL', 'AMZN','BAC','AMD','GE','MU','INTC','CSCO','FB','CVS','MMM','T','ADSK','KO','DFS','DLTR','EBAY','EA','EXPE','HLT','IBM','JPM','KSS','MAR','MCD','MSFT','NDAQ','NKE','NVDA','PYPL','LUV','UNP','V','WFC','VZ']

    #read adj close data from quandl in time span of 3 years ago to today
    quandl.ApiConfig.api_key = quandl_key
    for i in testlarge:
        #stock = pdr.get_data_quandl(symbols=i,start='2015-01-01',end= '2017-12-31')
        #adj_close = stock['AdjClose'].as_matrix()
        stock = quandl.get("WIKI/" + i + '.11', start_date='2015-01-02', end_date='2017-12-31', returns='numpy')
        adj_close = [i[1] for i in stock]
        list_of_stocks_name.append(i)
        list_of_stocks_data.append(adj_close)

    #Adjust initalial data to make sure all timeseries contain the same amout of data for covariance calculation
    length = [len(i) for i in list_of_stocks_data]
    min_length = min(length)
    list_of_stocks_data_truncated = [[j[i] for i in range(min_length)] for j in list_of_stocks_data]

    return raw_data(list_of_stocks_data_truncated, list_of_stocks_name,number_of_stocks,exp_port_ret,is_short_sell)

def raw_data(list_of_stocks_data, list_of_stocks_name,number_of_stocks,exp_port_ret,is_short_sell):
    #process data by calculate simple return's mean, standard deviation and covariance matrix
    list_of_stocks_return = [[(j[i+1]-j[i])/j[i] for i in range(1,len(j)-1)] for j in list_of_stocks_data]
    r_vect = [np.mean(i) for i in list_of_stocks_return]
    s_vect = [np.std(i) for i in list_of_stocks_return]
    cov_matrix = np.zeros((len(r_vect),len(r_vect)))
    for i in range(len(r_vect)):
        for j in range(len(r_vect)):
            cov_matrix[i][j] = np.cov(list_of_stocks_return[i],list_of_stocks_return[j])[0][1]
    set_of_stocks = list_of_stocks_name
    return muti_min_var_port(r_vect,s_vect,cov_matrix,number_of_stocks,exp_port_ret,is_short_sell,set_of_stocks)

def muti_min_var_port(r_vect, s_vect, cov_matrix, number_of_stocks, exp_port_ret, is_short_sell, set_of_stocks):
    # find relative optimal solution on high return-low risk
    def find_optimal():
        sols = []
        rets = []
        for w in range(0, 101, 10):
            (sol, ret, subset_of_stocks) = find_port(w / 100.0, r_vect, s_vect, number_of_stocks, cov_matrix,
                                                     exp_port_ret, is_short_sell, set_of_stocks)
            sols.append(sol)
            rets.append(ret)
        print(sols)
        return (subset_of_stocks, sols[np.argmax(rets)])

    # heuristic of selecting high return-low risk asset by weight
    def find_port(weight_risk, r_vect, s_vect, number_of_stocks, cov_matrix, exp_port_ret, is_short_sell,
                  set_of_stocks):
        weight_return = 1 - weight_risk

        set_of_stocks_idx = [i for i, j in enumerate(set_of_stocks)]
        grand_list = [(r_vect[i], s_vect[i], set_of_stocks[i], set_of_stocks_idx[i]) for i in
                      range(number_of_stocks)]
        grand_list.sort(key=lambda tup: tup[0] * weight_return - tup[1] * weight_risk, reverse=True)

        sub_r_vect = [grand_list[i][0] for i in range(number_of_stocks)]
        subset_of_stocks = [grand_list[i][2] for i in range(number_of_stocks)]
        sub_cov_matrix = np.zeros((number_of_stocks, number_of_stocks))
        for i in range(number_of_stocks):
            for j in range(number_of_stocks):
                sub_cov_matrix[i][j] = cov_matrix[grand_list[i][3]][grand_list[j][3]]

        sol = min_var_port(number_of_stocks, is_short_sell, exp_port_ret, sub_cov_matrix, sub_r_vect)
        ret = sum(sub_r_vect[i] * sol[i] for i in range(number_of_stocks))

        return (sol, ret, subset_of_stocks)

    return find_optimal()

'''
# solving NLP for CAPM model under mystic
def min_var_port(number_of_stocks, is_short_sell, exp_port_ret, cov_matrix, r_vect):
    # objective function
    def objective(w):
        ret = 0
        for i in range(number_of_stocks):
            for j in range(number_of_stocks):
                ret += w[i] * w[j] * cov_matrix[i][j]
        return ret

    def xs(len=number_of_stocks):
        return [1. / number_of_stocks] * len

    def ys(len=number_of_stocks):
        return objective(xs(len))

    # sum of w = 1 constraint
    def equations(len = number_of_stocks):
        eqn = "\nsum(["
        for i in range(len):
            eqn += 'x%s**2, ' % str(i)
        return eqn[:-2] + "]) - 1.0 = 0.0\n"

    # return of portfolio equals expected return constraint
    def constraint2(w):
        return np.dot(np.array(w),np.array(r_vect))-exp_port_ret

    def cf(len=3):
        return generate_constraint(generate_solvers(solve(equations(number_of_stocks))))

    def pf(len=3):
        return generate_penalty(generate_conditions(equations(number_of_stocks)))

    def bnds(len=number_of_stocks):
        if (is_short_sell):
            return [(-9999999999.9, 9999999999.9)] * len
        else:
            return [(0.0, 1.0)] * len

    mon = VerboseMonitor(10)

    result = diffev2(objective, x0=bnds, bounds=bnds, constraints=cf, penalty=pf, npop=10, gtol=200, disp=False, full_output=False, itermon=mon)

    print(result[0])
    return result[0]

'''

# solving NLP for CAPM model under scipy
def min_var_port(number_of_stocks, is_short_sell, exp_port_ret, cov_matrix, r_vect):
    # objective function
    def objective(w):
        ret = 0
        for i in range(number_of_stocks):
            for j in range(number_of_stocks):
                ret += w[i] * w[j] * cov_matrix[i][j]
        return ret

    # sum of w = 1 constraint
    def constraint1(w):
        return sum(w)-1

    # return of portfolio equals expected return constraint
    def constraint2(w):
        return np.dot(np.array(w),np.array(r_vect))-exp_port_ret

    def solve():
        # initial guess
        w0 = np.zeros((1,number_of_stocks))
        w0.fill(1 / float(number_of_stocks))

        # each weight constraint short selling nope possible:[0,1]; short sell possible:[-99999999999.9,9999999999.9]
        b = [0.0, 1.0]
        if (is_short_sell):
            b[0] = -9999999999.9
            b[1] = 9999999999.9
        bnds = tuple(b for i in range(number_of_stocks))

        con1 = {'type': 'eq', 'fun': constraint1}
        con2 = {'type': 'eq', 'fun': constraint2}
        if (exp_port_ret > 0):
            cons = ([con1, con2])
        else:
            cons = ([con1])

        solution = minimize(objective, w0, method='SLSQP', bounds=bnds, constraints=cons)
        return solution.x

    return solve()
'''
# solving NLP for CAPM model under gekko
def min_var_port(number_of_stocks, is_short_sell, exp_port_ret, cov_matrix, r_vect):
    #Initialize Model
    m = GEKKO()

    # define parameter
    eq = m.Param(value=1)

    #initialize variables
    w = [m.Var(lb=0, ub=1) for i in range(number_of_stocks)]

    #initial values
    w = [1/float(number_of_stocks) for i in range(number_of_stocks)]

    #Equations
    m.Equation(sum(w)==eq)

    #Objective
    m.Obj(sum([w[i] * w[j] * cov_matrix[i][j] for i in range(number_of_stocks) for j in range(number_of_stocks)]))

    #Set global options
    m.options.IMODE = 3 #steady state optimization

    #Solve simulation
    m.solve()
    print(w)
    return w
'''
print(main())