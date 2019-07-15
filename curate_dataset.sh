
#!/bin/bash

for filename in ./RawData/*.firings.mda; do
    ./curate_tetrode "$filename" $2 
done

rm ./RawData/*.raw*

aws s3 cp ./RawData/ s3://$1/TT/ --exclude '*' --include '*.mda' --recursive
aws s3 cp ./RawData/ s3://$1/TT/ --exclude '*' --include '*.log' --recursive
aws s3 cp ./RawData/ s3://$1/TT/ --exclude '*' --include '*.pdf' --recursive
aws s3 cp ./RawData/ s3://$1/TT/ --exclude '*' --include '*.t' --recursive
rm -f ./RawData/*

