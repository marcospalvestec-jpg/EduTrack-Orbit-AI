'use client';

import { useEffect, useState, type FormEvent } from 'react';
import { defaultFilters, duration, filterTasks, nextPhase, nextTask, remaining, searchSubjects, subjectProgress, type Phase, type Task, type TaskFilters } from '../lib/study';

const labels = { focus: 'Foco', short: 'Pausa curta', long: 'Pausa longa' };
const key = 'edutrack-web-demo-v1';
type Data = { subjects: string[]; tasks: Task[] };
const empty: Data = { subjects: [], tasks: [] };
type Timer = { phase: Phase; cycles: number; seconds: number; end: number | null };
const initialTimer: Timer = { phase: 'focus', cycles: 0, seconds: duration.focus, end: null };

export default function Home() {
  const [data, setData] = useState(empty);
  const [loaded, setLoaded] = useState(false);
  const [storageError, setStorageError] = useState(false);
  const [timer, setTimer] = useState(initialTimer);
  const [linked, setLinked] = useState('');
  const [filters, setFilters] = useState(defaultFilters);
  const [subjectQuery, setSubjectQuery] = useState('');
  const [includeOverdue, setIncludeOverdue] = useState(false);
  const { phase, cycles, seconds, end } = timer;

  useEffect(() => {
    try {
      const raw = localStorage.getItem(key);
      if (raw) {
        const saved = JSON.parse(raw);
        if (!Array.isArray(saved.subjects) || !Array.isArray(saved.tasks)) throw new Error();
        setData(saved);
      }
      setLoaded(true);
    } catch { setStorageError(true); }
  }, []);

  function save(next: Data) {
    setData(next);
    try { localStorage.setItem(key, JSON.stringify(next)); }
    catch { setStorageError(true); }
  }

  useEffect(() => {
    if (end === null) return;
    const tick = () => setTimer(current => {
      if (current.end !== end) return current;
      const left = remaining(end, Date.now());
      if (left > 0) return { ...current, seconds: left };
      const next = nextPhase(current.phase, current.cycles);
      return { ...next, seconds: duration[next.phase], end: null };
    });
    const interval = window.setInterval(tick, 200);
    return () => window.clearInterval(interval);
  }, [end]);

  function addSubject(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const name = String(new FormData(e.currentTarget).get('subject')).trim();
    if (!name || data.subjects.includes(name)) return;
    save({ ...data, subjects: [...data.subjects, name] });
    e.currentTarget.reset();
  }

  function addTask(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fields = new FormData(e.currentTarget);
    const title = String(fields.get('title')).trim();
    const subject = String(fields.get('subject'));
    if (!title || !data.subjects.includes(subject)) return;
    const task: Task = { id: crypto.randomUUID(), title, subject, deadline: String(fields.get('date')), priority: fields.get('priority') === 'alta' ? 'alta' : 'normal', done: false };
    save({ ...data, tasks: [...data.tasks, task] });
    e.currentTarget.reset();
  }

  const suggested = nextTask(data.tasks);
  const today = new Intl.DateTimeFormat('sv-SE', { timeZone: 'America/Sao_Paulo', year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date());
  const visibleTasks = filterTasks(data.tasks, filters, today);
  const visibleSubjects = searchSubjects(data.subjects, data.tasks, subjectQuery, includeOverdue, today);
  const completed = data.tasks.filter(t => t.done).length;
  const time = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;

  return <main className="mx-auto max-w-6xl px-5 py-8 sm:px-10 sm:py-12">
    <header className="mb-10">
      <p className="eyebrow">EDUTRACK / ORBIT AI</p>
      <h1>Seu espaço de estudo</h1>
      <p className="muted">Organize suas atividades e reserve tempo para o que importa.</p>
      <p className="badge">Demonstração local · os dados ficam neste navegador</p>
    </header>
    {storageError && <p role="alert">O armazenamento local não está disponível. Não foi possível carregar ou salvar seus dados no navegador.</p>}
    <div className="grid gap-5 md:grid-cols-2">
      <section className="panel" aria-labelledby="timer-title">
        <p className="eyebrow">01 / SESSÃO DE ESTUDO</p>
        <h2 id="timer-title">Pomodoro</h2>
        <p aria-live="polite">{labels[phase]} · {cycles} {cycles === 1 ? 'ciclo concluído' : 'ciclos concluídos'}</p>
        <p className="time" role="timer" aria-label={`${Math.floor(seconds / 60)} minutos e ${seconds % 60} segundos`}>{time}</p>
        {linked && <p className="muted">Tarefa em foco: {data.tasks.find(t => t.id === linked)?.title}</p>}
        <div className="flex flex-wrap gap-2">
          <button className="accent" onClick={() => setTimer(current => {
            const now = Date.now();
            if (current.end === null) return { ...current, end: now + current.seconds * 1000 };
            const left = remaining(current.end, now);
            if (left > 0) return { ...current, end: null, seconds: left };
            const next = nextPhase(current.phase, current.cycles);
            return { ...next, seconds: duration[next.phase], end: null };
          })}>{end !== null ? 'Pausar' : seconds < duration[phase] ? 'Retomar' : 'Iniciar'}</button>
          <button onClick={() => setTimer(current => ({ ...current, seconds: duration[current.phase], end: null }))}>Reiniciar etapa</button>
        </div>
        <p className="muted mt-4">25 min de foco · 5 min de pausa · 15 min após quatro ciclos</p>
      </section>
      <section className="panel" aria-labelledby="insight-title">
        <p className="eyebrow">02 / PRÓXIMO PASSO</p>
        <h2 id="insight-title">Sugestão do Orbit</h2>
        {suggested ? <>
          <p className="suggestion">{suggested.title}</p>
          <p className="muted">{suggested.subject} · {suggested.deadline ? `Prazo: ${suggested.deadline.split('-').reverse().join('/')}` : 'Sem prazo'} · Prioridade {suggested.priority}</p>
          <button onClick={() => setLinked(suggested.id)}>Vincular ao Pomodoro</button>
        </> : <p className="muted">{completed ? 'Tudo em dia. Aproveite para descansar ou planejar a semana.' : 'Cadastre uma disciplina e uma tarefa para receber sua primeira sugestão.'}</p>}
        <p className="mt-5" aria-live="polite">{completed} de {data.tasks.length} tarefas concluídas. {completed ? 'Cada conclusão conta.' : 'Comece por uma etapa pequena.'}</p>
      </section>
      <section className="panel" aria-labelledby="subjects-title">
        <p className="eyebrow">03 / ORGANIZAÇÃO</p>
        <h2 id="subjects-title">Disciplinas</h2>
        <form onSubmit={addSubject} className="form">
          <label>Nome da disciplina<input name="subject" required maxLength={80} /></label>
          <button className="accent" disabled={!loaded}>Adicionar disciplina</button>
        </form>
        {data.subjects.length > 0 && <div className="form mt-4">
          <label>Buscar disciplina por nome<input type="search" value={subjectQuery} onChange={event => setSubjectQuery(event.target.value)} /></label>
          <p><label className="inline-flex! items-center gap-2!"><input type="checkbox" checked={includeOverdue} onChange={event => setIncludeOverdue(event.target.checked)} /> {subjectQuery.trim() ? 'Incluir também disciplinas com tarefas atrasadas' : 'Mostrar disciplinas com tarefas atrasadas'}</label></p>
          {!visibleSubjects.length && <p role="status">Nenhuma disciplina encontrada.</p>}
          <ul className="subject-list">{visibleSubjects.map(subject => {
            const progress = subjectProgress(data.tasks, subject);
            return <li key={subject}><strong>{subject}</strong><p className="muted">{progress.completed} de {progress.total} concluídas · {progress.percent}%</p><progress aria-label={`Progresso em ${subject}`} value={progress.percent} max={100} /></li>;
          })}</ul>
        </div>}
      </section>
      <section className="panel" aria-labelledby="tasks-title">
        <p className="eyebrow">04 / PLANEJAMENTO</p>
        <h2 id="tasks-title">Tarefas</h2>
        {!data.subjects.length && <p className="muted">Adicione uma disciplina para cadastrar tarefas.</p>}
        <form onSubmit={addTask} className="form">
          <fieldset disabled={!loaded || !data.subjects.length} className="form">
            <label>Título<input name="title" required maxLength={120} /></label>
            <label>Disciplina<select name="subject" required><option value="">Selecione</option>{data.subjects.map(s => <option key={s}>{s}</option>)}</select></label>
            <div className="grid gap-3 sm:grid-cols-2"><label>Prazo<input name="date" type="date" /></label><label>Prioridade<select name="priority"><option value="normal">Normal</option><option value="alta">Alta</option></select></label></div>
            <button className="accent">Adicionar tarefa</button>
          </fieldset>
        </form>
        {data.tasks.length > 0 && <fieldset className="form mt-5">
          <legend>Filtrar tarefas</legend>
          <label>Disciplina<select value={filters.subject} onChange={e => setFilters({ ...filters, subject: e.target.value })}><option value="">Todas</option>{data.subjects.map(s => <option key={s}>{s}</option>)}</select></label>
          <div className="grid gap-3 sm:grid-cols-2">
            <label>Status<select value={filters.status} onChange={e => setFilters({ ...filters, status: e.target.value as TaskFilters['status'] })}><option value="all">Todos</option><option value="pending">Pendentes</option><option value="done">Concluídas</option></select></label>
            <label>Prazo<select value={filters.deadline} onChange={e => setFilters({ ...filters, deadline: e.target.value as TaskFilters['deadline'] })}><option value="all">Todos</option><option value="overdue">Atrasadas</option><option value="today">Vencem hoje</option><option value="none">Sem prazo</option></select></label>
          </div>
          <button type="button" onClick={() => setFilters(defaultFilters)}>Limpar filtros</button>
          <p className="muted" aria-live="polite">{visibleTasks.length ? `${visibleTasks.length} de ${data.tasks.length} tarefas` : 'Nenhuma tarefa corresponde aos filtros.'}</p>
        </fieldset>}
        <ul className="task-list">{visibleTasks.map(t => <li key={t.id}><label>
          <input type="checkbox" checked={t.done} onChange={() => save({ ...data, tasks: data.tasks.map(item => item.id === t.id ? { ...item, done: !item.done } : item) })} />
          <span>{t.title}<small>{t.subject}</small></span>
        </label></li>)}</ul>
      </section>
    </div>
  </main>;
}
