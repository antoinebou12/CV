---
post_kind: article
title: "Faire travailler ensemble Caddy, EC2, CloudWatch, Step Functions et Lambda"
date: 2024-05-14T18:00:00-04:00
description: Caddy sur EC2, journaux vers CloudWatch, scripts Python et orchestration Step Functions + Lambda pour un tableau de bord peu coûteux.
translationKey: caddy-ec2-cloudwatch-lambda
tags:
    - AWS
    - Caddy
    - EC2
    - CloudWatch
    - Lambda
    - Step Functions
canonicalURL: "https://medium.com/@antoine.boucher012/making-caddy-aws-ec2-cloudwatch-step-functions-and-lambda-work-together-creating-a-cheap-and-990fd0d9427d"
---

## Introduction

Monter une infra web solide et scalable peut être coûteux et complexe. Avec les bons outils, on peut rester efficace et économique. Cet article décrit **Caddy** sur **AWS EC2**, l’intégration à **CloudWatch** pour la supervision, et **Step Functions** + **Lambda** pour automatiser — une approche complète pour un tableau de bord à budget maîtrisé.

### Étape 1 : installer Caddy sur EC2

**Caddy** est un serveur web simple avec **HTTPS automatique**, adapté au trafic web et au reverse proxy. Je l’utilise aussi pour mes assistants à la maison.

Lancer une instance EC2 :

*   Connexion à la console AWS.
*   EC2 → lancer une instance (Amazon Linux 2 ou autre distro).
*   Type d’instance (ex. t2.micro free tier ou t4g.nano ~0,10 $/jour).

![](./img-001.png)

*   Groupe de sécurité : HTTP, HTTPS, SSH.

![](./img-002.png)

2. **Installer Caddy** — en SSH sur l’instance :

sudo yum update -y  
sudo yum install -y yum-utils  
sudo yum-config-manager — add-repo https://dl.cloudsmith.io/public/caddy/stable/rpm.repo  
sudo yum install caddy -y

3. **Configurer Caddy** — exemple de `Caddyfile` (domaine et proxy) :

{  
 email antoine@antoineboucher.info  
 servers {  
 metrics  
 }  
 admin :2019  
}  
(log\_site) {  
 log {  
 output file /home/ec2-user/caddy/logs/{args\[0\]}.log {  
 roll\_size 10mb  
 roll\_keep 5  
 roll\_keep\_for 168h  
 }  
 level INFO  
 }  
}  
antoineboucher.info www.antoineboucher.info {  
 import log\_site antoineboucher.info  
 reverse\_proxy <cloudfront\_url>  
 handle\_errors {  
 redir https://www.github.com/antoinebou12  
 }  
}  
linkedin.antoineboucher.info www.linkedin.antoineboucher.info {  
 import log\_site linkedin.antoineboucher.info  
 redir https://www.linkedin.com/in/antoineboucher12  
}  
home.antoineboucher.info www.home.antoineboucher.info {  
 import log\_site home.antoineboucher.info  
 reverse\_proxy http://homeip:port  
}

Démarrer / recharger Caddy : `sudo caddy reload`

### Étape 2 : supervision avec CloudWatch

**CloudWatch** collecte métriques et journaux pour AWS et au-delà.

1.  **Journaux Caddy → CloudWatch** : adapter la config Caddy ou pousser les fichiers de log via script (AWS CLI / SDK), comme l’exemple Python ci-dessous.

import os  
import boto3  
from datetime import datetime  
  
\# Initialize the CloudWatch client  
cloudwatch = boto3.client('logs', region\_name='us-east-1')  
  
\# Define your log group name  
log\_group\_name = 'reverse\_proxy'  
  
\# Path to your log directory  
log\_directory = "/home/ec2-user/caddy/logs"  
  
def send\_log\_to\_cloudwatch(log\_stream\_name, log\_message):  
    try:  
        \# Get or create the log stream  
        streams = cloudwatch.describe\_log\_streams(logGroupName=log\_group\_name, logStreamNamePrefix=log\_stream\_name)  
        if not streams\['logStreams'\]:  
            cloudwatch.create\_log\_stream(logGroupName=log\_group\_name, logStreamName=log\_stream\_name)  
        \# Send log to CloudWatch  
        cloudwatch.put\_log\_events(  
            logGroupName=log\_group\_name,  
            logStreamName=log\_stream\_name,  
            logEvents=\[  
                {  
                    'timestamp': int(datetime.now().timestamp() \* 1000),  
                    'message': log\_message  
                }  
            \]  
        )  
    except Exception as e:  
        print(f"Failed to send log to CloudWatch: {str(e)}")  
  
\# Read logs from files and send to CloudWatch  
for filename in os.listdir(log\_directory):  
    if filename.endswith(".log"):  
        log\_stream\_name = filename\[:-4\]  \# Remove .log from filename to use as stream name  
        file\_path = os.path.join(log\_directory, filename)  
        with open(file\_path, 'r') as file:  
            for line in file:  
                send\_log\_to\_cloudwatch(log\_stream\_name, line.strip())

Planifiez un **cron** sur l’instance pour exécuter ce script la nuit :

sudo yum install cronie -y  
sudo systemctl start crond  
sudo systemctl enable crond  
chmod +x /home/ec2-user/cloudwatch.py  
crontab -e  
0 0 \* \* \* /usr/bin/python3 /home/ec2-user/cloudwatch.py

1.  Créer les groupes de journaux CloudWatch :

aws logs create\-log\-group - log\-group-name reverse\_proxy  
aws logs create\-log\-group - log\-group-name geoip

**Fonction Lambda pour interroger les journaux :**

import boto3  
import json  
import time  
from datetime import datetime, timedelta  
  
def lambda\_handler(event, context):  
    client = boto3.client('logs')  
    query = """  
    fields @timestamp, @message  
    | parse @message /"remote\_ip": "(?<remote\_ip>\[^"\]+)"/  
    | stats count() by remote\_ip  
    | sort remote\_ip asc  
    """  
      
    log\_group = 'reverse\_proxy'  
    start\_query\_response = client.start\_query(  
        logGroupName=log\_group,  
        startTime=int((datetime.now() - timedelta(days=1)).timestamp()),  
        endTime=int(datetime.now().timestamp()),  
        queryString=query  
    )  
      
    query\_id = start\_query\_response\['queryId'\]  
    response = None  
    max\_wait\_time = 30  \# maximum wait time of 30 seconds  
    start\_time = time.time()  
      
    while response is None or response\['status'\] == 'Running':  
        if time.time() - start\_time > max\_wait\_time:  
            raise TimeoutError("Query did not complete within the maximum wait time.")  
        response = client.get\_query\_results(queryId=query\_id)  
        time.sleep(0.5)  \# Reduced sleep interval to check more frequently  
      
    ip\_addresses = \[\]  
    for result in response\['results'\]:  
        for field in result:  
            if field\['field'\] == 'remote\_ip':  
                ip\_addresses.append(field\['value'\])  
      
    return {  
        'statusCode': 200,  
        'body': json.dumps({'ip\_addresses': ip\_addresses})  
    }

**Étape 3 : automatisation avec Step Functions et Lambda**

{  
  "Comment": "Query CloudWatch Logs and Get IP Geolocation",  
  "StartAt": "QueryLogsInsights",  
  "States": {  
    "QueryLogsInsights": {  
      "Type": "Task",  
      "Resource": "arn:aws:lambda:us-east-1:590183756542:function:QueryLogsInsights",  
      "Next": "GetGeolocation"  
    },  
    "GetGeolocation": {  
      "Type": "Task",  
      "Resource": "arn:aws:lambda:us-east-1:590183756542:function:GeolocationIP",  
      "End": true  
    }  
  }  
}

![](./img-003.png)

**Lambda — requête CloudWatch Insights :**

import json  
import urllib3  
import boto3  
import time  
  
def lambda\_handler(event, context):  
    \# Extract IP addresses from the event  
    ip\_addresses = json.loads(event\['body'\])\['ip\_addresses'\]  
      
    http = urllib3.PoolManager()  
    results = \[\]  
  
    for ip in ip\_addresses:  
        response = http.request('GET', f"https://ipinfo.io/{ip}/json")  
        data = json.loads(response.data.decode('utf-8'))  
        results.append({  
            'IP': ip,  
            'Location': f"{data.get('city')}, {data.get('region')}, {data.get('country')}",  
            'Coordinates': data.get('loc'),  
            'Organization': data.get('org'),  
            'Timezone': data.get('timezone')  
        })  
      
    \# Log results to CloudWatch Logs  
    log\_client = boto3.client('logs')  
    log\_group\_name = 'geoip'  
    log\_stream\_name = 'geolocation\_results'  
      
    \# Ensure the log group exists  
    try:  
        log\_client.create\_log\_group(logGroupName=log\_group\_name)  
    except log\_client.exceptions.ResourceAlreadyExistsException:  
        pass  
  
    \# Ensure the log stream exists  
    try:  
        log\_client.create\_log\_stream(logGroupName=log\_group\_name, logStreamName=log\_stream\_name)  
    except log\_client.exceptions.ResourceAlreadyExistsException:  
        pass  
      
    \# Put log events for each location  
    log\_events = \[\]  
    for result in results:  
        log\_events.append({  
            'timestamp': int(time.time() \* 1000),  \# Current time in milliseconds  
            'message': json.dumps(result)  
        })  
      
    \# Split log events into batches of 10 (AWS limit for PutLogEvents)  
    batch\_size = 10  
    for i in range(0, len(log\_events), batch\_size):  
        response = log\_client.put\_log\_events(  
            logGroupName=log\_group\_name,  
            logStreamName=log\_stream\_name,  
            logEvents=log\_events\[i:i+batch\_size\]  
        )  
      
    return {  
        'statusCode': 200,  
        'body': json.dumps(results)  
    }

**Requête CloudWatch — IP uniques par sous-domaine**

fields @message  
| parse @message /"remote\_ip": "(?<remote\_ip>\[^"\]+)"/  
| stats count\_distinct(remote\_ip) as unique\_ip by remote\_ip  
| sort unique\_ip desc

![](./img-004.png)

**Requête CloudWatch — géolocalisation**

fields @timestamp, @message  
| parse @message /"IP": "(?<ip>\[^"\]+)", "Location": "(?<location\>\[^"\]+)"/  
| stats count() by ip, location  
| sort count desc

![](./img-005.png)

### Conclusion

En combinant **Caddy** sur **EC2**, **CloudWatch**, **Step Functions** et **Lambda**, on obtient une infra web plus simple à exploiter, avec supervision et automatisation utiles pour un coût maîtrisé.

---

*Publié à l’origine sur [Medium](https://medium.com/@antoine.boucher012/making-caddy-aws-ec2-cloudwatch-step-functions-and-lambda-work-together-creating-a-cheap-and-990fd0d9427d).*
