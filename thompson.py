# import helper.py
from copy import deepcopy
import time
import random as rand
class V:
    # identity global
    iden = th.V(["0", "1"], ["0", "1"])

    def __init__(self, D=[], R=[]):
        self.D = D
        self.R = R
        self.validate()

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
        raise Exception("Cannot apply the function to a word not below the antichain. Cannot apply to: " + string )

    @classmethod
    def is_prefix(self, string1, string2):
        # returns true iff string1 is a prefix of string2
        if len(string1) >= len(string2): return False
        if string2[0:len(string1)] == string1:
            return True
        return False

    @classmethod
    def is_antichain(self, words):
        # checks if the given iterable of words is an antichain
        for i in words:
            for j in words:
                if i != j and self.is_prefix(i,j):
                    return False
        return True
       
    def elem_expansion(self, index):
        if index >= len(self.D):
            raise Exception("Cannot expand at index out of range.")

        #expanding in D
        elem = self.D[index]
        self.D.pop(index)
        self.D.insert(index, elem + "0")
        self.D.insert(index + 1, elem + "1")

        # expanding at image of in R
        elem = self.R[index]
        self.R.pop(index)
        self.R.insert(index, elem + "0")
        self.R.insert(index + 1, elem + "1")

    def elem_minimise(self, tuple0, tuple1):
        # reverses an elementary expansion
        # input is tuples of words of r and image
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
    def invert(self, a):
        return V(a.R, a.D)

    @classmethod
    def product(self, a, b):
        # returns minimal product
        # making copies to not change state of a,b
        # minimising first
        a_copy = deepcopy(a)
        a_copy.minimise()
        b_copy = deepcopy(b)
        b_copy.minimise()

        # while the 'middle' trees of the product are not equal
        while sorted(b_copy.D) != sorted(a_copy.R):

            # python doesnt have features for breaking out of nested loops
            broken = False
            for i in a_copy.R:
                for j in b_copy.D:
                    if V.is_prefix(i,j):
                        a_copy.elem_expansion(a_copy.R.index(i))
                        broken = True
                        break
                    if V.is_prefix(j,i):
                        b_copy.elem_expansion(b_copy.D.index(j))
                        broken = True
                        break
                if broken: break

        new_R = []

        for leaf in a_copy.D:
            new_R.append(b_copy.apply(a_copy.apply(leaf)))
            
        res = V(a_copy.D, new_R) 
        res.minimise()
        return res
    
    @classmethod
    def rev_product(self, a, b):
        # returns revealing product
        # making copies to not change state of a,b
        # minimising first

        a_copy = deepcopy(a)
        b_copy = deepcopy(b)
        a_copy.minimise()
        b_copy.minimise()

        # while the 'middle' trees (R of a and D of b) of the product are not equal
        while sorted(b_copy.D) != sorted(a_copy.R):

            # python doesnt have features for breaking out of nested loops
            broken = False
            for i in a_copy.R:
                for j in b_copy.D:
                    if V.is_prefix(i,j):
                        a_copy.elem_expansion(a_copy.R.index(i))
                        broken = True
                        break
                    if V.is_prefix(j,i):
                        b_copy.elem_expansion(b_copy.D.index(j))
                        broken = True
                        break
                if broken: break

        new_R = []

        for leaf in a_copy.D:
            new_R.append(b_copy.apply(a_copy.apply(leaf)))
            
        res = V(a_copy.D, new_R) 
        Chains.make_revealing(res)
        return res

    @classmethod
    def conjugate(self, g, c):
        # returns c^-1 g c (right actions for now)
        return self.product(self.product(self.invert(c), g), c)
    
    @classmethod 
    def is_equal(self, a, b):
        a_copy = deepcopy(a)
        a_copy.minimise()
        b_copy = deepcopy(b)
        b_copy.minimise()

        return (a_copy.D == b_copy.D and a_copy.R == b_copy.R)

    def get_d_not_r(self):
        return [d for d in self.D if d not in self.R]

    def get_r_not_d(self):
        return [r for r in self.R if r not in self.D]

    def get_neutral_leaves(self):
        return [leaf for leaf in self.D if leaf in self.R]
    
    # def get_connected_components(self):
        # # I worked really hard on this and thought it was very clever but it was very unnecessary.
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

    @classmethod
    def DFS_to_antichain(self, dfs):
        achain = [""]
        current_word = ""
        stack = []
        for s in dfs:
            # print(achain, current_word, stack)
            if s == '1':
                achain.remove(current_word)
                achain.append(current_word + "0")
                achain.append(current_word + "1")
                stack.append(current_word + "1")
                current_word += "0"
            else:
                if len(stack) == 0:
                    break
                current_word = stack.pop()
        return achain

    # methods for testing on random antichains
    @classmethod
    def generate_random_antichain(self, length):
        achain = [""]
        while(len(achain) < length):
            chosen = rand.choice(achain)
            achain.remove(chosen)
            achain.append(chosen + "0")
            achain.append(chosen + "1")
        return achain

    @classmethod
    def generate_random_elements(self, size=10, n=1):
        elements = []
        for i in range(n):
            achain_D = self.generate_random_antichain(size)
            achain_D.sort()
            achain_R = self.generate_random_antichain(size)
            rand.shuffle(achain_R)
            elements.append(V(achain_D, achain_R))
        return elements

    def slow_rolling(self, chain):
        # adds a carrot(caret) for each word in the chain
        length = len(chain.chain)
        starting = chain.chain[0]
        for word in chain.chain[:-1]:
            index = self.D.index(word)
            # print("expanding at " + str(index))
            self.elem_expansion(index)
        return (Chain.generate_chain(starting + "0", self, length), Chain.generate_chain(starting + "1", self, length))
 

class Chain:
    # Individual chains formally presented as a tuple (iterated augmentation chain, label)
    def __init__(self, starting_point, function):
        self.chain = [] 
        self.type = ""

    def classify(self, function):
        # classifies the chain into types

        # print(self.chain)
        d_union_r = function.D + function.R
        d_intersect_r= function.get_neutral_leaves()
        self.type = "SS"
        if len(self.chain) == 0:
            # can't classify and ungenerated chain
            raise Exception("Attempting to classify empty chain.")
        
        # periodic chain
        if self.chain[0] == self.chain[-1]:
            self.type = "P"
            return self.type

        # neutral chain
        if self.chain[0] in d_intersect_r or self.chain[-1] in d_intersect_r:
            self.type = "N"
            return self.type

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
    def generate_chain(self, starting_point, function, length=None):
        # This function is the intended way to use Chain class, but pythons lack of private constructors doesn't let me block direct usage. Please don't instantiate Chain directly. This returns a classified Chain type object

        ch = Chain(starting_point, function)
        neutral_leaves = function.get_neutral_leaves()
        current_length = 0

        # applies function to the starting_point until the result isn't a neutral leaf, then returns the Chain of results
        ch.chain.append(starting_point)
        current_length += 1
        current = function.apply(starting_point)
        ch.chain.append(current)
        while current in neutral_leaves:
            # detects P type chains, but this functionality is usually unused as starting_point is intended to be a non-neutral leaf.
            if current == starting_point:
                self.type = "P"
                break
            if length != None and current_length == length:
                # if length was given cuts the chain to be the desired length
                break
            current = function.apply(current)
            ch.chain.append(current)
            current_length += 1
        ch.classify(function)

        return ch

    def slow_rolling(self, function):
        # adds a carrot(caret) for each word in the chain
        length = len(self.chain)
        starting = self.chain[0]
        for word in self.chain[:-1]:
            index = function.D.index(word)
            # print("expanding at " + str(index))
            function.elem_expansion(index)
        return (self.generate_chain(starting + "0", function, length), self.generate_chain(starting + "1", function, length))
        
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
    def is_revealing(self, function):
        chains = self.generate_chains(function)
        if len(chains) == 0:
            raise Exception("Chain must be generated to be revealing")
        
        types = [chain.type for chain in chains]
       
        # returns false if types contain any fragmentation labels
        return not ("SEF" in types or "SF" in types or "EF" in types)

    @classmethod
    def make_revealing(self, function, g=None, debug=False):
        stack = []

        # checks if its already revealing
        if self.is_revealing(function):
            print("Already revealing")
            return

        # minimises 
        function.minimise()
        # slow rolling algorithm
        chains = Chains.generate_chains(function)
        # print(Chains.is_revealing(chains))
        while not Chains.is_revealing(function):
            if debug:
                print("chains")
                for chain in chains:
                    print(chain.chain, chain.type)
            elif g != None:
                # animates the make_revealing process on screen
                g.clear_entities()
                g.add_entity(function)
                time.sleep(1)
                

            # if the stack is empty (the start of a big step, that concludes when the stack is empty again.)
            if len(stack) == 0:
                for ch in chains: 
                    if ch.type in ["SEF", "SF", "EF"]:
                        # print(ch.chain, ch.type)
                        stack.append(ch)
                        break

            # expand the chosen chain until the fragmentation is entirely mergable.
            while len(stack) != 0:
                # print([(s.chain, s.type) for s in stack])
                chosen = stack.pop()
                # print(chosen.chain, chosen.type)
                l_expansion, r_expansion = chosen.slow_rolling(function)
                if l_expansion.type in ["SEF", "SF", "EF"]:
                    stack.append(l_expansion)
                if r_expansion.type in ["SEF", "SF", "EF"]:
                    stack.append(r_expansion)
                
            # regenerating the chains (implicity merges our N chains away)
            chains = Chains.generate_chains(function)
