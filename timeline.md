# FedForge v1 - 14 Day Execution Plan

## Goal

Build a distributed federated-learning orchestration platform that:

* Runs in Docker
* Supports multiple worker nodes
* Uses PostgreSQL for persistence
* Uses FastAPI for orchestration
* Uses React for monitoring
* Supports FedAvg training
* Can be deployed across multiple VMs
* Includes observability, uptime tracking, and experiment monitoring

---

# Day 1 — Repository Foundation & Architecture

## Deliverables

### Repository Structure

```text
fedforge/

├── coordinator/
├── worker/
├── frontend/
├── shared/
├── docs/
├── deployments/
├── scripts/
├── datasets/
└── docker-compose.yml
```

### Documentation

Create:

```text
docs/
├── architecture.md
├── api.md
├── worker-protocol.md
└── deployment.md
```

### Backend Setup

Install:

* FastAPI
* SQLAlchemy
* Alembic
* Pydantic

### Goal

Coordinator launches successfully.

```bash
uvicorn main:app --reload
```

Success Criteria:

```text
GET /
returns coordinator status
```

---

# Day 2 — Worker Registration System

## Deliverables

Implement:

```text
POST /workers/register
GET /workers
GET /workers/{id}
```

Worker startup flow:

```text
Worker
   |
register
   |
Coordinator
```

Store:

```text
worker_id
hostname
ip
status
registered_at
```

Success Criteria:

Worker appears in database after startup.

---

# Day 3 — PostgreSQL Persistence Layer

## Deliverables

Setup:

```text
postgres container
```

Tables:

```text
workers
experiments
rounds
metrics
```

Introduce:

```text
SQLAlchemy ORM
```

Add migration system:

```text
Alembic
```

Success Criteria:

Worker survives coordinator restart.

---

# Day 4 — Heartbeat & Uptime Tracking

## Deliverables

Worker heartbeat service:

```text
POST /heartbeat
```

Coordinator tracks:

```text
last_seen
uptime
status
```

Offline detection:

```text
heartbeat timeout > 30 sec
```

Worker status:

```text
ONLINE
OFFLINE
TRAINING
IDLE
```

Success Criteria:

Stopping worker marks it offline automatically.

---

# Day 5 — Dockerization

## Deliverables

Dockerfiles:

```text
Coordinator
Worker
Frontend
```

Compose:

```text
postgres
coordinator
worker
```

Commands:

```bash
docker compose up
```

Success Criteria:

Entire platform starts through Docker.

---

# Day 6 — WebSocket Infrastructure

## Deliverables

Worker maintains:

```text
persistent websocket
```

Coordinator can:

```text
push commands
receive updates
```

Message schema:

```json
{
  "type": "heartbeat"
}
```

```json
{
  "type": "start_training"
}
```

```json
{
  "type": "training_complete"
}
```

Success Criteria:

Coordinator can push messages to workers.

---

# Day 7 — Frontend MVP

## Deliverables

Setup:

```text
React
Vite
TypeScript
```

Pages:

### Dashboard

Displays:

```text
Coordinator status
Connected workers
System uptime
```

### Workers

Displays:

```text
Worker list
Status
Last heartbeat
```

Success Criteria:

Frontend displays live worker information.

---

# Day 8 — Dataset Manager

## Deliverables

Create:

```text
DatasetService
```

Responsibilities:

```text
Download datasets
Partition datasets
Assign shards
```

Support:

```text
IID partitioning
```

Store:

```text
datasets/client_1/
datasets/client_2/
```

Success Criteria:

Each worker receives a unique dataset shard.

---

# Day 9 — Local Training Engine

## Deliverables

PyTorch integration.

Create:

```text
Trainer
ModelRegistry
```

Support:

```text
MNIST
```

Training API:

```text
train_local()
```

Success Criteria:

Single worker trains locally.

---

# Day 10 — Training Job System

## Deliverables

Coordinator creates:

```text
TrainingJob
```

Workflow:

```text
Coordinator
    |
dispatch job
    |
Workers
    |
train
    |
return results
```

Store:

```text
job_id
worker_id
status
```

Success Criteria:

Coordinator successfully launches training.

---

# Day 11 — FedAvg Aggregation

## Deliverables

Create:

```text
AggregationStrategy
```

Implement:

```text
FedAvg
```

Workflow:

```text
Collect updates
Aggregate weights
Generate global model
```

Store:

```text
round metrics
```

Success Criteria:

Global model updates after aggregation.

---

# Day 12 — Metrics & Experiment Tracking

## Deliverables

Track:

```text
loss
accuracy
training duration
participation rate
```

Database:

```text
experiments
rounds
metrics
```

Frontend charts:

```text
Accuracy vs Round
Loss vs Round
```

Success Criteria:

Training progress visible in dashboard.

---

# Day 13 — Multi-VM Deployment

## Deliverables

Environment:

```text
VM1 Coordinator
VM2 Worker
VM3 Worker
VM4 Worker
```

Options:

```text
VirtualBox
QEMU/KVM
AWS
```

Test:

```text
Cross-machine communication
Training execution
Aggregation
```

Success Criteria:

Workers train across separate machines.

---

# Day 14 — Release Engineering

## Deliverables

README:

```text
Architecture
Features
Deployment
Screenshots
Roadmap
```

Documentation:

```text
API docs
Worker protocol
Deployment guide
```

Demo:

```text
GIF
Video
Screenshots
```

Create:

```text
v1.0 release
```

Tag:

```bash
git tag v1.0
```

Success Criteria:

Fresh clone → docker compose up → fully working platform.

---

# Stretch Goals (Only If Ahead Of Schedule)

## Priority 1

Worker resource monitoring

```text
CPU
RAM
Disk
```

---

## Priority 2

Experiment comparison

```text
Run A
Run B
```

---

## Priority 3

Live training logs

```text
WebSocket streaming
```

---

## Priority 4

Redis-backed job queue

Move orchestration events from memory to Redis.

---

# Explicitly Deferred To V2

Authentication

```text
JWT
OAuth
```

Authorization

```text
RBAC
```

Infrastructure

```text
Kubernetes
Helm
```

Monitoring

```text
Prometheus
Grafana
```

Security

```text
TLS
Secure Aggregation
Differential Privacy
```

Multi-Tenancy

```text
Users
Organizations
Projects
Permissions
```

---

# Definition of Success

A user should be able to:

```bash
git clone fedforge
cd fedforge

docker compose up
```

Open the dashboard and observe:

* Coordinator online
* Multiple workers connected
* Worker uptime updating
* Dataset partitions assigned
* Training jobs executing
* FedAvg aggregation occurring
* Accuracy and loss graphs updating live

without modifying any source code.
