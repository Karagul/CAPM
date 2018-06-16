import numpy as np
import scipy.stats as sp

def BlackScholes(Option, K, T, S0, sigma, r, q, Exercise):
    d1 = np.log(S0 / K) + (r - q + sigma ** 2 / 2) * T / sigma / T ** 0.5
    d2 = d1 - sigma * T ** 0.5
    if (Option == "P"):
        return -S0 * np.exp(-q * T) * sp.norm.cdf(-d1) + K * np.exp(
            -r * T) * sp.norm.cdf(-d2)
    else:
        return S0 * np.exp(-q * T) * sp.norm.cdf(d1) - K * np.exp(
            -r * T) * sp.norm.cdf(d2)


def Binomial(Option, K, T, S0, sigma, r, q, N, Exercise):
    arr = np.zeros(N + 1,dtype=np.float64)
    arr[0] = (S0)
    # Fillup S (n,j)
    for n in range(N+1):
        for i in range(n+1):
            delta = T / float(N)
            u = np.exp(sigma * np.sqrt(delta))
            d = np.exp(-sigma * np.sqrt(delta))
            j = i
            arr[i] = u ** j * d ** (n - j) * S0
    # Transform into f (n,j)
    # fN
    for i in range(len(arr)):
        if (Option == "P"):
            arr[i] = max(0, K - arr[i])
        else:
            arr[i] = max(0, arr[i] - K)
    # fN-1~0
    for n in range(len(arr) - 2, -1, -1):
        for i in range(n+1):
            delta = T / float(N)
            u = np.exp(sigma * np.sqrt(delta))
            d = np.exp(-sigma * np.sqrt(delta))
            fu = arr[i + 1]
            fd = arr[i]
            pstar = ((np.exp((r - q) * delta) - d) / float(u - d))
            if (Exercise == "E"):
                arr[i] = np.exp(-r * delta) * (pstar * fu + (1 - pstar) * fd)
            elif (Option == "P"):
                S = u ** i * d ** (n - i) * S0
                arr[i] = max((K - S),np.exp(-r *  delta) * (pstar * fu + (1 - pstar) * fd))
            else:
                S = u ** i * d ** (n - i) * S0
                arr[i] = max((S - K), np.exp(-r * delta) * (pstar * fu + (1 - pstar) * fd))
    return arr[0]  # f0
