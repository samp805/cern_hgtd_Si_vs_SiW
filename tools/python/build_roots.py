import ROOT as root
import numpy as np

class BuildRoots():
    def __init__(self, tree, ext):
        self._tree = tree
        self._root_file = ext
        self._max_index = []

    def build_max_energy(self):
        self._get_max_energy()

    def _get_max_energy(self):
        f = root.TFile("~/workspace/hgtd/rootfiles/max_energy_"+self._root_file, "update")
        t = root.TTree("max_energy_tree", "max energy tree")
        max_energy = np.zeros(1, dtype=float)
        t.Branch('max_energy', max_energy, 'max_energy/D')
        for i in range(self._tree.GetEntries()):
            #load the entry
            self._tree.GetEntry(i)
            
            #get the index of the max & min energy in each event
            self._max_index.append(list(self._tree.towerE).index(max(self._tree.towerE)))

            max_energy[0] = self._tree.towerE[self._max_index[i]]
            t.Fill()
            
        f.Write()
        f.Close()
        return t

    #this algorithm assumes that the tower with max energy in each event will be a part of the maximum combined energy
    #theoretically there's the case where two towers with smaller energy than the max will combine to be more than the 
        #tower of max energy & a tower next to it
    def build_combined2_energy(self):
        '''builds the combined tower energy sum
        nTowers is number of towers to be combined'''
        self._get_combined2_energy()
    
    def _get_combined2_energy(self): 
        f = root.TFile("~/workspace/hgtd/rootfiles/combined2_energy_"+self._root_file, "update")
        t = root.TTree("combined2_energy_tree", "combined2 energy tree")
        combined_energy = np.zeros(1, dtype=float)
        t.Branch('combined2_energy', combined_energy, 'combined2_energy/D')

        #loop & load the entries
        for i in range(self._tree.GetEntries()):
            self._tree.GetEntry(i)
            
            west_index = self._get_west(self._max_index[i])
            east_index = self._get_east(self._max_index[i])
            north_index = self._get_north(self._max_index[i], self._tree.towerE.size())
            south_index = self._get_south(self._max_index[i], self._tree.towerE.size())
            
            west_energy = self._tree.towerE[west_index] if west_index is not None else 0
            east_energy = self._tree.towerE[east_index] if east_index is not None else 0
            north_energy = self._tree.towerE[north_index]
            south_energy = self._tree.towerE[south_index]
            
            max_adjacent = max(west_energy, east_energy, north_energy, south_energy)
            
            #===================================================================
            # west_of_max_index = self._max_index[i] - 1 if self._max_index[i] % 64 != 0  else list(self._tree.towerE).index(min(self._tree.towerE)) #max_index is at west edge 
            # east_of_max_index = self._max_index[i] + 1 if self._max_index[i] % 64 != 63 else list(self._tree.towerE).index(min(self._tree.towerE)) #max_index is at east edge
            # north_of_max_index = self._max_index[i] - 64 if self._max_index[i] - 64 >= 0 else (self._tree.towerE.size() - 64) + self._max_index[i] #wraps around bottom to top (north) BUG HERE
            # south_of_max_index = self._max_index[i] + 64 if self._max_index[i] + 64 < self._tree.towerE.size() else self._max_index[i] % 64 #wraps around top to bottom (south)
            #===================================================================
             
            #===================================================================
            # print("towerE size:  " + str(self._tree.towerE.size()))
            # print("max index:  " + str(self._max_index[i]))
            # print("west index:  " + str(west_of_max_index))
            # print("east index:  " + str(east_of_max_index))
            # print("north index:  " + str(north_of_max_index))
            # print("south index:  " + str(south_of_max_index))
            # print("--------------------")
            #===================================================================
             
            
            
            #gets the index of the next_maximum energy
            #===================================================================
            # next_max_index = list(self._tree.towerE).index(max(self._tree.towerE[west_of_max_index], self._tree.towerE[east_of_max_index], self._tree.towerE[south_of_max_index], self._tree.towerE[north_of_max_index]))
            #===================================================================
            
            #===================================================================
            # #this will be nice to have for information & fact checking
            # west_next = True if next_max_index == west_of_max_index else False
            # east_next = True if next_max_index == east_of_max_index else False
            # south_next = True if next_max_index == south_of_max_index else False
            # north_next = True if next_max_index == north_of_max_index else False
            #===================================================================
            
            combined_energy[0] = self._tree.towerE[self._max_index[i]] + max_adjacent
            t.Fill()
        
        f.Write()
        f.Close()
        return t
        

    def build_combined4_energy(self):
        self._get_combined4_energy()

    def _get_combined4_energy(self):
        f = root.TFile("~/workspace/hgtd/rootfiles/combined4_energy_"+self._root_file, "update")
        t = root.TTree("combined4_energy_tree", "combined4 energy tree")
        combined_energy = np.zeros(1, dtype=float)
        t.Branch('combine4_energy', combined_energy, 'combined4_energy/D')

        #loop & load the entries
        for i in range(self._tree.GetEntries()):
            self._tree.GetEntry(i)
            
            #===================================================================
            # #this is 3x3, but we just need the maximum 2x2 part
            # square = self._get_index_dictionary(self._max_index[i], self._tree.towerE.size())
            # 
            # nw_max = sum([self._tree.towerE[self._max_index[i]], self._tree.towerE[square["n"]], self._tree.towerE[square["w"]], self._tree.towerE[square["nw"]]])
            # ne_max = sum([self._tree.towerE[self._max_index[i]], self._tree.towerE[square["n"]], self._tree.towerE[square["e"]], self._tree.towerE[square["ne"]]])
            # sw_max = sum([self._tree.towerE[self._max_index[i]], self._tree.towerE[square["s"]], self._tree.towerE[square["w"]], self._tree.towerE[square["sw"]]])
            # se_max = sum([self._tree.towerE[self._max_index[i]], self._tree.towerE[square["s"]], self._tree.towerE[square["e"]], self._tree.towerE[square["se"]]])
            #===================================================================
            
            mat = {}
            mat["w"] = self._get_west(self._max_index[i])
            mat["e"] = self._get_east(self._max_index[i])
            mat["n"] = self._get_north(self._max_index[i], self._tree.towerE.size())
            mat["s"] = self._get_south(self._max_index[i], self._tree.towerE.size()
                                       )
            if mat["w"] is None:
                mat["ne"] = self._get_north(mat["e"], self._tree.towerE.size())
                mat["se"] = self._get_south(mat["e"], self._tree.towerE.size())
                ne_max = sum([self._tree.towerE[self._max_index[i]], self._tree.towerE[mat["n"]], self._tree.towerE[mat["e"]], self._tree.towerE[mat["ne"]]])
                se_max = sum([self._tree.towerE[self._max_index[i]], self._tree.towerE[mat["s"]], self._tree.towerE[mat["e"]], self._tree.towerE[mat["se"]]])
                combined_energy[0] = max(ne_max, se_max)
                
            elif mat["e"] is None:
                mat["nw"] = self._get_north(mat["w"], self._tree.towerE.size())
                mat["sw"] = self._get_south(mat["w"], self._tree.towerE.size())
                nw_max = sum([self._tree.towerE[self._max_index[i]], self._tree.towerE[mat["n"]], self._tree.towerE[mat["w"]], self._tree.towerE[mat["nw"]]])
                sw_max = sum([self._tree.towerE[self._max_index[i]], self._tree.towerE[mat["s"]], self._tree.towerE[mat["w"]], self._tree.towerE[mat["sw"]]])
                combined_energy[0] = max(nw_max, sw_max)
                
            else:
                mat["nw"] = self._get_north(mat["w"], self._tree.towerE.size())
                mat["ne"] = self._get_north(mat["e"], self._tree.towerE.size())
                mat["sw"] = self._get_south(mat["w"], self._tree.towerE.size())
                mat["se"] = self._get_south(mat["e"], self._tree.towerE.size())
                nw_max = sum([self._tree.towerE[self._max_index[i]], self._tree.towerE[mat["n"]], self._tree.towerE[mat["w"]], self._tree.towerE[mat["nw"]]])
                ne_max = sum([self._tree.towerE[self._max_index[i]], self._tree.towerE[mat["n"]], self._tree.towerE[mat["e"]], self._tree.towerE[mat["ne"]]])
                sw_max = sum([self._tree.towerE[self._max_index[i]], self._tree.towerE[mat["s"]], self._tree.towerE[mat["w"]], self._tree.towerE[mat["sw"]]])
                se_max = sum([self._tree.towerE[self._max_index[i]], self._tree.towerE[mat["s"]], self._tree.towerE[mat["e"]], self._tree.towerE[mat["se"]]])
                combined_energy[0] = max(nw_max, ne_max, sw_max, se_max)
            
            t.Fill()
            
        f.Write()
        f.Close()
        return t

    def build_combined9_energy(self):
        self._get_combined9_energy()

    def _get_combined9_energy(self):
        f = root.TFile("~/workspace/hgtd/rootfiles/combined9_energy_"+self._root_file, "update")
        t = root.TTree("combined9_energy_tree", "combined9 energy tree")
        combined_energy = np.zeros(1, dtype=float)
        t.Branch('combined9_energy', combined_energy, 'combined9_energy/D')

        #loop & load the entries
        for i in range(self._tree.GetEntries()):
            self._tree.GetEntry(i)
            
            #this is 3x3, but we just need the maximum 2x2 part
            square = self._get_index_dictionary(self._max_index[i], self._tree.towerE.size())
            
            top_sum = sum([self._tree.towerE[square["n"]], self._tree.towerE[square["ne"]], self._tree.towerE[square["nw"]]])
            middle_sum = sum([self._tree.towerE[square["m"]], self._tree.towerE[square["w"]], self._tree.towerE[square["e"]]])
            bottom_sum = sum([self._tree.towerE[square["s"]], self._tree.towerE[square["sw"]], self._tree.towerE[square["se"]]])
            
            combined_energy[0] = sum([top_sum, middle_sum, bottom_sum])
            t.Fill()
            
        f.Write()
        f.Close()
        return t
        #=======================================================================
        # self._tree.GetEntry(43)
        # max_i = list(self._tree.towerE).index(max(self._tree.towerE))
        # self._print_index_dictionary(max_i, self._get_index_dictionary(max_i, self._tree.towerE.size()))
        #=======================================================================


    def _print_index_dictionary(self, max_index, d):
        print('''
        {0}  {1}  {2}                       {3}  {4}  {5}
        {6}  {7}  {8}  ------value--------> {9}  {10}  {11}
        {12}  {13}  {14}                       {15}  {16}  {17}
        '''.format(
            d["nw"], d["n"], d["ne"],         self._tree.towerE[d["nw"]], self._tree.towerE[d["n"]], self._tree.towerE[d["ne"]],
            d["w"], d["m"], d["e"],         self._tree.towerE[d["w"]], self._tree.towerE[d["m"]], self._tree.towerE[d["e"]],
            d["sw"], d["s"], d["se"],         self._tree.towerE[d["sw"]], self._tree.towerE[d["s"]], self._tree.towerE[d["se"]]
            ))

    #this will be 3x3        
    def _get_index_dictionary(self, max_index, array_size):
        #mat = [3][3] --- i wish this syntax were valid but it's not
        mat = {}
        mat["m"] = max_index
        mat["w"] = self._get_west(max_index)
        mat["e"] = self._get_east(max_index)
        if mat["w"] is None:
            return self._get_index_dictionary(mat["e"], array_size, )
        elif mat["e"] is None:
            return self._get_index_dictionary(mat["w"], array_size, )

        mat["n"] = self._get_north(max_index, array_size)
        mat["s"] = self._get_south(max_index, array_size)
        
        mat["nw"] = self._get_north(mat["w"], array_size)
        mat["ne"] = self._get_north(mat["e"], array_size)
        mat["sw"] = self._get_south(mat["w"], array_size)
        mat["se"] = self._get_south(mat["e"], array_size)
        
        return mat

        
    def _get_west(self, index):
        return index - 1 if index % 64 != 0  else None
    
    def _get_east(self, index):
        return index + 1 if index % 64 != 63 else None
        
    def _get_north(self, index, array_size):
        return index - 64 if index - 64 >= 0 else (array_size - 64) + index

    def _get_south(self, index, array_size):
        return index + 64 if index + 64 < array_size else index % 64
        
# Things this algorithm assumes
#   -