# Merlin Redis Setup Guide for NERSC/Perlmutter

This guide covers deploying Redis as a message broker for Merlin workflows on NERSC systems.

## Overview

Merlin requires a persistent message broker (Redis or RabbitMQ) for task coordination. This guide focuses on Redis, which is simpler to deploy and sufficient for most workflows.

**Two deployment options:**
1. **SPIN (recommended):** Persistent containerized Redis on NERSC's Kubernetes platform
2. **Dedicated Allocation (fallback):** Redis in long-running batch job with workflow QOS

## Option 1: SPIN Deployment (Recommended)

SPIN is NERSC's Kubernetes-based platform for persistent services. It's ideal for Redis because:
- Runs independently of batch allocations
- Survives restarts automatically
- Accessible from Perlmutter compute nodes
- No allocation hours consumed

### Prerequisites

- SPIN account (request at https://iris.nersc.gov/spin)
- Basic familiarity with Docker/containers

### Step 1: Create Redis Container

**Create Dockerfile:**
```dockerfile
FROM redis:7.2-alpine

# Enable persistence
RUN echo "save 900 1" >> /etc/redis/redis.conf && \
    echo "save 300 10" >> /etc/redis/redis.conf && \
    echo "save 60 10000" >> /etc/redis/redis.conf

# Set password (CHANGE THIS)
RUN echo "requirepass YOUR_SECURE_PASSWORD_HERE" >> /etc/redis/redis.conf

EXPOSE 6379

CMD ["redis-server", "/etc/redis/redis.conf"]
```

**Build and push to registry:**
```bash
docker build -t registry.nersc.gov/$USER/redis-merlin:latest .
docker push registry.nersc.gov/$USER/redis-merlin:latest
```

### Step 2: Deploy to SPIN

**Create SPIN deployment:**
```yaml
# redis-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-merlin
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis-merlin
  template:
    metadata:
      labels:
        app: redis-merlin
    spec:
      containers:
      - name: redis
        image: registry.nersc.gov/$USER/redis-merlin:latest
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: redis-data
          mountPath: /data
      volumes:
      - name: redis-data
        persistentVolumeClaim:
          claimName: redis-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  type: ClusterIP
  ports:
  - port: 6379
    targetPort: 6379
  selector:
    app: redis-merlin

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

**Apply to SPIN:**
```bash
kubectl apply -f redis-deployment.yaml
```

**Get Redis hostname:**
```bash
kubectl get service redis-service
# Note the CLUSTER-IP (e.g., 10.100.x.x)
```

### Step 3: Configure Merlin

**Edit `~/.merlin/app.yaml`:**
```yaml
broker:
  name: redis
  server: 10.100.x.x  # CLUSTER-IP from above
  port: 6379
  password: /global/homes/u/$USER/.merlin/redis_password  # Store password securely

results_backend:
  name: redis
  server: 10.100.x.x
  port: 6379
  password: /global/homes/u/$USER/.merlin/redis_password
```

**Create password file:**
```bash
echo "YOUR_SECURE_PASSWORD_HERE" > ~/.merlin/redis_password
chmod 600 ~/.merlin/redis_password
```

### Step 4: Test Connection

**From Perlmutter login node:**
```bash
module load python
python -c "import redis; r=redis.Redis(host='10.100.x.x', port=6379, password='YOUR_PASSWORD'); r.ping()"
# Should print: True
```

**Test Merlin:**
```bash
merlin info
# Should show broker connection details
```

## Option 2: Dedicated Allocation (Fallback)

If SPIN access unavailable, run Redis in a persistent batch allocation.

### Step 1: Request Workflow QOS

Workflow QOS minimizes allocation hours for lightweight coordination processes.

**Request via NERSC ticket:**
- Subject: "Request workflow QOS access"
- Body: "I need workflow QOS for running Merlin coordinator on Perlmutter"
- Include NERSC repository (e.g., m4408)

### Step 2: Start Redis in Allocation

**Create batch script `start_redis.sh`:**
```bash
#!/bin/bash
#SBATCH --qos=workflow
#SBATCH --constraint=cpu
#SBATCH --nodes=1
#SBATCH --time=48:00:00
#SBATCH --account=m4408  # Change to your account
#SBATCH --job-name=redis-coordinator

module load redis

# Start Redis with password
redis-server --requirepass YOUR_PASSWORD --save 900 1 --save 300 10 --save 60 10000 --dir $SCRATCH/redis-data

# Keep job alive
wait
```

**Submit:**
```bash
sbatch start_redis.sh
```

**Get Redis hostname:**
```bash
squeue -u $USER -o "%.18i %.9P %.8j %.8u %.2t %.10M %.6D %R"
# Note the NODELIST (e.g., nid002345)
```

### Step 3: Configure Merlin for Dedicated Redis

**Edit `~/.merlin/app.yaml`:**
```yaml
broker:
  name: redis
  server: nid002345  # Replace with actual node from squeue
  port: 6379
  password: /global/homes/u/$USER/.merlin/redis_password

results_backend:
  name: redis
  server: nid002345
  port: 6379
  password: /global/homes/u/$USER/.merlin/redis_password
```

**Limitations:**
- Must update `server` if allocation ends and restarts on different node
- Redis stops when allocation time expires
- Less robust than SPIN deployment

### Step 4: Test Connection

```bash
python -c "import redis; r=redis.Redis(host='nid002345', port=6379, password='YOUR_PASSWORD'); r.ping()"
# Should print: True
```

## Security Considerations

**Password management:**
- NEVER commit passwords to git repositories
- Use `chmod 600` on password files
- Store passwords outside repository (e.g., `~/.merlin/`)

**Network access:**
- SPIN Redis accessible only from NERSC internal network
- Compute nodes can connect (Perlmutter → SPIN routable)
- External access requires VPN or SSH tunnel

## Troubleshooting

**Connection refused:**
- Check Redis is running: `kubectl get pods` (SPIN) or `squeue -u $USER` (allocation)
- Verify firewall/network rules allow port 6379
- Test with `telnet <redis-host> 6379`

**Authentication failed:**
- Verify password matches in `app.yaml` and Redis config
- Check password file permissions (`chmod 600`)
- Test password with `redis-cli`: `redis-cli -h <host> -a <password> ping`

**Workers can't connect:**
- Ensure workers running in environment with `~/.merlin/app.yaml` configured
- Check Redis hostname accessible from compute nodes
- Verify Slurm job network access (some QOS may restrict)

**Redis memory issues:**
- Monitor with `redis-cli INFO memory`
- Increase storage in SPIN PVC if needed
- Configure eviction policy for long-running workflows

## Performance Tuning

**For large workflows (>10k tasks):**
- Increase Redis maxmemory: `maxmemory 4gb`
- Enable persistence: `save 900 1` (avoids data loss on restart)
- Use multiple Redis instances (shard queues)

**For high-throughput workflows:**
- Disable persistence if transient data: `save ""`
- Increase worker concurrency: `--concurrency 64`
- Use `--prefetch-multiplier 1` for long-running HPC tasks

## Next Steps

After Redis setup:
1. Configure Merlin: `merlin config`
2. Test workflow: `merlin run spec.yaml`
3. Start workers: `merlin run-workers spec.yaml`
4. See `03-merlin/example1-distributed` for first distributed workflow
