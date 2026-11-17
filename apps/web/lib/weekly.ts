import type { Task } from './study';

export function weeklyReport(tasks: Task[], today: string) {
  const monday = new Date(today + 'T00:00:00Z');
  monday.setUTCDate(monday.getUTCDate() - (monday.getUTCDay() + 6) % 7);
  const sunday = new Date(monday);
  sunday.setUTCDate(sunday.getUTCDate() + 6);
  const start = monday.toISOString().slice(0, 10);
  const end = sunday.toISOString().slice(0, 10);
  const scheduled = tasks.filter(task => task.deadline >= start && task.deadline <= end)
    .sort((a, b) => a.deadline.localeCompare(b.deadline));
  return { start, end, tasks: scheduled, completed: scheduled.filter(task => task.done).length };
}
