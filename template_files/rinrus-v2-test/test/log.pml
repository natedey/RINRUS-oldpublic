load res_36.pdb
cmd.select("sel","res_36 and not resi 128")
cmd.h_add("sel")
cmd.save("./res_36_h.pdb")
