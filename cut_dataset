
#!/bin/bash
#script to loop over .ntt files and produce .t filesi

rm -f ./RawData/*
aws s3 cp s3://$1 ./RawData/ --exclude '*' --include '*.ntt' --recursive
 

#$autocurate="true"

for filename in ./RawData/*.ntt; do
    echo "Launching MountainSort for $filename"
    ./cut_tetrode "$filename" "$2" "$3" >> "$filename.log"
done
