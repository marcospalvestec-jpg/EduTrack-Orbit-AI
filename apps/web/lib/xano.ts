type Settings = { target?: string; baseUrl?: string };
type TaskInput = { subjectId: number; title: string; dueDate?: string; priority: 'Alta' | 'Média' | 'Baixa' };

export class XanoRequestError extends Error {
  readonly status: number;
  constructor(status: number) {
    super('Não foi possível concluir a operação no Xano.');
    this.status = status;
  }
}

/** Server-side adapter. Its responses are upstream data, not public DTOs. */
export function createXanoClient(settings: Settings = {
  target: process.env.EDUTRACK_TARGET,
  baseUrl: process.env.XANO_HML_BASE_URL,
}, fetcher: typeof fetch = fetch) {
  if (typeof window !== 'undefined') throw new Error('Integração disponível apenas no servidor.');
  let url: URL;
  try { url = new URL(settings.baseUrl ?? ''); }
  catch { throw new Error('Configure a URL de homologação do Xano.'); }
  if (settings.target !== 'homologacao' || url.protocol !== 'https:' || url.username || url.password || url.search || url.hash) {
    throw new Error('Configure um ambiente HTTPS exclusivo de homologação.');
  }
  const base = url.href.replace(/\/+$/, '');

  async function request(path: string, method: 'GET' | 'POST', token?: string, payload?: object): Promise<unknown> {
    if (token !== undefined && !token.trim()) throw new XanoRequestError(401);
    const headers: Record<string, string> = { Accept: 'application/json' };
    if (token) headers.Authorization = 'Bearer ' + token;
    if (payload) headers['Content-Type'] = 'application/json';
    try {
      const response = await fetcher(base + '/' + path, {
        headers, method, body: payload ? JSON.stringify(payload) : undefined,
        cache: 'no-store', redirect: 'error', signal: AbortSignal.timeout(10000),
      });
      if (!response.ok) throw new XanoRequestError(response.status);
      return await response.json();
    } catch (error) {
      if (error instanceof XanoRequestError) throw error;
      throw new XanoRequestError(502);
    }
  }

  return {
    signup: (name: string, email: string, password: string) => request('auth/signup', 'POST', undefined, { name, email, password }),
    login: (email: string, password: string) => request('auth/login', 'POST', undefined, { email, password }),
    profile: (token: string) => request('auth/me', 'GET', token),
    listSubjects: (token: string, page = 1) => request('subjects?page=' + page, 'GET', token),
    createSubject: (token: string, name: string) => request('subjects', 'POST', token, { name }),
    listTasks: (token: string, page = 1) => request('academic_tasks?page=' + page, 'GET', token),
    createTask: (token: string, input: TaskInput) => request('academic_tasks', 'POST', token, {
      subject_id: input.subjectId, title: input.title, due_date: input.dueDate, priority: input.priority,
    }),
  };
}
