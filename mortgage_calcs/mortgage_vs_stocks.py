fh = open("my_data.csv")

def millions(x, pos):
	'The two args are the value and tick position'
	if x >= 1000000:
		return '$%.1fM' % (x*1e-6)
	else:
		return '$%.0fk' % (x*1e-3)

def pcttck(x,pos):
	return "{0}%".format(int((x*100)))

#length of simulation in months
test_length = 360
mortgage_start = 100000
monthly_income = 2000

years,stock_gains,stock_divs,bond_gains,bond_divs,inflat = [],[],[],[],[],[]

for x in fh:
    y = map(float,x.strip().split(','))
    for alist,aval in zip([years,stock_gains,stock_divs,bond_gains,bond_divs,inflat],y[:]):
        alist.append(aval)

years2 = []
for y in years:
	z = str(y).split('.')
	zb = int(z[0]) + int(z[1])/float(12.0)
	years2.append(zb)

def find_bounds(list_of_paths,lower_bound,upper_bound):
    median = []
    upper = []
    lower = []
    mylength = len(list_of_paths[0])
    for x in range(mylength):
        all_vals = []
        for y in range(len(list_of_paths)):
            all_vals.append(list_of_paths[y][x])
        all_vals.sort()
        median.append(all_vals[int(len(all_vals)*.5)])
        lower.append(all_vals[int(len(all_vals)*lower_bound)])
        upper.append(all_vals[int(len(all_vals)*upper_bound)])
    return lower,median,upper

import random
import numpy
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import math
plt.style.use('seaborn-darkgrid')

stock_plot = ()

startmonths = range(0,len(stock_gains)-test_length)
mort_rates = []
stock_wins = 0
mortgage_wins = 0

monthly_winners = []
for x in range(test_length):
    monthly_winners.append([0,0,0])
net1,net2,mydiffs,mydiffs2 = [],[],[],[]
mort_end_val_nom = []
stock_end_val_nom = []
mort_end_val_real = []
stock_end_val_real = []
for astart in startmonths:
    mystockval,mystockval2,mystockval3,mystockval4 = [0.0],[0.0],[0.0],[0.0]
    mytrate = bond_divs[astart]
    #Based on formula from http://www.calculatedriskblog.com/2014/01/mortgage-rates-compared-to-ten-year.html
    mymrate = 0.0245 + (0.7335 * mytrate) + (1.9627 * mytrate * mytrate)
    mymrate = 0.04
    #Four scenarios. Minimum payments (no tax calcs)
    mymortgage = mortgage_start
    #Maximimum payments (no tax calcs)
    mymortgage2 = mymortgage
    #Minimum payments (with tax benefits factored in)
    mymortgage3 = mymortgage
    #Maximum payments (with tax benefits factored in)
    mymortgage4 = mymortgage
    mort_rates.append(mymrate)
    #Note this assumes annual interest rate is the nominal APR and not the effective APR.
    mymrate_monthly = mymrate/12.0
    #more messy math to figure out minimum payment per month
    mypayment = mymortgage *(mymrate_monthly*(math.pow((1+mymrate_monthly),test_length)))/((math.pow((1+mymrate_monthly),test_length))-1)
    cost_rate = 1.0
    for ind in range(test_length):
        target_month = astart+ind
        myincome = monthly_income
        myinterest1 = mymrate_monthly * mymortgage
        myinterest2 = mymrate_monthly * mymortgage2
        myinterest3 = mymrate_monthly * mymortgage3
        myinterest4 = mymrate_monthly * mymortgage4
        #Pay minimum on mortgage invest in stocks
        if mymortgage >= 0:
            mymortgage = mymortgage - mypayment + myinterest1
            newstockval = mystockval[-1]+myincome - mypayment
        else:
            newstockval = mystockval[-1] + myincome
        #pay maximum possible on mortgage, then invest in stocks once gone.
        if mymortgage2 >= 0:
            mymortgage2 = mymortgage2 - myincome + myinterest2
            newstockval2 = mystockval2[-1]
        else:
            newstockval2 = mystockval2[-1]+myincome
        #Pay minimum on mortgage, invest in stocks (including tax savings)
        if mymortgage3 >= 0:
            mymortgage3 = mymortgage3 - mypayment + myinterest3
            newstockval3 = mystockval3[-1]+ myincome - mypayment + (.25 * myinterest3)
        else:
            newstockval3 = mystockval3[-1] + myincome
        #Pay maximum possible on mortgage (including tax savings), then invest in stocks. 
        if mymortgage4 >= 0:
            mymortgage4 = mymortgage4 - myincome + myinterest4 - (.25* myinterest4)
            newstockval4 = mystockval4[-1]
        else:
            newstockval4 = mystockval4[-1]+myincome
        newstockval = newstockval*stock_gains[target_month]
        newstockval = newstockval + newstockval*stock_divs[target_month]
        mystockval.append(newstockval)
        newstockval2 = newstockval2*stock_gains[target_month]
        newstockval2 = newstockval2 + newstockval2*stock_divs[target_month]
        mystockval2.append(newstockval2)
        newstockval3 = newstockval3*stock_gains[target_month]
        newstockval3 = newstockval3 + newstockval3*stock_divs[target_month]
        mystockval3.append(newstockval3)
        newstockval4 = newstockval4*stock_gains[target_month]
        newstockval4 = newstockval4 + newstockval2*stock_divs[target_month]
        mystockval4.append(newstockval4)
        networth1 = 100000 - mymortgage + mystockval[-1]
        networth2 = 100000 - mymortgage2 + mystockval2[-1]
        networth3 = 100000 - mymortgage3 + mystockval3[-1]
        networth4 = 100000 - mymortgage4 + mystockval4[-1]
        net1.append(networth1)
        net2.append(networth2)
        #calculate inflation rate so that I can adjust savings/losses downward properly at the end.
        cost_rate = cost_rate * inflat[target_month]
    if networth1 > networth2:
        stock_wins += 1
    if networth2 > networth1:
        mortgage_wins += 1
    mydiff = networth1 - networth2
    mydiff2 = networth3 - networth4
    mydiffs.append(mydiff/cost_rate)
    mydiffs2.append(mydiff2/cost_rate)
    mort_end_val_nom.append(networth2)
    stock_end_val_nom.append(networth1)
    mort_end_val_real.append(networth2/cost_rate)
    stock_end_val_real.append(networth1/cost_rate)
    print ",".join(map(str,[years[astart],mymrate,mypayment,networth1,networth2,networth3,networth4,cost_rate]))
print stock_wins,mortgage_wins
#1/0
fig = plt.figure(figsize=(10,4))
results_ax = fig.add_subplot('111')
#rate_ax = fig.add_subplot('212')
results_ax.set_title("Comparison of extra mortgage paydown (4%) to stock market investing over 30 year intervals")

tter = FuncFormatter(millions)
pter = FuncFormatter(pcttck)
results_ax.yaxis.set_major_formatter(tter)

results_ax.set_ylabel("Dollars")
a = results_ax.plot(years2[:len(mydiffs)],mort_end_val_nom,'o')
b = results_ax.plot(years2[:len(mydiffs)],stock_end_val_nom,'o')
c = results_ax.plot(years2[:len(mydiffs)],mort_end_val_real,'o')
d = results_ax.plot(years2[:len(mydiffs)],stock_end_val_real,'o')
print years[:len(mydiffs)]

results_ax.legend([a[0],b[0],c[0],d[0]],['Final Networth, Mortgage Paydown, Nominal Dollars','Final Networth, Index Funds, Nominal Dollars','Final Networth, Mortgage Paydown, Real Dollars','Final Networth, Index Funds, Real Dollars'],loc=2)

plt.tight_layout()
plt.show()

