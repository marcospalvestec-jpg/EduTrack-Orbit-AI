import { test } from 'node:test';
import assert from 'node:assert/strict';
import { nextPhase, remaining, nextTask, filterTasks, searchSubjects, subjectProgress } from './study.ts';

test('search matches names without accents or subjects with pending overdue work', () => {
  const task = { id: '1', title: 'Estudar', subject: 'Redes', deadline: '2026-11-16', priority: 'normal', done: false };
  const subjects = ['Álgebra', 'Redes', 'Banco'];
  const tasks = [task, { ...task, subject: 'Banco', done: true }];
  assert.deepEqual(searchSubjects(subjects, tasks, 'algebra', true, '2026-11-17'), ['Álgebra', 'Redes']);
  assert.deepEqual(searchSubjects(subjects, tasks, '', true, '2026-11-17'), ['Redes']);
  assert.deepEqual(subjectProgress([...tasks, { ...task, done: true }], 'Redes'), { completed: 1, total: 2, percent: 50 });
  assert.equal(subjectProgress(tasks, 'Álgebra').percent, 0);
});

test('combines subject, status and deadline without treating completed work as overdue', () => {
  const task = { id: '1', title: 'Revisar', subject: 'Banco de Dados', deadline: '2026-11-16', priority: 'normal', done: false };
  const tasks = [task, { ...task, id: '2', done: true }, { ...task, id: '3', subject: 'Redes' }, { ...task, id: '4', deadline: '' }];
  assert.deepEqual(filterTasks(tasks, { subject: task.subject, status: 'pending', deadline: 'overdue' }, '2026-11-17'), [task]);
  assert.deepEqual(filterTasks(tasks, { subject: '', status: 'all', deadline: 'none' }, '2026-11-17').map(t => t.id), ['4']);
});

test('takes a long break after every fourth focus session', () => {
  assert.deepEqual(nextPhase('focus', 3), { phase: 'long', cycles: 4 });
  assert.deepEqual(nextPhase('focus', 4), { phase: 'short', cycles: 5 });
  assert.deepEqual(nextPhase('long', 4), { phase: 'focus', cycles: 4 });
});
test('uses elapsed time and never goes negative', () => {
  assert.equal(remaining(10001, 8000), 3);
  assert.equal(remaining(10001, 12000), 0);
});
test('ignores completed tasks and breaks deadline ties by priority', () => {
  const task = { id: '1', title: 'Revisar', subject: '', deadline: '2026-11-18', priority: 'normal', done: false };
  const urgent = { ...task, id: '2', priority: 'alta' };
  assert.equal(nextTask([task, urgent, { ...urgent, id: '3', deadline: '2026-11-17', done: true }]), urgent);
  assert.equal(nextTask([{ ...task, done: true }]), undefined);
});
