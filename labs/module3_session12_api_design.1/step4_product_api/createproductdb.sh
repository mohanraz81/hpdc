#!/bin/bash
productdb=$1
aws dynamodb create-table \
    --table-name $productdb \
    --attribute-definitions \
        AttributeName=id,AttributeType=S  \
    --key-schema \
        AttributeName=id,KeyType=HASH \
    --billing-mode \
        PAY_PER_REQUEST \
    --table-class STANDARD
