import ROOT as root

rootfile_dir = "~/workspace/hgtd/rootfiles/"

class FriendshipBuilder():
    def __init__(self, tree, ext):
        #ext should include the .root part
        self._tree = tree
        self._ext = ext

    def build_all(self):
        #self._initialize()
        self._build_max()
        self._build_combined2_energy()
        self._build_combined4_energy()
        self._build_combined9_energy()

    #===========================================================================
    # def _initialize(self):
    #     tf = root.TFile(rootfile_dir + self._ext)
    #     self._tree = tf.Get("tree")
    #     self._tree.GetEntries()
    #===========================================================================

    def _build_max(self):
        tfm = root.TFile(rootfile_dir + "max_energy_" + self._ext)
        tm = tfm.Get("max_energy_tree")
        tm.GetEntries()
        self._tree.AddFriend("max_energy_tree", rootfile_dir + "max_energy_" +self._ext)
        
    def _build_combined2_energy(self):
        tf2c = root.TFile(rootfile_dir + "combined2_energy_" +self._ext)
        t2c = tf2c.Get("combined2_energy_tree")
        t2c.GetEntries()
        self._tree.AddFriend("combined2_energy_tree", rootfile_dir + "combined2_energy_" +self._ext)
        
    def _build_combined4_energy(self):
        tf4c = root.TFile(rootfile_dir + "combined4_energy_" +self._ext)
        t4c = tf4c.Get("combined4_energy_tree")
        t4c.GetEntries()
        self._tree.AddFriend("combined4_energy_tree", rootfile_dir + "combined4_energy_" +self._ext)
     
    def _build_combined9_energy(self):
        tf9c = root.TFile(rootfile_dir + "combined9_energy_" +self._ext)
        t9c = tf9c.Get("combined9_energy_tree")
        t9c.GetEntries()
        self._tree.AddFriend("combined9_energy_tree", rootfile_dir + "combined9_energy_" +self._ext)





#===============================================================================
# tfwo = root.TFile(rootfile_dir + "withoutW.root")
# two = tfwo.Get("tree")
# two.GetEntries()
# 
# tfmwo = root.TFile(rootfile_dir + "max_energy_withoutW.root")
# tmwo = tfmwo.Get("max_energy_tree")
# tmwo.GetEntries()
# 
# tf2cwo = root.TFile(rootfile_dir + "combined2_energy_withoutW.root")
# t2cwo = tf2cwo.Get("combined2_energy_tree")
# t2cwo.GetEntries()
# 
# tf4cwo = root.TFile(rootfile_dir + "combined4_energy_withoutW.root")
# t4cwo = tf4cwo.Get("combined4_energy_tree")
# t4cwo.GetEntries()
# 
# tf9cwo = root.TFile(rootfile_dir + "combined9_energy_withoutW.root")
# t9cwo = tf9cwo.Get("combined9_energy_tree")
# t9cwo.GetEntries()
# 
# two.AddFriend("max_energy_tree", rootfile_dir + "max_energy_withoutW.root")
# two.AddFriend("combined2_energy_tree", rootfile_dir + "combined2_energy_withoutW.root")
# two.AddFriend("combined4_energy_tree", rootfile_dir + "combined4_energy_withoutW.root")
# two.AddFriend("combined9_energy_tree", rootfile_dir + "combined9_energy_withoutW.root")
#===============================================================================

#===============================================================================
# print('''
# tw = original tree with tungsten
# two = original tree without tungsten
# 
# tmw = max energy tree with tungsten
# tmwo = max energy tree without tungsten
# 
# t2cw = combined energy of 2 towers tree with tungsten
# t2cwo = combined energy of 2 towers tree without tungsten
# 
# t4cw = combined energy of 4 towers tree with tungsten
# t4cwo = combined energy of 4 towers tree without tungsten
# 
# t9cw = combined energy of 9 towers tree with tungsten
# t9cwo = combined energy of 9 towers tree without tungsten
# ''')
#===============================================================================
