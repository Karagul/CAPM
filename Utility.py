import CAPM
import Portfolio

#input
dow30 = ["MMM", "AXP", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DWDP", "XOM", "GE", "GS", "HD", "IBM", "INTC",
         "JNJ", "JPM", "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UNH", "UTX", "VZ", "V", "WMT", "DIS"]
iq100 = ["MMM", "ABT", "A", "ALGN", "AMZN", "AMAT", "AAPL", "BHGE", "BAC", "BAX", "BDX", "AVGO", "CA", "BA",
         "ELY", "CAT", "CBS", "CVX", "C", "CLX", "KO", "CTSH", "CREE", "DE", "DXCM", "DOV", "DWDP", "DXC", "EMN",
         "ETN",
         "EW", "ESRX", "XOM", "GRMN", "GE", "GM", "HAL", "HRS", "HIG", "HON", "HPQ", "IBM", "ITW",
         "INTC",
         "IP", "JNJ", "JPM", "KMB", "LMT", "MA", "MAT", "MDT", "MET", "MU", "MSFT", "MDLZ", "MSI", "NCR", "NKE",
         "NOC",
         "ORCL", "PFE", "PX", "PG", "PGR", "PRU", "QCOM", "RTN", "ROK", "SLB", "STX", "SEE", "SON", "SYK",
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
             "PYPL", "QCOM", "REGN", "ROST", "STX", "SIRI", "SWKS", "SBUX", "SYMC", "TSCO", "TSLA",
             "TXN", "TMUS", "ULTA", "VIAB", "VOD", "VRSK", "VRTX", "WBA", "WDC", "XLNX", "XRAY", "PCAR",
             "WYNN"]
snp500 = ['AAPL', 'ABT', 'ABBV', 'ACN', 'ACE', 'ADBE', 'ADT', 'AAP', 'AES', 'AET', 'AFL', 'AMG', 'A', 'GAS', 'ARE',
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

number_of_stocks = 2
is_short_sell = False
exp_port_ret = 0
quandl_key = "KAVVW6RCPX2WWvgJNigd"
start = '2017-12-22'
end = '2017-12-31'
investment = 1000000

me = Portfolio.portfolio("you")
me.readSQL()
me.topUp(investment)
capm = CAPM.main(number_of_stocks,is_short_sell,exp_port_ret,quandl_key,dow30,start,end)
for i in range(len(capm[0])):
    try:
        price = me.checkYahooAsk(capm[0][i])
        quant = int(investment * capm[1][i] / price)
        me.buy(capm[0][i],quant)
    except:
        print("Can't reach data for: " + capm[0][i])
me.writeSQL()


