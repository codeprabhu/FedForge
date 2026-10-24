"use client";

import { FormEvent, useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Round } from "@/lib/types";
import { formatDate, shortId } from "@/lib/format";
import Panel from "@/components/ui/Panel";
import StatusBadge from "@/components/ui/StatusBadge";

const initialForm = { model_name: "higgs_mlp", dataset_name: "higgs", num_workers: "1", epochs: "5", batch_size: "128", learning_rate: "0.001" };

export default function RoundsPage() {
    const [rounds, setRounds] = useState<Round[]>([]);
    const [form, setForm] = useState(initialForm);
    const [busy, setBusy] = useState(false);
    const [message, setMessage] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const load = async () => { try { setRounds((await api.get<Round[]>("/rounds")).data); setError(null); } catch { setError("Unable to load rounds."); } };
    useEffect(() => { const initialLoad = window.setTimeout(() => void load(), 0); const timer = window.setInterval(() => void load(), 5000); return () => { window.clearTimeout(initialLoad); window.clearInterval(timer); }; }, []);
    const createRound = async (event: FormEvent) => { event.preventDefault(); setBusy(true); setMessage(null); setError(null); try { await api.post("/rounds", { ...form, num_workers: Number(form.num_workers), epochs: Number(form.epochs), batch_size: Number(form.batch_size), learning_rate: Number(form.learning_rate) }); setMessage("Training round created."); await load(); } catch { setError("Round creation failed. Check the coordinator and worker capacity."); } finally { setBusy(false); } };
    return <div className="mx-auto max-w-[1500px] space-y-6"><header><p className="mb-3 text-[10px] uppercase tracking-[0.3em] text-pink-200/80">Orchestration / v1</p><h1 className="text-4xl font-light tracking-[0.12em]">Training rounds</h1><p className="mt-2 text-sm text-stone-400">Start a federated round and monitor its lifecycle.</p></header>{(error || message) && <div className={`rounded-lg border px-4 py-3 text-sm ${error ? "border-rose-300/30 bg-rose-300/10 text-rose-100" : "border-emerald-300/30 bg-emerald-300/10 text-emerald-100"}`}>{error ?? message}</div>}<div className="grid gap-6 xl:grid-cols-[360px_1fr]"><Panel title="Create round" eyebrow="Control"><form onSubmit={createRound} className="space-y-4">{(["model_name", "dataset_name", "num_workers", "epochs", "batch_size", "learning_rate"] as const).map((key) => <label key={key} className="block"><span className="mb-1 block text-[10px] uppercase tracking-[0.15em] text-stone-500">{key.replaceAll("_", " ")}</span><input required value={form[key]} onChange={(event) => setForm({ ...form, [key]: event.target.value })} type={key === "model_name" || key === "dataset_name" ? "text" : "number"} step={key === "learning_rate" ? "any" : "1"} min={key === "learning_rate" ? "0.000001" : "1"} className="w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm text-stone-100 outline-none focus:border-pink-200/50" /></label>)}<button disabled={busy} className="w-full rounded-lg border border-pink-200/40 bg-pink-200/10 px-4 py-3 text-xs uppercase tracking-[0.18em] text-pink-100 transition hover:bg-pink-200/20 disabled:cursor-wait disabled:opacity-50">{busy ? "Creating…" : "Create training round"}</button></form></Panel><Panel title={`${rounds.length} rounds`} eyebrow="History"><div className="space-y-3">{rounds.map((round) => <div key={round.round_id} className="flex flex-wrap items-center justify-between gap-4 rounded-lg border border-white/5 bg-white/[0.03] p-4"><div><p className="text-lg text-stone-100">Round #{round.round_number}</p><p className="mt-1 text-xs text-stone-500">{round.model_name} · {round.dataset_name} · {shortId(round.round_id)}</p><p className="mt-2 text-xs text-stone-500">Created {formatDate(round.created_at)} · Completed {formatDate(round.completed_at)}</p></div><StatusBadge status={round.status} /></div>)}{rounds.length === 0 && <p className="rounded-lg border border-dashed border-white/10 px-4 py-8 text-center text-sm text-stone-500">No rounds yet.</p>}</div></Panel></div></div>;
}
