"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { WorkerEvent } from "@/lib/types";

export default function LogPanel() {
    const [logs, setLogs] = useState<WorkerEvent[]>([]);

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const response = await api.get("/logs");
                setLogs(response.data);
            }
            catch (error) {
                console.error(error);
            }
        };

        fetchLogs();

        const interval = setInterval(
            fetchLogs,
            2000
        );

        return () => clearInterval(interval);
    }, []);

    return (
        <div
            className="
                border border-white/10
                bg-black/15
                backdrop-blur-xl
                p-8
                rounded-sm
                h-[420px]
                overflow-y-auto
                font-mono
            "
        >
            <h2
                className="
                    text-xl
                    uppercase
                    tracking-[0.25em]
                    text-stone-200
                    mb-8
                "
            >
                Coordinator Logs
            </h2>

            <div className="space-y-4 text-sm">

                {logs.map((log, index) => (
                    <div
                        key={index}
                        className="
                            flex
                            gap-3
                            text-stone-300
                        "
                    >
                        <span className="text-pink-300">
                            [{log.created_at.slice(11,19)}]
                        </span>

                        <span className="text-stone-100">
                            {log.event_type}
                        </span>

                        <span className="text-pink-300">
                            {log.worker_id?.slice(0,8)}
                        </span>
                    </div>
                ))}

                <div
                    className="
                        text-pink-300
                        animate-pulse
                    "
                >
                    █
                </div>

            </div>
        </div>
    );
}
