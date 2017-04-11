import numpy as np

class AddMaxEnergy():
    def __init__(self, source, target):
        self._source = source
        self._target = target
        self._max_index = []

    def add(self):
        max_energy = np.zeros(1, dtype=float)
        self._target.Branch('max_energy', max_energy, 'max_energy/D')
        for i in range(self._source.GetEntries()):
            #load the entry
            self._source.GetEntry(i)
            
            #get the index of the max & min energy in each event
            self._max_index.append(list(self._source.towerE).index(max(self._source.towerE)))

            max_energy[0] = self._source.towerE[self._max_index[i]]
            self._target.Fill()
            
    def get_max_indicies(self):
        return self._max_index