"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Task } from "@/lib/types";

export default function TasksPage() {
    const [tasks, setTasks] = useState<Task[]>([]);

    useEffect(() => {
        fetchTasks();

        const interval = setInterval(fetchTasks, 2000);

        return () => clearInterval(interval);
    }, []);

    const fetchTasks = async () => {
        try {
            const response = await api.get("/tasks");
            setTasks(response.data);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div className="space-y-6">
            <h1 className="text-4xl font-light">Tasks</h1>

            {tasks.map((task) => (
                <div
                    key={task.task_id}
                    className="
                        border border-white/10
                        bg-black/20
                        backdrop-blur-md
                        p-6
                        rounded-sm
                    "
                >
                    <p className="text-xl">
                        {task.task_type}
                    </p>

                    <p className="text-stone-300">
                        Status: {task.status}
                    </p>

                    <p className="text-stone-400">
                        Worker: {task.worker_id?.slice(0, 8)}
                    </p>
                </div>
            ))}
        </div>
    );
}