const BASE = import.meta.env.VITE_API || "/api";

export const fetchTasks = () => fetch(`${BASE}/tasks`).then(r => r.json());
export const addTask = (text: string) =>
    fetch(`${BASE}/tasks`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    }).then(r => r.json());
export const toggleTask = (id: string, done: boolean) =>
    fetch(`${BASE}/tasks/${id}?done=${done}`, { method: "PATCH" });

export const startTimer = () => fetch(`${BASE}/timer/start`, { method: "POST" });
export const stopTimer = () => fetch(`${BASE}/timer/stop`, { method: "POST" });
export const getTimer = () => fetch(`${BASE}/timer`).then(r => r.json());