"use client";

import Link from "next/link";
import {
    LayoutDashboard,
    Cpu,
    ClipboardList,
    BarChart3,
    Settings
} from "lucide-react";

export default function Sidebar() {
    return (
        <aside
            className="
                w-64
                h-screen
                border-r
                border-white/10
                bg-black/20
                backdrop-blur-md
                text-stone-200
                p-6
                flex
                flex-col
            "
        >
            <div className="mb-12">
                <h1 className="text-xl tracking-[0.45em] uppercase text-stone-100 font-light">
                FEDFORGE
                </h1>

                <p className="text-sm text-stone-200 mt-2">
                    Distributed Intelligence
                </p>
            </div>

            <nav className="space-y-4">
                <Link
                    href="/"
                    className="
                        flex gap-3 text-stone-100
                        text-xs
                        uppercase
                        tracking-[0.25em]
                    ">
                    <LayoutDashboard size={18}/>
                    Dashboard
                </Link>

                <Link
                    href="/workers"
                    className="flex gap-3 stone-100
                        text-xs
                        uppercase
                        tracking-[0.25em]
                    ">
                    <Cpu size={18}/>
                    Workers
                </Link>

                <Link
                    href="/tasks"
                    className="flex gap-3 stone-100
                        text-xs
                        uppercase
                        tracking-[0.25em]"
                >
                    <ClipboardList size={18}/>
                    Tasks
                </Link>

                <Link
                    href="#"
                    className="flex gap-3 stone-100
                        text-xs
                        uppercase
                        tracking-[0.25em]"
                >
                    <BarChart3 size={18}/>
                    Analytics
                </Link>

                <Link
                    href="#"
                    className="flex gap-3 stone-100
                        text-xs
                        uppercase
                        tracking-[0.25em]"
                >
                    <Settings size={18}/>
                    Settings
                </Link>
            </nav>

            <div className="mt-auto text-xs text-stone-500">
                FedForge v1
            </div>
        </aside>
    );
}