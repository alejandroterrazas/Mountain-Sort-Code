
#!/bin/bash

filename="minibatch.txt"

cat $filename | while read line
do
   echo "Running batch for $line"
   rm -r -f ./RawData/
   dsname="narp-alext/$line"
   echo $dsname

   aws s3 cp s3://$dsname ./RawData/ --exclude '*' --include '*.ntt' --recursive   
   for filename in ./RawData/*.ntt; do
     echo "Launcing MountainSort for $filename"
     ./cut_tetrode_nocurate "$filename" "false" "32051" >> "$filename.log"
    sudo rm -r /tmp/*
   done
   ./make_tfiles
   ./upload_dataset_nocurate $dsname
#NOW DO HTE uncurated version

done
