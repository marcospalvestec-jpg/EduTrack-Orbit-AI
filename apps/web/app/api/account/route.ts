import { NextRequest, NextResponse } from 'next/server';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { AccountError, AccountStore } from '../../../lib/accounts';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
const cookie = 'edutrack_session';
let instance: AccountStore;
function store() {
  if (!instance) {
    mkdirSync(join(process.cwd(), '.data'), { recursive: true });
    instance = new AccountStore(join(process.cwd(), '.data', 'accounts.sqlite'));
  }
  return instance;
}
const json = (data: object, status = 200) => NextResponse.json(data, { status, headers: { 'Cache-Control': 'no-store' } });
function errorResponse(error: unknown) {
  return error instanceof AccountError ? json({ error: error.message }, error.status) : json({ error: 'Não foi possível concluir. Tente novamente.' },500);
}
export async function GET(request: NextRequest) {
  try { return json(store().read(request.cookies.get(cookie)?.value ?? '')); }
  catch (error) { return errorResponse(error); }
}
export async function POST(request: NextRequest) {
  try {
    const origin = request.headers.get('origin');
    if (!origin || new URL(origin).host !== request.headers.get('host')) return json({ error: 'Origem não autorizada.' },403);
    const text = await request.text();
    if (text.length > 550000) return json({ error: 'Requisição muito grande.' },413);
    const body = JSON.parse(text);
    const token = request.cookies.get(cookie)?.value ?? '';
    if (body.action === 'save') { store().save(token, body.data); return json({ ok: true }); }
    if (body.action === 'logout') {
      store().logout(token);
      const response = json({ ok: true });
      response.cookies.set(cookie,'',{ httpOnly: true, sameSite:'lax', path:'/', maxAge:0 });
      return response;
    }
    if (!['login','register'].includes(body.action) || typeof body.email !== 'string' || typeof body.password !== 'string' ||
        body.email.length > 254 || body.password.length > 128 || (body.action === 'register' && typeof body.name !== 'string')) return json({error:'Preencha os campos corretamente.'},400);
    const result = body.action === 'register' ? await store().register(body.name,body.email,body.password) : await store().login(body.email,body.password);
    const response = json(store().read(result.token));
    response.cookies.set(cookie,result.token,{ httpOnly:true, sameSite:'lax', secure:request.nextUrl.protocol === 'https:', path:'/', maxAge:86400 });
    return response;
  } catch (error) { return errorResponse(error); }
}
