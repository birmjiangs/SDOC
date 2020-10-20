use strict;

my $do_celltype = $ARGV[0]; #"GM12878"
my $out_dir = $ARGV[1]; #"./out_SDOC/"

print "$do_celltype\n";

mkdir("$out_dir$do_celltype/PASTIS_out/");

my $dirname = "$out_dir$do_celltype/TAD_matrices/";
opendir(DIR,"$dirname") or die "readdir error!";
my @files = readdir(DIR);
my $flen = @files;
my $i0 = -1;
foreach my $file(@files)
{	
	$i0++;
	if ($file eq "." or $file eq ".." or $file eq "dont_want_this_name"){next;}
	print "doing $i0 of $flen: $file\n";

	open OUT,">$out_dir$do_celltype/PASTIS_out/config.ini";
	print OUT "[all]\n";
	print OUT "output_name: $file\n";
	print OUT "verbose: 0\n";
	print OUT "max_iter: 100\n";
	print OUT "counts: ../TAD_interactions/$file.matrix\n";
	print OUT "lengths: ../TAD_bins/$file\n";
	print OUT "normalize: False\n";
	close OUT;

	my $cmd = `pastis-pm2 $out_dir$do_celltype/PASTIS_out/`;
}
