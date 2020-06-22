# dead_broke

Various scripts based on python and matplotlib for simulating and visualizing various types of data relevant to personal finance. 

Examples of the output: 

A DAB (Death and Bankruptcy) graph.

![alt tag](https://raw.githubusercontent.com/maizeman/dead_broke/master/DAB_graphs/Example_Output.png)

How the tax code favors or penalizes married couples relative to two single people with equivalent incomes. 

![alt tag](https://raw.githubusercontent.com/maizeman/dead_broke/master/marriage_bonus_figure/marriage_bonus_pct_example.png)

Whether bonds, stocks, or cash are likely to provide the best overall returns in different historical time periods.

![alt tag](https://raw.githubusercontent.com/maizeman/dead_broke/master/stocks_vs_bonds_vs_cash/projections_threeway_example.png)

What portfolio mix of bonds, stocks, or cash provide the best return in different percentiles.

![alt tag](stocks_vs_bonds_vs_cash_portfolio_mix/projections_threeway_example.png)

# running

* install humor sans font (on debian/ubuntu `sudo apt install fonts-humor-sans`)
* `pip3 install matplotlib`
* `cd stocks_vs_bonds_vs_cash`
* `python3 projections_threeway.py`

