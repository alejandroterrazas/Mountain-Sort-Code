
#!/bin/bash
# script to run tetrode cutting on MS

#tfile="1"
#echo "$tfile"

basefile="${1/.firings.mda/""}"
echo "$basefile"

rawfile="$basefile.raw.mda"
echo "$rawfile"

curatedfile="$basefile.firings.curated.mda"
echo "$curatedfile"
#fsize=$(stat -c$s $basefile)
cmfile="$basefile.cluster_metrics.json"
echo "$cmfile"

#rm firings.curated.mda
fsize=$(stat -c%s "$basefile.firings.mda")
echo "$fsize"
if [ $fsize -gt 21 ]
then
  mountainview --raw=$rawfile --firings=$1 --cluster_metrics=$cmfile --geom=data/geom.csv --samplerate=$2
  mv firings.curated.mda $curatedfile
  python MakeTFiles.py $basefile
fi
#mountainview --raw=$rawfile --firings=$1 --cluster_metrics=$cmfile --geom=data/geom.csv --samplerate=$2

#echo "$tfile"
#python MakeTFiles.py $basefile 
