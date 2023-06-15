# import helper.py
class V:
    def __init__(self, D=[], R=[]):
        self.D = D
        self.R = R
        # TODO implement storing dynamical data in this class 
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
    def is_prefix(self, string1, string2):
        # returns true iff string1 is a prefix of string2
        if len(string1) >= len(string2): return False
        if string2[0:len(string1)] == string1:
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
    
    # def get_connected_components(self):
        # # I worked really hard on this and thought it was very clever but it was deeply unnecessary.
        # # returns tuple of lists of leaves that are in the same connected component.
        # # first index for D and second index for R
        # connected_components = ([],[])
        # common_tree = Trees.intersect(Trees.build_tree(self.D), Trees.build_tree(self.R))
        # d_not_r = self.get_d_not_r()
        # r_not_d = self.get_r_not_d()
        
        # while len(d_not_r) > 0:
            # d = d_not_r[0]
            # con_comp = []

            # i = 1
            # while (d[:-i] not in common_tree):
                # i = i + 1
            
            # con_comp = [v for v in d_not_r if V.is_prefix(d[:-i], v)]
            
            # d_not_r = [d for d in d_not_r if d not in con_comp]
            # connected_components[0].append(con_comp)
    
        # while len(r_not_d) > 0:
            # r = r_not_d[0]
            # con_comp = []

            # i = 1
            # while (r[:-i] not in common_tree):
                # i = i + 1
            
            # con_comp = [v for v in r_not_d if V.is_prefix(r[:-i], v)]
            
            # r_not_d = [r for r in r_not_d if r not in con_comp]
            # connected_components[1].append(con_comp)
        # return connected_components

    def clear_dynamics(self):
        # not yet usable as dynamical data is not yet stored in this class
        # meant to be a general 'clear metadata' function
        self.repellers = []
        self.attractors = []

    def classify(self, leaf):
        # very WIP
        # TODO redo with chains
        #returns leaf type. 9 types
        # if leaf in get_netural_leaves():
            # return "neutral_leaf"
        # if leaf in [pair[0] for pair in repellers]:
            # return "repellers"
        # if leaf in [pair[1] for pair in repellers]:
            # return "range_of_repulsion"
        # if leaf in [pair[0] for pair in attractor]:
            # return "attractor"
        # if leaf in [pair[1] for pair in attractor]:
            # return "domain_of_attraction"
        
        # current = self.apply(leaf)
        # while current != leaf:
            # if V.is_prefix(current, leaf):
                # self.repellers.append((leaf,current))
                # return "repeller"
            # if V.is_prefix(leaf, current):
                # self.attractors.append((leaf,current))
                # return "attractor"
            # current = self.apply(current)

        # current = self.apply_inverse(leaf)
        # while current != leaf:
            # if is_ancestor(leaf, current):
                # self.repellers.append((current,leaf))
                # return "range_of_repulsion"
            # if is_ancestor(current, leaf):
                # self.attractors.append((current,leaf))
                # return "domain_of_attraction"
            # current = self.apply_inverse(current)
        pass
        
class Chain:
    # Individual chains formally presented as a tuple (iterated augmentation chain, label)
    def __init__(self, starting_point, function):
        self.chain = [] 
        self.type = ""

    def classify(self, function):
        # classifies the chain into types

        # print(self.chain)
        d_union_r = function.D + function.R
        self.type = "SS"
        if len(self.chain) == 0:
            # can't classify and ungenerated chain
            raise Exception("Attempting to classify empty chain.")
        
        # attractor
        if V.is_prefix(self.chain[0], self.chain[-1]):
            self.type = "A"
            return self.type

        # repeller
        if V.is_prefix(self.chain[-1], self.chain[0]):
            self.type = "R"
            return self.type
        
        # checking for Fragmentation*
        EF = False
        SF = False
        for leaf in function.get_d_not_r():
            if V.is_prefix(self.chain[-1], leaf):
                self.type = "EF"
                EF = True
                break

        for leaf in function.get_r_not_d():
            if V.is_prefix(self.chain[0], leaf):
                self.type = "SF"
                SF = True
                break

        if EF and SF:
            self.type = "SEF"

        return self.type

    @classmethod
    def generate_chain(self, starting_point, function):
        # This function is the intended way to use Chain class, but pythons lack of private constructors doesn't let me block direct usage. Please don't instantiate Chain directly. Returns a classified Chain type object

        # might be useful error checking, but unnecessary at this point
        # if starting_point not in Tree.subtract(self.function.D, self.function.R):
            # raise Exception("Chain must start at leaf of D which is not a leaf of R")
        ch = Chain(starting_point, function)
        neutral_leaves = function.get_neutral_leaves()

        # applies function to the starting_point until the result isn't a neutral leaf, then returns the Chain of results
        ch.chain.append(starting_point)
        current = function.apply(starting_point)
        ch.chain.append(current)
        while current in neutral_leaves:
            # detects P type chains, but this functionality is usually unused as starting_point is intended to be a non-neutral leaf.
            if current == starting_point:
                self.type = "P"
                break
            current = function.apply(current)
            ch.chain.append(current)
        ch.classify(function)

        return ch

    def slow_rolling(self, function):
        # adds a carrot(caret) for each word in the chain
        for word in self.chain[:-1]:
            index = function.D.index(word)
            print("expanding at " + str(index))
            function.elem_expansion(index)


class Chains:
    @classmethod
    def generate_chains(self, function):
        # generates the chains for a given element of V
        starting_points = function.get_d_not_r()
        chains = []

        for point in starting_points:
            chains.append(Chain.generate_chain(point, function))

        return chains

    @classmethod
    def is_revealing(self, chains):
        if len(chains) == 0:
            raise Exception("Chain must be generated to be revealing")
        
        types = []
        for chain in chains:
            types.append(chain.type)
        
        # returns false if types contain any fragmentation labels
        return not ("SEF" in types or "SF" in types or "EF" in types)

    @classmethod
    def make_revealing(self, function):
        # slow rolling algorithm
        chains = Chains.generate_chains(function)
        while not Chains.is_revealing(chains):
            chosen_sef = None
            chosen_ef = None
            chosen_sf = None

            # debug 
            for chain in chains:
                print(chain.chain, chain.type)

            for ch in chains:
                if ch.type == "SEF":
                    chosen_sef = ch
                    # forces sef to be resolved first at each step
                    break
                elif ch.type == "SF":
                    chosen_sf = ch
                elif ch.type == "EF":
                    chosen_ef = ch

            # maintains priority for order of chain resolution
            if chosen_sef != None:
                chosen_sef.slow_rolling(function)
            elif chosen_ef != None:
                chosen_ef.slow_rolling(function)
            elif chosen_sf != None:
                chosen_sf.slow_rolling(function)

            print(len(function.D))
            chains = Chains.generate_chains(function)
v = V()
# v.D = ["000", "0010", "0011", "01", "1000", "1001", "101", "11"]
# v.R = ["01", "1100", "1110", "10", "1111", "11011", "00", "11010"]

v.D = ["000", "0010", "0011","010", "011", "100", "101", "110","111"]
v.R = ["100", "1010", "110", "1110", "11110", "01", "00", "11111", "1011"]
# v.elem_expansion(6)
# v.elem_expansion(7)
# v.elem_expansion(10)
ch = Chains.generate_chains(v)
# for chain in ch:
    # print(chain.chain, chain.type)

Chains.make_revealing(v)

ch = Chains.generate_chains(v)
for chain in ch:
    print(chain.chain, chain.type)
print(Chains.is_revealing(ch))

