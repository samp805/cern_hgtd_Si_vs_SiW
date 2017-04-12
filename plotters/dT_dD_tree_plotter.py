import ROOT as root
import numpy as np


t_file = raw_input("root file (change program for v5):  ")
tf = root.TFile(t_file)
tree = tf.Get("tree")
total_entries = tree.GetEntriesFast()
max_entries = int(raw_input("max_entries (out of {0}:  ".format(total_entries))) if t_file.startswith("withW") else total_entries


#can't plot all layers at once because then you'd have too iterate thru the four layers because different hgtd_z
#so this file is pretty useless, but i'm gonna keep it because it has a stupid long command & is useful probably sometime
tree.Draw("sqrt(((3516 - z) * 2 * exp(eta) / (exp(2 * eta) - 1) * cos(phi) - sign(hgtd_x) * abs(.5*(hgtd_x - 1)))**2 + ((3516 - z) * 2 * exp(eta) / (exp(2 * eta) - 1) * sign(phi) - sign(hgtd_y) * abs(.5*(hgtd_y - 1)))**2):(hgtd_time - Sum$(hgtd_time)/Length$(hgtd_time))>>h(200,-1,.2,200,0,50)", "hgtd_time < 1.3", "COLZ", max_entries)

#tree.Draw("(sqrt(((3516 - z) * 2 * exp(eta) / (exp(2 * eta) - 1) * cos(phi) - hgtd_x)**2 + ((3516 - z) * 2 * exp(eta) / (exp(2 * eta) - 1) * sign(phi) - hgtd_y)**2)):(hgtd_time - Sum$(hgtd_time)/Length$(hgtd_time))>>h(200,-1,1,200,0,12)", "hgtd_time < 1.3", "COLZ")

raw_input()
