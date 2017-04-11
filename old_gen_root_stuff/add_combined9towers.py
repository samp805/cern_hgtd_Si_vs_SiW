import numpy as np
from add_combined import AddCombined
import utils

class AddCombined9Towers(AddCombined):
    def add(self):
        combined_energy = np.zeros(1, dtype=float)
        self._target.Branch('combined9_energy', combined_energy, 'combined9_energy/D')

        #loop & load the entries
        for i in range(self._source.GetEntries()):
            self._source.GetEntry(i)
            
            #this is 3x3, but we just need the maximum 2x2 part
            square = self._get_index_dictionary(self._max_index[i], self._source.towerE.size())
            
            top_sum = sum([self._source.towerE[square["n"]], self._source.towerE[square["ne"]], self._source.towerE[square["nw"]]])
            middle_sum = sum([self._source.towerE[square["m"]], self._source.towerE[square["w"]], self._source.towerE[square["e"]]])
            bottom_sum = sum([self._source.towerE[square["s"]], self._source.towerE[square["sw"]], self._source.towerE[square["se"]]])
            
            combined_energy[0] = sum([top_sum, middle_sum, bottom_sum])
            self._target.Fill()
            
    def _print_index_dictionary(self, max_index, d):
        print('''
        {0}  {1}  {2}                       {3}  {4}  {5}
        {6}  {7}  {8}  ------value--------> {9}  {10}  {11}
        {12}  {13}  {14}                       {15}  {16}  {17}
        '''.format(
            d["nw"], d["n"], d["ne"],         self._source.towerE[d["nw"]], self._source.towerE[d["n"]], self._source.towerE[d["ne"]],
            d["w"], d["m"], d["e"],         self._source.towerE[d["w"]], self._source.towerE[d["m"]], self._source.towerE[d["e"]],
            d["sw"], d["s"], d["se"],         self._source.towerE[d["sw"]], self._source.towerE[d["s"]], self._source.towerE[d["se"]]
            ))

    #this will be 3x3        
    def _get_index_dictionary(self, max_index, array_size):
        #mat = [3][3] --- i wish this syntax were valid but it's not
        mat = {}
        mat["m"] = max_index
        mat["w"] = utils.get_west(max_index)
        mat["e"] = utils.get_east(max_index)
        if mat["w"] is None:
            return self._get_index_dictionary(mat["e"], array_size, )
        elif mat["e"] is None:
            return self._get_index_dictionary(mat["w"], array_size, )

        mat["n"] = utils.get_north(max_index, array_size)
        mat["s"] = utils.get_south(max_index, array_size)
        
        mat["nw"] = utils.get_north(mat["w"], array_size)
        mat["ne"] = utils.get_north(mat["e"], array_size)
        mat["sw"] = utils.get_south(mat["w"], array_size)
        mat["se"] = utils.get_south(mat["e"], array_size)
        
        return mat