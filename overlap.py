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

#sort bed file
def sort_list(list_in):
	list_out = sorted(list_in, key=lambda items: int(items.split('\t')[1]))
	list_out = sorted(list_out, key=lambda items: items.split('\t')[0])
	return list_out

print("parameters: -base_filename -data_dirname -do_sort(0/1) -with_title?(0/1) -out_dir(default: ./overlapped/)")

in_base = sys.argv[1]
in_dir = sys.argv[2]
do_sort = sys.argv[3]
with_title = sys.argv[4]
if len(sys.argv) == 6:
	out_dir = sys.argv[5]
	mkdir(out_dir)
else:
	mkdir("overlapped")
	out_dir = "./overlapped/"

#read base file
base_chrs = {}
base = []
title = ""
f = open(in_base)   		
lines=f.readlines() 
nrow = len(lines)					
for i in range(len(lines)):
	if i == 0 and float(with_title) == 1:
		title = lines[0].strip()
		continue
	line = lines[i].strip()
	L = line.split('\t')
	base_chrs[L[0]] = 1
	base.append(line)
f.close()

base_file_name = in_base.split("/")[-1]

#read each data files:
if in_dir[-1] != "/":
	in_dir = in_dir + "/"
if out_dir[-1] != "/":
	out_dir = out_dir + "/"

files = os.listdir(in_dir)			#get file list of dir
file_name = []  
for fl in files:
	file_name.append(fl)

	data_chrs = {}
	chr_2_index = {}
	chr_index = 0
	data = []
	f = open(in_dir+str(fl))   		#open each file
	lines=f.readlines() 
	nrow = len(lines)					#get each line
	for i in range(len(lines)):
		line = lines[i].strip()
		L = line.split('\t')
		chrN = L[0]
		if chrN not in chr_2_index:
			data.append([line])
			chr_2_index[chrN] = chr_index
			chr_index+=1
		else:
			data[chr_2_index[chrN]].append(line)
		data_chrs[L[0]] = 1

	f.close()

	#get common chrs:
	common_chrs = []
	for chrN in base_chrs:
		if chrN in data_chrs:
			common_chrs.append(chrN)

	out_unmatched_chrs = []
	for i in range(len(base)):
		L = base[i].split('\t')
		if (L[0] in common_chrs) == False:
			out_unmatched_chrs.append(base[i])

	out = []
	#seperate
	for chrN in common_chrs:
		print("doing", chrN)
		base_chrN = []
		data_chrN = data[chr_2_index[chrN]]
		if float(do_sort) == 1.0:
			print("do_sort:1, sorting data of", chrN)
			data_chrN = sort_list(data_chrN)

		for i in range(len(base)):
			L = base[i].split('\t')
			chr_this = L[0]
			if chr_this != chrN:
				continue
			base_chrN.append(base[i])

		if float(do_sort) == 1.0:
			print("do_sort:1, sorting base of", chrN)
			base_chrN = sort_list(base_chrN)

		#do overlaps:
		data_start = 0
		largest_end_point_of_data_before_data_start = 0
		for i in range(len(base_chrN)):
			cache_largest_data_end_point = largest_end_point_of_data_before_data_start

			B = base_chrN[i].split('\t')
			B[1:3] = map(int,B[1:3])

			overlap_part = []
			for j in range(data_start,len(data_chrN)):
				D = data_chrN[j].split('\t')
				D[1:3] = map(int,D[1:3])

				if D[2] > cache_largest_data_end_point:
					cache_largest_data_end_point = D[2]
				#renew largest data end point:


				if D[1] > B[2]:
					break
				if D[2] < B[1] and cache_largest_data_end_point < B[1]:
					data_start = j
					largest_end_point_of_data_before_data_start = cache_largest_data_end_point

				if D[1] <= B[2] and B[1] <= D[2]:
					overlap_part.append(data_chrN[j])
			overlap_str = "\t".join(overlap_part)
			out.append(base_chrN[i]+"\t"+overlap_str)

	out = out + out_unmatched_chrs
	out = sort_list(out)
	if float(with_title) == 1:
		out = [title] + out

	fout = open(out_dir+base_file_name+"_"+fl+".txt",'w')
	for i in range(len(out)):
		line_out = out[i]
		fout.write(line_out+'\n')
	fout.close()
	#savetxt(out_dir+base_file_name+"_"+fl+".txt", out)
	print(base_file_name, fl, "done.., output file:", out_dir+base_file_name+"_"+fl+".txt")













