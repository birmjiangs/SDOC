# USAGE: python ./get_SDOC.py -celltype -TAD_dir -Hi-C_dir -resolution -out_dir -DHS_dir
import os
import sys

def main():

      # run with example dataset
    do_celltype = "IMR90"# 
    TAD_input_dir = "./example_data/TADs/"
    HiC_matrix_dir = "./example_data/HiC_matrices/"
    resolution = 25000
    out_dir = "./out_SDOC/"
    DHS_file_in = "./example_data/DNase_seq_peaks/ENCSR477RTP_rep1_1_rep1_2_rep1_3_rep1_4_se_bwa_biorep_filtered_peaks.bed"
    
    if len(sys.argv) == 7:
        do_celltype = sys.argv[1]# "GM12878" #  , job name,  #GM12878, IMR90, K562, HUVEC
        TAD_input_dir = sys.argv[2]#"./TADs/"
        HiC_matrix_dir = sys.argv[3]#"/mnt/hgfs/E/SupWork/2020/SDOC_analysis/BIB/a0-get_matrix/5kb/1-binning&KRnorm/2_norm_matrix/" #sys.argv[2]
        resolution = sys.argv[4] #5000 # 
        out_dir = sys.argv[5] #"./out_SDOC/"  #sys.argv[4]
        DHS_file_in = sys.argv[6] #./open_chromatin_peaks/GM12878"
    
    if TAD_input_dir[-1] != "/":
        TAD_input_dir = TAD_input_dir + "/"
    if HiC_matrix_dir[-1] != "/":
        HiC_matrix_dir = HiC_matrix_dir + "/"
    if out_dir[-1] != "/":
        out_dir = out_dir + "/"

    os.system("python ./get_TAD_matrices.py %s %s %s %s %s" % (do_celltype, TAD_input_dir, HiC_matrix_dir, resolution, out_dir))
    os.system("python ./reshape_to_pastis_input_format.py %s %s %s" % (do_celltype, out_dir, resolution))
    os.system("perl ./configure_ini_and_runPastis.pl %s %s" % (do_celltype, out_dir))
    os.system("python ./get_DHS_len_in_each_TAD.py %s %s %s %s" % (do_celltype, out_dir, TAD_input_dir, DHS_file_in))
    os.system("python ./raw_SDOC.py %s %s" % (do_celltype, out_dir))
    os.system("Rscript ./quantile_normalize_SDOC.r %s %s" % (do_celltype, out_dir))	
    
    
if __name__ == '__main__':
    main()

    