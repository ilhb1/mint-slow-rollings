import graphics as g
import thompson as t

# g = g.Graphics()
v = t.V()
# v.D = ["000", "0010", "0011", "01", "1000", "1001", "101", "11"]
# v.R = ["01", "1100", "1110", "10", "1111", "11011", "00", "11010"]

v.D = ["000", "0010", "0011","010", "011", "100", "101", "110","111"]
v.R = ["100", "1010", "110", "1110", "11110", "01", "00", "11111", "1011"]
# v.elem_expansion(6)
# v.elem_expansion(7)
# v.elem_expansion(10)

ch = t.Chains.generate_chains(v)
# for chain in ch:
    # print(chain.chain, chain.type)

t.Chains.make_revealing(v)

ch = t.Chains.generate_chains(v)
for chain in ch:
    print(chain.chain, chain.type)
print(t.Chains.is_revealing(ch))


# g.add_entity(v)
# g.run_window()
