import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createXanoClient } from './xano.ts';

const url = 'https://hml.example.invalid/api';

test('requires explicit HTTPS homologation configuration', () => {
  assert.throws(() => createXanoClient({ target: 'production', baseUrl: url }));
  assert.throws(() => createXanoClient({ target: 'homologacao', baseUrl: 'http://example.invalid' }));
});

test('uses the account token and sends only task fields', async () => {
  const calls = [];
  const api = createXanoClient({ target: 'homologacao', baseUrl: url }, async (path, init) => {
    calls.push({ path, init });
    return Response.json({ id: 7 });
  });
  await api.createTask('synthetic-token', { subjectId: 3, title: 'Revisar', priority: 'Alta', user_id: 99 });
  const [{ path, init }] = calls;
  assert.equal(path, url + '/academic_tasks');
  assert.equal(init.headers.Authorization, 'Bearer synthetic-token');
  assert.equal(init.redirect, 'error');
  assert.deepEqual(JSON.parse(init.body), { subject_id: 3, title: 'Revisar', priority: 'Alta' });
});

test('upstream failures expose status but no remote response body', async () => {
  const api = createXanoClient({ target: 'homologacao', baseUrl: url }, async () => new Response('private detail', {status: 403}));
  await assert.rejects(api.listSubjects('synthetic-token'), error => error.status === 403 && !error.message.includes('private detail'));
});
