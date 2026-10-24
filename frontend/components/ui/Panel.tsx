import type { ReactNode } from "react";

export default function Panel({ title, eyebrow, children, className = "" }: {
    title: string;
    eyebrow?: string;
    children: ReactNode;
    className?: string;
}) {
    return (
        <section className={`rounded-xl border border-white/10 bg-black/25 p-5 shadow-2xl backdrop-blur-xl ${className}`}>
            {eyebrow && <p className="mb-2 text-[10px] uppercase tracking-[0.24em] text-pink-200/80">{eyebrow}</p>}
            <h2 className="mb-5 text-sm uppercase tracking-[0.2em] text-stone-100">{title}</h2>
            {children}
        </section>
    );
}
