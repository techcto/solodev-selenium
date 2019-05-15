#!/usr/bin/env bash

for BUCKET in $(aws s3api list-buckets --region us-east-1 | ./jq -r '.Buckets[].Name')
do
    if [[ $BUCKET == *"-selenium-"* ]]; then
        echo "I found one. Time to delete a bucket: ${BUCKET}.  Bye-Bye!"
        aws s3 rb s3://$BUCKET --force 
    fi
done

echo $(aws cloudformation describe-stacks)
for STACK in $(aws cloudformation describe-stacks --region us-east-1 | ./jq -r '.Stacks[].StackName')
do
    if [[ $STACK == *"-selenium-"* ]]; then
        echo "I found one. Time to delete stack: ${STACK}.  Bye-Bye!"
        aws cloudformation delete-stack --stack-name $STACK
    fi
done