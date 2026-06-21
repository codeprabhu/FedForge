# FedForge Architecture

## 1. Vision

### Goal

FedForge is a distributed federated-learning orchestration platform designed to coordinate training workloads across independent worker nodes.

The objective is not merely to implement FedAvg, but to build a reusable distributed systems platform capable of supporting:

* Federated learning experiments
* Multiple aggregation strategies
* Distributed worker pools
* Monitoring and observability
* Multi-machine deployments
* Future security and authentication features

---

## 2. Architectural Principles

### Separation of Concerns

Each component owns a clearly defined responsibility.

| Component   | Responsibility                      |
| ----------- | ----------------------------------- |
| Coordinator | Orchestration and control           |
| Worker      | Training and dataset ownership      |
| PostgreSQL  | Metadata persistence                |
| Frontend    | Visualization and control           |
| Redis       | Coordination and messaging (future) |

No component should perform responsibilities belonging to another component.

---

### Data Locality

Datasets belong to workers.

Training data must never pass through the coordinator.

The coordinator only handles:

* Scheduling commands
* Model parameters
* Metrics
* Metadata

This mirrors production federated learning systems.

---

### Fault Tolerance

Workers are treated as disposable compute resources.

Workers may:

* Disconnect
* Crash
* Restart
* Become unavailable

The coordinator must continue operating despite worker failures.

Training rounds operate on available capacity rather than fixed worker identities.

---

### Container First

Every service must be deployable as a Docker container.

Development and production should run identical container images.

---

### Multi-Machine Ready

The architecture must support:

* Single machine deployment
* Multiple VMs
* Cloud infrastructure

without requiring architectural changes.

---

## 3. System Architecture

```text
Browser
    |
React Frontend
    |
Coordinator API
    |
Coordinator
    |
------------------------------------------------
|                    |                         |
PostgreSQL         Redis                  WebSockets
|
------------------------------------------------
|
Worker Pool
|
|------ Worker A
|------ Worker B
|------ Worker C
```

---

## 4. Coordinator Architecture

### Purpose

The coordinator acts as the system control plane.

### Responsibilities

* Worker registration
* Heartbeat tracking
* Worker monitoring
* Event generation
* Training orchestration
* Round management
* Aggregation
* Metrics collection

### Non-Responsibilities

The coordinator must never:

* Own datasets
* Perform training
* Store raw training data

---

## 5. Worker Architecture

### Purpose

Workers act as execution nodes.

### Responsibilities

* Maintain local datasets
* Execute training
* Report metrics
* Submit model updates
* Send heartbeats

Workers may run on:

* Local machines
* Docker containers
* VMs
* Cloud instances

Each worker is independent.

---

### Internal Worker Architecture

```text
WorkerRuntime
      ↓
RegistrationService
      ↓
WorkerClient
      ↓
Coordinator API
```

#### Identity Layer

Components:

```text
WorkerIdentity
IdentityStore
IdentityManager
```

Responsibilities:

* Persist worker identity
* Recover identity after restart

Identity generation remains coordinator-owned.

---

#### Runtime Layer

Component:

```text
WorkerRuntime
```

Responsibilities:

* Startup orchestration
* Registration
* Heartbeat startup
* Future training execution

---

#### Communication Layer

Component:

```text
WorkerClient
```

Responsibilities:

* Registration
* Heartbeats
* Future task communication

---

#### Heartbeat Layer

Component:

```text
HeartbeatService
```

Responsibilities:

* Maintain worker liveness
* Periodically notify coordinator

---

### Worker Lifecycle

Current:

```text
Worker Start
    ↓
Load Identity
    ↓
Register If Needed
    ↓
Persist Identity
    ↓
Start Heartbeat Loop
    ↓
Wait For Work
```

Future:

```text
Worker Start
    ↓
Register
    ↓
Receive Training Task
    ↓
Train
    ↓
Submit Update
    ↓
Wait For Next Task
```

---

## 6. Monitoring & Event Architecture

FedForge separates:

### Current State

Stored in:

```text
workers
```

Contains:

* Current status
* Last heartbeat
* Latest metadata

---

### Historical State

Stored in:

```text
worker_events
```

Contains:

* Worker lifecycle history
* Operational audit trail

Events are immutable.

Examples:

```text
WORKER_REGISTERED
WORKER_ONLINE
WORKER_OFFLINE
```

---

### Event Flow

Registration:

```text
WorkerRegistry
    ↓
EventLogger
    ↓
WorkerEventRepository
    ↓
PostgreSQL
```

Offline Detection:

```text
WorkerMonitor
    ↓
EventLogger
    ↓
WorkerEventRepository
    ↓
PostgreSQL
```

---

### EventLogger

Responsibilities:

* Create events
* Apply timestamp policy
* Persist through repositories

EventLogger does not own:

* Database sessions
* Transactions
* SQLAlchemy models

---

## 7. Training Architecture

### Dataset Manager

Responsibilities:

* Download datasets
* Partition datasets
* Assign shards
* Track ownership

Supported strategies:

* IID
* Non-IID

Future:

* Dirichlet partitioning

Datasets remain worker-local.

---

### Aggregation Engine

The aggregation engine is pluggable.

Interface:

```text
AggregationStrategy
```

Implementations:

* FedAvg (v1)
* FedProx (future)
* FedAdam (future)

The coordinator performs aggregation after receiving worker updates.

---

### Metrics Service

Tracks:

* Accuracy
* Loss
* Participation rate
* Throughput
* Worker uptime
* Round duration

Metrics are persisted in PostgreSQL.

---

## 8. Persistence Layer

### Workers Table

Stores:

```text
worker_id
status
last_seen
dataset_size
uptime
```

---

### Worker Events Table

Stores:

```text
event_id
worker_id
event_type
created_at
```

---

### Experiments Table (Future)

Stores:

```text
experiment_id
dataset
strategy
created_at
```

---

### Rounds Table (Future)

Stores:

```text
round_number
accuracy
loss
duration
```

---

### Metrics Table (Future)

Stores:

```text
worker metrics
training metrics
resource metrics
```

---

## 9. Communication Flows

### Registration

```text
Worker
    ↓
Register
    ↓
Coordinator
    ↓
Persist Worker
```

---

### Heartbeats

```text
Worker
    ↓
Heartbeat
    ↓
Coordinator
    ↓
Update last_seen
```

---

### Training Round

```text
Coordinator
    ↓
Select Workers
    ↓
Distribute Model
    ↓
Train Locally
    ↓
Receive Updates
    ↓
Aggregate
    ↓
Publish Metrics
```

---

## 10. Deployment Architecture

### Development

Docker Compose

Services:

* coordinator
* postgres
* worker

Future:

* redis
* frontend

---

### Production Simulation

VM 1

* coordinator
* postgres
* redis
* frontend

VM 2+

* worker

Workers connect through network endpoints.

No architectural changes required.

---

## 11. Observability

### Worker Metrics

* Online status
* Last heartbeat
* Dataset size
* Uptime

### Coordinator Metrics

* Active workers
* Active rounds
* Aggregation latency

### Training Metrics

* Accuracy
* Loss
* Participation rate

---

## 12. Future Roadmap

### Authentication

* JWT
* OAuth

### Authorization

* RBAC

### Infrastructure

* Kubernetes
* Helm

### Monitoring

* Prometheus
* Grafana

### Tracing

* OpenTelemetry

### Federated Learning

* Secure Aggregation
* Differential Privacy
* FedProx
* FedAdam

### Multi-Tenancy

* Organizations
* User Accounts
* Project Isolation

```
```
