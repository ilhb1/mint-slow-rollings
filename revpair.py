import time
class Trees:
    #TODO rewrite with sets and verify
    @classmethod
    def subtract(a, b):
        #returns a not in b
        V,E = [],[]
        V = [e for e in a[0] if e not in b[0]]
        E = [e for e in a[1] if e[0] not in b[0] and e[1] not in b[0]]
        return (V,E)
    @classmethod
    def intersect(a, b):
        #returns a intersection b
        V,E = [],[]
        V = [e for e in a[0] if e in b[0]]
        union_of_edges = a[1].append(b[1])
        E = [e for e in union_of_edges if e[0] in a[0] and e[0] in b[0] and e[1] in a[0] and e[1] in b[0]]
        return (V,E)

    @classmethod
    def _rec_build_tree(self, tree, antichain, prefix):
        if prefix not in antichain:
            prefix1 = prefix + "0"
            tree[0].append(prefix1)
            tree[1].append((prefix, prefix1))
            self._rec_build_tree(tree,antichain, prefix1)

            prefix2 = prefix + "1"
            tree[0].append(prefix2)
            tree[1].append((prefix, prefix2))
            self._rec_build_tree(tree,antichain, prefix2)
        else:
            return

    @classmethod
    def build_tree(self, antichain):
        V = []
        E = []
        tree = (V, E)
        tree[0].append("")
        self._rec_build_tree(tree, antichain, "")
        return tree



class V:
    def __init__(self):
        self.D = []
        self.R = []
        self.attractor_orbits = []
        self.repeller_orbits = []
        # list of tuples with (attractor, domain of attraction)
        self.attractors = []
        # list of tuples with (repeller, range of repulsion)
        self.repellers = []

    def apply(self, string):
        # identifying prefix
        for i in range(len(self.D)):
            prefix = string[0 : len(self.D[i])]
            rest = string[len(self.D[i]) : -1]
            if prefix == self.D[i]:
                # changing prefix to R
                return self.R[i] + rest
    def apply_inverse(self, string):
        #TODO
        pass

    @classmethod
    def is_ancestor(string1, string2):
        if len(string1) <= len(string2): return False
        if string1[0:len(string2)] == string2:
            return True
        return False
       
    def elem_expansion(self, index):
        elem = self.D[index]
        self.D.pop(index)
        self.D.insert(index, elem + "0")
        self.D.insert(index + 1, elem + "1")

        elem = self.R[index]
        self.R.pop(index)
        self.R.insert(index, elem + "0")
        self.R.insert(index + 1, elem + "1")
    

    def get_d_not_r(self):
        return [d for d in self.D if d not in self.R]

    def get_r_not_d(self):
        return [r for r in self.R if r not in self.D]

    def get_neutral_leaves(self):
        return [leaf for leaf in self.D if leaf in self.R]
    
    def get_connected_components(self):
        # returns tuple of lists of leaves that are in the same connected component.
        # first index for D and second index for R
        connected_components = ([],[])
        common_tree = Trees.intersect(Trees.build_tree(self.D), Trees.build_tree(self.R))
        d_not_r = self.get_d_not_r()
        r_not_d = self.get_r_not_d()
        
        while len(d_not_r) > 0:
            d = d_not_r[0]
            con_comp = []

            i = 1
            while (d[:-i] not in common_tree):
                i = i + 1
            
            con_comp = [v for v in d_not_r if V.is_ancestor(d[:-i], v)]
            
            d_not_r = [d for d in d_not_r if d not in con_comp]
            connected_components[0].append(con_comp)
    
        while len(r_not_d) > 0:
            r = r_not_d[0]
            con_comp = []

            i = 1
            while (r[:-i] not in common_tree):
                i = i + 1
            
            con_comp = [v for v in r_not_d if V.is_ancestor(r[:-i], v)]
            
            r_not_d = [r for r in r_not_d if r not in con_comp]
            connected_components[1].append(con_comp)
        return connected_components

    def clear_dynamics(self):
        self.repellers = []
        self.attractors = []

    def classify(self, leaf):
        # TODO domain of sourcing, range of sinking, sources, and sinks
        #returns leaf type. 9 types
        if leaf in get_netural_leaves():
            return "neutral_leaf"
        if leaf in [pair[0] for pair in repellers]:
            return "repellers"
        if leaf in [pair[1] for pair in repellers]:
            return "range_of_repulsion"
        if leaf in [pair[0] for pair in attractor]:
            return "attractor"
        if leaf in [pair[1] for pair in attractor]:
            return "domain_of_attraction"
        
        current = self.apply(leaf)
        while current != leaf:
            if V.is_ancestor(current, leaf):
                self.repellers.append((leaf,current))
                return "repeller"
            if V.is_ancestor(leaf, current):
                self.attractors.append((leaf,current))
                return "attractor"
            current = self.apply(current)

        current = self.apply_inverse(leaf)
        while current != leaf:
            if is_ancestor(leaf, current):
                self.repellers.append((current,leaf))
                return "range_of_repulsion"
            if is_ancestor(current, leaf):
                self.attractors.append((current,leaf))
                return "domain_of_attraction"
            current = self.apply_inverse(current)
        
    def check_revealing(self):
        # TODO check revealing
        connected_components = self.get_connected_components()
        
    # def verify_revealing(self):
        # to_check = [i for i in self.D]
        # endpoints = []

        # for node in to_check:
            # prev = [] 
            # theta = node
            # prev.append(theta)

            # print(theta)
            # theta = self.apply(theta)

            # while theta not in endpoints:
                # print("Theta: " + theta)
                # print(endpoints)
                # if theta not in [i for i in self.D if i in self.R]:

                    # for p in prev:
                        # print("p: " + p)
                        # if self.is_ancestor(theta, p):
                            # endpoints.append(p)
                            # endpoints.append(theta)
                            # self.repellers.append(p)
                        # elif self.is_ancestor(p, theta):
                            # endpoints.append(p)
                            # endpoints.append(theta)
                            # self.attractors.append(p)

                    # for d in self.D:
                        # print("d: " + d)
                        # if self.is_ancestor(d,theta):
                            # self.elem_expansion(self.R.index(theta))
                            # print("roll back")
                            # return False

                        # elif self.is_ancestor(theta, d):
                            # self.elem_expansion(self.D.index(d))
                            # print("roll forward")
                            # return False

                # else:
                    # if theta in prev:
                        # break

                # prev.append(theta)
                # if theta not in endpoints:
                    # theta = self.apply(theta)
        # return True

        # for d in self.D:
            # theta = d
            # prev = []
            # prev.append(theta)
            # theta = self.apply(d)
            # while theta in [i for i in self.D if i in self.R] or theta in self.attractors or theta in self.repellers:
                # if (theta in prev): 
                    # # periodic neutral points
                    # break
                # if (self.is_ancestor(theta, d)):
                    # # repellers
                    # self.repellers.append(d)
                # if (self.is_ancestor(d, theta)):
                    # #attractors
                    # self.attractors.append(d)
                # prev.append(theta)
                # theta = self.apply(d)
                # print(theta)

            # if (theta not in [i for i in self.D if i in self.R]):
                # return theta

    def rev_pair(self):

        while self.verify_revealing() == False:
            print("done")
            print(v.D, v.R)
            time.sleep(1)

        # to_expand = self.verify_revealing()
        # while to_expand != None:
            # print("to_expand: " + to_expand)
            # expanded = False
            # for d in self.D:
                # print(d)
                # if self.is_ancestor(d, to_expand): 
                    # print("poop")
                    
                    # # for i in range(len(to_expand) - len(d)):
                    # self.elem_expansion(self.D.index(d))
                    # expanded = True
                    # break
            # if not expanded:
                # for r in self.R:
                    # print(r)
                    # if self.is_ancestor(r, to_expand): 
                        # print("poop")
                        
                        # # for i in range(len(to_expand) - len(d)):
                        # self.elem_expansion(self.R.index(r))
                        # break
            # print(v.D, v.R)
            # time.sleep(1)
            # to_expand = self.verify_revealing()
class Chain:
    def __init__(self, starting_point, function):
        self.chain = [] 
        self.type = ""
        self.function = function

    def classify(self):
        d_union_r = self.function.D + self.function.R
        if len(chain) == 0:
            # can't classify and ungenerated chain
            raise Exception("Attempting to classify empty chain.")
        
        if self.chain[-1] in self.function.R:
            self.type = "SS"
            return self.type
        if V.is_ancestor(self.chain[0], self.chain[-1]):
            self.type = "A"
            return self.type
        if V.is_ancestor(self.chain[-1], self.chain[0]):
            self.type = "R"
            return self.type
        
        EF = False
        for leaf in self.function.get_d_not_r().remove(self.chain[0]):
            if V.is_ancestor(self.chain[-1], leaf):
                self.type = "EF"
                EF = True
        for leaf in self.function.get_r_not_d().remove(self.chain[0]):
            if V.is_ancestor(self.chain[0], leaf):
                if EF == True:
                    self.type = "SEF"
                else:
                    self.type = "SF"
        return self.type

                
        


    @classmethod
    def generate_chain(self, starting_point, function):
        # if starting_point not in Tree.subtract(self.function.D, self.function.R):
            # raise Exception("Chain must start at leaf of D which is not a leaf of R")
        ch = Chain(starting_point, function)
        neutral_leaves = ch.function.get_neutral_leaves()

        ch.chain.append(starting_point)
        current = ch.function.apply(starting_point)
        ch.chain.append(current)
        while current in neutral_leaves:
            if current == starting_points:
                self.type = "P"
                break
            current = ch.function.apply(current)
            ch.chain.append(current)

        ch.chain.append(current)
        ch.chain = chain
        ch.classify()

        return ch

class Chains:
    # TODO chains merging and extending
    def __init__(self, function):
        self.chains
        self.function = function

    def generate_chains(self):
        starting_points = self.function.get_d_not_r()

        for points in starting_points:
            self.chains.append(Chain.generate_chain(point))

    def make_revealing():
        pass
        

v = V()
v.D = ["000", "0010", "0011", "01", "1000", "1001", "101", "11"]
v.R = ["01", "1100", "1110", "10", "1111", "11011", "00", "11010"]

ch = Chains(v)
ch.generate_chains()
print(ch.chains)


# print(v.D, v.R)
# v.rev_pair()
# print(v.D, v.R)
