## Usage:
### V: 
This class has all the code for representing elements of V. 
``` 
v = V(D, R)
```
D and R are lists of words on {0,1} that form a complete antichain. The ith index of D is mapped to the ith index of R.

### Chains: 
```
Chains.generate_chains(v)
```
Generates a list of leaf chains.

Code for printing chains:
```
for chain in ch:
    print(chain.chain, chain.type)

```

#### Making revealing pairs:
```
Chains.make_revealing(v)
```
or
```
Chains.make_revealing(v,g)
```
for an optional graphics component.
