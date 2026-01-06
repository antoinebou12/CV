# Kubernetes Infrastructure

Detailed documentation for Kubernetes configuration and deployment.

## Overview

Kubernetes is used for:
- **Production deployments**
- **Scaling** and high availability
- **Container orchestration**
- **Service management**

## Components

### Namespace

**File**: `k8s/namespace.yaml`

- **Name**: `cv-stack`
- **Purpose**: Isolate CV website resources

### Deployments

#### CV Site Deployment
**File**: `k8s/cv-site-deployment.yaml`

- **Replicas**: 2 (configurable)
- **Image**: `nginx:alpine`
- **Resources**: 
  - Requests: 64Mi memory, 50m CPU
  - Limits: 128Mi memory, 100m CPU
- **Health Checks**: Liveness and readiness probes
- **Volumes**: Static content, Nginx config

#### Linktree Site Deployment
**File**: `k8s/linktree-site-deployment.yaml`

Similar configuration to CV site.

### Services

**File**: `k8s/services.yaml`

- **Type**: ClusterIP (internal access)
- **Port**: 80
- **Selector**: Matches deployment labels
- **Purpose**: Internal service discovery

### Ingress

**File**: `k8s/ingress.yaml`

- **Controller**: Traefik or your Ingress controller
- **Host**: Configured per environment
- **TLS**: Optional, configure certificates
- **Rules**: Routing to services

### ConfigMaps

**File**: `k8s/configmaps.yaml`

- **nginx-configs**: Contains Nginx configuration files
- **Mounted**: At `/etc/nginx/conf.d/` in pods
- **Purpose**: Centralized configuration management

### Volumes

**File**: `k8s/volumes.yaml`

- **Static Content**: HostPath or PersistentVolume
- **Config**: ConfigMap volume
- **Purpose**: Persistent storage

## Deployment

### Apply All Resources

```bash
kubectl apply -f k8s/
```

### Apply Specific Resource

```bash
kubectl apply -f k8s/cv-site-deployment.yaml
```

### Check Status

```bash
# Pods
kubectl get pods -n cv-stack

# Services
kubectl get svc -n cv-stack

# Deployments
kubectl get deployments -n cv-stack

# Ingress
kubectl get ingress -n cv-stack
```

## Configuration

### Update Replicas

```bash
kubectl scale deployment/cv-site --replicas=3 -n cv-stack
```

Or edit deployment file and apply.

### Update Resources

Edit deployment file:
```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "200m"
```

Apply changes:
```bash
kubectl apply -f k8s/cv-site-deployment.yaml
```

### Update Nginx Config

1. Edit `configs/nginx/cv-site.conf`
2. Update ConfigMap:
   ```bash
   kubectl create configmap nginx-configs \
     --from-file=configs/nginx/ \
     -n cv-stack \
     --dry-run=client -o yaml | kubectl apply -f -
   ```
3. Restart pods:
   ```bash
   kubectl rollout restart deployment/cv-site -n cv-stack
   ```

## Scaling

### Manual Scaling

```bash
kubectl scale deployment/cv-site --replicas=3 -n cv-stack
```

### Horizontal Pod Autoscaler

Create HPA resource:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: cv-site-hpa
  namespace: cv-stack
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: cv-site
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Monitoring

### View Logs

```bash
# All pods with label
kubectl logs -f -l app=cv-site -n cv-stack

# Specific pod
kubectl logs <pod-name> -n cv-stack

# Previous container (if crashed)
kubectl logs <pod-name> -n cv-stack --previous
```

### Describe Resources

```bash
kubectl describe deployment/cv-site -n cv-stack
kubectl describe pod <pod-name> -n cv-stack
kubectl describe service/cv-site -n cv-stack
```

### Events

```bash
kubectl get events -n cv-stack --sort-by='.lastTimestamp'
```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n cv-stack

# Describe pod
kubectl describe pod <pod-name> -n cv-stack

# Check logs
kubectl logs <pod-name> -n cv-stack
```

### Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints -n cv-stack

# Test from within cluster
kubectl run -it --rm debug --image=busybox --restart=Never -n cv-stack -- wget -O- http://cv-site:80
```

### Ingress Issues

```bash
# Check ingress
kubectl describe ingress -n cv-stack

# Verify ingress controller
kubectl get pods -n ingress-nginx
```

## Production Best Practices

1. **Use specific image tags** (not `latest`)
2. **Set appropriate resource limits**
3. **Enable TLS/HTTPS** via Ingress
4. **Configure autoscaling** (HPA)
5. **Set up monitoring** (Prometheus, Grafana)
6. **Use PersistentVolumes** for data
7. **Configure network policies** for security
8. **Use secrets** for sensitive data
9. **Enable pod disruption budgets**
10. **Set up backup strategies**

## Helm Charts (Optional)

If using Helm:

```bash
# Install
helm install cv-stack ./helm/cv-stack

# Upgrade
helm upgrade cv-stack ./helm/cv-stack

# Uninstall
helm uninstall cv-stack
```

## Next Steps

- [Nginx Configuration](./nginx.md) - Nginx setup
- [Kubernetes Deployment](../deployment/kubernetes.md) - Deployment guide
- [Docker Setup](./docker.md) - Docker documentation
