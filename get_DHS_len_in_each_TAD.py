import numpy as np
import os 
import sys

def mkdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

def savetxt(filename,x):
    np.savetxt(filename,x,delimiter = '\t',fmt='%s')

def sort_list(list_in): #use when using '\t' to seperate items
    list_out = sorted(list_in, key=lambda items: int(items.split('\t')[1]))
    list_out = sorted(list_out, key=lambda items: items.split('\t')[0])
    return list_out

def main():
    do_celltype = sys.argv[1]  #"GM12878", job name,  #GM12878, IMR90, K562, HUVEC
    out_dir = sys.argv[2]  #"./out_SDOC/" 
    TAD_in_dir = sys.argv[3]  #"./TADs/"
    DHS_file_in = sys.argv[4]  #"./open_chromatin_peaks/GM12878"
    #1. reformat ATAC-seq data:
    mkdir(out_dir+do_celltype+"/DHS_3_col/")
    
    out = []    
    f = open(DHS_file_in)           
    lines=f.readlines() 
    nrow = len(lines)                   
    for i in range(len(lines)):
        L = lines[i].strip().split('\t')
        out.append(L[0]+'\t'+L[1]+'\t'+L[2])
    f.close()
    out = sort_list(out)
    savetxt(out_dir+do_celltype+"/DHS_3_col/DHS", out)
    
    mkdir(out_dir + do_celltype + "/TAD_combined/")
    os.system("cat " + TAD_in_dir + "* > "+ out_dir + do_celltype + "/TAD_combined/TAD")
    os.system("python3 overlap.py " + out_dir + do_celltype + "/TAD_combined/TAD " + out_dir + do_celltype + "/DHS_3_col/ 1 0 "+out_dir + do_celltype + "/4-overlapped") 
    
       
    fout = open(out_dir + do_celltype + "/4-TAD_with_DHS_length",'w')
    f = open(out_dir + do_celltype + "/4-overlapped/TAD_DHS.txt")      
    lines=f.readlines() 
    nrow = len(lines)                    
    for i in range(len(lines)):
        DHS_len = 0
        L = lines[i].strip().split('\t')
        if len(L) == 3:
            fout.write(L[0]+'\t'+L[1]+'\t'+L[2]+'\t0.0\n')
            continue
        for j in range(4,len(L),3):
            DHS_len += 1.0
    
        fout.write(L[0]+'\t'+L[1]+'\t'+L[2]+'\t'+str(DHS_len)+'\n')
    
    f.close()
    fout.close()
    

if __name__ == '__main__':
    main()

    