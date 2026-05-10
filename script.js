const solvedColumns = [];

let selectedCells = [];

let tickets = 5;

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

    showMessage("Already solved", "error");

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

    line1.innerText =
      options[Math.floor(Math.random() * options.length)];

    line2.innerText =
      options[Math.floor(Math.random() * options.length)];

    counter++;

    if (counter > 18) {

      clearInterval(interval);

      line1.innerText = "HIGH DENSITY";

      line2.innerText = "LOCAL SERVICES";
    }

  }, 120);
}
