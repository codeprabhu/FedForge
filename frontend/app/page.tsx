"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import LogPanel from "@/components/dashboard/LogPanel";

export default function Home() {
    const [dashboard, setDashboard] = useState({
        workers_online: 0,
        running_tasks: 0,
        completed_tasks: 0,
        coordinator_status: "OFFLINE"
    });

    useEffect(() => {
        const fetchDashboard = async () => {
            try {
                const response = await api.get("/dashboard");
                setDashboard(response.data);
            }
            catch(error) {
                console.error(error);
            }
        };

        fetchDashboard();

        const interval = setInterval(
            fetchDashboard,
            1000
        );

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="space-y-8">
            <div>
                <h1 className="
                    text-5xl
                    tracking-[0.2em]
                    uppercase
                    text-stone-100
                    font-light
                ">
                    Dashboard
                </h1>

                    <p className="
                        text-stone-100
                        text-xs
                        uppercase
                        tracking-[0.25em]">
                    Coordinator online.
                </p>
            </div>

            <div className="grid grid-cols-4 gap-6">

                <div className="
                    border border-white/10
                    bg-black/15
                    backdrop-blur-xl
                    p-8
                    rounded-sm
                    shadow-2xl
                    ">
                    <p className="
                        text-stone-100
                        text-xs
                        uppercase
                        tracking-[0.25em]
                    ">
                        Workers Online
                    </p>

                    <h2 className="
                        text-5xl
                        mt-2
                        font-light
                    ">
                        {dashboard.workers_online}
                    </h2>
                </div>

                <div className="
                    border border-white/10
                    bg-black/15
                    backdrop-blur-xl
                    p-8
                    rounded-sm
                    shadow-2xl
                    ">
                    <p className="
                        text-stone-100
                        text-xs
                        uppercase
                        tracking-[0.25em]
                    ">
                        Running Tasks
                    </p>

                    <h2 className="
                        text-5xl
                        mt-2
                        font-light
                    ">
                        {dashboard.running_tasks}
                    </h2>
                </div>

                <div className="
                    border border-white/10
                    bg-black/15
                    backdrop-blur-xl
                    p-8
                    rounded-sm
                    shadow-2xl
                    ">
                    <p className="
                        text-stone-100
                        text-xs
                        uppercase
                        tracking-[0.25em]
                    ">
                        Completed Tasks
                    </p>

                    <h2 className="
                        text-5xl
                        mt-2
                        font-light
                    ">
                        {dashboard.completed_tasks}
                    </h2>
                </div>

                <div className="
                    border border-white/10
                    bg-black/15
                    backdrop-blur-xl
                    p-8
                    rounded-sm
                    shadow-2xl
                    ">
                    <p className="
                        text-stone-100
                        text-xs
                        uppercase
                        tracking-[0.25em]
                    ">
                        Coordinator
                    </p>

                    <h2 className="text-4xl mt-2 text-green-100">
                        {dashboard.coordinator_status}
                    </h2>
                </div>

            </div>

            <div className="grid grid-cols-2 gap-6">

                <div className="
                    border border-white/10
                    bg-black/15
                    backdrop-blur-xl
                    p-8
                    rounded-sm
                    h-[420px]
                ">
                    <h2 className="
                        text-xl
                        uppercase
                        tracking-[0.25em]
                        text-stone-100
                        mb-8
                    ">
                        Operations Console
                    </h2>

                    <div className="
                        font-mono
                        text-sm
                        text-stone-100
                        space-y-4
                    ">
                        <div>
                            Awaiting federated training round...
                        </div>

                        <div>
                            Coordinator ready.
                        </div>

                        <div>
                            Worker pool synchronized.
                        </div>

                        <div className="
                            text-pink-100
                            animate-pulse
                        ">
                            █
                        </div>
                    </div>
                </div>

                <LogPanel />

                </div>
        </div>
        );
}