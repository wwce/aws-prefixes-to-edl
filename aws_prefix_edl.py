"""
/*****************************************************************************
 * Copyright (c) 2016, Palo Alto Networks. All rights reserved.              *
 *                                                                           *
 * This Software is the property of Palo Alto Networks. The Software and all *
 * accompanying documentation are copyrighted.                               *
 *****************************************************************************/

Copyright 2016 Palo Alto Networks

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Author jharris@paloaltonetworks.com
        harrisjr10@gmail.com
"""


import boto3
import botocore
import logging
import requests
import os
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')
ec2_client = boto3.client('ec2')


def get_aws_ips(url):
    try:
        response = requests.get(url, timeout=2)
        return json.loads(response.text)
    except Exception as e:
        print('unable to retrieve list from url {} got error {}'.format(url, e))
        return


def lambda_handler(event, context):
    logger.info('Got event {}'.format(event))
    aws_region = os.environ['Region']
    s3_path = os.environ['s3_path']
    s3Bucket = os.environ['s3_bucket']
    aws_list_url = os.environ['aws_list_url']

    s3 = boto3.resource('s3', region_name=aws_region)

    res = get_aws_ips(aws_list_url)
    aws_prefix_list = ''

    for item in res['prefixes']:
        aws_prefix_list = aws_prefix_list + item['ip_prefix'] + '\n'

    try:
        obj = s3.Object(s3Bucket, s3_path)
        obj.put(Body=aws_prefix_list.encode('utf-8'))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        logger.info('Got error {}'.format(e))


