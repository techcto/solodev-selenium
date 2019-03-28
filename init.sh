#! /bin/bash
#
# Dependencies:
#   brew install jq
#
# Setup:
#   chmod +x ./aws-cli-assumerole.sh
#
# Execute:
#   source ./aws-cli-assumerole.sh
#
# Description:
#   Makes assuming an AWS IAM role (+ exporting new temp keys) easier

unset  AWS_SESSION_TOKEN
export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
export AWS_REGION=${AWS_REGION}

curl -qL -o jq https://stedolan.github.io/jq/download/linux64/jq && chmod +x ./jq

temp_role=$(aws sts assume-role \
                    --role-arn "${AWS_ROLE_ARN}" \
                    --role-session-name "solodev-selenium")

export AWS_ACCESS_KEY_ID=$(echo $temp_role | jq .Credentials.AccessKeyId | xargs)
export AWS_SECRET_ACCESS_KEY=$(echo $temp_role | jq .Credentials.SecretAccessKey | xargs)
export AWS_SESSION_TOKEN=$(echo $temp_role | jq .Credentials.SessionToken | xargs)

env | grep -i AWS_