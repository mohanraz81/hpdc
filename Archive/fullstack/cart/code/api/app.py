from flask import Flask, jsonify
from flask import request
import sys,os,boto3
import logging,json
import pymysql, base64
import random,string
import hashlib,uuid,datetime
app = Flask(__name__)
@app.route('/status', methods=['GET'])
def status():
    successmessage={"status": 200}
    return(successmessage)
@app.route('/api/v1.0/addtocart', methods=['POST'])
def addtocart():
    rds_host = os.environ['MYSQL_HOST']
    name = os.environ['MYSQL_USER']
    password = os.environ['MYSQL_PASSWORD']
    db_name = os.environ['MYSQL_DATABASE']
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
        logger.info("Connection to RDS MySQL")
    except pymysql.MySQLError as e:
        sys.exit()
    productid = request.json['id']
    user = request.json['user']
    try:
        cursor = conn.cursor()
        print("Creating User Entity")
        sql = "CREATE TABLE  IF NOT EXISTS carttable ( id INT(11) AUTO_INCREMENT PRIMARY KEY, user VARCHAR(32) NOT NULL, productid VARCHAR(32));"
        cursor.execute(sql)
        cursor = conn.cursor()
        print("Creating User Entity")
        sql = "INSERT INTO carttable (user,productid) VALUES ('{0}', '{1}');".format(user,productid)
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        logger.error("ERROR: Unexpected error: "+str(e))
        conn.rollback()
    conn.close()
    successmessage={
        "Status": 200,
        "StatusMessage": "Added to Cart"
    }
    return(successmessage)
@app.route('/api/v1.0/getcart', methods=['POST'])
def getcart():
    rds_host = os.environ['MYSQL_HOST']
    name = os.environ['MYSQL_USER']
    password = os.environ['MYSQL_PASSWORD']
    db_name = os.environ['MYSQL_DATABASE']
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
        logger.info("Connection to RDS MySQL")
    except pymysql.MySQLError as e:
        sys.exit()
    user = request.json['user']
    try:
        cursor = conn.cursor()
        print("Creating User Entity")
        sql = "select * from carttable where user = '{0}';".format(user)
        cursor.execute(sql)
        rows = cursor.fetchall()
        output=[]
        for row in rows:
            outputrow={
                "cartid": row[0],
                "user": row[1],
                "productid": row[2]
            }
            output.append(outputrow)
            print(output)
    except Exception as e:
        logger.error("ERROR: Unexpected error: "+str(e))
        conn.rollback()
    conn.close()
    response={
      "status": 200,
      "data": output
    }
    return(jsonify(response))