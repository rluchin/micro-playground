import { useEffect, useState } from "react";
import {
    fetchTasks,
    addTask,
    toggleTask,
    startTimer,
    stopTimer,
    getTimer
} from "./api";

type Task = { id: string; text: string; done: boolean };

export default function App() {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [newText, setNewText] = useState("");
    const [elapsed, setElapsed] = useState(0);

    useEffect(() => {
        fetchTasks().then(setTasks);
    }, []);

    useEffect(() => {
        const id = setInterval(() => getTimer().then(r => setElapsed(r.elapsed)), 1000);
        return () => clearInterval(id);
    }, []);

    const onAdd = async () => {
        if (!newText.trim()) return;
        const t = await addTask(newText);
        setTasks([...tasks, t]);
        setNewText("");
    };

    const onToggle = async (t: Task) => {
        await toggleTask(t.id, !t.done);
        setTasks(tasks.map(x => (x.id === t.id ? { ...x, done: !x.done } : x)));
    };

    return (
        <main style={{ fontFamily: "sans-serif", maxWidth: 600, margin: "2rem auto" }}>
            <h1>Micro?Playground</h1>

            <section>
                <h2>Tasks</h2>
                <input
                    placeholder="New task"
                    value={newText}
                    onChange={e => setNewText(e.target.value)}
                />
                <button onClick={onAdd}>Add</button>

                <ul>
                    {tasks.map(t => (
                        <li key={t.id}>
                            <label style={{ textDecoration: t.done ? "line-through" : "none" }}>
                                <input
                                    type="checkbox"
                                    checked={t.done}
                                    onChange={() => onToggle(t)}
                                />
                                {t.text}
                            </label>
                        </li>
                    ))}
                </ul>
            </section>

            <section style={{ marginTop: "2rem" }}>
                <h2>Timer</h2>
                <button onClick={() => startTimer()}>Start</button>
                <button onClick={() => stopTimer()}>Stop</button>
                <p>Elapsed: {elapsed.toFixed(1)}?s</p>
            </section>
        </main>
    );
}
