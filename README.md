# cern_hgtd_Si_vs_SiW
Code used to analyze the results of electron-electron collisions in the High Granularity Timing Detector. Explores the advantages/disadvantages of having the detector be just Si or SiW.

# My local code uses:
Python 2.7
gcc 5.4.0
ROOT 6.04/16


# USE LXPLUS, DONT MAKE THE SAME MISTAKE AS ME
    1. Running MVA regression and other extremely CPU intensive programs will take a shorter amount of time & won't slowly destroy your computer
    2. It's easy to grab useful tools from others (like the egamma packages blenzi made that I use)
    3. If you're picking up where I left off, you'll be dealing with lots of samples that include pileup. Processing these will take lots of time and storage.
    4. I never had to, but you'll probably have to use a cluster, and my guess is that it's easier to send jobs from lxplus.

The reason coding locally then switching to lxplus was such a pain was because I had the newest version of gcc, root, numpy, and mva on my computer, and lxplus uses old versions of all of those. So I had lots of compatibility issues, and I spent an inordinate amout of time debugging when I could've been progressing my work. Don't make the same mistake I did, develop on lxplus.

Have Bruno send you his lxplus's .bashrc or something. Just ask him about it.


# Stuff that might be confusing
    - with(out)W.root --> original beam data with electron momentum 20 GeV
    - with(out)Wv2.root --> flat electron momentum ranging from 20 GeV to 100 GeV (you train on this one)
    - with(out)Wv3.root --> 100 GeV
    - with(out)Wv4.root --> 45 GeV
    - withoutWv5.root --> 45 GeV with pileup deposited around the electron(s) in the event

You don't see these files in this repo because they're too large, but I refer to them in my code a lot. Sometimes I refer to the energies they correspond to as v2, v3, v4 but other times I use the actual energy itself (like in applied results below).


# Explanation of different energies (max_energy, combined2_energy, etc)
To reduce noise, we want to take the energy in the calorimeter to as small of area as possible. At the same time, we want the detection efficiency to be as close to unity as possible. I test a range of clusters: one tower (max energy), 2 adjacent towers (combined2_energy), 4 (2x2 square) adjacent towers (combined4_energy), and 9 (3x3 square) adjacent towers (combined9_towers). You'll find that combined9_towers often performs the best in detection efficiency, but keep in mind when you have pileup it'll also have the most noise.

# applied_results/
    - These root files are the outputs of applying the weights from your MVA boosted regression tree training
    - The filename scheme is applied_{hgtd||noHGTD}_{target_energy}_{withW||withoutW}{pt_of_electron}.root
    - I was investigating the benefit of including HGTD data as variables in the MVA training, so that's why you have hgtd vs no HGTD. The conclusion was that including the HGTD did help (duh). Now we need to see if that's true for cases with pileup.
    - Just "root new TBrowser" to browse these files and get a feel. 
    - I recommend entering into a python shell session, and plotting from there at first. After you're comfortable with the quantity you want to plot, write a python script to run it for you.
    
# dT_dD/
    - These are plots of time spread (t_hit - t_avg) versus distance from electron (sqrt((e_x - h_x)^2 + (e_y - h_y)^2))
    - This is a 2D histogram with a "heatmap" showing you number of points in a specific binning
    - Use these plots to create a selection of hits in time and space to include only the most relevant hits in the HGTD
    - This is where I left off, so you'll probably have lots of questions about these plots

# from_lxplus/
    - As I mentioned in the previous section, I started coding locally then moved to lxplus once I started having to do regressions and applications a lot. These two files just helped me run them because there are so many command line arguments, and it's easier to automate all the regression & application at once rather than just changing the command slightly and rerunning.
    - calib_runner.sh is the script that defines and executes the MVA BDT regression (always train on the flat pt sample [v2])
    - egamma_runner.sh is the script that applies the output weights from the MVA BDT regression to the other samples

# old_gen_root_stuff/
    - Useful stuff might be hidden in here, but it's not likely. If some python file from tools/ isn't working, check here because it'll probably have an older version of it.

# plotters/
    - This directory contains the python code used to make plots of stuff. For example, the dT_dD directory is made by dT_dD_hist_plotter.py

# sample_roots/
    - I can't include all the root files because it'd be too large for github to handle, but I included one of each just so you know what the outputs of certain programs are.
    - analysis_tree_withW.root is the output of generate_roots.py.
    - applied_hgtd_combined2_energy_withW20GeV.root is the output of egamma_runner.sh in from_lxplus/
    - applied_noHGTD_combined2_energy_withW20GeV.root is the same thing but with no HGTD data included

# tools/
    - tools/python contains the bulk of my code, but it's also surrounded Bruno's code.
    - generate_roots.py will make analysis trees. This is what you'll run, everything else is just a dependancy of this.
    - If you want to peek at how I calculate the different energies, look at add_combined_*.py and add_max_energy.py
    - Some of my code in here is useless, sorry about that.

# xmls/
    - These are just the weights that get spit out from MVA training (from_lxplus/calib_runner.py)
    - You'll source from these in applying your regression to other samples. 

If you have any questions, and I'm pretty sure you will because, I admit, this code is very disorganized and dependancy-ridden, email me at samp805@gmail.com
