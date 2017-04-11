import numpy as np
from add_combined import AddCombined
import utils

class AddCombined2Towers(AddCombined):
    def add(self):
        combined_energy = np.zeros(1, dtype=float)
        self._target.Branch('combined2_energy', combined_energy, 'combined2_energy/D')

        #loop & load the entries
        for i in range(self._source.GetEntries()):
            self._source.GetEntry(i)
            
            west_index = utils.get_west(self._max_index[i])
            east_index = utils.get_east(self._max_index[i])
            north_index = utils.get_north(self._max_index[i], self._source.towerE.size())
            south_index = utils.get_south(self._max_index[i], self._source.towerE.size())
            
            west_energy = self._source.towerE[west_index] if west_index is not None else 0
            east_energy = self._source.towerE[east_index] if east_index is not None else 0
            north_energy = self._source.towerE[north_index]
            south_energy = self._source.towerE[south_index]
            
            max_adjacent = max(west_energy, east_energy, north_energy, south_energy)
            
            combined_energy[0] = self._source.towerE[self._max_index[i]] + max_adjacent
            self._target.Fill()
