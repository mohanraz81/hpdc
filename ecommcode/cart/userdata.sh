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
dbhostname=${}
dbname=${}
dbusername=${}
dbpassword=${}
cd archeplay-ecomm-demo/cart
sed -i "s/cart-db/$dbhostname/g" docker-compose.yaml
sed -i "s/cartdb/$dbname/g" docker-compose.yaml
sed -i "s/dbusername/$dbusername/g" docker-compose.yaml
sed -i "s/dbpassword/$dbpassword/g" docker-compose.yaml
cp cart.service /etc/systemd/system/cart.service
systemctl daemon-reload
systemctl enable cart.service
systemctl start cart.service