export type Phase = 'focus' | 'short' | 'long';
export type Task = { id: string; title: string; subject: string; deadline: string; priority: 'normal' | 'alta'; done: boolean; completedOn?: string };
export type TaskFilters = { subject: string; status: 'all' | 'pending' | 'done'; deadline: 'all' | 'overdue' | 'today' | 'none' };
export const defaultFilters: TaskFilters = { subject: '', status: 'all', deadline: 'all' };
export function subjectProgress(tasks: Task[], subject: string) {
  const own = tasks.filter(task => task.subject === subject);
  const completed = own.filter(task => task.done).length;
  return { completed, total: own.length, percent: own.length ? Math.round(100 * completed / own.length) : 0 };
}

export function searchSubjects(subjects: string[], tasks: Task[], query: string, includeOverdue: boolean, today: string) {
  const normalize = (value: string) => value.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLocaleLowerCase('pt-BR');
  const term = normalize(query.trim());
  const overdue = new Set(filterTasks(tasks, { ...defaultFilters, deadline: 'overdue' }, today).map(task => task.subject));
  if (!term && !includeOverdue) return subjects;
  return subjects.filter(subject => (term && normalize(subject).includes(term)) || (includeOverdue && overdue.has(subject)));
}
export function filterTasks(tasks: Task[], filters: TaskFilters, today: string) {
  return tasks.filter(task => {
    if (filters.subject && task.subject !== filters.subject) return false;
    if (filters.status !== 'all' && task.done !== (filters.status === 'done')) return false;
    if (filters.deadline === 'overdue') return !task.done && Boolean(task.deadline) && task.deadline < today;
    if (filters.deadline === 'today') return task.deadline === today;
    if (filters.deadline === 'none') return !task.deadline;
    return true;
  });
}
export const duration: Record<Phase, number> = { focus: 1500, short: 300, long: 900 };
export function nextPhase(phase: Phase, cycles: number): { phase: Phase; cycles: number } {
  if (phase !== 'focus') return { phase: 'focus', cycles };
  return { phase: (cycles + 1) % 4 === 0 ? 'long' : 'short', cycles: cycles + 1 };
}
export function remaining(end: number, now: number) {
  return Math.max(0, Math.ceil((end - now) / 1000));
}
export function nextTask(tasks: Task[]) {
  return tasks.filter(t => !t.done).sort((a, b) =>
    (a.deadline || '9999').localeCompare(b.deadline || '9999') ||
    Number(b.priority === 'alta') - Number(a.priority === 'alta'))[0];
}
