#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import sys

def read_contact_map(mapf):
    with open(mapf) as f:
        lines = f.readlines()
    size = int((1+np.sqrt(1+4*len(lines)*2))/2)
    dist_mat = np.zeros((size,size)) 
    indx = []
    indy = []
    count = 0
    for i in range(size):
        for j in range(i+1,size):
            line = lines[count]
            v = line.split()
            if int(v[1]) not in indx:
                indx.append(int(v[1]))
            if int(v[3]) not in indy:
                indy.append(int(v[3]))
            dist_mat[i,j] = float(v[-1])
            count += 1
    return indx,indy,dist_mat


def heatmap(data,row_labels,col_labels,ax=None,cbar_kw={},cbarlabel="",**kwargs):
    if not ax:
        ax = plt.gca()

    # Plot the heatmap    
    im = ax.imshow(data,**kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im,ax=ax,**cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
    cbar.set_clim(-0.5,1)

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_xticklabels(labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]))
    ax.set_yticklabels(labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",rotation_mode="anchor")

    # Turn spines off and create white grid.
    #ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar

def annotate_heatmap(im, data=None, valfmt="{x:.2f}", textcolors=("black", "white"),threshold=None, **textkw):
    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2

    # Set default alignment to center, but allow it to be overwritten by textkw.
    kw = dict(horizontalalignment="center",verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts



if __name__ == '__main__':
    map1 = sys.argv[1]
    map2 = sys.argv[2]
    indx1,indy1,dist_mat1 = read_contact_map(map1)
    indx2,indy2,dist_mat2 = read_contact_map(map2)
   
    fig, ax = plt.subplots()
    dist_diff = dist_mat1-dist_mat2
    ytk = indy1
    ytk.insert(0,indx1[0])
    xtk = indx1
    xtk.append(indy1[-1])
#    im = ax.imshow(dist_diff)
    im,cbar = heatmap(dist_diff,ytk,xtk,ax=ax,cmap="Spectral",cbarlabel="distance_diff")


#    ax.set_xticks(np.arange(dist_mat1.shape[1]))
#    ytk = indy1
#    ytk.insert(0,indx1[0])
#    print(ytk)
#    ax.set_xticklabels(ytk)
#    ax.set_yticks(np.arange(dist_mat1.shape[0]))
#    xtk = indx1
#    xtk.insert(-1,indy1[-1])
#    print(xtk)
#    ax.set_yticklabels(xtk)

#    plt.setp(ax.get_xticklabels(),rotation=45,ha="right",rotation_mode="anchor")

#    for i in range(len(indy1)):
#        for j in range(len(indx1)):
#            if dist_diff[i,j] != 0.0:
#                text = ax.text(j,i,dist_diff[i,j]*10,ha="center",va="center",color="w")

#    ax.set_title("Residue Pair Distance Map")
    fig.tight_layout()
#    plt.show()
    plt.savefig("Residue_Pair_Distance_Change.png",dpi=150)

