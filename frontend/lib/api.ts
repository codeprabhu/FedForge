import axios from "axios";

export const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_COORDINATOR_URL ?? "http://localhost:8000",
    timeout: 15_000,
});
