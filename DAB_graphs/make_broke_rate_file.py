import sys

fh = open("shiller_data_formatted2.csv")

def pcttck(x,pos):
    return "{0}%".format(int((x*100)))

#Starting portfolio size
start_portfolio = 1200000

#Monthly withdrawl size
#if starting portfolio is $1.2M, each $1,000/month = 1% withdrawal rate.
monthly_spend = 4000

#Make graph comparing trinity and life expectancy style failure rate calculations
#Requires matplotlib
make_graph = False

#Percent stocks
stock_pro = 50

#Percent bonds
bond_pro = 50

#Any money not in bonds or stocks is assumed to be invested in cash. 


if (stock_pro+bond_pro) > 100 or (stock_pro+bond_pro) < 0: 
    sys.exit("The proportion of your portfolio devoted to stocks plus bonds must be between 0 and 100%")


years = []
trad = []
new = []

stock_gains,stock_divs,bond_gains,bond_divs,inflat = [],[],[],[],[]

for x in fh:
    y = map(float,x.strip().split(','))
    for alist,aval in zip([stock_gains,stock_divs,bond_gains,bond_divs,inflat],y[1:]):
        alist.append(aval)

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

cum_rate = 1.0

#This whole loop is ridiculously wasteful
#I shouldn't be recalculating for each year length
#Need to refactor so it only runs the simulations to completion once and then scores failures each year. 
for year in range(1,101):
    ymonths = year*12
    startmonths = range(0,len(stock_gains)-ymonths-1)
#    print year,len(startmonths)
    survived_to_year = 0
    survived_past_year = 0
    survived_up = 0
    for astart in startmonths:
        myportfolioval = [float(start_portfolio)]
        for ind in range(ymonths):
            target_month = astart+ind
#            print myportfolioval[-1]
            mystock_alloc = myportfolioval[-1]*(stock_pro/100.0)
            mybond_alloc = myportfolioval[-1]*(bond_pro/100.0)
            mycash_alloc = myportfolioval[-1] - mybond_alloc - mystock_alloc
#            print myportfolioval[-1],mystock_alloc,mybond_alloc,mycash_alloc
            newstockval = mystock_alloc*stock_gains[target_month]
            newstockval = newstockval + newstockval*stock_divs[target_month]
            newbondval = mybond_alloc*bond_gains[target_month]
            newbondval = newbondval + newbondval*bond_divs[target_month]
            newcashval = mycash_alloc/inflat[target_month]
#            print myportfolioval[-1],newstockval,newbondval,newcashval
            totalnewval = newstockval+newbondval+newcashval - monthly_spend
            myportfolioval.append(totalnewval)
            if ind == ymonths - 12:
                if myportfolioval[-1] > 0:
                    survived_to_year += 1
        if myportfolioval[-1] > 0:
            survived_past_year += 1
        if myportfolioval[-1] >= float(start_portfolio):
            survived_up += 1
    if survived_past_year == 0:
        print "{0},{1},{2},{3}".format(year,1.0,0.0,survived_to_year)
        continue
    fail_rate = (survived_to_year-survived_past_year)/float(survived_to_year)
    up_rate = survived_up/float(survived_past_year)
    cum_rate = cum_rate * (1-fail_rate)
    years.append(year)
    trad.append(1-(float(survived_past_year)/len(startmonths)))
    new.append(1-cum_rate)
    #Number of years
    #proportion of simulations that failed in that year
    #proportion of surviving simulations where the portfolio was greater than the starting value
    #total number of simulations which didn't fail prior to this year and had enough historical data to simulate this year.
    print "{0},{1},{2},{3}".format(year,fail_rate,up_rate,survived_to_year)


if make_graph:
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    #plt.xkcd()
    plt.style.use('seaborn-darkgrid')

    fig = plt.figure(figsize=(10,5))

    ax_trad = fig.add_subplot('111')

    ax_trad.set_ylabel("Failure Rate")
    ax_trad.set_xlabel("Simulated Retirement Length (Years)")
    ax_trad.set_title("Failure rate of 4% annual withdrawals from a 100% stock portfolio")

    t_l = ax_trad.plot(years,trad)
    n_l = ax_trad.plot(years,new)
    pter = FuncFormatter(pcttck)
    ax_trad.yaxis.set_major_formatter(pter)
    ax_trad.legend([t_l[0],n_l[0]],["Traditional Trinity Style\nFailure Rate Calculation","Portfolio Life Expectancy\nCalculation"],loc=2)

    plt.show()
