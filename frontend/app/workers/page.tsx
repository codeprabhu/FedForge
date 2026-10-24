"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Worker, WorkerMetric } from "@/lib/types";
import { formatDate, shortId } from "@/lib/format";
import Panel from "@/components/ui/Panel";
import StatusBadge from "@/components/ui/StatusBadge";

export default function WorkersPage() {
    const [workers, setWorkers] = useState<Worker[]>([]);
    const [metrics, setMetrics] = useState<Record<string, WorkerMetric | null>>({});
    const [error, setError] = useState<string | null>(null);
    useEffect(() => { const fetchWorkers = async () => { try { const result = (await api.get<Worker[]>("/workers")).data; setWorkers(result); const pairs = await Promise.all(result.map(async (worker) => { try { return [worker.worker_id, (await api.get<WorkerMetric>(`/workers/${worker.worker_id}/metrics/latest`)).data] as const; } catch { return [worker.worker_id, null] as const; } })); setMetrics(Object.fromEntries(pairs)); setError(null); } catch { setError("Unable to load workers."); } }; void fetchWorkers(); const timer = window.setInterval(() => void fetchWorkers(), 5000); return () => window.clearInterval(timer); }, []);
    return <div className="mx-auto max-w-[1500px] space-y-6"><header><p className="mb-3 text-[10px] uppercase tracking-[0.3em] text-pink-200/80">Compute fleet / v1</p><h1 className="text-4xl font-light tracking-[0.12em]">Workers</h1><p className="mt-2 text-sm text-stone-400">Availability, capacity, identity, and latest reported resource usage.</p></header>{error && <div className="rounded-lg border border-rose-300/30 bg-rose-300/10 px-4 py-3 text-sm text-rose-100">{error}</div>}<div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">{workers.map((worker) => <Panel key={worker.worker_id} title={worker.hostname} eyebrow={shortId(worker.worker_id)}><div className="flex items-center justify-between"><StatusBadge status={worker.status} /><span className="text-xs text-stone-500">v{worker.worker_version}</span></div><div className="mt-5 grid grid-cols-2 gap-4 text-xs"><Metric label="Address" value={worker.ip} /><Metric label="Capacity" value={`${worker.cpu_cores} CPU / ${worker.memory_gb} GB`} /><Metric label="CPU" value={metrics[worker.worker_id] ? `${metrics[worker.worker_id]!.cpu_percent.toFixed(1)}%` : "No sample"} /><Metric label="Memory" value={metrics[worker.worker_id] ? `${metrics[worker.worker_id]!.memory_percent.toFixed(1)}%` : "No sample"} /><Metric label="Disk" value={metrics[worker.worker_id] ? `${metrics[worker.worker_id]!.disk_percent.toFixed(1)}%` : "No sample"} /><Metric label="Last seen" value={formatDate(worker.last_seen)} /></div></Panel>)}{workers.length === 0 && <div className="sm:col-span-2 xl:col-span-3"><Panel title="No workers" eyebrow="Compute fleet"><p className="text-sm text-stone-500">Start a worker to see it register here.</p></Panel></div>}</div></div>;
}
function Metric({ label, value }: { label: string; value: string }) { return <div><p className="text-[10px] uppercase tracking-[0.16em] text-stone-500">{label}</p><p className="mt-1 text-stone-200">{value}</p></div>; }
