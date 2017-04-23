# dead_broke

Requires matplotlib

By modifying make_broke_rate_file.py one can change withdrawal rates, portfolio composition, and even implement more complex withdrawal strategies. Run this code to generate a new "broke_rates.csv" file.

```
python make_broke_rate_file.py > broke_rates.csv
```

Then run death and bankrupty graph.py 

```
python death_and_bankruptcy_graph.py
```

This will generate the final output which is formatted like this:

![alt tag](https://raw.githubusercontent.com/maizeman/dead_broke/master/Example_Output.png)

