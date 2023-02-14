aws iam create-role --role-name hpdcadminrole --assume-role-policy-document file://trust-policy.json
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AdministratorAccess --role-name  hpdcadminrole
aws iam create-instance-profile --instance-profile-name hpdcadminip
aws iam add-role-to-instance-profile --role-name hpdcadminrole --instance-profile-name hpdcadminip
instanceid=`curl http://169.254.169.254/latest/meta-data/instance-id`
sleep 20
aws ec2 associate-iam-instance-profile --instance-id $instanceid --iam-instance-profile Name=hpdcadminip
rm -rf ~/.aws
aws sts get-caller-identity