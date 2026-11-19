import { DatabaseSync } from 'node:sqlite';
import { createHash, randomBytes, scrypt as derive, timingSafeEqual } from 'node:crypto';
import { promisify } from 'node:util';
const scrypt = promisify(derive);
const digest = (value: string) => createHash('sha256').update(value).digest('hex');
const blank = () => ({ subjects: [], tasks: [], revisions: [] });

export class AccountError extends Error {
  status: number;
  constructor(message: string, status = 400) { super(message); this.status = status; }
}

export class AccountStore {
  private db: DatabaseSync;
  constructor(path: string) {
    this.db = new DatabaseSync(path);
    this.db.exec(`
      PRAGMA journal_mode=WAL;
      PRAGMA foreign_keys=ON;
      CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, salt TEXT NOT NULL, hash TEXT NOT NULL, data TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id), expires INTEGER NOT NULL);
      CREATE TABLE IF NOT EXISTS attempts(email TEXT PRIMARY KEY, count INTEGER NOT NULL, expires INTEGER NOT NULL);
    `);
  }
  close() { this.db.close(); }
  private session(user: { id: number; name: string; email: string }) {
    const token = randomBytes(32).toString('hex');
    this.db.prepare('DELETE FROM sessions WHERE expires < ?').run(Date.now());
    this.db.prepare('INSERT INTO sessions VALUES (?, ?, ?)').run(digest(token), user.id, Date.now() + 86400000);
    return { user: { id: user.id, name: user.name, email: user.email }, token };
  }
  async register(name: string, email: string, password: string) {
    name = name.trim(); email = email.trim().toLowerCase();
    if (name.length < 2 || name.length > 80 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 254 || password.length < 10 || password.length > 128) {
      throw new AccountError('Informe nome, e-mail válido e senha de 10 a 128 caracteres.');
    }
    const salt = randomBytes(16).toString('hex');
    const hash = (await scrypt(password, salt, 64) as Buffer).toString('hex');
    if (this.db.prepare('SELECT id FROM users WHERE email=?').get(email)) throw new AccountError('Não foi possível cadastrar este e-mail. Tente entrar.');
    const result = this.db.prepare('INSERT INTO users(name,email,salt,hash,data) VALUES (?,?,?,?,?)').run(name,email,salt,hash,JSON.stringify(blank()));
    return this.session({ id: Number(result.lastInsertRowid), name, email });
  }
  async login(email: string, password: string) {
    email = email.trim().toLowerCase();
    const now = Date.now();
    const attempts = this.db.prepare('SELECT count,expires FROM attempts WHERE email=?').get(email);
    if (attempts && Number(attempts.expires) > now && Number(attempts.count) >= 8) throw new AccountError('Muitas tentativas. Aguarde 15 minutos.', 429);
    this.db.prepare('INSERT INTO attempts VALUES (?,1,?) ON CONFLICT(email) DO UPDATE SET count=CASE WHEN expires<? THEN 1 ELSE count+1 END, expires=CASE WHEN expires<? THEN excluded.expires ELSE expires END').run(email,now+900000,now,now);
    const user = this.db.prepare('SELECT id,name,email,salt,hash FROM users WHERE email=?').get(email);
    const hash = await scrypt(password, String(user?.salt ?? 'unknown-account-salt'), 64) as Buffer;
    if (!user || !timingSafeEqual(hash, Buffer.from(String(user.hash),'hex'))) throw new AccountError('E-mail ou senha inválidos.',401);
    this.db.prepare('DELETE FROM attempts WHERE email=?').run(email);
    return this.session({ id: Number(user.id), name: String(user.name), email: String(user.email) });
  }
  read(token: string) {
    const user = this.db.prepare('SELECT u.id,u.name,u.email,u.data FROM users u JOIN sessions s ON s.user_id=u.id WHERE s.token=? AND s.expires>?').get(digest(token), Date.now());
    if (!user) throw new AccountError('Entre na sua conta para continuar.',401);
    return { user: { id: Number(user.id), name: String(user.name), email: String(user.email) }, data: JSON.parse(String(user.data)) };
  }
  save(token: string, data: unknown) {
    const { user } = this.read(token);
    if (!data || typeof data !== 'object') throw new AccountError('Dados inválidos.');
    const value = data as Record<string, unknown>;
    if (!Array.isArray(value.subjects) || !value.subjects.every(s => typeof s === 'string' && s.length <= 80) ||
        !Array.isArray(value.tasks) || !value.tasks.every(t => t && typeof t.id === 'string' && typeof t.title === 'string' && value.subjects instanceof Array && value.subjects.includes(t.subject) && typeof t.done === 'boolean' && typeof t.deadline === 'string') ||
        !Array.isArray(value.revisions)) throw new AccountError('Dados inválidos.');
    const json = JSON.stringify({ subjects: value.subjects, tasks: value.tasks, revisions: value.revisions });
    if (json.length > 500000) throw new AccountError('Limite de dados excedido.');
    this.db.prepare('UPDATE users SET data=? WHERE id=?').run(json, user.id);
  }
  logout(token: string) { this.db.prepare('DELETE FROM sessions WHERE token=?').run(digest(token)); }
}
