#!/usr/bin/env bash
make build
echo "Upload Lambda to S3"
aws s3 cp build.zip s3://solodev-aws-ha/solodev-selenium.zip
aws lambda update-function-code --function-name solodevSelenium --s3-bucket solodev-aws-ha --s3-key solodev-selenium.zip
DATE=$(date +%d%H%M)
echo "Create Solodev Lite"
echo $(aws s3 cp s3://build-secure/params/solodev-lite-single.json - ) > solodev-lite-single.json
aws cloudformation create-stack --disable-rollback --stack-name lite-selenium-${DATE} --disable-rollback --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
    --parameters file://solodev-lite-single.json \
    --template-url https://s3.amazonaws.com/solodev-aws-ha/aws/solodev-lite-linux.yaml \
    --notification-arns ${NOTIFICATION_ARN}