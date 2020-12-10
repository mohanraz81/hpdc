#!/bin/bash
docker rmi `docker images|grep lambda|awk '{print $3}'`
rm -vf ${HOME}/.aws/credentials
curl -sSL https://raw.githubusercontent.com/aws-samples/one-observability-demo/main/PetAdoptions/envsetup.sh | bash -s stable
export ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)
export AWS_REGION=$(curl -s 169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.region')
echo "export ACCOUNT_ID=${ACCOUNT_ID}" | tee -a ~/.bash_profile
echo "export AWS_REGION=${AWS_REGION}" | tee -a ~/.bash_profile
aws configure set default.region ${AWS_REGION}
aws configure get default.region
cd workshopfiles/one-observability-demo/PetAdoptions/cdk/pet_stack
npm install
cdk bootstrap
cdk deploy Services
aws ssm get-parameter --name '/petstore/petsiteurl'  | jq -r .Parameter.Value