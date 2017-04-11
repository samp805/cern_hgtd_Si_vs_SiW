import ROOT


def compute_event_id(tree, branches=("EventNumber", "RunNumber")):
    return tuple([tree.__getattr__(branch) for branch in branches])


def main(output_filename, filenames, treename):
    output_file = ROOT.TFile(output_filename, "recreate")

    chain = ROOT.TChain(treename, treename)
    for filename in filenames:
        print "adding filename %s" % filename
        chain.Add(filename)

    print "entries: %d" % chain.GetEntries()

    if chain.GetEntries() == 0:
        print "no events. Exit"
        return

    output_tree = chain.CloneTree(0)
    output_tree.SetDirectory(output_file)

    event_ids = set()
    nduplicates = 0

    branches_id = ("EventNumber", "RunNumber")
    #chain.SetBranchStatus("*", 0)
    #for branch in branches_id:
#        chain.SetBranchStatus(branch, 1)

    for ievent in xrange(chain.GetEntries()):
        if ievent % 10000 == 0 and ievent > 0:
            print "done %d events %d" % (ievent, chain.GetEntries())
        chain.GetEntry(ievent)
        event_id = compute_event_id(chain, branches_id)
        if event_id in event_ids:
#            print "duplicate found %s" % str(event_id)
            nduplicates += 1
            continue
        event_ids.add(event_id)
        output_tree.Fill()
    print "duplicate = %d / %d" % (nduplicates, ievent)

    output_file.cd()
    output_tree.Write()
    output_file.Close()


if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser("usage: %prog input output treename")

    (options, args) = parser.parse_args()
    main(args[1], [args[0]], args[2])
