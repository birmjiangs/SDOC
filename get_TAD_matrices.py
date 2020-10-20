#time: ~20min per celltype at 20kb resolution

import os
import sys
import numpy as np


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
  
################
def main():
    do_celltype = sys.argv[1]# "GM12878" #  , job name,  #GM12878, IMR90, K562, HUVEC
    TAD_input_dir = sys.argv[2]#"./TADs/"
    HiC_matrix_dir = sys.argv[3]#"/mnt/hgfs/E/SupWork/2020/SDOC_analysis/BIB/a0-get_matrix/5kb/1-binning&KRnorm/2_norm_matrix/" #sys.argv[2]
    resolution = int(sys.argv[4]) #5000 # 
    out_dir = sys.argv[5] #"./out_SDOC/"  #sys.argv[4]
    
    
    #read TADs in bed format
    matrix_coord_to_extract = [] 
    
    files = os.listdir(TAD_input_dir)     
    for fl in files:
        f = open(TAD_input_dir+str(fl))  
        lines=f.readlines() 
        nrow = len(lines)					
        for i in range(len(lines)):
            L = lines[i].strip().split('\t')
            start_coord = int(int(L[1]) / resolution)
            end_coord = int(int(L[2]) / resolution)
            chrN = L[0]
            matrix_coord_to_extract.append([chrN, start_coord, end_coord])
        f.close()
    
    
    #read hic matrix file to extract TAD matrix
    mkdir(out_dir)
    mkdir(out_dir+do_celltype)
    mkdir(out_dir+do_celltype+"/TAD_matrices/")
    
    files = os.listdir(HiC_matrix_dir)		
    for fl in files:
        chrN = fl.split("_")[1]
    
        f = open(HiC_matrix_dir+do_celltype+"_"+chrN)
        lines=f.readlines() 
        nrow = len(lines)  
        HiC_matrix_of_this_chr = np.zeros((nrow,nrow))                 
        for i in range(len(lines)):
            line = lines[i].strip().split('\t')
            HiC_matrix_of_this_chr[i,:] = line[:]
        f.close()
        #print(type(HiC_matrix_of_this_chr),np.shape(HiC_matrix_of_this_chr))
        #read each TAD coord to output the matrix
        for i in range(len(matrix_coord_to_extract)):
            if chrN != matrix_coord_to_extract[i][0]:
                continue   #not same chr
    
            start_coord = matrix_coord_to_extract[i][1]
            end_coord = matrix_coord_to_extract[i][2]
            TAD_matrix = HiC_matrix_of_this_chr[start_coord:end_coord+1,start_coord:end_coord+1]
    
            out_file_name = matrix_coord_to_extract[i][0] + '_' + str((matrix_coord_to_extract[i][1])*resolution) + '_' + str((matrix_coord_to_extract[i][2])*resolution)
    
            savetxt(out_dir+do_celltype+"/TAD_matrices/"+out_file_name, TAD_matrix)
    
if __name__ == '__main__':
    main()

    
    

        
    