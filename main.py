import graphics as graphics
import thompson as t
import logging
import threading
import time
g = None
def thread_function(name):
    logging.info("Thread %s: starting", name)
    logging.info("Thread %s: finishing", name)
    global g 
    g = graphics.Graphics()
    g.run_window()

# format = "%(asctime)s: %(message)s"
# logging.basicConfig(format=format, level=logging.INFO,
                    # datefmt="%H:%M:%S")

# logging.info("Main    : before creating thread")
x = threading.Thread(target=thread_function, args=(1,))
# logging.info("Main    : before running thread")
x.start()
# logging.info("Main    : wait for the thread to finish")
# logging.info("Main    : all done")
# v = t.V()

# Homer?
Homer = t.V(["000", "0010", "0011", "01", "1000", "1001", "101", "11"],["01", "1100", "1110", "10", "1111", "11011", "00", "11010"])

# Monk
# v.D = ["000", "0010", "0011","010", "011", "100", "101", "110","111"]
# v.R = ["100", "1010", "110", "1110", "11110", "01", "00", "11111", "1011"]
Monk = t.V(["000", "0010", "0011","010", "011", "100", "101", "110","111"], ["100", "1010", "110", "1110", "11110", "01", "00", "11111", "1011"])
# v.elem_expansion(6)
# v.elem_expansion(7)
# v.elem_expansion(10)

# Kermit
# v.D = ["000", "0010", "0011", "01", "1000", "1001", "101", "11"]
# v.R = ["01", "1100", "1110", "10", "1111", "11011", "00", "11010"]

# g.add_entity(v)
# ch = t.Chains.generate_chains(v)
# for chain in ch:
    # print(chain.chain, chain.type)

# t.Chains.make_revealing(v,g)

# ch = t.Chains.generate_chains(v)
# for chain in ch:
    # print(chain.chain, chain.type)
# print(t.Chains.is_revealing(ch))

# v.classify()

# print("Now minimising")
# v.minimise(g)
# g.clear_entities()
identity = t.V(["0", "1"], ["0", "1"])
# result = t.V.product(Homer, Monk)
result = t.V.conjugate(Homer, identity)
print(result.D, result.R)
print(Homer.D, Homer.R)
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

x.join()
