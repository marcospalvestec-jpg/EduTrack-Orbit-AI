import type { Task } from './study';

export function completionHistory(tasks: Task[], today: string) {
  const currentWeek = new Date(weeklyReport([], today).start + 'T00:00:00Z');
  return Array.from({ length: 6 }, (_, index) => {
    const start = new Date(currentWeek);
    start.setUTCDate(start.getUTCDate() - (5 - index) * 7);
    const week = weeklyReport([], start.toISOString().slice(0, 10));
    const end = week.end < today ? week.end : today;
    return { start: week.start, count: tasks.filter(task => task.done && task.completedOn && task.completedOn >= week.start && task.completedOn <= end).length };
  });
}

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
