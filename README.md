# aws-prefixes-to-edl
Converts AWS published IP Ranges to EDL

A simple lambda function that converts a list of IP addresses that host AWS services from json to an EDL sutiable for 
a Paloaltonetworks Firewall.

##Instructions

Upload the following file to S3 prior to deployment
layer.zip
aws_prefix_edl.py.zip

Load the Cloud Formation Template

###Input Parameters

EDLBucket - The Name of the S3 Bucket that will host the dynamic list

PrefixListURL - Location of the Json file published by AWS Default: https://ip-ranges.amazonaws.com/ip-ranges.json

EdlPrefixListFileName - Name of the file published to S3 and read by the firewall Default: aws-prefix-edl.txt

LambdaFunctionsBucketName - The name of the S3 bucket that contains the 'layer.zip' 'aws_prefix_edl.py.zip' files

