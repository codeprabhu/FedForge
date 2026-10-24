export default function StatusBadge({ status }: { status: string }) {
    const normalized = status.toUpperCase();
    const color = normalized === "ONLINE" || normalized === "COMPLETED"
        ? "border-emerald-300/30 bg-emerald-300/10 text-emerald-200"
        : normalized === "FAILED" || normalized === "OFFLINE"
            ? "border-rose-300/30 bg-rose-300/10 text-rose-200"
            : "border-amber-300/30 bg-amber-300/10 text-amber-200";
    return <span className={`inline-flex rounded-full border px-2.5 py-1 text-[10px] tracking-[0.18em] ${color}`}>{normalized}</span>;
}
