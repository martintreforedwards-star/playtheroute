// Deterministic "today's puzzle" picker.
// Same puzzle for everyone worldwide on a given UTC day, no server/database needed -
// just the quiz's precomputed puzzlebank_{quiz}.json (array of {rows, columns} id pairs).
//
// How it avoids repeats:
//   - The bank (N puzzles) is walked in a shuffled order, one per day.
//   - That covers N days with zero repeats, whatever N happens to be for that quiz.
//   - Once the bank is exhausted, it reshuffles (seeded by the new cycle number) and
//     starts a fresh N-day pass - so cycle 2's order is different from cycle 1's.

function fnv1aHash(str) {
  let h = 0x811c9dc5;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return h >>> 0;
}

function mulberry32(seed) {
  let a = seed;
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function seededShuffleIndices(n, seed) {
  const rand = mulberry32(seed);
  const arr = Array.from({ length: n }, (_, i) => i);
  for (let i = n - 1; i > 0; i--) {
    const j = Math.floor(rand() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

const LAUNCH_DATE_UTC = Date.UTC(2026, 0, 1); // fix once at launch, never change

function daysSinceLaunch(now = new Date()) {
  const todayUTC = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
  return Math.floor((todayUTC - LAUNCH_DATE_UTC) / 86400000);
}

// quizId: e.g. "c2c_ga" | bank: the loaded puzzlebank_{quiz}.json array
function getTodaysPuzzle(quizId, bank, now = new Date()) {
  const n = bank.length;
  const day = daysSinceLaunch(now);
  const cycle = Math.floor(day / n);
  const dayInCycle = day % n;
  const seed = fnv1aHash(`${quizId}:${cycle}`);
  const order = seededShuffleIndices(n, seed);
  return bank[order[dayInCycle]]; // { rows: [id, id], columns: [id, id, id, id] }
}

// Usage:
//   const bank = await fetch(`puzzlebank_${quizId}.json`).then(r => r.json());
//   const { rows, columns } = getTodaysPuzzle(quizId, bank);
//   const rowClues = rows.map(id => rowPool.find(c => c.id === id));
//   const colClues = columns.map(id => columnPool.find(c => c.id === id));
