"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Task } from "@/lib/types";
import { formatDate, formatDuration, shortId } from "@/lib/format";
import Panel from "@/components/ui/Panel";
import StatusBadge from "@/components/ui/StatusBadge";

export default function TasksPage() {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [error, setError] = useState<string | null>(null);
    useEffect(() => { const fetchTasks = async () => { try { setTasks((await api.get<Task[]>("/tasks")).data); setError(null); } catch { setError("Unable to load tasks."); } }; void fetchTasks(); const timer = window.setInterval(() => void fetchTasks(), 4000); return () => window.clearInterval(timer); }, []);
    return <div className="mx-auto max-w-[1500px] space-y-6"><header><p className="mb-3 text-[10px] uppercase tracking-[0.3em] text-pink-200/80">Execution plane / v1</p><h1 className="text-4xl font-light tracking-[0.12em]">Tasks</h1><p className="mt-2 text-sm text-stone-400">Inspect assignment, execution state, results, and failures.</p></header>{error && <Notice text={error} />}<Panel title={`${tasks.length} tasks`} eyebrow="Live queue">{tasks.length ? <div className="overflow-x-auto"><table className="w-full min-w-[760px] text-left text-sm"><thead className="border-b border-white/10 text-[10px] uppercase tracking-[0.18em] text-stone-500"><tr><th className="pb-3">Task</th><th className="pb-3">Status</th><th className="pb-3">Worker</th><th className="pb-3">Round</th><th className="pb-3">Result</th><th className="pb-3">Created</th></tr></thead><tbody>{tasks.map((task) => <tr key={task.task_id} className="border-b border-white/5"><td className="py-4"><p className="text-stone-200">{task.task_type}</p><p className="font-mono text-[10px] text-stone-500">{shortId(task.task_id)}</p></td><td><StatusBadge status={task.status} />{task.error_message && <p className="mt-2 max-w-52 text-xs text-rose-200">{task.error_message}</p>}</td><td className="font-mono text-xs text-stone-400">{shortId(task.worker_id)}</td><td className="font-mono text-xs text-stone-400">{shortId(task.round_id)}</td><td className="text-xs text-stone-400">{task.result ? <><p>loss {task.result.loss.toFixed(4)} · acc {(task.result.accuracy * 100).toFixed(1)}%</p><p>{task.result.num_samples.toLocaleString()} samples · {formatDuration(task.result.training_time_seconds)}</p></> : "Pending"}</td><td className="whitespace-nowrap text-xs text-stone-500">{formatDate(task.created_at)}</td></tr>)}</tbody></table></div> : <Empty text="No tasks have been scheduled." />}</Panel></div>;
}
function Notice({ text }: { text: string }) { return <div className="rounded-lg border border-rose-300/30 bg-rose-300/10 px-4 py-3 text-sm text-rose-100">{text}</div>; }
function Empty({ text }: { text: string }) { return <p className="rounded-lg border border-dashed border-white/10 px-4 py-8 text-center text-sm text-stone-500">{text}</p>; }
