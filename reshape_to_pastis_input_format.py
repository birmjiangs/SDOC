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
	do_celltype = sys.argv[1]  #"GM12878" 
	out_dir = sys.argv[2]  #"./out_SDOC/"  #
	resolution = int(sys.argv[3]) #5000  #
	
	TAD_matrix_dir = out_dir + do_celltype + "/TAD_matrices/"
	
	mkdir(out_dir + do_celltype + "/TAD_bins/")
	mkdir(out_dir + do_celltype + "/TAD_interactions/")
	print("directory created:", out_dir + do_celltype + "/TAD_bins/")
	print("directory created:", out_dir + do_celltype + "/TAD_interactions/")
	
	
	files = os.listdir(TAD_matrix_dir)			#get file list of dir  
	for fl in files:
		chrN = fl.split("_")[0]
	
		#f = open(TAD_matrix_dir+do_celltype+"/"+str(fl))
		#lines=f.readlines()  
		#nrow = len(lines)
		#matrix = np.zeros((nrow,nrow))
		#
		#if nrow < 5: 
		#	continue
	#
		#for i in range(nrow):
		#	line=lines[i].strip().split('\t')
		#	matrix[i,:] = line[:]
		#f.close()
	
		matrix = np.loadtxt(TAD_matrix_dir+"/"+str(fl), delimiter = "\t")
		if len(matrix) < 5: #omit TADs that are too small
			continue
		
		fout1 = open(out_dir + do_celltype + "/TAD_bins/" + fl, 'w')
		fout2 = open(out_dir + do_celltype + "/TAD_interactions/" + fl + '.matrix', 'w')
	
		for i in range(len(matrix)):
	
			fout1.write(chrN+"\t"+str(i*resolution+1)+'\t'+str((i+1)*resolution)+'\t'+str(i)+'\n')
	
			for j in range(len(matrix)):
				if i >= j:
					continue
	
				fout2.write(str(i)+'\t'+str(j)+'\t'+str(int(matrix[i,j]))+'\n')
	
		fout1.close();
		fout2.close();
	
if __name__ == '__main__':
	main()

	