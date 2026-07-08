export interface Worker {
    worker_id: string;
    status: string;
    last_seen: string;
}

export interface Task {
    task_id: string;
    worker_id: string;
    status: string;
    task_type: string;
}