#!/usr/bin/env sh

sam package --template-file template.yaml --s3-bucket thehedgenetbridge --output-template-file packaged.yaml
sam deploy --template-file packaged.yaml --stack-name dev-bridge --capabilities CAPABILITY_IAM

