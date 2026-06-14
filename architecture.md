# FedForge v1 Architecture Document

## Overview

FedForge is a distributed federated-learning orchestration platform designed to simulate and manage federated training workloads across multiple worker nodes.

The system separates orchestration, training, storage, monitoring, and visualization concerns into distinct components.

The primary objective is not simply to implement FedAvg, but to build a reusable distributed training platform capable of running on multiple machines and supporting future extensions such as authentication, secure aggregation, Kubernetes deployment, and additional training strategies.

---

# Core Design Principles

## Separation of Concerns

Each service has a clearly defined responsibility.

Coordinator:

* Scheduling
* Aggregation
* Worker management

Worker:

* Local training
* Dataset ownership
* Metric reporting

Database:

* Metadata persistence

Frontend:

* Visualization and control

No service should perform responsibilities belonging to another service.

---

## Data Locality

Datasets belong to workers.

Training data must never pass through the coordinator.

The coordinator only handles:

* Model parameters
* Metrics
* Metadata
* Scheduling commands

This mirrors real federated learning systems.

---

## Fault Tolerance

Workers may:

* Disconnect
* Crash
* Restart
* Become unavailable

The coordinator must continue operating even when workers disappear.

Offline workers should not block orchestration.

---

## Container First

Every service must be deployable as a Docker container.

Local development and deployment environments should use identical container images.

---

## Multi-Machine Ready

The architecture should support deployment across:

* Single machine
* Multiple VMs
* Cloud instances

without requiring architectural changes.

---

# High-Level Architecture

```
                Browser
                    |
                    |
              React Frontend
                    |
                    |
                FastAPI API
                    |
  ------------------------------------
  |                |                 |
  |                |                 |
```

PostgreSQL         Redis          WebSockets
|                |                 |
------------------------------------
|
Coordinator
|
-

|                    |                         |
|                    |                         |
Worker A          Worker B                 Worker C
|                    |                         |
Dataset A        Dataset B               Dataset C

---

# Component Design

## Coordinator Service

The coordinator acts as the control plane.

Responsibilities:

* Worker registration
* Heartbeat tracking
* Training orchestration
* Round management
* Model aggregation
* Metric collection
* Event publication

The coordinator never performs local training.

The coordinator never owns training datasets.

---

## Worker Service

Workers act as execution nodes.

Responsibilities:

* Maintain local datasets
* Receive training jobs
* Execute local training
* Report metrics
* Return model updates
* Send heartbeats

Workers may run on:

* Local machine
* Docker container
* Separate VM
* Cloud instance

Each worker is independent.

---

## Dataset Manager

The dataset manager is responsible for:

* Downloading datasets
* Partitioning datasets
* Assigning shards
* Tracking ownership

Supported partition strategies:

* IID
* Non-IID
* Dirichlet (future)

Datasets are stored locally on workers.

---

## Aggregation Engine

The aggregation engine is a pluggable module.

Interface:

AggregationStrategy

Implementations:

* FedAvg (v1)
* FedProx (future)
* FedAdam (future)

The coordinator uses the aggregation engine after receiving worker updates.

---

## Metrics Service

Tracks:

* Worker uptime
* Round duration
* Accuracy
* Loss
* Participation rate
* Throughput

Metrics are persisted in PostgreSQL.

---

## Frontend

Provides:

Dashboard
Workers View
Experiments View
Metrics View

The frontend never directly accesses workers.

All communication occurs through coordinator APIs.

---

# Communication Architecture

## Registration

Worker Startup

Worker -> Coordinator

register(worker_id)

Coordinator stores worker metadata.

---

## Heartbeats

Every worker sends:

heartbeat()

at a fixed interval.

Coordinator updates:

last_seen

Offline workers are detected automatically.

---

## Training Round

Coordinator:

1. Select workers
2. Send model
3. Start round

Workers:

1. Receive model
2. Train locally
3. Return updates

Coordinator:

1. Collect updates
2. Aggregate weights
3. Publish metrics

---

# Persistence Layer

## Workers Table

Stores:

worker_id
status
last_seen
uptime
dataset_size

---

## Experiments Table

Stores:

experiment_id
dataset
strategy
created_at

---

## Rounds Table

Stores:

round_number
accuracy
loss
duration

---

## Metrics Table

Stores:

worker metrics
training metrics
resource metrics

---

# Deployment Model

Development

Docker Compose

Services:

* coordinator
* postgres
* redis
* frontend
* worker

---

Production Simulation

VM1

* coordinator
* postgres
* redis
* frontend

VM2

* worker

VM3

* worker

VM4

* worker

Workers connect through network endpoints.

No code changes required.

---

# Observability

Worker Metrics

* Online status
* Last heartbeat
* Dataset size
* Uptime

Coordinator Metrics

* Active workers
* Active rounds
* Aggregation latency

Training Metrics

* Accuracy
* Loss
* Participation rate

---

# Version 2 Roadmap

Authentication

* JWT
* OAuth

Authorization

* RBAC

Infrastructure

* Kubernetes
* Helm

Monitoring

* Prometheus
* Grafana

Tracing

* OpenTelemetry

Federated Learning

* Secure Aggregation
* Differential Privacy
* FedProx
* FedAdam

Multi-Tenancy

* Organizations
* User Accounts
* Project Isolation

---
