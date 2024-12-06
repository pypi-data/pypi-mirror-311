#!/usr/bin/perl -w
use strict;

my (@temp);
my ($pip,$pip2,$i,$j,$name,$nat,$enetest,$updn);

die "Usage: gather_energy.pl [case] [-up/-dn] \n" if $#ARGV < 0;
$name = $ARGV[0];
$updn = '';

if($#ARGV == 1){
$updn = $ARGV[1];
$updn =~ s/-//gi; #Removes dash (-) in front of up or dn
}

open(STRUC,"$name.struct");
$nat = 0;
while(<STRUC>) {
    $nat++ if (/RMT=/);
}
close(STRUC);
if( -s "$name.inso" ){
    system("cat $name.energyso${updn}_? $name.energyso${updn}_?? > pip") ;
    open(ENE,">$name.energyso");
} else {
    system("cat $name.energy${updn}_? $name.energy${updn}_?? > pip") ;
    open(ENE,">$name.energy${updn}");
}

open(PIPF,"pip");
$enetest = <PIPF>;
printf ENE "$enetest";
for ($j = 2; $j <= (2*$nat); $j++) {
    $pip = <PIPF>;
    printf ENE "$pip";
}
while (<PIPF>) {
    if(/$enetest/) {
	for ($j = 2; $j <= (2*$nat); $j++) {
	    $pip = <PIPF>;
	}
	
    } else {
	printf ENE $_;
    }
}
close(ENE);
close(PIPF);
