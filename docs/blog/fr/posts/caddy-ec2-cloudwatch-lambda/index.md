# Faire travailler ensemble Caddy, EC2, CloudWatch, Step Functions et Lambda

> Caddy sur EC2 pas cher — logs structurés, CloudWatch Insights, cron Python, requêtes Lambda.

- Page HTML: https://antoineboucher.info/CV/blog/fr/posts/caddy-ec2-cloudwatch-lambda/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/posts/caddy-ec2-cloudwatch-lambda/index.md
- Publié: 2024-05-14
- Mis à jour: 2026-05-22
- Tags: AWS, Caddy, EC2, CloudWatch, Lambda, Step Functions
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)**Caddy** déjà à la maison pour Home Assistant ; ici la version **bordure AWS** : **EC2**, HTTPS auto, logs JSON vers **CloudWatch**, shipper Python en cron, **Lambda** pour requêtes Insights.

## Étape 1 — EC2 + Caddy

Instance nano/micro, ports 22/80/443, install yum depuis dépôt Caddy. `Caddyfile` avec snippets `log_site` et `reverse_proxy`. `sudo caddy reload`.

![EC2](images/img-001.png) ![SG](images/img-002.png)

## Étape 2 — CloudWatch

Logs rotatifs sous `/home/ec2-user/caddy/logs/`, script **boto3** `put_log_events`, cron nocturne.

## Étape 3 — Lambda / Insights

Exemple IP distinctes :

```sql
fields @message
| parse @message /"remote_ip": "(?<remote_ip>[^"]+)"/
| stats count_distinct(remote_ip) as unique_ip by remote_ip
```

![Résultats](images/img-004.png)

## Bilan

Visibilité reverse-proxy sans SaaS cher — avec délai cron accepté.

## Articles liés

- [Lab réseau maison](https://antoineboucher.info/CV/blog/fr/posts/home-networking-evolution/)
- [Certification AWS Cloud Practitioner](https://antoineboucher.info/CV/blog/fr/posts/aws-certified-cloud-practitioner/)

---

*[Medium](https://medium.com/@antoine.boucher012/making-caddy-aws-ec2-cloudwatch-step-functions-and-lambda-work-together-creating-a-cheap-and-990fd0d9427d).*
