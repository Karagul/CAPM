import numpy as np
from scipy.optimize import minimize
import quandl

def main(number_of_stocks,is_short_sell,exp_port_ret,quandl_key,stockRange,start,end):
    list_of_stocks_data = []
    list_of_stocks_name = []

    #read adj close data from quandl in time span of 3 years ago to today
    quandl.ApiConfig.api_key = quandl_key
    for i in stockRange:
        stock = quandl.get("WIKI/" + i + '.11', start_date=start, end_date=end, returns='numpy')
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
            ij = [list_of_stocks_return[i][k]*list_of_stocks_return[j][k] for k in range(len(list_of_stocks_return[i]))]
            cov_matrix[i][j] = np.mean(ij)-np.mean(list_of_stocks_return[i])*np.mean(list_of_stocks_return[j])
    set_of_stocks = list_of_stocks_name
    return muti_min_var_port(r_vect,s_vect,cov_matrix,number_of_stocks,exp_port_ret,is_short_sell,set_of_stocks)

def muti_min_var_port(r_vect, s_vect, cov_matrix, number_of_stocks, exp_port_ret, is_short_sell, set_of_stocks):
    # find relative optimal solution on high return-low risk
    def find_optimal():
        sols = []
        rets = []
        stocks = []
        for w in range(0, 101, 10):
            (sol, ret, subset_of_stocks) = find_port(w / 100.0, r_vect, s_vect, number_of_stocks, cov_matrix,
                                                     exp_port_ret, is_short_sell, set_of_stocks)
            sols.append(sol)
            rets.append(ret)
            stocks.append(subset_of_stocks)
        return (stocks[np.argmax(rets)], sols[np.argmax(rets)])

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
