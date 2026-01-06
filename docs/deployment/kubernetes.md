# Kubernetes Deployment

Deploy the CV/resume website to a Kubernetes cluster.

## Overview

The Kubernetes deployment includes:
- **Deployments**: CV site and Linktree site (Nginx pods)
- **Services**: ClusterIP services for internal access
- **Ingress**: External access via Traefik or Ingress controller
- **ConfigMaps**: Nginx configurations
- **Volumes**: Static content storage

## Prerequisites

- Kubernetes cluster (1.20+)
- kubectl configured
- Access to cluster
- (Optional) Helm 3.0+ for Helm charts

## Quick Start

### 1. Create Namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

### 2. Create ConfigMaps

```bash
kubectl apply -f k8s/configmaps.yaml
```

### 3. Deploy Services

```bash
kubectl apply -f k8s/
```

Or deploy all at once:
```bash
kubectl apply -f k8s/ -R
```

### 4. Verify Deployment

```bash
# Check pods
kubectl get pods -n cv-stack

# Check services
kubectl get svc -n cv-stack

# Check ingress
kubectl get ingress -n cv-stack
```

## Deployment Components

### Namespace
- **Name**: `cv-stack`
- **Purpose**: Isolate CV website resources

### Deployments

#### CV Site Deployment
- **Replicas**: 2 (configurable)
- **Image**: `nginx:alpine`
- **Resources**: 64Mi-128Mi memory, 50m-100m CPU
- **Health Checks**: Liveness and readiness probes

#### Linktree Site Deployment
- Similar configuration to CV site
- Serves `linktree/` directory

### Services
- **Type**: ClusterIP (internal access)
- **Port**: 80
- **Selector**: Matches deployment labels

### Ingress
- **Controller**: Traefik (or your Ingress controller)
- **Host**: Configured in ingress.yaml
- **TLS**: Optional, configure certificates

### ConfigMaps
- **nginx-configs**: Contains Nginx configuration files
- **Mounted**: At `/etc/nginx/conf.d/` in pods

### Volumes
- **Static Content**: HostPath or PersistentVolume
- **Config**: ConfigMap volume for Nginx configs

## Configuration

### Update Replicas

Edit `k8s/cv-site-deployment.yaml`:
```yaml
spec:
  replicas: 3  # Change number of replicas
```

Apply changes:
```bash
kubectl apply -f k8s/cv-site-deployment.yaml
```

### Update Resources

Edit resource limits in deployment files:
```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "200m"
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

## Using Helm (Optional)

If using Helm charts:

```bash
# Install
helm install cv-stack ./helm/cv-stack

# Upgrade
helm upgrade cv-stack ./helm/cv-stack

# Uninstall
helm uninstall cv-stack
```

## Scaling

### Manual Scaling

```bash
# Scale CV site
kubectl scale deployment/cv-site --replicas=3 -n cv-stack

# Scale Linktree site
kubectl scale deployment/linktree-site --replicas=2 -n cv-stack
```

### Auto-scaling (HPA)

Create HorizontalPodAutoscaler:
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

### Check Pod Status

```bash
kubectl get pods -n cv-stack -o wide
```

### View Logs

```bash
# All pods
kubectl logs -f -l app=cv-site -n cv-stack

# Specific pod
kubectl logs <pod-name> -n cv-stack
```

### Describe Resources

```bash
kubectl describe deployment/cv-site -n cv-stack
kubectl describe service/cv-site -n cv-stack
```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod events
kubectl describe pod <pod-name> -n cv-stack

# Check logs
kubectl logs <pod-name> -n cv-stack
```

### Service Not Accessible

```bash
# Verify service endpoints
kubectl get endpoints -n cv-stack

# Test service from within cluster
kubectl run -it --rm debug --image=busybox --restart=Never -n cv-stack -- wget -O- http://cv-site:80
```

### Ingress Issues

```bash
# Check ingress status
kubectl describe ingress -n cv-stack

# Verify ingress controller
kubectl get pods -n ingress-nginx  # or your ingress namespace
```

## Production Considerations

1. **Use specific image tags** (not `latest`)
2. **Set resource requests/limits** appropriately
3. **Enable TLS/HTTPS** via Ingress
4. **Configure autoscaling** (HPA)
5. **Set up monitoring** (Prometheus, Grafana)
6. **Use PersistentVolumes** for static content
7. **Configure backup** strategies
8. **Set up network policies** for security
9. **Use secrets** for sensitive data
10. **Enable pod disruption budgets**

## Cleanup

Remove all resources:

```bash
kubectl delete -f k8s/
# Or
kubectl delete namespace cv-stack
```

## Next Steps

- [Docker Deployment](./docker.md) - Alternative deployment method
- [Infrastructure Docs](../infrastructure/kubernetes.md) - Detailed K8s documentation
- [GitHub Pages](./github-pages.md) - Simpler deployment option
