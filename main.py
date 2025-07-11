import graphics as graphics
import thompson as th
import logging
import threading
import time
import engine as eng

# required for starting the graphics thread
g = None
def thread_function(name):
    logging.info("Thread %s: starting", name)
    logging.info("Thread %s: finishing", name)
    global g 
    g = graphics.Graphics()
    g.run_window()
x = threading.Thread(target=thread_function, args=(1,))
x.start()

# list of prebuilt examples
examples = {
            "Homer" : th.V(["000", "0010", "0011", "01", "1000", "1001", "101", "11"],["01", "1100", "1110", "10", "1111", "11011", "00", "11010"]),
            "Monk" : th.V(["000", "0010", "0011","010", "011", "100", "101", "110","111"], ["100", "1010", "110", "1110", "11110", "01", "00", "11111", "1011"]),
            "Kermit" : th.V(["000", "0010", "0011", "01", "1000", "1001", "101", "11"], ["01", "1100", "1110", "10", "1111", "11011", "00", "11010"]),

            "Carl" : th.V(["000", "0010", "00110", "00111", "0100", "0101", "011", "10", "1100", "1101", "111"], ["1001", "010", "011", "110", "10000", "001", "0000", "101", "10001", "0001", "111"]),

            "Mullet" :  th.V(['00000', '00001', '00010', '000110', '000111', '0010', '0011', '010', '011', '1'], ['11', '001', '0110', '101', '0111', '0101', '0100', '0000', '100', '0001']),

            "Goofy" : th.V(['0100', '0101', '0000', '0001', '0111', '01100', '01101', '10', '1100', '1101', '1110', '1111', '0010', '0011'],['0111100', '0111101', '1', '01100', '011100', '01101', '011101', '0101', '0000', '0001', '0010', '0011', '011111', '0100']),

            "Doof" : th.V(th.V.DFS_to_antichain("110111000011000"),th.V.DFS_to_antichain("110111000011000"))
        }

###################### Write code here #########################
#to engage graphics, use g.clear_entities() then g.add_entity({element of V})
# a = examples["Monk"]
a = th.V(["0","10","1100","1101","111"],["0","11","1011","1010","100"])
ch = th.Chains.generate_chains(a)
for c in ch:
    print(c.chain, c.type)
# th.Chains.make_revealing(a, g=g, debug=True)
g.add_entity(a)





# b = examples["Kermit"]
# prod_chains = th.Chains.generate_chains(th.V.rev_product(a,b))
# for p in prod_chains:
    # print(p.chain, p.type)

# g.add_entity(a)
# th.Chains.make_revealing(a, g)

# current = examples["identity"]
# for i in range(3):
    # print("product a^" + str(i + 1))
    # current = th.V.rev_product(current,a)
    # prod_chains = th.Chains.generate_chains(current)
    # for p in prod_chains:
        # print(p.chain, p.type)


# Random element experiment
# elements = t.V.generate_random_elements(5, 10)
# for e in elements:    
    # print(elements.index(e),  " " , e.D,e.R)
    # metrics = t.Chains.make_revealing(e, debug = True)

    # print("Revealing pair")
    # ch = t.Chains.generate_chains(e)
    # for c in ch:
        # print(c.chain)
    # print(t.Chains.is_revealing(ch))

    # if not (metrics == sorted(metrics, reverse=True)):
        # print(elements.index(e),  " " , e.D,e.R)
        # chains = t.Chains.generate_chains(e)
        # print(metrics)
        # for ch in chains:
            # print(ch.chain, ch.type)
        # print(False)


# Product testing
# result = t.V.product(Homer, Monk)
# result = t.V.conjugate(Homer, identity)
# print(result.D, result.R)
# print(Homer.D, Homer.R)
# g.add_entity(result)
# time.sleep(5)
# result.minimise()
# g.clear_entities()
# g.add_entity(result)
# for leaf in Homer.D:
#     print(leaf + ": ")
#     string = leaf + "0"
#     print(string)
#     # print(Monk.apply(Homer.apply(string)) == result.apply(string))
#     # print(Homer.apply(string),Monk.apply(Homer.apply(string)), result.apply(string))
#     string = leaf + "1"
#     print(string)
#     # print(Monk.apply(Homer.apply(string)) == result.apply(string))
#     # print(Homer.apply(string),Monk.apply(Homer.apply(string)), result.apply(string))

# g.add_entity(Doof)

# try
# small = th.V(["000","001","010","011","10","11"],["010","111","00","10","011","110"])
# ch = th.Chains.generate_chains(small)
# for c in ch:
    # print(c.chain, c.type)
# th.Chains.make_revealing(small, g=g, debug=True)
# g.add_entity(small)

# required for joining the graphics thread
x.join()
