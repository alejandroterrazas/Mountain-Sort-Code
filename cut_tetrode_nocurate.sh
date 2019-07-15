
#!/bin/bash
# script to run tetrode cutting on MS

python ./PrepareTetrodeData.py $1
rawfile="$1.raw.mda"
echo "$rawfile"
ffile="$1.firings.mda"
echo "$ffile"

clustfile="$1.cluster_metrics.json"
echo "$clustfile"

prv-create $rawfile "$rawfile.prv"

pfile="$3.json"

sudo mlp-run alex-nocurate.mlp sort --curate=$2 --raw=$rawfile --geom=data/geom.csv --firings_out=$ffile --_params=$pfile --cluster_metrics_out=$clustfile
