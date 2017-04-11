import numpy as np
from add_combined import AddCombined
import utils

class AddCombined4Towers(AddCombined):
    def add(self):
        combined_energy = np.zeros(1, dtype=float)
        self._target.Branch('combine4_energy', combined_energy, 'combined4_energy/D')

        #loop & load the entries
        for i in range(self._source.GetEntries()):
            self._source.GetEntry(i)
            
            mat = {}
            mat["w"] = utils.get_west(self._max_index[i])
            mat["e"] = utils.get_east(self._max_index[i])
            mat["n"] = utils.get_north(self._max_index[i], self._source.towerE.size())
            mat["s"] = utils.get_south(self._max_index[i], self._source.towerE.size()
                                       )
            if mat["w"] is None:
                mat["ne"] = utils.get_north(mat["e"], self._source.towerE.size())
                mat["se"] = utils.get_south(mat["e"], self._source.towerE.size())
                ne_max = sum([self._source.towerE[self._max_index[i]], self._source.towerE[mat["n"]], self._source.towerE[mat["e"]], self._source.towerE[mat["ne"]]])
                se_max = sum([self._source.towerE[self._max_index[i]], self._source.towerE[mat["s"]], self._source.towerE[mat["e"]], self._source.towerE[mat["se"]]])
                combined_energy[0] = max(ne_max, se_max)
                
            elif mat["e"] is None:
                mat["nw"] = utils.get_north(mat["w"], self._source.towerE.size())
                mat["sw"] = utils.get_south(mat["w"], self._source.towerE.size())
                nw_max = sum([self._source.towerE[self._max_index[i]], self._source.towerE[mat["n"]], self._source.towerE[mat["w"]], self._source.towerE[mat["nw"]]])
                sw_max = sum([self._source.towerE[self._max_index[i]], self._source.towerE[mat["s"]], self._source.towerE[mat["w"]], self._source.towerE[mat["sw"]]])
                combined_energy[0] = max(nw_max, sw_max)
                
            else:
                mat["nw"] = utils.get_north(mat["w"], self._source.towerE.size())
                mat["ne"] = utils.get_north(mat["e"], self._source.towerE.size())
                mat["sw"] = utils.get_south(mat["w"], self._source.towerE.size())
                mat["se"] = utils.get_south(mat["e"], self._source.towerE.size())
                nw_max = sum([self._source.towerE[self._max_index[i]], self._source.towerE[mat["n"]], self._source.towerE[mat["w"]], self._source.towerE[mat["nw"]]])
                ne_max = sum([self._source.towerE[self._max_index[i]], self._source.towerE[mat["n"]], self._source.towerE[mat["e"]], self._source.towerE[mat["ne"]]])
                sw_max = sum([self._source.towerE[self._max_index[i]], self._source.towerE[mat["s"]], self._source.towerE[mat["w"]], self._source.towerE[mat["sw"]]])
                se_max = sum([self._source.towerE[self._max_index[i]], self._source.towerE[mat["s"]], self._source.towerE[mat["e"]], self._source.towerE[mat["se"]]])
                combined_energy[0] = max(nw_max, ne_max, sw_max, se_max)
            
            self._target.Fill()
            