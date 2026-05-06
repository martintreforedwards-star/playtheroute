let selectedCell = null;

let tickets = 3;

const validStations = [
  "Brighton",
  "Blackfriars",
  "East Croydon",
  "London Bridge",
  "St Albans"
];

function selectCell(cell) {

  if (selectedCell) {
    selectedCell.classList.remove("selected");
  }

  selectedCell = cell;

  selectedCell.classList.add("selected");
}

function placeStation() {

  const input =
    document.getElementById("stationInput");

  const value =
    input.value.trim();

  if (!selectedCell) {
    alert("Select a cell first");
    return;
  }

  if (validStations.includes(value)) {

    selectedCell.textContent = value;

    selectedCell.classList.remove("selected");
    selectedCell.classList.add("correct");

  } else {

    selectedCell.classList.add("incorrect");

    loseTicket();
  }

  input.value = "";
}

function loseTicket() {

  tickets--;

  const ticketDisplay =
    document.getElementById("tickets");

  ticketDisplay.textContent =
    "🎫 ".repeat(tickets);

  if (tickets <= 0) {

    alert("Out of tickets!");

  }
}
