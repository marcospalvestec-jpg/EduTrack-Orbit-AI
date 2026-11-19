import { test } from 'node:test';
import assert from 'node:assert/strict';
import { AccountStore } from './accounts.ts';

test('registers, authenticates, isolates accounts and revokes sessions', async () => {
  const store = new AccountStore(':memory:');
  try {
    const a = await store.register('Aluno A', 'a@example.invalid', 'Example-password-123');
    const b = await store.register('Aluno B', 'b@example.invalid', 'Example-password-123');
    assert.notEqual(a.user.id, b.user.id);
    store.save(a.token, { subjects: ['Banco'], tasks: [], revisions: [] });
    assert.deepEqual(store.read(b.token).data.subjects, []);
    await assert.rejects(store.login('a@example.invalid', 'wrong'), /inválidos/);
    await assert.rejects(store.register('Outro', 'A@example.invalid', 'Example-password-123'));
    store.logout(a.token);
    assert.throws(() => store.read(a.token), /Entre/);
    const again = await store.login('a@example.invalid', 'Example-password-123');
    assert.deepEqual(store.read(again.token).data.subjects, ['Banco']);
    store.save(b.token, { subjects: [], tasks: [], revisions: [] });
    assert.deepEqual(store.read(again.token).data.subjects, ['Banco']);
    assert.throws(() => store.save('forged-token', { subjects: [], tasks: [], revisions: [] }));
    assert.throws(() => store.save(again.token, { subjects: 'invalid' }));
  } finally { store.close(); }
});
