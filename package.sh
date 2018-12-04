make build
echo "Upload Lambda to S3"
aws s3 cp build.zip s3://solodev-aws-ha/solodev-selenium.zip
aws lambda update-function-code --function-name solodevSelenium --s3-bucket solodev-aws-ha --s3-key solodev-selenium.zip