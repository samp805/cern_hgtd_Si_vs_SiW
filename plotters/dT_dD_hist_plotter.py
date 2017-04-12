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
h = root.TH2F("h", "layer {0}".format(LAYER), 700, -1, 1, 700, 0, 20)


if LAYER == 0:
    hgtd_z = 3516.93 if not tungsten else 3506.43
elif LAYER == 1: 
    hgtd_z = 3525.12 if not tungsten else 3518.12
elif LAYER == 2: 
    hgtd_z = 3533.33 if not tungsten else 3529.83
elif LAYER == 3: 
    hgtd_z = 3541.52 #this is actually true haha
else:
    print("you got some error there homie")
    exit()

print(str(hgtd_z))


try:
    for i in range(num_entries):
        tree.GetEntry(i)
        h_time = np.asarray(tree.hgtd_time)
        cut_indices = np.where(h_time[np.where(np.asarray(tree.hgtd_sampling) == LAYER)] < 1.3)
        scope = i
        if any(cut_indices[0]):
            tav = np.mean(h_time[cut_indices])
            e_r = (hgtd_z - tree.z) * 2 * np.exp(tree.eta) / (np.exp(2*tree.eta) - 1)
            e_x = e_r * np.cos(tree.phi)
            e_y = e_r * np.sin(tree.phi)
            for j in cut_indices[0]:
                h_x = _get_x(tree.hgtd_x[j]) if tf.GetPath() != "withoutWv5.root:/" else tree.hgtd_x[j]
                h_y = _get_y(tree.hgtd_y[j]) if tf.GetPath() != "withoutWv5.root:/" else tree.hgtd_y[j]

                dT = h_time[j] - tav
                dD = np.sqrt(np.power(e_x - h_x, 2) + np.power(e_y - h_y, 2))

                h.Fill(dT, dD)
            if i % (num_entries/4) == 0:
                print("quart of the way done")
    print("ended on entry:  " + str(scope))
    h.Draw("COLZ")
    #root.gPad.SetLogy()
    raw_input()

except KeyboardInterrupt:
    print("ended on entry:  " + str(scope))
    h.Draw("COLZ")
    #root.gPad.SetLogy()
    raw_input()
