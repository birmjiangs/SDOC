library(preprocessCore)

args <- commandArgs(trailingOnly = TRUE)
celltype = args[1]
out_dir = args[2]#"./out_SDOC/"

#dir.create(SDOC_output_dir)

QN_SDOC <- function(){
	data = read.table(file = paste0(out_dir,celltype,"/TAD_SDOC/raw_SDOC"), sep = "\t")

	d = as.matrix(as.numeric(data[,6]))
	normalize.quantiles.use.target(d, target = rnorm(50000), copy=FALSE, subset=NULL)
	d <- as.character(d)
	data[,6] = d

	data <- as.vector(data)

	write.table(file = paste0(out_dir, celltype, "_SDOC.tsv"), data, quote = FALSE, sep = '\t', row.names = FALSE, col.names = FALSE)
	return(0)
}
QN_SDOC()
