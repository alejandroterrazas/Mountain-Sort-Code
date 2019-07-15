
#!/bin/bash
#script to loop over .ntt files and produce .t filesi

rm -f ./RawData/*
#aws s3 cp s3://$1 ./RawData/ --exclude '*' --include '*.ntt' --recursive
#aws s3 ls s3://$1/
#$autocurate="true"

for VARIABLE in 1 2 3 4 5 6 7 8 9 10 11 12; do
    fname="Sc$VARIABLE.ntt"
    echo "$fname"
    aws s3 cp s3://$1 ./RawData/  --exclude '*' --include $fname --recursive
    ./cut_tetrode "./RawData/$fname" "$2" "$3" >> "$fname.log"
done
