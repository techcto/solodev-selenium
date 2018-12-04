make build
echo "Upload Lambda to S3"
aws s3 cp build.zip s3://solodev-aws-ha/solodev-selenium.zip