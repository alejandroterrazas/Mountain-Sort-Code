#aws s3 cp ./RawData/ s3://$1N/NOCURATE/ --exclude '*' --include '*.mda' --recursive
aws s3 cp ./RawData/ s3://$1/NOCURATE/ --exclude '*' --include '*.log' --recursive
aws s3 cp ./RawData/ s3://$1/NOCURATE/ --exclude '*' --include '*.png' --recursive
aws s3 cp ./RawData/ s3://$1/NOCURATE/ --exclude '*' --include '*.t' --recursive
rm -f ./RawData/*

