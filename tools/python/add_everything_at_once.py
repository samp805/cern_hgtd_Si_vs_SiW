import math
import numpy as np
import time
import sys
import utils
import ROOT as root

class AddAllEnergy():
    def __init__(self, source, target, ext):
        self._source = source
        self._target = target
        self._ext = ext
        self._max_index = []

    def add_everything(self):
        #add variables from the original tree for later use
        pt = np.zeros(1, dtype=float)
        self._target.Branch('pt', pt, 'pt/D')
        
        eta = np.zeros(1, dtype=float)
        self._target.Branch('eta', eta, 'eta/D')

        hgtd_hits = np.zeros(1, dtype=float)
        self._target.Branch('hgtd_hits', hgtd_hits, 'hgtd_hits/D')

        hgtd_sumE = np.zeros(1, dtype=float)
        self._target.Branch('hgtd_sumE', hgtd_sumE, 'hgtd_sumE/D')

        #make the different energies
        max_energy = np.zeros(1, dtype=float)
        self._target.Branch('max_energy', max_energy, 'max_energy/D')

        combined2_energy = np.zeros(1, dtype=float)
        self._target.Branch('combined2_energy', combined2_energy, 'combined2_energy/D')
        
        combined4_energy = np.zeros(1, dtype=float)
        self._target.Branch('combined4_energy', combined4_energy, 'combined4_energy/D')
        
        combined9_energy = np.zeros(1, dtype=float)
        self._target.Branch('combined9_energy', combined9_energy, 'combined9_energy/D')
        
        #make the hgtd params
#===============================================================================
#         hgtd_eta = root.vector(float)()
#         self._target.Branch('hgtd_eta', hgtd_eta)        
# 
#         hgtd_phi = root.vector(float)()
#         self._target.Branch("hgtd_phi", hgtd_phi)
#===============================================================================
        selected_hgtd_energy = np.zeros(1, dtype = float)
        self._target.Branch('selected_hgtd_energy', selected_hgtd_energy, 'selected_hgtd_energy/D')
        hgtd_energy_selection = 0
        eta_diff_mean = []
        eta_diff_mean.append([])
        eta_diff_mean.append([])
        eta_diff_mean.append([])
        eta_diff_mean.append([])
        
        eta_diff_std = []
        eta_diff_std.append([])
        eta_diff_std.append([])
        eta_diff_std.append([])
        eta_diff_std.append([])
        
        t0 = time.time()
        BLIND_CUT = 1.3 #ns, time to include before this number 
        
        for i in range(self._source.GetEntries()):
            #load the entry
            self._source.GetEntry(i)
            
            #--------Original variables----------#
            pt[0] = self._source.pt
            eta[0] = self._source.eta
            hgtd_hits[0] = self._source.hgtd_nHits
            hgtd_sumE[0] = sum(self._source.hgtd_e) #eventually will replace this cuz pileup
            
            #-------MAX ENERGY------------#
            self._max_index.append(list(self._source.towerE).index(max(self._source.towerE)))

            max_energy[0] = self._source.towerE[self._max_index[i]]

            #-----------COMBINED2_ENERGY--------------#
    
            west_index = utils.get_west(self._max_index[i])
            east_index = utils.get_east(self._max_index[i])
            north_index = utils.get_north(self._max_index[i], self._source.towerE.size())
            south_index = utils.get_south(self._max_index[i], self._source.towerE.size())
            
            west_energy = self._source.towerE[west_index] if west_index is not None else 0
            east_energy = self._source.towerE[east_index] if east_index is not None else 0
            north_energy = self._source.towerE[north_index]
            south_energy = self._source.towerE[south_index]
            
            max_adjacent = max(west_energy, east_energy, north_energy, south_energy)
            
            combined2_energy[0] = self._source.towerE[self._max_index[i]] + max_adjacent
    
            #-----------COMBINED4_ENERGY--------------#
    
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
                combined4_energy[0] = max(ne_max, se_max)
                
            elif mat["e"] is None:
                mat["nw"] = utils.get_north(mat["w"], self._source.towerE.size())
                mat["sw"] = utils.get_south(mat["w"], self._source.towerE.size())
                nw_max = sum([self._source.towerE[self._max_index[i]], self._source.towerE[mat["n"]], self._source.towerE[mat["w"]], self._source.towerE[mat["nw"]]])
                sw_max = sum([self._source.towerE[self._max_index[i]], self._source.towerE[mat["s"]], self._source.towerE[mat["w"]], self._source.towerE[mat["sw"]]])
                combined4_energy[0] = max(nw_max, sw_max)
                
            else:
                mat["nw"] = utils.get_north(mat["w"], self._source.towerE.size())
                mat["ne"] = utils.get_north(mat["e"], self._source.towerE.size())
                mat["sw"] = utils.get_south(mat["w"], self._source.towerE.size())
                mat["se"] = utils.get_south(mat["e"], self._source.towerE.size())
                nw_max = sum([self._source.towerE[self._max_index[i]], self._source.towerE[mat["n"]], self._source.towerE[mat["w"]], self._source.towerE[mat["nw"]]])
                ne_max = sum([self._source.towerE[self._max_index[i]], self._source.towerE[mat["n"]], self._source.towerE[mat["e"]], self._source.towerE[mat["ne"]]])
                sw_max = sum([self._source.towerE[self._max_index[i]], self._source.towerE[mat["s"]], self._source.towerE[mat["w"]], self._source.towerE[mat["sw"]]])
                se_max = sum([self._source.towerE[self._max_index[i]], self._source.towerE[mat["s"]], self._source.towerE[mat["e"]], self._source.towerE[mat["se"]]])
                combined4_energy[0] = max(nw_max, ne_max, sw_max, se_max)

            #-----------COMBINED9_ENERGY--------------#
            square = self._get_index_dictionary(self._max_index[i], self._source.towerE.size())
            
            top_sum = sum([self._source.towerE[square["n"]], self._source.towerE[square["ne"]], self._source.towerE[square["nw"]]])
            middle_sum = sum([self._source.towerE[square["m"]], self._source.towerE[square["w"]], self._source.towerE[square["e"]]])
            bottom_sum = sum([self._source.towerE[square["s"]], self._source.towerE[square["sw"]], self._source.towerE[square["se"]]])
            
            combined9_energy[0] = sum([top_sum, middle_sum, bottom_sum])
            
            #--------------HGTD PARAMS------------------#
            #===================================================================
            # for j in range(self._source.hgtd_nHits):
            #     hgtd_eta.push_back(self._get_eta(self._source.hgtd_x[j], self._source.hgtd_y[j], self._source.hgtd_sampling[j]))
            #     hgtd_phi.push_back(self._get_phi(self._source.hgtd_x[j], self._source.hgtd_y[j]))
            #===================================================================
            
            #needs more sophisticated checking of NaN values
            if self._source.hgtd_nHits != 0:            
                eta_h = []
                eta_diff = []
                
                phi_h = []
                phi_diff = []
                
                r_diff = []
                
                sample_bools = []
                
                #defining the cut/selection
                mean_t = np.mean(self._source.hgtd_time)
                std_t = np.std(self._source.hgtd_time)
                selection = np.asarray(map(lambda x : x < BLIND_CUT and x > (mean_t - 2 * std_t) and x < (mean_t + 2 * std_t), np.asarray(self._source.hgtd_time)))
                h_x = np.asarray(self._source.hgtd_x)[selection]
                h_y = np.asarray(self._source.hgtd_y)[selection]
                h_sample = np.asarray(self._source.hgtd_sampling)[selection]
                h_e = 0

                #zeroth layer
                sample_bools.append(np.asarray(map(lambda x : x == 0, h_sample)))
                if any(sample_bools[0]):
                    eta_h.append(np.asarray(map(self._get_eta, h_x[sample_bools[0]], h_y[sample_bools[0]], 0 + np.zeros(len(h_x[sample_bools[0]])))))
                    eta_diff.append(self._source.eta - eta_h[0])
                    
                    phi_h.append(np.asarray(map(self._get_phi, h_x[sample_bools[0]], h_y[sample_bools[0]])))
                    phi_diff.append(self._source.phi - phi_h[0])
                    
                    r_diff.append(np.asarray(map(lambda x,y : np.sqrt(np.power(x,2) + np.power(y,2), eta_diff[0], phi_diff[0]))))
                    
                    h_e += sum(np.asarray(self._source.hgtd_energy)[np.asarray(map(lambda x : x < (np.mean(r_diff[0])+ 2 * np.std(r_diff[0])) and x < (eta_diff_mean[0][i] - 2 * eta_diff_std[0][i], eta_diff[0])))])

                    #first layer
                    sample_bools.append(np.asarray(map(lambda x : x == 1, h_sample)))
                    if any(sample_bools[1]):
                        eta_h.append(np.asarray(map(self._get_eta, h_x[sample_bools[1]], h_y[sample_bools[1]], 1 + np.zeros(len(h_x[sample_bools[1]])))))
                        eta_diff.append(self._source.eta - eta_h[1])
                        eta_diff_mean[1].append(np.mean(eta_diff[1]))
                        eta_diff_std[1].append(np.std(eta_diff[1]))
                        h_e += sum(np.asarray(self._source.hgtd_energy)[np.asarray(map(lambda x : x < (eta_diff_mean[1][i] + 2 * eta_diff_std[1][i]) and x < (eta_diff_mean[1][i] - 2 * eta_diff_std[1][i], eta_diff[1])))])

                        #second layer
                        sample_bools.append(np.asarray(map(lambda x : x == 2, h_sample)))
                        if any(sample_bools[2]):
                            eta_h.append(np.asarray(map(self._get_eta, h_x[sample_bools[2]], h_y[sample_bools[2]], 2 + np.zeros(len(h_x[sample_bools[2]])))))
                            eta_diff.append(self._source.eta - eta_h[2])
                            eta_diff_mean[2].append(np.mean(eta_diff[2]))
                            eta_diff_std[2].append(np.std(eta_diff[2]))
                            h_e += sum(np.asarray(self._source.hgtd_energy)[np.asarray(map(lambda x : x < (eta_diff_mean[2][i] + 2 * eta_diff_std[2][i]) and x < (eta_diff_mean[2][i] - 2 * eta_diff_std[2][i], eta_diff[2])))])

                            #third layer
                            sample_bools.append(np.asarray(map(lambda x : x == 3, h_sample)))
                            if any(sample_bools[3]):
                                eta_h.append(np.asarray(map(self._get_eta, h_x[sample_bools[3]], h_y[sample_bools[3]], 3 + np.zeros(len(h_x[sample_bools[3]])))))
                                eta_diff.append(self._source.eta - eta_h[3])
                                eta_diff_mean[3].append(np.mean(eta_diff[3]))
                                eta_diff_std[3].append(np.std(eta_diff[3]))
                                h_e += sum(np.asarray(self._source.hgtd_energy)[np.asarray(map(lambda x : x < (eta_diff_mean[3][i] + 2 * eta_diff_std[3][i]) and x < (eta_diff_mean[3][i] - 2 * eta_diff_std[3][i], eta_diff[3])))])
        
            selected_hgtd_energy[0] = h_e
            
            if i %  int(90008/10) == 0 and i != 0:
                sys.stdout.write("runtime after a(nother) tenth:  {0} minutes\n".format((time.time() - t0)/60))
                sys.stdout.flush()
            
            #Finally, we fill
            self._target.Fill()
            h_e = 0
            #===================================================================
            # hgtd_eta.clear()
            # hgtd_phi.clear()
            #===================================================================
        
        tf = time.time()
        print("took {0} minutes".format(str((tf-t0)/60)))
        print()
        
        print("Zeroth Layer Overal Stats")
        print("Mean:  {0}  |||||  Std:  {1}".format(np.mean(eta_diff_mean[0]), np.std(eta_diff_mean[0])))
        print()
        print("First Layer Overal Stats")
        print("Mean:  {0}  |||||  Std:  {1}".format(np.mean(eta_diff_mean[1]), np.std(eta_diff_mean[1])))
        print()
        print("Second Layer Overal Stats")
        print("Mean:  {0}  |||||  Std:  {1}".format(np.mean(eta_diff_mean[2]), np.std(eta_diff_mean[2])))
        print()
        print("Third Layer Overal Stats")
        print("Mean:  {0}  |||||  Std:  {1}".format(np.mean(eta_diff_mean[3]), np.std(eta_diff_mean[3])))
        print()
        
    def _get_x(self, x):
        '''given the cell number, returns x position in mm'''
        return np.sign(x) * np.abs(.5 * (x - 1))
    
    def _get_y(self, y):
        '''given the cell number, returns y position in mm'''
        return np.sign(y) * np.abs(.5 * (y - 1))

    def _get_eta(self, x, y, sample): 
        if x is None or y is None or sample is None:
            print("you got a no entry...quitting")
            exit()
        xp = self._get_x(x)
        yp = self._get_y(y)
        if self._ext.startswith("withW"):
            if sample == 0:
                zp = 3516.93
            elif sample == 1:
                zp = 3525.12
            elif sample == 2:
                zp = 3533.33
            elif sample == 3:
                zp = 3541.52
            else:
                print("something wrong with sample, did the HGTD get more layers???")
                exit()

        elif self._ext.startswith("withoutW"):
            if sample == 0:
                zp = 3506.43
            elif sample == 1:
                zp = 3518.12
            elif sample == 2:
                zp = 3529.83
            elif sample == 3:
                zp = 3541.52
            else:
                print("something wrong with sample, did the HGTD get more layers???")
                exit()
        else:
            print("did you rename your rootfiles or something?")
            exit()
         
        #super duper unlikely that xp & yp will both be zero
        if xp == 0:
            return np.arcsinh(zp/yp)
        elif yp == 0:
            return np.arcsinh(zp/xp)
        else:
            return np.arcsinh(zp/np.sqrt(np.power(xp, 2) + np.power(yp,2)))
 
    def _get_phi(self, x, y):
        xp = np.sign(x)*np.abs(.5*(x-1))
        yp = np.sign(y)*np.abs(.5*(y-1))
     
        if xp == 0:
            return np.pi / 2 if yp > 0 else -np.pi / 2
        else:
            return np.sign(yp) * np.arctan(yp/xp)
        
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


def _get_x(x):
    '''given the cell number, returns x position in mm'''
    return np.sign(x) * np.abs(.5 * (x - 1))

def _get_y(y):
    '''given the cell number, returns y position in mm'''
    return np.sign(y) * np.abs(.5 * (y - 1))

def _get_eta_with(x, y, sample): 
    if x is None or y is None or sample is None:
        print("you got a no entry...quitting")
        exit()
    xp = _get_x(x)
    yp = _get_y(y)
    if sample == 0:
        zp = 3516.93
    elif sample == 1:
        zp = 3525.12
    elif sample == 2:
        zp = 3533.33
    elif sample == 3:
        zp = 3541.52
    else:
        print("something wrong with sample, did the HGTD get more layers???")
        exit()
     
    #super duper unlikely that xp & yp will both be zero
    if xp == 0:
        return np.arcsinh(zp/yp)
    elif yp == 0:
        return np.arcsinh(zp/xp)
    else:
        return np.arcsinh(zp/np.sqrt(np.power(xp, 2) + np.power(yp,2)))
    
def _get_eta_without(x, y, sample): 
    if x is None or y is None or sample is None:
        print("you got a no entry...quitting")
        exit()
    xp = _get_x(x)
    yp = _get_y(y)
    if sample == 0:
        zp = 3506.43
    elif sample == 1:
        zp = 3518.12
    elif sample == 2:
        zp = 3529.83
    elif sample == 3:
        zp = 3541.52
    else:
        print("something wrong with sample, did the HGTD get more layers???")
        exit()
     
    #super duper unlikely that xp & yp will both be zero
    if xp == 0:
        return np.arcsinh(zp/yp)
    elif yp == 0:
        return np.arcsinh(zp/xp)
    else:
        return np.arcsinh(zp/np.sqrt(np.power(xp, 2) + np.power(yp,2)))

def _get_phi(x, y):
    xp = np.sign(x)*np.abs(.5*(x-1))
    yp = np.sign(y)*np.abs(.5*(y-1))
 
    if xp == 0:
        return np.pi / 2 if yp > 0 else -np.pi / 2
    else:
        return np.sign(yp) * np.arctan(yp/xp)
 
#===============================================================================
#         
# 
#             #make faster
#             
#             #need stratified handling to make selection circles progressively (2**n) bigger
#             for j in range(self._source.hgtd_nHits):
#                 
#                 if self._source.hgtd_sampling[j] == 0:
#                     tolerance = .00001
#                     eta_p = self._get_eta(self._source.hgtd_x[j], self._source.hgtd_y[j], self._source.hgtd_sampling[j])
#                     if np.abs(eta_p - self._source.eta) < tolerance:
#                         hgtd_energy_selection += self._source.hgtd_e[j]
#                         eta_arr[0][j] = eta_p
#                     else:
#                         eta_arr[0][j] = None
#                     phi_arr[0][j] = self._get_phi(self._source.hgtd_x[j], self._source.hgtd_y[j])
#                     
#                
#                 elif self._source.hgtd_sampling[j] == 1:
#                     tolerance = .00002
#                     eta_p = self._get_eta(self._source.hgtd_x[j], self._source.hgtd_y[j], self._source.hgtd_sampling[j])
#                     if np.abs(eta_p - self._source.eta) < tolerance:
#                         hgtd_energy_selection += self._source.hgtd_e[j]
#                         eta_arr[1][j] = eta_p
#                     else:
#                         eta_arr[1][j] = None
#                     phi_arr[1][j] = self._get_phi(self._source.hgtd_x[j], self._source.hgtd_y[j])
#                
#                 
#                 elif self._source.hgtd_sampling[j] == 2:
#                     tolerance = .00004
#                     eta_p = self._get_eta(self._source.hgtd_x[j], self._source.hgtd_y[j], self._source.hgtd_sampling[j])
#                     if np.abs(eta_p - self._source.eta) < tolerance:
#                         hgtd_energy_selection += self._source.hgtd_e[j]
#                         eta_arr[2][j] = eta_p
#                     else:
#                         eta_arr[2][j] = None
#                     phi_arr[2][j] = self._get_phi(self._source.hgtd_x[j], self._source.hgtd_y[j])
#                 
#                 
#                 elif self._source.hgtd_sampling[j] == 3:
#                     tolerance = .00008
#                     eta_p = self._get_eta(self._source.hgtd_x[j], self._source.hgtd_y[j], self._source.hgtd_sampling[j])
#                     if np.abs(eta_p - self._source.eta) < tolerance:
#                         hgtd_energy_selection += self._source.hgtd_e[j]
#                         eta_arr[3][j] = eta_p
#                     else:
#                         eta_arr[3][j] = None
#                     phi_arr[3][j] = self._get_phi(self._source.hgtd_x[j], self._source.hgtd_y[j])
#                 
#                 
#                 else:
#                     print("ERROR: MORE LAYERS??")
#===============================================================================