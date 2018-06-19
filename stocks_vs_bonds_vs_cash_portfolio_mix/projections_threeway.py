fh = open("shiller_data_formatted2.csv")

def pcttck(x,pos):
    return "{0}%".format(int((x*100)))

#length of simulation in months
test_length = 240
num_sims = 500

stock_gains,stock_divs,bond_gains,bond_divs,inflat = [],[],[],[],[]

for x in fh:
    y = map(float,x.strip().split(','))
    for alist,aval in zip([stock_gains,stock_divs,bond_gains,bond_divs,inflat],y[1:]):
        alist.append(aval)

import random
import numpy
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator
plt.style.use('seaborn-darkgrid')

PERCENTILE=[5, 15, 25]

fig = plt.figure(figsize=(10,6))
winners_ax = {}
winners_ax[PERCENTILE[0]] = fig.add_subplot('221')
winners_ax[PERCENTILE[2]] = fig.add_subplot('222')
winners_ax[PERCENTILE[1]] = fig.add_subplot('212')
pter = FuncFormatter(pcttck)
for percentile in PERCENTILE:
    winners_ax[percentile].xaxis.set_major_locator(MultipleLocator(5.))
    winners_ax[percentile].yaxis.set_major_formatter(pter)


startmonths = random.sample(range(0,len(stock_gains)-test_length),num_sims)

stock_paths = [[] for ind in range(test_length)]
bond_paths = [[] for ind in range(test_length)]
cash_paths = [[] for ind in range(test_length)]

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
        
        stock_paths[ind].append(mystockval[-1])
        bond_paths[ind].append(mybondval[-1])
        cash_paths[ind].append(mycashval[-1])

for ind in range(test_length):
    stock_paths[ind] = numpy.array(stock_paths[ind]).reshape(-1, 1)
    bond_paths[ind] = numpy.array(bond_paths[ind]).reshape(-1, 1)
    cash_paths[ind] = numpy.array(cash_paths[ind]).reshape(-1, 1)

cash_wins={}
bond_wins={}
stock_wins={}

for percentile in PERCENTILE:
    cash_wins[percentile] = [0] + [1.0]*(test_length)
    bond_wins[percentile] = [0]
    stock_wins[percentile] = [0]

stock_scenarios=[]
bond_scenarios=[]
cash_scenarios=[]
for percent_stock in range(0,101):
    stock_ratio = percent_stock / 100.
    for percent_bond in range(0,101-percent_stock,2):
        bond_ratio = percent_bond / 100.
        cash_ratio = 1-stock_ratio-bond_ratio
        stock_scenarios.append(stock_ratio)
        bond_scenarios.append(bond_ratio)
        cash_scenarios.append(cash_ratio)

stock_scenarios = numpy.array(stock_scenarios).reshape(1, -1)
bond_scenarios = numpy.array(bond_scenarios).reshape(1, -1)
cash_scenarios = numpy.array(cash_scenarios).reshape(1, -1)

for ind in range(test_length):
    print '%d / %d' % (ind+1, test_length)
    max_value = {percentile: None for percentile in PERCENTILE}
    test_lists = numpy.dot(stock_paths[ind], stock_scenarios) + numpy.dot(bond_paths[ind], bond_scenarios) + numpy.dot(cash_paths[ind], cash_scenarios)
    for percentile in PERCENTILE:
        max_scenario = numpy.argmax(numpy.percentile(test_lists, percentile, axis=0))
        stock_wins[percentile].append(stock_scenarios[0][max_scenario])
        bond_wins[percentile].append(bond_scenarios[0][max_scenario]+stock_scenarios[0][max_scenario])

xval = numpy.arange(test_length+1)/12.0

xvals2 = [0]
for x in xval[:-1]:
        xvals2.append(x)
xvals2.append(xvals2[-1])
for percentile in PERCENTILE:
    cash_wins[percentile].append(0)
    bond_wins[percentile].append(0)
    stock_wins[percentile].append(0)
    c_f = winners_ax[percentile].fill(xvals2,cash_wins[percentile],color='b')
    b_f = winners_ax[percentile].fill(xvals2,bond_wins[percentile],color='#7e1e9c')
    s_f = winners_ax[percentile].fill(xvals2,stock_wins[percentile],color='r')

    winners_ax[percentile].set_xlim(0,xvals2[-1])
    wl = winners_ax[percentile].legend([c_f[0],b_f[0],s_f[0]],['Cash portfolio ratio','Bond portfolio ratio', 'Stock portfolio ratio'],loc=4,frameon=True)

    winners_ax[percentile].set_xlabel("Years")
    winners_ax[percentile].set_ylabel("Portfolio mix")
    winners_ax[percentile].set_title('Best portfolio mix to maximize the %dth percentile' % (percentile))
plt.tight_layout()
plt.show()
