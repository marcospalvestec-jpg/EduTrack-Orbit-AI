export type Outcome = 'remembered' | 'review';
export type RevisionPlan = {
  id: string;
  topic: string;
  exam: string;
  sessions: string[];
  results: Partial<Record<string, Outcome>>;
};

export function revisionSessions(start: string, exam: string, times: string[]) {
  function parse(value: string) {
    const date = new Date(value + 'T00:00:00Z');
    if (!Number.isFinite(date.valueOf()) || date.toISOString().slice(0, 10) !== value) {
      throw new Error('Informe datas válidas.');
    }
    return date;
  }
  const day = parse(start);
  const end = parse(exam);
  const span = (end.valueOf() - day.valueOf()) / 86400000;
  if (span < 1 || span > 365) throw new Error('A prova deve ocorrer entre amanhã e 365 dias depois do início.');
  if (times.length < 1 || times.length > 2 || new Set(times).size !== times.length ||
      times.some(time => !/^([01]\d|2[0-3]):[0-5]\d$/.test(time))) {
    throw new Error('Informe um ou dois horários diferentes.');
  }
  const ordered = [...times].sort();
  const sessions: string[] = [];
  while (day < end) {
    const date = day.toISOString().slice(0, 10);
    for (const time of ordered) sessions.push(date + 'T' + time);
    day.setUTCDate(day.getUTCDate() + 1);
  }
  return sessions;
}
