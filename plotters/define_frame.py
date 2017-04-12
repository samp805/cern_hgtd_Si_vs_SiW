import ROOT as root
import numpy as np

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












file_in = raw_input("root file:  ")
tf = root.TFile(file_in)
tree = tf.Get("tree")

num_entries = tree.GetEntriesFast()

print("number of entries: " + str(num_entries))

#CONFIG STUFF
LAYER = int(raw_input("layer:  "))
tungsten = False if tf.GetPath().startswith("without") else True

#define the frame based on plots from dT_dD
if LAYER == 0:
    #52% for 20 GeV, could be better
    if tungsten:
        hgtd_z = 3506.43
        x_min = -.18
        x_max = .005
        y_min = 0
        y_max = 14
    
    #50% for 20 GeV, could be better
    else:
        hgtd_z = 3516.93
        x_min = -.04
        x_max = .005
        y_min = 0
        y_max = 14

elif LAYER == 1: 
    #63% for 20GeV, not bad
    if tungsten:
        hgtd_z = 3518.12
        x_min = -.5
        x_max = .02
        y_min = 0
        y_max = 14
    #13% foor 20 GeV, terrible
    else:
        hgtd_z = 3525.12
        x_min = -.04
        x_max = .02
        y_min = 0
        y_max = 14

elif LAYER == 2: 
    #63% for 20 GeV, pretty good
    if tungsten:
        hgtd_z = 3529.83
        x_min = -.35
        x_max = .02
        y_min = 0
        y_max = 14
    #11% for 20 GeV, terrible 
    else:
        hgtd_z = 3533.33
        x_min = -.04
        x_max = .02
        y_min = 0
        y_max = 14

elif LAYER == 3: 
    hgtd_z = 3529.83
    #65% for 20 GeV, pretty good
    if tungsten:
        x_min = -.29
        x_max = .01
        y_min = 0
        y_max = 14
    #10% for 20 GeV, garbage 
    else:
        x_min = -.04
        x_max = .02
        y_min = 0
        y_max = 14

else:
    print("you got some error there homie")
    exit()

print(str(hgtd_z))
h = root.TH2F("h", "layer {0}".format(LAYER), 700, x_min, x_max, 700, y_min, y_max)

#count the fraction of hits you're including, define some vars to keep track
total_hits = 0
valid_hits = 0
included_hits = 0

try:
    for i in range(num_entries):
        tree.GetEntry(i)

        total_hits += tree.hgtd_nHits
        h_time = np.asarray(tree.hgtd_time)
        cut_indices = np.where(h_time[np.where(np.asarray(tree.hgtd_sampling) == LAYER)] < 1.3)
        scope = i
        if any(cut_indices[0]):
            valid_hits += len(cut_indices[0])
            tav = np.mean(h_time[cut_indices])
            e_r = (hgtd_z - tree.z) * 2 * np.exp(tree.eta) / (np.exp(2*tree.eta) - 1)
            e_x = e_r * np.cos(tree.phi)
            e_y = e_r * np.sin(tree.phi)
            for j in cut_indices[0]:
                
                h_x = _get_x(tree.hgtd_x[j]) if tf.GetPath() != "withoutWv5.root:/" else tree.hgtd_x[j]
                h_y = _get_y(tree.hgtd_y[j]) if tf.GetPath() != "withoutWv5.root:/" else tree.hgtd_y[j]

                dT = h_time[j] - tav
                dD = np.sqrt(np.power(e_x - h_x, 2) + np.power(e_y - h_y, 2))

                if h.Fill(dT, dD) != -1:
                    included_hits += 1
            if i % (num_entries/4) == 0:
                print("quart of the way done")
    print("ended on entry:  " + str(scope))
    h.Draw("COLZ")
    print("plotted {0} hits of {1} valid hits of {2} total hits".format(included_hits, valid_hits, total_hits))
    print("that is: {0}% of valid_hits, and {1}% of total hits".format(float(included_hits) / valid_hits * 100, float(included_hits) / total_hits * 100))
    #root.gPad.SetLogy()
    raw_input()

except KeyboardInterrupt:
    print("ended on entry:  " + str(scope))
    h.Draw("COLZ")
    #root.gPad.SetLogy()
    print("plotted {0} hits of {1} valid hits of {2} total hits".format(included_hits, valid_hits, total_hits))
    print("that is: {0}% of valid_hits, and {1}% of total hits".format(float(included_hits) / valid_hits * 100, float(included_hits) / total_hits * 100))
    raw_input()
