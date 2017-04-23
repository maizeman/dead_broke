# dead_broke

Requires matplotlib

By modifying make_broke_rate_file.py one can change withdrawal rates, portfolio composition, and even implement more complex withdrawal strategies. Run this code to generate a new "broke_rates.csv" file.

```
python make_broke_rate_file.py > broke_rates.csv
```

Then run death and bankrupty graph.py. The main variables you can change in this script are age and gender, which are used together to determine risk of death in each year. 

```
python death_and_bankruptcy_graph.py
```

This will generate the final output which is formatted like this:

![alt tag](https://raw.githubusercontent.com/maizeman/dead_broke/master/DAB_graphs/Example_Output.png)

