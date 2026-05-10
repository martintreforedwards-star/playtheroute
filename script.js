# FILE: `play.html`

```html
<!DOCTYPE html>
<html lang="en">

<head>

  <meta charset="UTF-8">

  <meta
    name="viewport"
    content="width=device-width, initial-scale=1.0">

  <title>The Route — Southeastern Alpha</title>

  <link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap"
    rel="stylesheet">

  <link
    rel="stylesheet"
    href="./assets/css/style.css">

</head>

<body>

  <div class="container">

    <img
      src="logo.svg"
      alt="The Route logo"
      class="logo">

    <h1>The Route</h1>

    <p class="subtitle">
      Southeastern Alpha 001
    </p>

    <div
      class="tickets"
      id="tickets">

      🎟 🎟 🎟 🎟 🎟

    </div>

    <div
      id="message"
      class="message">
    </div>

    <div class="board-wrapper">

      <div class="column-headers">

        <div>A</div>
        <div>B</div>
        <div>C</div>
        <div>D</div>

      </div>

      <div class="platform-row">

        <div class="platform-title platform-one">
          PLATFORM 1
        </div>

        <div
          class="cell"
          data-column="A"
          data-station="Chatham"
          onclick="selectCell(this)">

          <div class="station-name">
            Chatham
          </div>

          <div class="status-text">
            arriving
          </div>

        </div>

        <div
          class="cell"
          data-column="B"
          data-station="Dartford"
          onclick="selectCell(this)">

          <div class="station-name">
            Dartford
          </div>

          <div class="status-text">
            delayed
          </div>

        </div>

        <div
          class="cell"
          data-column="C"
          data-station="Lewisham"
          onclick="selectCell(this)">

          <div class="station-name">
            Lewisham
          </div>

          <div class="status-text">
            waiting
          </div>

        </div>

        <div
          class="cell"
          data-column="D"
          data-station="Charing Cross"
          onclick="selectCell(this)">

          <div class="station-name small-text">
            Charing Cross
          </div>

          <div class="status-text">
            arriving
          </div>

        </div>

      </div>

      <div class="platform-row">

        <div class="platform-title platform-two">
          PLATFORM 2
        </div>

        <div
          class="cell"
          data-column="A"
          data-station="Fulham"
          onclick="selectCell(this)">

          <div class="station-name">
            Fulham
          </div>

          <div class="status-text">
            delayed
          </div>

        </div>

        <div
          class="cell"
          data-column="B"
          data-station="Deptford"
          onclick="selectCell(this)">

          <div class="station-name">
            Deptford
          </div>

          <div class="status-text">
            waiting
          </div>

        </div>

        <div
          class="cell"
          data-column="C"
          data-station="London Bridge"
          onclick="selectCell(this)">

          <div class="station-name small-text">
            London Bridge
          </div>

          <div class="status-text">
            arriving
          </div>

        </div>

        <div
          class="cell"
          data-column="D"
          data-station="Cannon Street"
          onclick="selectCell(this)">

          <div class="station-name small-text">
            Cannon Street
          </div>

          <div class="status-text">
            delayed
          </div>

        </div>

      </div>

    </div>

    <div class="controls">

      <button onclick="submitPair()">
        Submit Pair
      </button>

      <button
        class="secondary-button"
        onclick="clearSelection()">
        Clear
      </button>

    </div>

    <div
      id="splitFlap"
      class="split-flap hidden">

      <div class="split-title">
        SERVICE UPDATE
      </div>

      <div
        id="flapLine1"
        class="flap-line">
        THAMESLINK
      </div>

      <div
        id="flapLine2"
        class="flap-line">
        HIGH SPEED
      </div>

    </div>

  </div>

  <script src="script.js"></script>

</body>

</html>
```

---

# FILE: `script.js`

```javascript
const solvedColumns = [];

let selectedCells = [];

let tickets = 5;

const solution = {
  A: ["Chatham", "Fulham"],
  B: ["Dartford", "Deptford"],
  C: ["Lewisham", "London Bridge"],
  D: ["Charing Cross", "Cannon Street"]
};

function selectCell(cell) {

  if (cell.classList.contains("solved")) {
    return;
  }

  if (cell.classList.contains("selected")) {

    cell.classList.remove("selected");

    selectedCells = selectedCells.filter(c => c !== cell);

    return;
  }

  if (selectedCells.length >= 2) {
    return;
  }

  cell.classList.add("selected");

  selectedCells.push(cell);
}

function clearSelection() {

  selectedCells.forEach(cell => {
    cell.classList.remove("selected");
  });

  selectedCells = [];
}

function submitPair() {

  if (selectedCells.length !== 2) {

    showMessage("Select two stations", "error");

    return;
  }

  const column1 = selectedCells[0].dataset.column;
  const column2 = selectedCells[1].dataset.column;

  if (column1 !== column2) {

    loseTicket();

    flashIncorrect();

    showMessage("Incorrect pair", "error");

    clearSelection();

    return;
  }

  if (solvedColumns.includes(column1)) {

    showMessage("Column already solved", "error");

    clearSelection();

    return;
  }

  solvedColumns.push(column1);

  transformToTrain(selectedCells, column1);

  showMessage("Correct pair", "success");

  clearSelection();

  if (solvedColumns.length === 4) {

    setTimeout(() => {
      showSplitFlap();
    }, 1000);
  }
}

function transformToTrain(cells, column) {

  cells.forEach(cell => {

    cell.classList.remove("selected");

    cell.classList.add("solved");

    if (column === "D") {

      cell.innerHTML = `
        <div class="train-icon engine">
          🚆
        </div>
      `;

    } else {

      cell.innerHTML = `
        <div class="train-icon">
          🚃
        </div>
      `;
    }
  });
}

function loseTicket() {

  tickets--;

  updateTickets();

  if (tickets <= 0) {

    showMessage("Journey ended", "error");

    document.querySelectorAll(".cell").forEach(cell => {
      cell.onclick = null;
    });
  }
}

function updateTickets() {

  const ticketDisplay = document.getElementById("tickets");

  let output = "";

  for (let i = 0; i < tickets; i++) {
    output += "🎟 ";
  }

  for (let i = tickets; i < 5; i++) {
    output += "❌ ";
  }

  ticketDisplay.innerHTML = output;
}

function flashIncorrect() {

  selectedCells.forEach(cell => {

    cell.classList.add("incorrect");

    setTimeout(() => {
      cell.classList.remove("incorrect");
    }, 600);
  });
}

function showMessage(text, type) {

  const message = document.getElementById("message");

  message.innerText = text;

  message.className = `message ${type}`;
}

function showSplitFlap() {

  const flap = document.getElementById("splitFlap");

  flap.classList.remove("hidden");

  const line1 = document.getElementById("flapLine1");
  const line2 = document.getElementById("flapLine2");

  const options = [
    "THAMESLINK",
    "COASTAL ROUTE",
    "AIRPORT LINK",
    "HIGH SPEED",
    "COMMUTER LINE",
    "INTERCHANGE"
  ];

  let counter = 0;

  const interval = setInterval(() => {

    line1.innerText = options[Math.floor(Math.random() * options.length)];

    line2.innerText = options[Math.floor(Math.random() * options.length)];

    counter++;

    if (counter > 18) {

      clearInterval(interval);

      line1.innerText = "HIGH DENSITY";

      line2.innerText = "LOCAL SERVICES";
    }

  }, 120);
}
```

---

# FILE: `/assets/css/style.css`

```css
body {

  margin: 0;

  min-height: 100vh;

  display: flex;

  justify-content: center;

  align-items: center;

  background:
    linear-gradient(
      180deg,
      #020817 0%,
      #031525 100%
    );

  font-family: 'Inter', sans-serif;

  color: white;
}

.container {

  width: 100%;

  max-width: 1100px;

  padding: 40px 20px 80px;

  text-align: center;
}

.logo {

  width: 90px;

  margin-bottom: 28px;
}

h1 {

  margin: 0;

  font-size: 82px;

  font-weight: 700;

  letter-spacing: -2px;
}

.subtitle {

  margin-top: 18px;

  font-size: 34px;

  color: rgba(255,255,255,0.7);
}

.tickets {

  margin-top: 24px;

  font-size: 34px;
}

.message {

  height: 32px;

  margin-top: 18px;

  font-size: 22px;

  font-weight: 700;

  opacity: 0;

  transition: 0.2s;
}

.message.success {

  color: #57d37c;

  opacity: 1;
}

.message.error {

  color: #ff6b6b;

  opacity: 1;
}

.board-wrapper {

  margin-top: 50px;
}

.column-headers {

  display: grid;

  grid-template-columns: repeat(4, 1fr);

  gap: 18px;

  margin-left: 230px;

  margin-bottom: 18px;

  color: rgba(255,255,255,0.6);

  font-size: 22px;

  font-weight: 700;
}

.platform-row {

  display: grid;

  grid-template-columns: 190px repeat(4, 1fr);

  gap: 18px;

  margin-bottom: 26px;

  align-items: center;
}

.platform-title {

  text-align: left;

  padding: 24px;

  border-left: 6px solid #57d37c;

  background: rgba(255,255,255,0.04);

  border-radius: 18px;

  font-size: 24px;

  font-weight: 700;

  letter-spacing: 1px;
}

.platform-two {

  border-left-color: #60a5fa;
}

.cell {

  min-height: 150px;

  border-radius: 22px;

  background: #0f172a;

  border: 3px solid #22345c;

  transition: 0.2s;

  cursor: pointer;

  display: flex;

  flex-direction: column;

  justify-content: center;

  align-items: center;

  padding: 12px;
}

.cell:hover {

  border-color: #57d37c;

  transform: translateY(-2px);
}

.cell.selected {

  border-color: #57d37c;

  box-shadow:
    0 0 0 4px rgba(87,211,124,0.25);
}

.cell.solved {

  background: #132238;

  border-color: #57d37c;
}

.cell.incorrect {

  border-color: #ff6b6b;
}

.station-name {

  font-size: 26px;

  font-weight: 700;

  line-height: 1.2;
}

.small-text {

  font-size: 22px;
}

.status-text {

  margin-top: 12px;

  font-size: 16px;

  text-transform: uppercase;

  letter-spacing: 2px;

  color: rgba(255,255,255,0.45);
}

.train-icon {

  font-size: 54px;
}

.engine {

  transform: scaleX(-1);
}

.controls {

  margin-top: 40px;

  display: flex;

  justify-content: center;

  gap: 20px;
}

button {

  padding: 20px 34px;

  border: none;

  border-radius: 18px;

  background: #2ecc71;

  color: white;

  font-size: 24px;

  font-weight: 700;

  cursor: pointer;
}

.secondary-button {

  background: #334155;
}

.split-flap {

  margin-top: 60px;

  max-width: 600px;

  margin-left: auto;

  margin-right: auto;

  padding: 30px;

  border-radius: 20px;

  background: #050b16;

  border: 3px solid #22345c;
}

.hidden {

  display: none;
}

.split-title {

  margin-bottom: 24px;

  font-size: 24px;

  letter-spacing: 3px;

  color: rgba(255,255,255,0.7);
}

.flap-line {

  margin-top: 14px;

  padding: 18px;

  background: black;

  border-radius: 12px;

  font-size: 38px;

  font-weight: 700;

  letter-spacing: 4px;

  font-family: monospace;
}
```
