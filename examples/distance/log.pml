load res_13.pdb
cmd.select("sel","res_13 and not resi 203 and not name NH1 and not name NH2")
cmd.h_add("sel")
cmd.save("./res_13_h.pdb")
