import { test } from 'node:test';
import assert from 'node:assert/strict';
import { weeklyReport } from './weekly.ts';

test('includes Monday through Sunday, across a year boundary', () => {
  const deadlines = ['2026-12-27','2026-12-28','2027-01-03','2027-01-04',''];
  const tasks = deadlines.map((deadline, index) => ({ deadline, done: index === 1, subject: 'Redes' }));
  const report = weeklyReport(tasks, '2027-01-03');
  assert.equal(report.start, '2026-12-28');
  assert.equal(report.end, '2027-01-03');
  assert.deepEqual(report.tasks, [tasks[1], tasks[2]]);
  assert.equal(report.completed, 1);
});
