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


    # def check_revealing(self):
        # # TODO check revealing
        # connected_components = self.get_connected_components()
        
    # # def verify_revealing(self):
        # # to_check = [i for i in self.D]
        # # endpoints = []

        # # for node in to_check:
            # # prev = [] 
            # # theta = node
            # # prev.append(theta)

            # # print(theta)
            # # theta = self.apply(theta)

            # # while theta not in endpoints:
                # # print("Theta: " + theta)
                # # print(endpoints)
                # # if theta not in [i for i in self.D if i in self.R]:

                    # # for p in prev:
                        # # print("p: " + p)
                        # # if self.is_ancestor(theta, p):
                            # # endpoints.append(p)
                            # # endpoints.append(theta)
                            # # self.repellers.append(p)
                        # # elif self.is_ancestor(p, theta):
                            # # endpoints.append(p)
                            # # endpoints.append(theta)
                            # # self.attractors.append(p)

                    # # for d in self.D:
                        # # print("d: " + d)
                        # # if self.is_ancestor(d,theta):
                            # # self.elem_expansion(self.R.index(theta))
                            # # print("roll back")
                            # # return False

                        # # elif self.is_ancestor(theta, d):
                            # # self.elem_expansion(self.D.index(d))
                            # # print("roll forward")
                            # # return False

                # # else:
                    # # if theta in prev:
                        # # break

                # # prev.append(theta)
                # # if theta not in endpoints:
                    # # theta = self.apply(theta)
        # # return True

        # # for d in self.D:
            # # theta = d
            # # prev = []
            # # prev.append(theta)
            # # theta = self.apply(d)
            # # while theta in [i for i in self.D if i in self.R] or theta in self.attractors or theta in self.repellers:
                # # if (theta in prev): 
                    # # # periodic neutral points
                    # # break
                # # if (self.is_ancestor(theta, d)):
                    # # # repellers
                    # # self.repellers.append(d)
                # # if (self.is_ancestor(d, theta)):
                    # # #attractors
                    # # self.attractors.append(d)
                # # prev.append(theta)
                # # theta = self.apply(d)
                # # print(theta)

            # # if (theta not in [i for i in self.D if i in self.R]):
                # # return theta

    # def rev_pair(self):

        # while self.verify_revealing() == False:
            # print("done")
            # print(v.D, v.R)
            # time.sleep(1)

        # # to_expand = self.verify_revealing()
        # # while to_expand != None:
            # # print("to_expand: " + to_expand)
            # # expanded = False
            # # for d in self.D:
                # # print(d)
                # # if self.is_ancestor(d, to_expand): 
                    # # print("poop")
                    
                    # # # for i in range(len(to_expand) - len(d)):
                    # # self.elem_expansion(self.D.index(d))
                    # # expanded = True
                    # # break
            # # if not expanded:
                # # for r in self.R:
                    # # print(r)
                    # # if self.is_ancestor(r, to_expand): 
                        # # print("poop")
                        
                        # # # for i in range(len(to_expand) - len(d)):
                        # # self.elem_expansion(self.R.index(r))
                        # # break
            # # print(v.D, v.R)
            # # time.sleep(1)
            # # to_expand = self.verify_revealing()


