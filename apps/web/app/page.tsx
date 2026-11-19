'use client';

import { useEffect, useRef, useState, type FormEvent } from 'react';
import { completionHistory, weeklyReport } from '../lib/weekly';
import { revisionSessions, type Outcome, type RevisionPlan } from '../lib/revision';
import { defaultFilters, duration, filterTasks, nextPhase, nextTask, remaining, searchSubjects, subjectProgress, type Phase, type Task, type TaskFilters } from '../lib/study';

const labels = { focus: 'Foco', short: 'Pausa curta', long: 'Pausa longa' };
const themeKey = 'edutrack-web-theme';
type Theme = 'system' | 'light' | 'dark';

function applyTheme(theme: Theme) {
  if (theme === 'system') delete document.documentElement.dataset.theme;
  else document.documentElement.dataset.theme = theme;
}
const sections = {"inicio":"visao-geral","subjects-title":"disciplinas","tasks-title":"tarefas","agenda-title":"agenda","timer-title":"pomodoro","insight-title":"orbit","weekly-title":"relatorio"} as const;
type Section = typeof sections[keyof typeof sections];

function sectionFromHash(): Section {
  const hash = window.location.hash.slice(1);
  if (Object.hasOwn(sections, hash)) return sections[hash as keyof typeof sections];
  return Object.values(sections).find(section => section === hash) ?? 'visao-geral';
}
type Data = { subjects: string[]; tasks: Task[]; revisions: RevisionPlan[] };
const empty: Data = { subjects: [], tasks: [], revisions: [] };
type Timer = { phase: Phase; cycles: number; seconds: number; end: number | null };
const initialTimer: Timer = { phase: 'focus', cycles: 0, seconds: duration.focus, end: null };

export default function Home() {
  const [user, setUser] = useState<{ name: string; email: string } | null>(null);
  const [authReady, setAuthReady] = useState(false);
  const [registering, setRegistering] = useState(false);
  const [authBusy, setAuthBusy] = useState(false);
  const [authError, setAuthError] = useState('');
  const [saving, setSaving] = useState(0);
  const queue = useRef(Promise.resolve());
  const [data, setData] = useState(empty);
  const [loaded, setLoaded] = useState(false);
  const [storageError, setStorageError] = useState(false);
  const [timer, setTimer] = useState(initialTimer);
  const [linked, setLinked] = useState('');
  const [filters, setFilters] = useState(defaultFilters);
  const [subjectQuery, setSubjectQuery] = useState('');
  const [includeOverdue, setIncludeOverdue] = useState(false);
  const [agendaMonth, setAgendaMonth] = useState('');
  const [notice, setNotice] = useState('');
  const [menuOpen, setMenuOpen] = useState(true);
  const [theme, setTheme] = useState<Theme>('system');
  const [systemDark, setSystemDark] = useState(false);
  useEffect(() => {
    const preference = window.matchMedia('(prefers-color-scheme: dark)');
    const updateSystemTheme = () => setSystemDark(preference.matches);
    updateSystemTheme();
    preference.addEventListener('change', updateSystemTheme);
    try {
      const saved = localStorage.getItem(themeKey);
      if (saved === 'light' || saved === 'dark') {
        setTheme(saved);
        applyTheme(saved);
      }
    } catch { /* The system theme still works without local storage. */ }
    return () => preference.removeEventListener('change', updateSystemTheme);
  }, []);
  const isDark = theme === 'dark' || (theme === 'system' && systemDark);

  function changeTheme(value: Theme) {
    setTheme(value);
    applyTheme(value);
    try { localStorage.setItem(themeKey, value); }
    catch { /* Keep the choice for this visit. */ }
  }
  const [section, setSection] = useState<Section>('visao-geral');
  useEffect(() => {
    const sync = () => setSection(sectionFromHash());
    sync();
    window.addEventListener('hashchange', sync);
    return () => window.removeEventListener('hashchange', sync);
  }, []);

  function navigation(target: Section) {
    return { href: '#' + target, 'aria-current': section === target ? 'page' as const : undefined };
  }
  const { phase, cycles, seconds, end } = timer;

  useEffect(() => {
    fetch('/api/account', { cache: 'no-store' }).then(async response => {
      if (response.status === 401) return;
      if (!response.ok) throw new Error();
      const result = await response.json();
      setUser(result.user); setData(result.data); setLoaded(true);
    }).catch(() => setAuthError('Não foi possível consultar sua sessão. Atualize a página.'))
      .finally(() => setAuthReady(true));
  }, []);

  function save(next: Data) {
    setData(next);
    setSaving(count => count + 1);
    queue.current = queue.current.then(async () => {
      try {
        const response = await fetch('/api/account', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ action: 'save', data: next }) });
        if (!response.ok) throw new Error();
        setStorageError(false);
      } catch { setStorageError(true); }
      finally { setSaving(count => count - 1); }
    });
  }

  async function authenticate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setAuthError(''); setAuthBusy(true);
    const fields = new FormData(event.currentTarget);
    if (registering && fields.get('password') !== fields.get('confirmation')) {
      setAuthError('As senhas precisam ser iguais.'); setAuthBusy(false); return;
    }
    try {
      const response = await fetch('/api/account', { method:'POST', headers:{'Content-Type':'application/json'},
        body:JSON.stringify({ action: registering ? 'register' : 'login', name:fields.get('name'), email:fields.get('email'), password:fields.get('password') }) });
      const result = await response.json();
      if (!response.ok) { setAuthError(result.error); return; }
      setData(result.data); setUser(result.user); setLoaded(true); setStorageError(false);
      setSection('visao-geral'); window.location.hash = 'visao-geral';
    } catch { setAuthError('Não foi possível conectar. Tente novamente.'); }
    finally { setAuthBusy(false); }
  }

  async function logout() {
    if (saving) return;
    try {
      const response = await fetch('/api/account', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({action:'logout'}) });
      if (!response.ok) throw new Error();
      setUser(null); setData(empty); setLoaded(false); setTimer(initialTimer); setLinked(''); setNotice(''); setAuthError('');
    } catch { setNotice('Não foi possível sair. Tente novamente.'); }
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

  function renameSubject(event: FormEvent<HTMLFormElement>, previous: string) {
    event.preventDefault();
    const name = String(new FormData(event.currentTarget).get('name') ?? '').trim();
    if (!name || name === previous) return;
    if (data.subjects.includes(name)) {
      setNotice('Já existe uma disciplina com esse nome.');
      return;
    }
    save({
      ...data,
      subjects: data.subjects.map(subject => subject === previous ? name : subject),
      tasks: data.tasks.map(task => task.subject === previous ? { ...task, subject: name } : task),
    });
    if (filters.subject === previous) setFilters({ ...filters, subject: name });
    setNotice('Disciplina atualizada.');
  }

  function removeSubject(name: string) {
    if (data.tasks.some(task => task.subject === name)) {
      setNotice('Mova as tarefas para outra disciplina antes de excluir esta.');
      return;
    }
    if (!window.confirm(`Excluir a disciplina “${name}”?`)) return;
    save({ ...data, subjects: data.subjects.filter(subject => subject !== name) });
    if (filters.subject === name) setFilters({ ...filters, subject: '' });
    setNotice('Disciplina excluída.');
  }

  function editTask(event: FormEvent<HTMLFormElement>, task: Task) {
    event.preventDefault();
    const fields = new FormData(event.currentTarget);
    const title = String(fields.get('title') ?? '').trim();
    const subject = String(fields.get('subject') ?? '');
    if (!title || !data.subjects.includes(subject)) return;
    const updated: Task = { ...task, title, subject, deadline: String(fields.get('date') ?? ''), priority: fields.get('priority') === 'alta' ? 'alta' : 'normal' };
    save({ ...data, tasks: data.tasks.map(item => item.id === task.id ? updated : item) });
    event.currentTarget.closest('details')?.removeAttribute('open');
    setNotice('Tarefa atualizada.');
  }

  function removeTask(task: Task) {
    if (!window.confirm(`Excluir a tarefa “${task.title}”? Não é possível desfazer.`)) return;
    save({ ...data, tasks: data.tasks.filter(item => item.id !== task.id) });
    if (linked === task.id) setLinked('');
    setNotice('Tarefa excluída.');
  }

  const suggested = nextTask(data.tasks);
  const today = new Intl.DateTimeFormat('sv-SE', { timeZone: 'America/Sao_Paulo', year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date());
  const [twoSessions, setTwoSessions] = useState(false);
  const [revisionError, setRevisionError] = useState('');

  function addRevision(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setRevisionError('');
    const fields = new FormData(event.currentTarget);
    const topic = String(fields.get('topic') ?? '').trim();
    const exam = String(fields.get('exam') ?? '');
    if (!topic) { setRevisionError('Informe o conteúdo da prova.'); return; }
    try {
      const times = [String(fields.get('first') ?? '')];
      if (twoSessions) times.push(String(fields.get('second') ?? ''));
      const sessions = revisionSessions(today, exam, times);
      save({ ...data, revisions: [...data.revisions, { id: crypto.randomUUID(), topic, exam, sessions, results: {} }] });
      event.currentTarget.reset();
      setTwoSessions(false);
    } catch (error) {
      setRevisionError(error instanceof Error ? error.message : 'Não foi possível criar o plano.');
    }
  }

  function markRevision(id: string, session: string, outcome: Outcome) {
    save({ ...data, revisions: data.revisions.map(plan => plan.id === id
      ? { ...plan, results: { ...plan.results, [session]: outcome } } : plan) });
  }
  const visibleTasks = filterTasks(data.tasks, filters, today);
  const week = weeklyReport(data.tasks, today);
  const history = completionHistory(data.tasks, today);
  const maxCompleted = Math.max(1, ...history.map(item => item.count));
  const displayDate = (date: string) => date.split('-').reverse().join('/');
  const visibleSubjects = searchSubjects(data.subjects, data.tasks, subjectQuery, includeOverdue, today);
  const completed = data.tasks.filter(t => t.done).length;
  const overdue = filterTasks(data.tasks, { ...defaultFilters, deadline: 'overdue' }, today).length;
  const month = agendaMonth || today.slice(0, 7);
  const agenda = data.tasks.filter(task => task.deadline.startsWith(month + '-'))
    .sort((a, b) => a.deadline.localeCompare(b.deadline));
  const time = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;

  if (!authReady) return <main className="mx-auto max-w-md p-8" role="status">Carregando sua conta…</main>;
  if (!user) return <main className="mx-auto max-w-md px-5 py-12">
    <p className="eyebrow">EDUTRACK / ORBIT AI</p>
    <h1 className="mt-4">{registering ? 'Crie sua conta' : 'Bem-vindo de volta'}</h1>
    <p className="muted mb-6">Organize seus estudos com uma conta individual.</p>
    <form className="panel form" onSubmit={authenticate} key={registering ? 'register' : 'login'}>
      {registering && <label>Nome<input name="name" autoComplete="name" minLength={2} maxLength={80} required /></label>}
      <label>E-mail<input type="email" name="email" autoComplete="username" maxLength={254} required /></label>
      <label>Senha<input type="password" name="password" autoComplete={registering ? 'new-password' : 'current-password'} minLength={registering ? 10 : undefined} maxLength={128} required /></label>
      {registering && <><p className="muted">Use pelo menos 10 caracteres.</p><label>Confirmar senha<input type="password" name="confirmation" autoComplete="new-password" minLength={10} maxLength={128} required /></label></>}
      {authError && <p role="alert">{authError}</p>}
      <button className="accent" disabled={authBusy}>{authBusy ? 'Aguarde…' : registering ? 'Cadastrar e entrar' : 'Entrar'}</button>
      <button type="button" disabled={authBusy} onClick={() => { setRegistering(!registering); setAuthError(''); }}>{registering ? 'Já tenho uma conta' : 'Criar novo usuário'}</button>
    </form>
  </main>;
  return <div className="orbit-shell">
    <aside className="orbit-sidebar" aria-label="Barra lateral">
      <p className="muted px-3 mb-2">{user.name}</p>
      <button className="mb-4 w-full" disabled={saving > 0} onClick={logout}>Sair da conta</button>
      <a className="orbit-mark" href="#visao-geral">EduTrack <span>Orbit AI</span>
        <svg className="ml-1.5 inline-block align-middle text-[var(--accent)]" aria-hidden="true" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
          <rect x="4" y="7" width="16" height="13" rx="4" />
          <path d="M12 7V4m-2 0h4M2 13v2m20-2v2M9 16h6" />
          <circle cx="9" cy="12" r=".8" fill="currentColor" stroke="none" />
          <circle cx="15" cy="12" r=".8" fill="currentColor" stroke="none" />
        </svg>
      </a>
      <nav aria-label="Seções do EduTrack">
        <a className="orbit-link" {...navigation('visao-geral')}>Visão geral</a>
        <button type="button" className="orbit-menu-toggle" aria-expanded={menuOpen} aria-controls="study-submenu" onClick={() => setMenuOpen(open => !open)}>
          Organização <span aria-hidden="true" className="orbit-chevron">⌄</span>
        </button>
        <div id="study-submenu" className="orbit-submenu" data-open={menuOpen} inert={!menuOpen}>
          <ul>
            <li><a className="orbit-link" {...navigation('disciplinas')}><SubmenuIcon name="book" />Disciplinas</a></li>
            <li><a className="orbit-link" {...navigation('tarefas')}><SubmenuIcon name="checklist" />Tarefas</a></li>
            <li><a className="orbit-link" {...navigation('agenda')}><SubmenuIcon name="calendar" />Agenda</a></li>
          </ul>
        </div>
        <a className="orbit-link" {...navigation('pomodoro')}>Pomodoro</a>
        <a className="orbit-link" {...navigation('orbit')}>Sugestão do Orbit</a>
        <a className="orbit-link" {...navigation('relatorio')}>Relatório semanal</a>
        <a className="orbit-link" href="https://classroom.google.com/" target="_blank" rel="noopener noreferrer" aria-label="Abrir Google Classroom em outra aba">
          Abrir Google Classroom <span className="ml-auto pl-2" aria-hidden="true">↗</span>
        </a>
      </nav>
    </aside>
    <main id="inicio" className="mx-auto w-full max-w-6xl px-5 py-8 sm:px-10 sm:py-12">
    <div className="mb-3 flex justify-end">
      <button type="button" className="grid size-11 place-items-center rounded-full p-0"
        aria-label={isDark ? 'Ativar tema claro' : 'Ativar tema escuro'}
        title={isDark ? 'Ativar tema claro' : 'Ativar tema escuro'}
        onClick={() => changeTheme(isDark ? 'light' : 'dark')}>
        <svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
          {isDark ? <><circle cx="12" cy="12" r="4" /><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19m0-14-1.5 1.5m-11 11L5 19" /></> :
            <path d="M20.9 13.4A9 9 0 0 1 10.6 3.1a9 9 0 1 0 10.3 10.3Z" />}
        </svg>
      </button>
    </div>
    <header className="mb-10" hidden={section !== 'visao-geral'}>
      <p className="eyebrow">EDUTRACK / ORBIT AI</p>
      <h1>Seu espaço de estudo</h1>
      <p className="muted">Organize suas atividades e reserve tempo para o que importa.</p>
      <p className="badge">Conta: {user.email} · {saving ? 'Salvando…' : 'Dados salvos neste servidor local'}</p>
    </header>
    <section className="panel mb-5" aria-label="Resumo acadêmico" hidden={section !== 'visao-geral'}>
      <dl className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <div><dt>Disciplinas</dt><dd className="suggestion">{data.subjects.length}</dd></div>
        <div><dt>Pendentes</dt><dd className="suggestion">{data.tasks.length - completed}</dd></div>
        <div><dt>Atrasadas</dt><dd className="suggestion">{overdue}</dd></div>
        <div><dt>Concluídas</dt><dd className="suggestion">{completed}</dd></div>
      </dl>
    </section>
    <p className="muted mb-3" role="status">{notice}</p>
    {storageError && <p role="alert">Não foi possível salvar as últimas alterações no servidor. <button onClick={() => save(data)}>Tentar salvar novamente</button></p>}
    <div>
      <section className="panel" aria-labelledby="timer-title" hidden={section !== 'pomodoro'} key="timer-title">
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
      <section className="panel" aria-labelledby="insight-title" hidden={section !== 'orbit'} key="insight-title">
        <p className="eyebrow">02 / PRÓXIMO PASSO</p>
        <h2 id="insight-title">Sugestão do Orbit</h2>
        {suggested ? <>
          <p className="suggestion">{suggested.title}</p>
          <p className="muted">{suggested.subject} · {suggested.deadline ? `Prazo: ${suggested.deadline.split('-').reverse().join('/')}` : 'Sem prazo'} · Prioridade {suggested.priority}</p>
          <button onClick={() => setLinked(suggested.id)}>Vincular ao Pomodoro</button>
        </> : <p className="muted">{completed ? 'Tudo em dia. Aproveite para descansar ou planejar a semana.' : 'Cadastre uma disciplina e uma tarefa para receber sua primeira sugestão.'}</p>}
        <p className="mt-5" aria-live="polite">{completed} de {data.tasks.length} tarefas concluídas. {completed ? 'Cada conclusão conta.' : 'Comece por uma etapa pequena.'}</p>
      </section>
      <section className="panel" aria-labelledby="subjects-title" hidden={section !== 'disciplinas'} key="subjects-title">
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
            return <li key={subject}><strong>{subject}</strong><p className="muted">{progress.completed} de {progress.total} concluídas · {progress.percent}%</p><progress aria-label={`Progresso em ${subject}`} value={progress.percent} max={100} />
              <details className="my-2">
                <summary className="cursor-pointer">Gerenciar disciplina</summary>
                <form className="form mt-2" onSubmit={event => renameSubject(event, subject)}>
                  <label>Novo nome<input name="name" defaultValue={subject} maxLength={80} required /></label>
                  <div className="flex flex-wrap gap-2"><button>Salvar nome</button><button type="button" onClick={() => removeSubject(subject)}>Excluir disciplina</button></div>
                </form>
              </details>
            </li>;
          })}</ul>
        </div>}
      </section>
      <section className="panel" aria-labelledby="tasks-title" hidden={section !== 'tarefas'} key="tasks-title">
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
          <input type="checkbox" checked={t.done} onChange={() => save({ ...data, tasks: data.tasks.map(item => item.id === t.id ? { ...item, done: !item.done, completedOn: item.done ? undefined : today } : item) })} />
          <span>{t.title}<small>{t.subject} · {t.deadline ? displayDate(t.deadline) : 'Sem prazo'} · {t.done ? 'Concluída' : t.deadline && t.deadline < today ? 'Atrasada' : 'Pendente'}</small></span>
        </label>
          <details className="my-2">
            <summary className="cursor-pointer">Gerenciar tarefa</summary>
            <form className="form mt-2" onSubmit={event => editTask(event, t)}>
              <label>Título<input name="title" defaultValue={t.title} required maxLength={120} /></label>
              <label>Disciplina<select name="subject" defaultValue={t.subject} key={t.subject}>{data.subjects.map(subject => <option key={subject}>{subject}</option>)}</select></label>
              <label>Prazo<input type="date" name="date" defaultValue={t.deadline} /></label>
              <label>Prioridade<select name="priority" defaultValue={t.priority}><option value="normal">Normal</option><option value="alta">Alta</option></select></label>
              <div className="flex flex-wrap gap-2"><button>Salvar tarefa</button><button type="button" onClick={() => removeTask(t)}>Excluir tarefa</button></div>
            </form>
          </details>
        </li>)}</ul>
      </section>
    </div>
    <section className="panel mt-5" aria-labelledby="agenda-title" hidden={section !== 'agenda'} key="agenda-title">
      <p className="eyebrow">05 / PRAZOS</p>
      <h2 id="agenda-title">Agenda de tarefas</h2>
      <section className="panel mb-5" aria-labelledby="revision-title">
        <p className="eyebrow">PLANO DE ESTUDO</p>
        <h3 id="revision-title" className="suggestion">Revisão Orbit</h3>
        <p className="muted mb-4">Revise uma ou duas vezes por dia até a véspera. Tente explicar sem consultar; depois confira o que esqueceu.</p>
        <form className="form" onSubmit={addRevision}>
          <label>Matéria e conteúdo da prova<input name="topic" maxLength={120} required placeholder="Ex.: Banco de Dados — normalização" /></label>
          <div className="grid gap-3 sm:grid-cols-2">
            <label>Data da prova<input name="exam" type="date" required /></label>
            <label>Sessões por dia<select value={twoSessions ? '2' : '1'} onChange={event => setTwoSessions(event.target.value === '2')}><option value="1">Uma</option><option value="2">Duas</option></select></label>
            <label>Primeiro horário<input name="first" type="time" defaultValue="08:00" required /></label>
            {twoSessions && <label>Segundo horário<input name="second" type="time" defaultValue="20:00" required /></label>}
          </div>
          <button className="accent" disabled={!loaded}>Criar plano de revisão</button>
          {revisionError && <p role="alert">{revisionError}</p>}
        </form>
        <ul className="mt-4 grid gap-3">{data.revisions.map(plan => {
          const previous = plan.sessions.findLast(session => plan.results[session]);
          const upcoming = plan.sessions.find(session => session.slice(0, 10) >= today && !plan.results[session]);
          return <li className="panel" key={plan.id}>
            <h4 className="font-bold">{plan.topic}</h4>
            <p className="muted">Prova: {displayDate(plan.exam)} · {Object.keys(plan.results).length} de {plan.sessions.length} sessões registradas</p>
            {previous && plan.results[previous] === 'review' && <p>Antes de reler, retome os pontos difíceis da última revisão.</p>}
            <p className="my-2">{upcoming ? `Próxima sessão pendente: ${displayDate(upcoming.slice(0, 10))} às ${upcoming.slice(11)}` : 'Não há sessões pendentes a partir de hoje.'}</p>
            <details>
              <summary className="cursor-pointer">Ver sessões e registrar revisão</summary>
              <ol className="mt-2 grid max-h-80 gap-3 overflow-auto pr-2">{plan.sessions.map(session => (
                <li key={session} className="grid gap-1">
                  <label>{displayDate(session.slice(0, 10))} às {session.slice(11)}
                    <select value={plan.results[session] ?? ''} disabled={session.slice(0, 10) > today} onChange={event => markRevision(plan.id, session, event.target.value as Outcome)}>
                      <option value="" disabled>Sem registro</option><option value="remembered">Consegui explicar</option><option value="review">Preciso rever</option>
                    </select>
                  </label>
                </li>
              ))}</ol>
            </details>
          </li>;
        })}</ul>
      </section>
      <label className="form sm:max-w-xs">Mês<input type="month" value={month} onChange={event => setAgendaMonth(event.target.value)} /></label>
      {!agenda.length ? <p className="muted mt-3">Nenhuma tarefa com prazo neste mês.</p> :
        <ol className="task-list">{agenda.map(task => <li key={task.id}>
          <time dateTime={task.deadline}>{displayDate(task.deadline)}</time> · <strong>{task.title}</strong> · {task.subject} · {task.done ? 'Concluída' : task.deadline < today ? 'Atrasada' : 'Pendente'}
        </li>)}</ol>}
    </section>
    <section className="panel weekly-report mt-5" aria-labelledby="weekly-title" hidden={section !== 'relatorio'} key="weekly-title">
      <p className="eyebrow">06 / RELATÓRIO</p>
      <h2 id="weekly-title">EduTrack · Relatório semanal</h2>
      <figure className="study-history" aria-labelledby="history-title">
        <figcaption id="history-title" className="suggestion">Evolução dos estudos</figcaption>
        <p className="muted">Tarefas concluídas nas últimas 6 semanas, por data de conclusão. As datas abaixo indicam o início de cada semana.</p>
        {!history.some(item => item.count > 0) && <p className="muted mt-2">Marque uma tarefa como concluída para começar seu histórico.</p>}
        <ol className="mt-3 grid gap-2">{history.map(item => <li className="study-history-row" key={item.start}>
          <time dateTime={item.start}>{displayDate(item.start).slice(0, 5)}</time>
          <div className="study-history-track" aria-hidden="true"><span style={{ width: (100 * item.count / maxCompleted) + '%' }} /></div>
          <strong aria-label={item.count + ' tarefas concluídas'}>{item.count}</strong>
        </li>)}</ol>
      </figure>
      <p>De {displayDate(week.start)} a {displayDate(week.end)}</p>
      <p>{week.completed} de {week.tasks.length} tarefas concluídas</p>
      <p className="muted">Inclui tarefas com vencimento nesta semana.</p>
      {week.tasks.length === 0 ? <p className="mt-3">Nenhuma tarefa com prazo nesta semana.</p> :
        <ul className="task-list">{week.tasks.map(task => <li key={task.id}>
          <strong>{task.title}</strong> — {task.subject} · {displayDate(task.deadline)} · {task.done ? 'Concluída' : 'Pendente'}
        </li>)}</ul>}
      <button className="accent mt-4" type="button" disabled={!loaded} onClick={() => window.print()}>Imprimir ou salvar como PDF</button>
    </section>
    </main>
  </div>;
}

function SubmenuIcon({ name }: { name: 'book' | 'checklist' | 'calendar' }) {
  const paths = {
    book: 'M12 6v14M12 6C9 4 6 4 3 5v14c3-1 6-1 9 1 3-2 6-2 9-1V5c-3-1-6-1-9 1Z',
    checklist: 'm3 6 2 2 3-4m-5 9 2 2 3-4m-5 9 2 2 3-4M12 6h9m-9 7h9m-9 7h9',
    calendar: 'M7 3v4m10-4v4M3 10h18M5 5h14a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2Z',
  };
  return <svg className="mr-2 shrink-0" aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d={paths[name]} />
  </svg>;
}
