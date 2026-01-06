# CV Stack Helm Chart

This Helm chart deploys the CV Stack application with Traefik, CV Site, and Linktree Site.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- Traefik ingress controller (if using ingress)

## Installation

```bash
# Install the chart
helm install cv-stack ./helm/cv-stack

# Install with custom values
helm install cv-stack ./helm/cv-stack -f my-values.yaml

# Install in a specific namespace
helm install cv-stack ./helm/cv-stack --namespace cv-stack --create-namespace
```

## Configuration

The following table lists the configurable parameters and their default values:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `namespace.name` | Namespace name | `cv-stack` |
| `namespace.create` | Create namespace | `true` |
| `cvSite.enabled` | Enable CV site | `true` |
| `cvSite.replicas` | Number of CV site replicas | `2` |
| `cvSite.image.repository` | CV site image repository | `nginx` |
| `cvSite.image.tag` | CV site image tag | `alpine` |
| `linktreeSite.enabled` | Enable linktree site | `true` |
| `linktreeSite.replicas` | Number of linktree site replicas | `2` |
| `linktreeSite.image.repository` | Linktree site image repository | `nginx` |
| `linktreeSite.image.tag` | Linktree site image tag | `alpine` |
| `traefik.enabled` | Enable Traefik | `true` |
| `traefik.replicas` | Number of Traefik replicas | `1` |
| `traefik.image.repository` | Traefik image repository | `traefik` |
| `traefik.image.tag` | Traefik image tag | `v2.10` |
| `traefik.service.type` | Traefik service type | `LoadBalancer` |
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.className` | Ingress class name | `traefik` |

## Upgrading

```bash
helm upgrade cv-stack ./helm/cv-stack
```

## Uninstallation

```bash
helm uninstall cv-stack
```

## Notes

- The static content volumes use hostPath mounts. Update the paths in the deployment templates to match your environment.
- Traefik RBAC is created by default. Set `traefik.rbac.create: false` to disable.
