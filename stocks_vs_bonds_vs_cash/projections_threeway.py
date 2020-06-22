fh = open("shiller_data_formatted2.csv")

def millions(x, pos):
    'The two args are the value and tick position'
    if x >= 1000000:
        return '$%.1fM' % (x*1e-6)
    else:
        return '$%.0fk' % (x*1e-3)

def pcttck(x,pos):
    return "{0}%".format(int((x*100)))

#length of simulation in months
test_length = 240
num_sims = 500

stock_gains,stock_divs,bond_gains,bond_divs,inflat = [],[],[],[],[]

for x in fh:
    y = list(map(float,x.strip().split(',')))
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
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
#plt.xkcd()
plt.style.use('seaborn-darkgrid')

fig = plt.figure(figsize=(10,6))
stock_ax = fig.add_subplot('221')
bond_ax = fig.add_subplot('222')
winners_ax = fig.add_subplot('212')
stock_ax.set_title("Stocks")
bond_ax.set_title("Bonds")
tter = FuncFormatter(millions)
pter = FuncFormatter(pcttck)
stock_ax.yaxis.set_major_formatter(tter)
bond_ax.yaxis.set_major_formatter(tter)
winners_ax.yaxis.set_major_formatter(pter)
stock_ax.set_xlabel("Years")
stock_ax.set_ylabel("Dollars (Not Inflation Adjusted)")


stock_plot = ()

startmonths = random.sample(range(0,len(stock_gains)-test_length),num_sims)

stock_paths = []
bond_paths = []
cash_paths = []

monthly_winners = []
for x in range(test_length):
    monthly_winners.append([0,0,0])

for astart in startmonths:
    mystockval,mybondval,mycashval = [100000.0],[100000.0],[100000.0]
    for ind in range(test_length):
        target_month = astart+ind
        newstockval = mystockval[-1]*stock_gains[target_month]
        newstockval = newstockval + newstockval*stock_divs[target_month]
        mystockval.append(newstockval)
        newbondval = mybondval[-1]*bond_gains[target_month]
        newbondval = newbondval + newbondval*(bond_divs[target_month])
        mybondval.append(newbondval)
        #replace with monthly value of 1% interest for constant interest.
        mycashval.append(mycashval[-1]*1.00083)
        if mycashval[-1] >= mybondval[-1] and mycashval[-1] >= mystockval[-1]:
            monthly_winners[ind][0] += 1
        elif mybondval[-1] >= mystockval[-1]:
            monthly_winners[ind][1] += 1
        else:
            monthly_winners[ind][2] += 1
    stock_paths.append(mystockval)
    bond_paths.append(mybondval)
    cash_paths.append(mycashval)

cash_wins = [0] + [1.0]*(test_length)
print(len(cash_wins))
bond_wins = [0]
stock_wins = [0]
for ind in monthly_winners:
    bond_wins.append((ind[1]+ind[2])/float(sum(ind)))
    stock_wins.append(ind[2]/float(sum(ind)))

cash_wins.append(0)
bond_wins.append(0)
stock_wins.append(0)



stock_lower,stock_median,stock_upper = find_bounds(stock_paths,0.1,0.9)
bond_lower,bond_median,bond_upper = find_bounds(bond_paths,0.1,0.9)

xval = numpy.arange(test_length+1)/12.0
print(len(xval))
for s in stock_paths:
    stock_ax.plot(xval,s,color='.5',lw='.3',alpha=.3)
cont = stock_ax.plot(xval,mycashval,color='b',lw=2)
med = stock_ax.plot(xval,stock_median,color='r',lw=2)
stock_ax.plot(xval,stock_lower,'--',color='r',lw=2)
bound = stock_ax.plot(xval,stock_upper,'--',color='r',lw=2)
stock_ax.legend([med[0],bound[0],cont[0]],["50th Percentile of Simulations","10th/90th Percentiles","Control (Save Cash)"],loc=2)
for b in bond_paths:
    bond_ax.plot(xval,b,color='.5',lw='.3',alpha=.3)
cont = bond_ax.plot(xval,mycashval,color='b',lw=2)
med = bond_ax.plot(xval,bond_median,color='#7e1e9c',lw=2)
bond_ax.plot(xval,bond_lower,'--',color='#7e1e9c',lw=2)
bound = bond_ax.plot(xval,bond_upper,'--',color='#7e1e9c',lw=2)
bond_ax.set_ylim(stock_ax.get_ylim())

xvals2 = [0]
for x in xval[:-1]:
        xvals2.append(x)
xvals2.append(xvals2[-1])
print(len(xvals2))
print(len(cash_wins))
c_f = winners_ax.fill(xvals2,cash_wins,color='b')
b_f = winners_ax.fill(xvals2,bond_wins,color='#7e1e9c')
s_f = winners_ax.fill(xvals2,stock_wins,color='r')

winners_ax.set_xlim(0,xvals2[-1])
wl = winners_ax.legend([c_f[0],b_f[0],s_f[0]],['Cash Has Best Return','Bonds Have Best Return','Stocks Have Best Return'],loc=4,frameon=True)

winners_ax.set_xlabel("Years")
winners_ax.set_ylabel("Probability")
winners_ax.set_title("Chance Each Asset Is the Right One To Invest in At Different Time Frames")
plt.tight_layout()
plt.show()
