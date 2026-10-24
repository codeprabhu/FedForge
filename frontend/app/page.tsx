"use client";

import { useCallback, useEffect, useState } from "react";
import { api } from "@/lib/api";
import { DashboardData, GlobalModel, Round, Task, Worker, WorkerEvent } from "@/lib/types";
import { formatDate, shortId } from "@/lib/format";
import Panel from "@/components/ui/Panel";
import StatusBadge from "@/components/ui/StatusBadge";

const emptyDashboard: DashboardData = { workers_online: 0, running_tasks: 0, completed_tasks: 0, coordinator_status: "OFFLINE" };

export default function Home() {
    const [dashboard, setDashboard] = useState<DashboardData>(emptyDashboard);
    const [workers, setWorkers] = useState<Worker[]>([]);
    const [tasks, setTasks] = useState<Task[]>([]);
    const [rounds, setRounds] = useState<Round[]>([]);
    const [logs, setLogs] = useState<WorkerEvent[]>([]);
    const [globalModel, setGlobalModel] = useState<GlobalModel | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchOverview = useCallback(async () => {
        try {
            const [dashboardResponse, workersResponse, tasksResponse, roundsResponse, logsResponse, modelResponse] = await Promise.all([
                api.get<DashboardData>("/dashboard"), api.get<Worker[]>("/workers"), api.get<Task[]>("/tasks"),
                api.get<Round[]>("/rounds"), api.get<WorkerEvent[]>("/logs"), api.get<GlobalModel | null>("/global-model/latest", { params: { include_weights: false } }),
            ]);
            setDashboard(dashboardResponse.data); setWorkers(workersResponse.data); setTasks(tasksResponse.data);
            setRounds(roundsResponse.data); setLogs(logsResponse.data); setGlobalModel(modelResponse.data); setError(null);
        } catch { setError("Coordinator unavailable. Check the API and database services."); }
        finally { setLoading(false); }
    }, []);

    useEffect(() => {
        const initialFetch = window.setTimeout(() => void fetchOverview(), 0);
        const interval = window.setInterval(() => void fetchOverview(), 5000);
        return () => { window.clearTimeout(initialFetch); window.clearInterval(interval); };
    }, [fetchOverview]);

    const latestRound = rounds[0];
    const failedTasks = tasks.filter((task) => task.status === "FAILED").length;
    const activeWorkers = workers.filter((worker) => worker.status === "ONLINE").length;

    return (
        <div className="mx-auto max-w-[1500px] space-y-6">
            <header className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
                <div><p className="mb-3 text-[10px] uppercase tracking-[0.3em] text-pink-200/80">Federated operations / v1</p><h1 className="text-4xl font-light tracking-[0.12em] text-stone-100 md:text-6xl">Command center</h1><p className="mt-3 max-w-2xl text-sm text-stone-300">A live view of worker capacity, training rounds, task execution, and global model progress.</p></div>
                <div className="flex items-center gap-3 text-xs text-stone-400"><span className={`h-2 w-2 rounded-full ${dashboard.coordinator_status === "ONLINE" ? "bg-emerald-300" : "bg-rose-300"}`} />{loading ? "Synchronizing" : `Updated ${new Date().toLocaleTimeString()}`}</div>
            </header>

            {error && <div className="rounded-lg border border-rose-300/30 bg-rose-300/10 px-4 py-3 text-sm text-rose-100">{error}</div>}
            <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                {[["Online workers", activeWorkers, `${workers.length} registered`], ["Running tasks", dashboard.running_tasks, `${tasks.length} total tasks`], ["Completed tasks", dashboard.completed_tasks, `${failedTasks} failed`], ["Latest round", latestRound ? `#${latestRound.round_number}` : "—", latestRound?.status ?? "No rounds yet"]].map(([label, value, detail]) => <div key={String(label)} className="rounded-xl border border-white/10 bg-black/25 p-5 backdrop-blur-xl"><p className="text-[10px] uppercase tracking-[0.22em] text-stone-400">{label}</p><p className="mt-3 text-3xl font-light text-stone-100">{value}</p><p className="mt-2 text-xs text-stone-500">{detail}</p></div>)}
            </div>

            <div className="grid gap-6 xl:grid-cols-[1.35fr_1fr]">
                <Panel title="Current federated round" eyebrow="Training state">
                    {latestRound ? <div className="space-y-5"><div className="flex flex-wrap items-center justify-between gap-3"><div><p className="text-xl text-stone-100">Round #{latestRound.round_number}</p><p className="mt-1 text-xs text-stone-500">{latestRound.model_name} · {latestRound.dataset_name}</p></div><StatusBadge status={latestRound.status} /></div><div className="grid gap-3 sm:grid-cols-3"><Info label="Created" value={formatDate(latestRound.created_at)} /><Info label="Completed" value={formatDate(latestRound.completed_at)} /><Info label="Round ID" value={shortId(latestRound.round_id)} /></div><div className="h-2 overflow-hidden rounded-full bg-white/10"><div className={`h-full rounded-full ${latestRound.status === "COMPLETED" ? "w-full bg-emerald-300" : latestRound.status === "FAILED" ? "w-full bg-rose-300" : "w-2/3 bg-pink-300"}`} /></div><div className="border-t border-white/5 pt-4"><Info label="Latest global model" value={globalModel ? `${globalModel.model_name} · version ${globalModel.version}` : "No aggregated model yet"} /></div></div> : <Empty text="The scheduler has not created a training round yet." />}
                </Panel>
                <Panel title="Recent events" eyebrow="Coordinator log">
                    {logs.length ? <div className="max-h-56 space-y-3 overflow-y-auto">{logs.slice(0, 8).map((log) => <div key={log.event_id} className="flex items-start justify-between gap-3 border-b border-white/5 pb-3 text-xs"><div><p className="text-stone-200">{log.event_type.replaceAll("_", " ")}</p><p className="mt-1 font-mono text-stone-500">worker {shortId(log.worker_id)}</p></div><span className="whitespace-nowrap text-stone-500">{formatDate(log.created_at)}</span></div>)}</div> : <Empty text="No worker events recorded." />}
                </Panel>
            </div>

            <div className="grid gap-6 xl:grid-cols-2">
                <Panel title="Worker pool" eyebrow="Capacity">{workers.length ? <div className="space-y-3">{workers.slice(0, 6).map((worker) => <div key={worker.worker_id} className="flex items-center justify-between gap-3 rounded-lg border border-white/5 bg-white/[0.03] p-3"><div><p className="text-sm text-stone-200">{worker.hostname}</p><p className="mt-1 font-mono text-[11px] text-stone-500">{shortId(worker.worker_id)} · {worker.cpu_cores} CPU · {worker.memory_gb} GB</p></div><StatusBadge status={worker.status} /></div>)}</div> : <Empty text="No workers registered." />}</Panel>
                <Panel title="Task execution" eyebrow="Queue health">{tasks.length ? <div className="space-y-3">{tasks.slice(0, 6).map((task) => <div key={task.task_id} className="flex items-center justify-between gap-3 rounded-lg border border-white/5 bg-white/[0.03] p-3"><div><p className="text-sm text-stone-200">{task.task_type} <span className="font-mono text-[11px] text-stone-500">{shortId(task.task_id)}</span></p><p className="mt-1 text-[11px] text-stone-500">worker {shortId(task.worker_id)} · {formatDate(task.created_at)}</p></div><StatusBadge status={task.status} /></div>)}</div> : <Empty text="No tasks have been scheduled." />}</Panel>
            </div>
        </div>
    );
}

function Info({ label, value }: { label: string; value: string }) { return <div><p className="text-[10px] uppercase tracking-[0.18em] text-stone-500">{label}</p><p className="mt-1 truncate text-sm text-stone-200">{value}</p></div>; }
function Empty({ text }: { text: string }) { return <p className="rounded-lg border border-dashed border-white/10 px-4 py-8 text-center text-sm text-stone-500">{text}</p>; }
