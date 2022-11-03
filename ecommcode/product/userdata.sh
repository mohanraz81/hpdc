#!/bin/bash
yum install docker -y
usermod -a -G docker ec2-user
systemctl  start docker
systemctl status docker
systemctl enable docker
curl -L "https://github.com/docker/compose/releases/download/1.27.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
yum -y install git
git clone https://github.com/mohanraz81/archeplay-ecomm-demo.git
cd archeplay-ecomm-demo/product
sed -i "s/REGIONNAME/${ AWS::Region }/g" docker-compose.yaml
sed -i "s/TABLENAME/${ TABLENAME }/g" docker-compose.yaml
cp product.service /etc/systemd/system/product.service
systemctl daemon-reload
systemctl enable product.service
systemctl start product.service