export interface Worker {
    worker_id: string;
    hostname: string;
    ip: string;
    cpu_cores: number;
    memory_gb: number;
    worker_version: string;
    status: string;
    last_seen: string | null;
    registered_at: string;
}

export interface Task {
    task_id: string;
    worker_id: string | null;
    status: string;
    task_type: string;
    round_id: string | null;
    payload: Record<string, unknown>;
    result: TrainingResult | null;
    error_message: string | null;
    created_at: string;
    assigned_at: string | null;
    started_at: string | null;
    completed_at: string | null;
}

export interface TrainingResult {
    accuracy: number;
    loss: number;
    epochs: number;
    num_samples: number;
    training_time_seconds: number;
}

export interface Round {
    round_id: string;
    round_number: number;
    model_name: string;
    dataset_name: string;
    status: string;
    created_at: string;
    completed_at: string | null;
}

export interface WorkerMetric {
    cpu_percent: number;
    memory_percent: number;
    disk_percent: number;
    recorded_at: string;
}

export interface WorkerEvent {
    event_id: string;
    worker_id: string;
    event_type: string;
    created_at: string;
}

export interface DashboardData {
    workers_online: number;
    running_tasks: number;
    completed_tasks: number;
    coordinator_status: string;
}

export interface GlobalModel {
    model_id: number;
    model_name: string;
    version: number;
    created_at: string;
}
