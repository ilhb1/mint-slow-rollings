# import helper.py
from copy import deepcopy
import time
class V:
    def __init__(self, D=[], R=[]):
        self.D = D
        self.R = R
        # list of tuples with (attractor, domain of attraction)
        self.attractors = []
        # list of tuples with (repeller, range of repulsion)
        self.repellers = []

        self.sources_and_sinks = []

    def validate(self):
        if len(self.D) != len(self.R):
            raise Exception("element must be a bijection")
        if not self.is_antichain(self.D) or not self.is_antichain(self.R):
            raise Exception("D and R must be antichains " + str(self.is_antichain(self.D)) + " " + str(self.is_antichain(self.R)))


    def apply(self, string):
        self.validate()
        # identifying prefix
        for i in range(len(self.D)):
            # prefix = string[0 : len(self.D[i])]
            if self.is_prefix(self.D[i], string) or self.D[i] == string:
                rest = string[len(self.D[i]) :]
                # changing prefix to R
                if rest != None:
                    return self.R[i] + rest
                else:
                    return self.R[i]
        raise Exception("Cannot apply to a point not in cone. " + string )
        return (self.apply(string + "0"), self.apply(string + "1"))

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

    @classmethod
    def is_antichain(self, words):
        for i in words:
            for j in words:
                if i != j and self.is_prefix(i,j):
                    return False
        return True


       
    def elem_expansion(self, index):
        if index >= len(self.D):
            raise Exception("Cannot expand at index out of range.")
        elem = self.D[index]
        self.D.pop(index)
        self.D.insert(index, elem + "0")
        self.D.insert(index + 1, elem + "1")

        elem = self.R[index]
        self.R.pop(index)
        self.R.insert(index, elem + "0")
        self.R.insert(index + 1, elem + "1")

    def elem_minimise(self, tuple0, tuple1):
        word_in_D = tuple0[0][:-1]
        word_in_R = tuple0[1][:-1]

        index = self.D.index(tuple0[0])

        self.D.remove(tuple0[0])
        self.R.remove(tuple0[1])

        self.D.remove(tuple1[0])
        self.R.remove(tuple1[1])

        self.D.insert(index, word_in_D)
        self.R.insert(index, word_in_R)

    def _rec_minimise(self):
        for d in self.D:
            # print(d)
            # print(self.D)
            root = d[:-1]
            r0 = root + "0"
            r1 = root + "1"
            if r1 in self.D and r0 in self.D:
                img_r0 = self.apply(r0)
                img_r1 = self.apply(r1)

                if img_r0 == img_r1[:-1] + "0" and img_r1[-1] == "1":
                    self.elem_minimise((r0, img_r0), (r1, img_r1))   
                    return True
        return False

    def minimise(self, g=None):
        while self._rec_minimise():
            if g != None:

                time.sleep(2)
                g.clear_entities()
                g.add_entity(self)
                print(self.is_antichain(self.D), self.is_antichain(self.R))
            self._rec_minimise()

    @classmethod
    def product(self, a, b):
        # making copies to not change state of a,b
        # minimising first
        a_copy = deepcopy(a)
        a_copy.minimise()
        b_copy = deepcopy(b)
        b_copy.minimise()

        # while the 'middle'trees of the product are not equal
        while sorted(b_copy.D) != sorted(a_copy.R):
            # picks the bigger element to expand
            expand, target , is_first = (b_copy, a_copy, False) if len(b_copy.D) > len(a_copy.D) else (a_copy, b_copy, True)
            tree_expand, other = (expand.R, target.D) if is_first else (expand.D, target.R)

            # run until an expansion happens then break
            broken = False
            for i in tree_expand:
                for j in other:
                    if V.is_prefix(i,j):
                        expand.elem_expansion(tree_expand.index(i))
                        broken = True
                        break
                if broken: break
            if broken: break

        new_R = []
        
        for leaf in a_copy.D:
            new_R.append(b_copy.apply(a_copy.apply(leaf)))
            
        return V(a_copy.D, new_R) 

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

    def classify(self):
        # very WIP
        #returns leaf type. 9 types
        
        chains = Chains.generate_chains(self)

        for ch in chains:
            if ch.type == "A":
                self.attractors.append((ch.chain[0], ch.chain[-1]))
            if ch.type == "R":
                self.repellers.append((ch.chain[0], ch.chain[-1]))
            if ch.type == "SS":
                self.sources_and_sinks.append((ch.chain[0], ch.chain[-1]))

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
    def make_revealing(self, function, g=None):
        # slow rolling algorithm
        chains = Chains.generate_chains(function)
        while not Chains.is_revealing(chains):
            chosen_sef = None
            chosen_ef = None
            chosen_sf = None

            if g == None:
                # debug 
                for chain in chains:
                    print(chain.chain, chain.type)
            else:
                time.sleep(2)
                g.clear_entities()
                g.add_entity(function)

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
            # print(len(function.D))
            chains = Chains.generate_chains(function)

