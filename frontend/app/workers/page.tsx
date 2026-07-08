"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Worker } from "@/lib/types";

export default function WorkersPage() {
    const [workers, setWorkers] = useState<Worker[]>([]);

    useEffect(() => {
        fetchWorkers();

        const interval = setInterval(fetchWorkers, 2000);

        return () => clearInterval(interval);
    }, []);

    const fetchWorkers = async () => {
        try {
            const response = await api.get("/workers");
            setWorkers(response.data);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div className="space-y-6">
            <h1 className="text-4xl font-light">Workers</h1>

            {workers.map((worker) => (
                <div
                    key={worker.worker_id}
                    className="
                        border border-white/10
                        bg-black/20
                        backdrop-blur-md
                        p-6
                        rounded-sm
                    "
                >
                    <p className="text-xl">
                        {worker.worker_id.slice(0, 8)}
                    </p>

                    <p className="text-stone-300">
                        Status: {worker.status}
                    </p>

                    <p className="text-stone-400 text-sm">
                        Last Seen: {worker.last_seen}
                    </p>
                </div>
            ))}
        </div>
    );
}