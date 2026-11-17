import { test } from 'node:test';
import assert from 'node:assert/strict';
import { revisionSessions } from './revision.ts';

test('schedules both periods daily up to the eve of the exam', () => {
  assert.deepEqual(revisionSessions('2026-12-31', '2027-01-02', ['08:00', '20:00']), [
    '2026-12-31T08:00', '2026-12-31T20:00', '2027-01-01T08:00', '2027-01-01T20:00',
  ]);
});

test('rejects duplicate times and invalid or empty study periods', () => {
  assert.throws(() => revisionSessions('2026-11-17', '2026-11-18', ['08:00', '08:00']));
  assert.throws(() => revisionSessions('2026-11-17', '2026-11-17', ['08:00']));
  assert.throws(() => revisionSessions('2026-02-30', '2026-03-03', ['08:00']));
});
