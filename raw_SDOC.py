import os
import sys
import numpy as np
from sklearn import manifold
from sklearn.metrics import euclidean_distances
from math import *
from scipy.spatial import ConvexHull
from scipy.spatial import Delaunay
################

do_celltype = sys.argv[1] # "GM12878" #sys.argv[1]  , job name,  #GM12878, IMR90, K562, HUVEC
out_dir = sys.argv[2] #"./out_SDOC/"  #sys.argv[4]


def mkdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

def tetrahedron_volume(a, b, c, d):
    return np.abs(np.einsum('ij,ij->i', a-d, np.cross(b-d, c-d))) / 6

def concave_hull_volume(pts,lenCutoff):
	dt = Delaunay(pts)    #tetrahedrons formed up with 4 points
	tets = dt.points[dt.simplices]   
	max_length = [0 for i in range(len(tets))]
	min_length = [0 for i in range(len(tets))]
	min2max = [0 for i in range(len(tets))]

	vol = 0
	count_valid_dts = 0
	count_total_dts = len(tets)

	total_vol = tetrahedron_volume(tets[:, 0], tets[:, 1], tets[:, 2], tets[:, 3])
	for i in range(len(tets)):

		max_length[i] = max(np.linalg.norm(tets[i, 0] - tets[i, 1]),np.linalg.norm(tets[i, 0] - tets[i, 2]),
			np.linalg.norm(tets[i, 0] - tets[i, 3]),np.linalg.norm(tets[i, 1] - tets[i, 2]),
		 	np.linalg.norm(tets[i, 1] - tets[i, 3]),np.linalg.norm(tets[i, 2] - tets[i, 3]))
		min_length[i] = min(np.linalg.norm(tets[i, 0] - tets[i, 1]),np.linalg.norm(tets[i, 0] - tets[i, 2]),
			np.linalg.norm(tets[i, 0] - tets[i, 3]),np.linalg.norm(tets[i, 1] - tets[i, 2]),
		 	np.linalg.norm(tets[i, 1] - tets[i, 3]),np.linalg.norm(tets[i, 2] - tets[i, 3]))
		min2max[i] = min_length[i] / float(max_length[i])

		if max_length[i] > lenCutoff:
			vol += 0
		else:
			vol += total_vol[i] #tets[:,0-4] are the four points
			count_valid_dts += 1 
	
	if count_total_dts == 0 or vol == 0 or len(min2max) == 0:
		print(pts) 
		return 0,0,0,0

	return vol, len(pts)/float(vol), float(sum(min2max))/len(min2max), float(count_valid_dts)/count_total_dts        #point density

def get_density(pos):
	lenCutoff = 1000
	vol,density,min2max,validprop = concave_hull_volume(pos,lenCutoff)
	return vol, density


def main():
	TAD_2_volume = {}
	
	coord_dir = out_dir + do_celltype + "/PASTIS_out/"
	
	files = os.listdir(coord_dir)	
	flen = len(files)
	i0 = -1
	for fl in files:
		#omit invalid file
		i0 += 1
		F = fl.split('.')
		if F[-1] == "ini" or F[-1] == "pdb":
			continue
	
	
		f = open(coord_dir+fl) 
		lines=f.readlines() 
		nrow = len(lines)			
		coords = []
		count_nan = 0
		for i in range(len(lines)):
			line = lines[i].strip()
			L = line.split(' ')
			if L[0] == "nan":
				count_nan += 1
				continue
			for j in range(len(L)):
				L[j] = float(L[j])
			coords.append(L)
		if count_nan * 3 >= nrow:
			continue
		coords = np.array(coords)
		vol, density = get_density(coords)
		if density == 0:#invalid one
			continue
	
		F = fl.split(".")[1].split("_")
		TAD_pos = F[0]+'\t'+F[1]+'\t'+str(int(F[2]))
	
		TAD_2_volume[TAD_pos] = vol
	
		if i0 % 100 == 0:
			print(i0,"of",len(files),"done...")
	
	mkdir(out_dir + do_celltype + "/TAD_SDOC")
	
	f = open(out_dir + do_celltype + "/4-TAD_with_DHS_length")   		
	fout = open(out_dir + do_celltype + "/TAD_SDOC/raw_SDOC",'w')
	lines=f.readlines() 
	nrow = len(lines)					
	for i in range(len(lines)):
		L = lines[i].strip().split('\t')
		if L[0]+'\t'+L[1]+'\t'+L[2] not in TAD_2_volume:
			print(0)
			continue
		TFBS_len = float(L[3])
	
		pseudo_DHS_count = 0
	
		fout.write(lines[i].strip()+'\t'+str(TAD_2_volume[L[0]+'\t'+L[1]+'\t'+L[2]])+'\t' + str((TFBS_len+pseudo_DHS_count) / float(TAD_2_volume[L[0]+'\t'+L[1]+'\t'+L[2]]))+'\n')
	fout.close()
	f.close()
	
	
if __name__ == '__main__':
    main()

		
	