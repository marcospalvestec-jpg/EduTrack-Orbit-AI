import { test } from 'node:test';
import assert from 'node:assert/strict';
import { completionHistory, weeklyReport } from './weekly.ts';

test('groups dated completions by week and ignores undone, undated and future tasks', () => {
  const counts = completionHistory([
    { done: true, completedOn: '2026-12-28' },
    { done: true, completedOn: '2027-01-05' },
    { done: true, completedOn: '2027-01-06' },
    { done: false, completedOn: '2027-01-05' },
    { done: true, deadline: '2027-01-05' },
  ], '2027-01-05').map(week => week.count);
  assert.deepEqual(counts, [0, 0, 0, 0, 1, 1]);
});

test('includes Monday through Sunday, across a year boundary', () => {
  const deadlines = ['2026-12-27','2026-12-28','2027-01-03','2027-01-04',''];
  const tasks = deadlines.map((deadline, index) => ({ deadline, done: index === 1, subject: 'Redes' }));
  const report = weeklyReport(tasks, '2027-01-03');
  assert.equal(report.start, '2026-12-28');
  assert.equal(report.end, '2027-01-03');
  assert.deepEqual(report.tasks, [tasks[1], tasks[2]]);
  assert.equal(report.completed, 1);
});
