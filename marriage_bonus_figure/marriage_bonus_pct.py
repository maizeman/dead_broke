import matplotlib

matplotlib.rcParams['xtick.major.size'] = 0
matplotlib.rcParams['xtick.minor.size'] = 0
matplotlib.rcParams['ytick.major.size'] = 0
matplotlib.rcParams['ytick.minor.size'] = 0
#matplotlib.rcParams['lines.linewidth'] = 3
matplotlib.rcParams['patch.linewidth'] = 2
matplotlib.rcParams['axes.linewidth'] = 2
matplotlib.rcParams['legend.fancybox'] = 'True'
matplotlib.rcParams['legend.shadow'] = 'True'
matplotlib.rcParams['legend.fontsize'] = 'medium'
matplotlib.rcParams['legend.markerscale'] = .4
matplotlib.rcParams['xtick.labelsize'] = 'medium'

single_brackets = [
0,
9275,
37650,
91150,
190150,
413340,
415050,
]
married_brackets = [
0,
18550,
75300,
151900,
231450,
413350,
466950,
]
tax_pct = [
0,
.1,
.15,
.25,
.28,
.33,
.35,
.396
]
import numpy as np
for x in range(len(single_brackets)):
    single_brackets[x] += 4050 + 6300
    married_brackets[x] += (4050*2) + 12600

def cal_tax(income,brackets,pct,married=False):
    max_eitc_val = 506
    min_full_credit = 6610
    if married:
        max_credit = 20420
    else:
        max_credit = 14880
    max_full_credit = max_credit-min_full_credit
    old = 0
    tax = 0
    bins = []
    for x in brackets:
        bins.append(x-old)
        old = x
    oldbrac = 0
    for mybrac,mybin,myrate in zip(brackets,bins,pct):
        if income > mybrac:
            tax += mybin * myrate
            oldbrac = mybrac
        elif income-oldbrac > 0:
            tax += (income-oldbrac)* myrate
            oldbrac = mybrac
    if income < max_credit:
        if income > max_full_credit:
            tax -= (max_eitc_val - (income-max_full_credit)*0.0765)
        elif income > min_full_credit:
            tax -= max_eitc_val
        else:
            tax -= income*0.0765
    return tax

import sys

#test = cal_tax(int(sys.argv[1]),married_brackets,tax_pct)
#print(test)

data = []
for myincome in range(0,310000,1000):
    plist = [myincome]
    for low_spouse in range(0,101,5):
        s1_inc = (low_spouse/100.0)* myincome
        s2_inc = myincome - s1_inc
        married = cal_tax(myincome,married_brackets,tax_pct)
        s1_tax = cal_tax(s1_inc,single_brackets,tax_pct)
        s2_tax = cal_tax(s2_inc,single_brackets,tax_pct)
        plist.append(married - s1_tax - s2_tax)
#    print(",".join(map(str,plist)))
    data.append(plist)
@np.vectorize
def marriage_bonus_calc(myincome,low_spouse):
    s1_inc = (low_spouse/100.0)* myincome
    s2_inc = myincome - s1_inc
    married = cal_tax(myincome,married_brackets,tax_pct,married=True)
    s1_tax = cal_tax(s1_inc,single_brackets,tax_pct)
    s2_tax = cal_tax(s2_inc,single_brackets,tax_pct)
    bonus = married - s1_tax - s2_tax
#    print(bonus)
    return ((bonus*-1)/float(myincome+1))*100.0

print(married_brackets)

#print np.array(data)

def yblah(x,pos):
    x = x/1000.0
    return "${0:,.0f}k".format(x)


from matplotlib.ticker import FuncFormatter
formatter = FuncFormatter(yblah)
import matplotlib.pyplot as plt

dx = .1
dy = 1000

y,x = np.mgrid[slice(0,303000,dy),slice(1,99,dx)]
#print x
z = marriage_bonus_calc(y,x)
z = z[:-1,:-1]
#print z
z_min, z_max = -np.abs(z).max(), np.abs(z).max()
#z_min,z_max = -3000,3000
#plt.xkcd()
fig,ax = plt.subplots()
heatmap = ax.pcolor(x,y,z,cmap="seismic_r",vmin=z_min,vmax=z_max)
ax.set_xlabel("Percent of total income earned by one spouse")
ax.set_ylabel("Total income of couple")
ax.yaxis.set_major_formatter(formatter)
plt.title("Tax reduction (or increase) from getting married\n(as a percentage of total income)")
plt.axis([x.min(), x.max(), y.min(), y.max()])
import matplotlib.ticker as ticker
def pct_fmt(x,pos):
    return "{0:.2f}%".format(x)
plt.colorbar(heatmap,format=ticker.FuncFormatter(pct_fmt))
plt.tight_layout()
plt.show()
