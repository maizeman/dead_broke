fire_age = 45
male = True

fh = open("Death_rate.csv")
fh.readline()
death_dict = {}
for x in fh:
    y = x.strip().split(',')
    if male:
        death_dict[(int(y[0]))] = float(y[1])
    else:
        death_dict[(int(y[0]))] = float(y[4])
tfails = 0
broke_dict = {}
win_dict = {}
fh = open("broke_rates.csv")
for x in fh:
    y = x.strip().split(',')
    broke_dict[int(y[0])] = float(y[1])
    win_dict[int(y[0])] = float(y[2])

fire = [0,1000000]
broke = [0,0]
dead = [0,0]
win = [0,1000000]
xvals = [fire_age,fire_age]
for x in range(fire_age+1,101):
    new_broke = fire[-1]*broke_dict[x-fire_age]
    tfails += new_broke
    new_fire_dead = (fire[-1]-new_broke)*death_dict[x]
    new_broke_dead = (broke[-1]+new_broke)*death_dict[x]
    fire.append(fire[-1]-new_broke-new_fire_dead)
    broke.append(broke[-1]+new_broke-new_broke_dead)
    dead.append(dead[-1]+new_fire_dead+new_broke_dead)
    win.append(fire[-1]*win_dict[x-fire_age])
    xvals.append(x)
print dead[-1],fire[-1],broke[-1]
dfill,bfill,ffill,wfill = [],[],[],[]
for f,b,d,w in zip(fire,broke,dead,win):
    dfill.append(d)
    bfill.append(d+b)
    ffill.append(d+b+f-w)
    wfill.append(d+b+f)
for f in (dfill,bfill,ffill,wfill):
    f.append(0)
xvals.append(100)

import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
plt.xkcd()
fig = plt.figure(figsize=(12,4))
ax = fig.add_subplot('111')

w_f = ax.fill(xvals,wfill,color='#0343df')
f_f = ax.fill(xvals,ffill,color='#00ffff')
b_f = ax.fill(xvals,bfill,color='#e50000')
d_f = ax.fill(xvals,dfill,color='#929591')
ax.set_xlabel("Age (Years)")
ax.set_ylabel("Probability")
ax.legend([w_f[0],f_f[0],b_f[0],d_f[0]],['FIRE','FIRE (stash below start)','Broke','Dead'],loc=2)
plt.tick_params(
    axis='x',         
    which='both',     
    bottom='off',      
    top='off',         
)
plt.tick_params(
    axis='y',         
    which='both',     
    left='off',     
    right='off',         
    labelleft="off"
)
ax.set_title("4% withdrawal, 100% stocks")
ax.set_ylim([0,1000000])
ax.set_xlim([fire_age,100])
plt.tight_layout()
#The risk of your portfolio dying before you do. 
print tfails/1000000.0
plt.show()
