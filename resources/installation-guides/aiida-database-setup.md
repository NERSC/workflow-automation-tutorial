# AiiDA Database Setup Guide for NERSC/Perlmutter

This guide covers deploying PostgreSQL and RabbitMQ as infrastructure for AiiDA workflows on NERSC systems.

## Overview

AiiDA requires a relational database (PostgreSQL) for provenance storage and a message broker (RabbitMQ) for daemon coordination. This guide covers both components.

**Two deployment options:**
1. **SPIN (recommended):** Persistent containerized PostgreSQL + RabbitMQ on NERSC's Kubernetes platform
2. **Dedicated Allocation (fallback):** PostgreSQL + RabbitMQ in long-running batch job with workflow QOS

## Option 1: SPIN Deployment (Recommended)

SPIN is NERSC's Kubernetes-based platform for persistent services. It's ideal for AiiDA because:
- Runs independently of batch allocations
- Survives restarts automatically
- Accessible from Perlmutter compute nodes
- No allocation hours consumed
- Scalable storage for provenance data

### Prerequisites

- SPIN account (request at https://iris.nersc.gov/spin)
- Basic familiarity with Docker/containers
- Access to NERSC registry (registry.nersc.gov)

### Step 1: Create PostgreSQL Container

**Create Dockerfile for PostgreSQL:**
```dockerfile
FROM postgres:15-alpine

ENV POSTGRES_DB=aiida_db
ENV POSTGRES_USER=aiida
# CHANGE THIS PASSWORD
ENV POSTGRES_PASSWORD=YOUR_SECURE_PASSWORD_HERE

# Enable connection from Perlmutter
RUN echo "host    all    all    0.0.0.0/0    md5" >> /var/lib/postgresql/data/pg_hba.conf

# Optimize for AiiDA workloads
RUN echo "shared_buffers = 256MB" >> /var/lib/postgresql/postgresql.conf && \
    echo "effective_cache_size = 1GB" >> /var/lib/postgresql/postgresql.conf && \
    echo "work_mem = 16MB" >> /var/lib/postgresql/postgresql.conf && \
    echo "maintenance_work_mem = 64MB" >> /var/lib/postgresql/postgresql.conf && \
    echo "max_connections = 200" >> /var/lib/postgresql/postgresql.conf && \
    echo "max_prepared_transactions = 100" >> /var/lib/postgresql/postgresql.conf

EXPOSE 5432
```

**Build and push to registry:**
```bash
docker build -t registry.nersc.gov/$USER/postgresql-aiida:15-alpine .
docker push registry.nersc.gov/$USER/postgresql-aiida:15-alpine
```

### Step 2: Create RabbitMQ Container

**Create Dockerfile for RabbitMQ:**
```dockerfile
FROM rabbitmq:3.12-management-alpine

# Enable required plugins
RUN rabbitmq-plugins enable rabbitmq_management rabbitmq_federation

# Create default user (CHANGE PASSWORD)
ENV RABBITMQ_DEFAULT_USER=aiida
ENV RABBITMQ_DEFAULT_PASS=YOUR_RABBITMQ_PASSWORD_HERE

# Optimize for AiiDA daemon coordination
ENV RABBITMQ_VM_MEMORY_HIGH_WATERMARK=0.6

EXPOSE 5672 15672

CMD ["rabbitmq-server"]
```

**Build and push to registry:**
```bash
docker build -t registry.nersc.gov/$USER/rabbitmq-aiida:3.12-alpine .
docker push registry.nersc.gov/$USER/rabbitmq-aiida:3.12-alpine
```

### Step 3: Deploy to SPIN

**Create SPIN deployment manifest (save as `aiida-deployment.yaml`):**
```yaml
---
# PostgreSQL Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgresql-aiida
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgresql-aiida
  template:
    metadata:
      labels:
        app: postgresql-aiida
    spec:
      containers:
      - name: postgresql
        image: registry.nersc.gov/$USER/postgresql-aiida:15-alpine
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: "aiida_db"
        - name: POSTGRES_USER
          value: "aiida"
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: aiida-secrets
              key: postgres-password
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        volumeMounts:
        - name: postgres-data
          mountPath: /var/lib/postgresql/data
        livenessProbe:
          exec:
            command:
            - /bin/sh
            - -c
            - pg_isready -U aiida
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command:
            - /bin/sh
            - -c
            - pg_isready -U aiida
          initialDelaySeconds: 10
          periodSeconds: 5
      volumes:
      - name: postgres-data
        persistentVolumeClaim:
          claimName: postgres-pvc

---
# PostgreSQL Service
apiVersion: v1
kind: Service
metadata:
  name: postgresql-service
  namespace: default
spec:
  type: ClusterIP
  ports:
  - port: 5432
    targetPort: 5432
    protocol: TCP
  selector:
    app: postgresql-aiida

---
# RabbitMQ Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rabbitmq-aiida
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: rabbitmq-aiida
  template:
    metadata:
      labels:
        app: rabbitmq-aiida
    spec:
      containers:
      - name: rabbitmq
        image: registry.nersc.gov/$USER/rabbitmq-aiida:3.12-alpine
        ports:
        - containerPort: 5672
          name: amqp
        - containerPort: 15672
          name: management
        env:
        - name: RABBITMQ_DEFAULT_USER
          value: "aiida"
        - name: RABBITMQ_DEFAULT_PASS
          valueFrom:
            secretKeyRef:
              name: aiida-secrets
              key: rabbitmq-password
        - name: RABBITMQ_VM_MEMORY_HIGH_WATERMARK
          value: "0.6"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        volumeMounts:
        - name: rabbitmq-data
          mountPath: /var/lib/rabbitmq
        livenessProbe:
          exec:
            command:
            - rabbitmq-diagnostics
            - ping
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command:
            - rabbitmq-diagnostics
            - ping
          initialDelaySeconds: 10
          periodSeconds: 5
      volumes:
      - name: rabbitmq-data
        persistentVolumeClaim:
          claimName: rabbitmq-pvc

---
# RabbitMQ Service
apiVersion: v1
kind: Service
metadata:
  name: rabbitmq-service
  namespace: default
spec:
  type: ClusterIP
  ports:
  - port: 5672
    targetPort: 5672
    name: amqp
    protocol: TCP
  - port: 15672
    targetPort: 15672
    name: management
    protocol: TCP
  selector:
    app: rabbitmq-aiida

---
# PostgreSQL PersistentVolumeClaim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: default
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi

---
# RabbitMQ PersistentVolumeClaim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: rabbitmq-pvc
  namespace: default
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi

---
# Secret for database credentials
apiVersion: v1
kind: Secret
metadata:
  name: aiida-secrets
  namespace: default
type: Opaque
stringData:
  postgres-password: "YOUR_SECURE_PASSWORD_HERE"
  rabbitmq-password: "YOUR_RABBITMQ_PASSWORD_HERE"
```

**Create secrets and deploy to SPIN:**
```bash
# Edit aiida-deployment.yaml and set actual passwords

# Apply manifest
kubectl apply -f aiida-deployment.yaml

# Monitor deployment
kubectl get pods
kubectl logs deployment/postgresql-aiida
kubectl logs deployment/rabbitmq-aiida
```

**Get service endpoints:**
```bash
kubectl get service postgresql-service
kubectl get service rabbitmq-service
# Note the CLUSTER-IP addresses (e.g., 10.100.x.x and 10.100.y.y)
```

### Step 4: Configure AiiDA Profile

Once PostgreSQL and RabbitMQ are running on SPIN, configure AiiDA to connect.

**Create AiiDA profile using `verdi presto`:**
```bash
verdi presto --use-postgres
# Interactive prompts:
# - Profile name: default (or custom name)
# - PostgreSQL hostname: 10.100.x.x (PostgreSQL service CLUSTER-IP)
# - PostgreSQL port: 5432
# - PostgreSQL database: aiida_db
# - PostgreSQL user: aiida
# - PostgreSQL password: (enter password from secret)
# - First name: (e.g., "Research")
# - Last name: (e.g., "User")
# - Email: user@institution.edu
```

**Verify profile:**
```bash
verdi profile list
verdi status
```

### Step 5: Register Perlmutter Computer

Configure Perlmutter as a remote compute resource accessible to AiiDA.

**Interactive setup:**
```bash
verdi computer setup
# Prompts:
# - Label: perlmutter
# - Hostname: perlmutter.nersc.gov
# - Description: NERSC Perlmutter system
# - Transport plugin: core.ssh
# - Scheduler plugin: core.slurm
# - Work directory: /pscratch/sd/$USER/aiida_workdir
# - Shebang line: #!/bin/bash
# - Username: (your NERSC username)
```

**Configure SSH for key-based auth:**
```bash
# Generate key pair if needed
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_perlmutter -N ""

# Add to Perlmutter authorized_keys (one-time setup)
ssh perlmutter.nersc.gov "cat >> ~/.ssh/authorized_keys" < ~/.ssh/id_ed25519_perlmutter.pub

# Test connection
verdi computer test perlmutter
```

**Configure computation defaults:**
```bash
verdi computer configure core.ssh perlmutter
# Set:
# - proxy_command: (leave blank if direct access)
# - username: (your NERSC username)
# - port: 22
# - look_for_private_keys: True
# - key_filename: ~/.ssh/id_ed25519_perlmutter
# - timeout: 60
```

### Step 6: Start AiiDA Daemon

The daemon processes workflow submissions and manages calculations.

**Start daemon:**
```bash
verdi daemon start
verdi daemon status
```

**Create daemon queue (for background processes):**
```bash
verdi devel create-worker default
```

### Step 7: Test Database Connection

**From Perlmutter login node:**
```bash
module load python
python << 'EOF'
import psycopg2

try:
    conn = psycopg2.connect(
        host="10.100.x.x",
        port=5432,
        database="aiida_db",
        user="aiida",
        password="YOUR_PASSWORD"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    print("PostgreSQL connection successful!")
    print(cursor.fetchone())
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
EOF
```

**Test RabbitMQ connection:**
```bash
python << 'EOF'
import pika

try:
    credentials = pika.PlainCredentials('aiida', 'YOUR_RABBITMQ_PASSWORD')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('10.100.y.y', 5672, credentials=credentials)
    )
    print("RabbitMQ connection successful!")
    connection.close()
except Exception as e:
    print(f"Connection failed: {e}")
EOF
```

**Test AiiDA daemon:**
```bash
verdi status
# Should show:
# - Profile active
# - PostgreSQL connected
# - Broker (RabbitMQ) connected
# - Daemon running
```

## Option 2: Dedicated Allocation (Fallback)

If SPIN access unavailable, run PostgreSQL and RabbitMQ in a persistent batch allocation.

### Step 1: Request Workflow QOS

Workflow QOS minimizes allocation hours for lightweight coordination processes.

**Request via NERSC ticket:**
- Subject: "Request workflow QOS access"
- Body: "I need workflow QOS for running AiiDA databases on Perlmutter"
- Include NERSC repository (e.g., m4408)

### Step 2: Build Local PostgreSQL and RabbitMQ

**Download and compile PostgreSQL (if modules unavailable):**
```bash
# Check available versions
module avail postgresql
module load postgresql  # Use available version

# If not available, compile locally
wget https://ftp.postgresql.org/pub/source/v15.2/postgresql-15.2.tar.gz
tar xzf postgresql-15.2.tar.gz
cd postgresql-15.2
./configure --prefix=$HOME/local/postgresql --with-python
make
make install
export PATH=$HOME/local/postgresql/bin:$PATH
```

**Build RabbitMQ (if modules unavailable):**
```bash
# Check for Erlang (RabbitMQ dependency)
module avail erlang

# If not available, use community Docker image in allocation
# See container-based approach below
```

### Step 3: Start Services in Batch Job

**Create batch script `start_aiida_services.sh`:**
```bash
#!/bin/bash
#SBATCH --qos=workflow
#SBATCH --constraint=cpu
#SBATCH --nodes=1
#SBATCH --time=168:00:00  # 1 week
#SBATCH --account=m4408  # Change to your account
#SBATCH --job-name=aiida-services

set -e

# Load modules
module load python postgresql

# Create directories
mkdir -p $SCRATCH/aiida_services/{postgres,rabbitmq}
export PGDATA=$SCRATCH/aiida_services/postgres
export RABBITMQ_MNESIA_BASE=$SCRATCH/aiida_services/rabbitmq

# Initialize PostgreSQL
if [ ! -d "$PGDATA" ]; then
    echo "Initializing PostgreSQL database..."
    initdb -D $PGDATA \
        -U aiida \
        --locale en_US.UTF-8 \
        --auth-local trust \
        --auth-host md5
fi

# Configure PostgreSQL
cat >> $PGDATA/postgresql.conf << 'PGCONF'
listen_addresses = '*'
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 16MB
maintenance_work_mem = 64MB
max_connections = 200
max_prepared_transactions = 100
PGCONF

cat > $PGDATA/pg_hba.conf << 'PGHBA'
local   all             all                                     trust
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
host    all             all             0.0.0.0/0               md5
PGHBA

# Set PostgreSQL password
echo "Setting PostgreSQL password..."
pg_ctl -D $PGDATA -l $SCRATCH/aiida_services/postgres.log start
sleep 3
psql -U aiida -d postgres << PSQL
ALTER USER aiida WITH PASSWORD 'YOUR_SECURE_PASSWORD_HERE';
CREATE DATABASE aiida_db OWNER aiida;
PSQL
pg_ctl -D $PGDATA stop

# Start PostgreSQL
echo "Starting PostgreSQL..."
pg_ctl -D $PGDATA -l $SCRATCH/aiida_services/postgres.log start

# Start RabbitMQ (using Singularity if available, or prebuilt binary)
echo "Starting RabbitMQ..."
# Option A: Use Singularity container
singularity run docker://rabbitmq:3.12-management-alpine \
    -e RABBITMQ_DEFAULT_USER=aiida \
    -e RABBITMQ_DEFAULT_PASS=YOUR_RABBITMQ_PASSWORD_HERE \
    > $SCRATCH/aiida_services/rabbitmq.log 2>&1 &

# OR Option B: Use precompiled binary (if available)
# export PATH=$HOME/local/rabbitmq/sbin:$PATH
# rabbitmq-server > $SCRATCH/aiida_services/rabbitmq.log 2>&1 &

echo "AiiDA services started on $(hostname)"
echo "PostgreSQL: localhost:5432"
echo "RabbitMQ: localhost:5672"

# Keep job alive
wait
```

**Submit job:**
```bash
sbatch start_aiida_services.sh
squeue -u $USER
```

**Get service hostname:**
```bash
squeue -u $USER -o "%.18i %.9P %.8j %.8u %.2t %.10M %.6D %R"
# Note the NODELIST (e.g., nid002345)
```

### Step 4: Configure AiiDA Profile for Dedicated Services

**Setup profile with local databases:**
```bash
verdi presto --use-postgres
# Prompts:
# - PostgreSQL hostname: nid002345 (replace with node from squeue)
# - PostgreSQL port: 5432
# - PostgreSQL database: aiida_db
# - PostgreSQL user: aiida
# - PostgreSQL password: YOUR_SECURE_PASSWORD_HERE
```

**Configure Perlmutter computer (same as Option 1, Step 5):**
```bash
verdi computer setup
# Same configuration as Option 1
```

**Start daemon:**
```bash
verdi daemon start
verdi daemon status
```

### Step 5: Limitations and Monitoring

**Limitations of dedicated allocation:**
- Must update hostname in profile if allocation restarts on different node
- Services stop when allocation time expires
- Requires workflow QOS access
- Less robust than SPIN

**Monitor services:**
```bash
# Check allocation
squeue -u $USER --long

# Monitor database
psql -h nid002345 -U aiida -d aiida_db -c "SELECT * FROM information_schema.tables;"

# Monitor RabbitMQ
rabbitmqctl -n rabbit status
```

## Security Considerations

**Database password management:**
- NEVER commit passwords to git repositories
- Store passwords in secure location outside repository (e.g., `~/.aiida/secrets/`)
- Use `chmod 600` on password files
- Use Kubernetes Secrets for SPIN deployments
- Rotate passwords regularly

**RabbitMQ security:**
- Change default credentials immediately
- Disable guest user if not needed
- Configure firewall rules to restrict access
- Use SSL/TLS for remote connections

**PostgreSQL security:**
- Use strong passwords (min 12 characters, mixed case/numbers/symbols)
- Restrict connections to trusted networks
- Enable SSL/TLS for SPIN deployments
- Regular backups to prevent data loss

**Network access:**
- SPIN services accessible only from NERSC internal network
- Compute nodes can connect (Perlmutter → SPIN routable)
- External access requires VPN or SSH tunnel
- Test connectivity from compute nodes

## Troubleshooting

**PostgreSQL connection failures:**
```bash
# Check PostgreSQL running (SPIN)
kubectl get pods -l app=postgresql-aiida
kubectl logs deployment/postgresql-aiida

# Check PostgreSQL running (dedicated)
pg_ctl -D $PGDATA status

# Test connection with psql
psql -h 10.100.x.x -U aiida -d aiida_db -c "SELECT 1;"

# Verify password correct
echo "SELECT 1;" | psql -h 10.100.x.x -U aiida -W aiida_db
# Enter password when prompted
```

**RabbitMQ connection failures:**
```bash
# Check RabbitMQ running (SPIN)
kubectl get pods -l app=rabbitmq-aiida
kubectl logs deployment/rabbitmq-aiida

# Check RabbitMQ running (dedicated)
ps aux | grep rabbitmq

# Test RabbitMQ connection
python << 'EOF'
import pika
try:
    conn = pika.BlockingConnection(
        pika.ConnectionParameters('10.100.y.y', 5672,
        credentials=pika.PlainCredentials('aiida', 'PASSWORD'))
    )
    print("RabbitMQ OK")
    conn.close()
except Exception as e:
    print(f"RabbitMQ error: {e}")
EOF
```

**AiiDA daemon won't start:**
```bash
# Check daemon status
verdi daemon status

# Increase debug level
verdi daemon --debug

# Check log files
tail -f ~/.aiida/daemon/worker.log

# Verify profile active
verdi profile list
verdi status
```

**Slow database queries:**
```bash
# Check PostgreSQL configuration
psql -h 10.100.x.x -U aiida -d aiida_db -c "SHOW all;" | grep -i shared_buffers

# Monitor active connections
psql -h 10.100.x.x -U aiida -d aiida_db -c "SELECT * FROM pg_stat_activity;"

# Increase resource limits in SPIN
# Edit deployment and increase memory/CPU requests
```

**Out of disk space:**
```bash
# Check SPIN PVC usage
kubectl get pvc

# Resize PostgreSQL PVC (requires downtime)
kubectl patch pvc postgres-pvc -p \
  '{"spec":{"resources":{"requests":{"storage":"100Gi"}}}}'

# Check database size
psql -h 10.100.x.x -U aiida -d aiida_db \
  -c "SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname)) FROM pg_database;"
```

## Performance Tuning

**For large provenance databases (>1M nodes):**
- Increase PostgreSQL shared_buffers: `shared_buffers = 512MB`
- Enable parallelization: `max_parallel_workers = 4`
- Adjust work_mem for sorts: `work_mem = 32MB`
- Create indexes on frequently queried fields

**For high-frequency daemon operations:**
- Increase RabbitMQ memory: `RABBITMQ_VM_MEMORY_HIGH_WATERMARK=0.8`
- Enable RabbitMQ compression for large messages
- Configure multiple daemon workers: `verdi devel create-worker worker2`

**For long-running workflows:**
- Enable PostgreSQL connection pooling (PgBouncer)
- Configure RabbitMQ durable queues
- Set appropriate workflow timeouts in AiiDA configuration

## Backup and Recovery

**PostgreSQL backups:**
```bash
# Full backup
pg_dump -h 10.100.x.x -U aiida aiida_db > aiida_backup.sql

# Continuous archival
pg_basebackup -h 10.100.x.x -U aiida -D /path/to/backup -Ft

# Restore from backup
psql -h 10.100.x.x -U aiida -d aiida_db < aiida_backup.sql
```

**RabbitMQ message persistence:**
- Enabled by default in SPIN manifests
- Survives RabbitMQ restarts
- Check with: `rabbitmqctl report | grep queue`

**AiiDA provenance export:**
```bash
# Export complete provenance
verdi archive create --all complete_study.aiida

# Export specific workflow
verdi archive create --nodes <PK> workflow_snapshot.aiida

# Verify export integrity
verdi archive inspect workflow_snapshot.aiida
```

## Next Steps

After PostgreSQL + RabbitMQ setup:
1. Verify profile and daemon: `verdi status`
2. Test connection from compute node: `verdi process list`
3. See `04-aiida/example1-workflow-def` for first AiiDA workflow
4. See `04-aiida/example2-provenance` for querying provenance
5. See `04-aiida/example3-data-graph` for visualizing workflows
