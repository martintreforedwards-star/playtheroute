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

  if (cell.classList.contains("correct")) {
    return;
  }

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

  const message =
    document.getElementById("message");

  if (!selectedCell) {

    showMessage(
      "Select a cell first.",
      "error"
    );

    return;
  }

  if (!value) {

    showMessage(
      "Enter a station name.",
      "error"
    );

    return;
  }

  if (validStations.includes(value)) {

    selectedCell.textContent = value;

    selectedCell.classList.remove("selected");

    selectedCell.classList.add("correct");

    showMessage(
      "Correct station.",
      "success"
    );

  } else {

    selectedCell.classList.add("incorrect");

    setTimeout(() => {
      selectedCell.classList.remove("incorrect");
    }, 400);

    loseTicket();

    showMessage(
      "Station not accepted.",
      "error"
    );
  }

  input.value = "";

  selectedCell = null;
}

function loseTicket() {

  tickets--;

  const ticketDisplay =
    document.getElementById("tickets");

  ticketDisplay.textContent =
    "🎫 ".repeat(tickets);

  if (tickets <= 0) {

    showMessage(
      "Out of tickets!",
      "error"
    );
  }
}

function showMessage(text, type) {

  const message =
    document.getElementById("message");

  message.textContent = text;

  message.className =
    "message " + type;
}

document
  .getElementById("stationInput")
  .addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
      placeStation();
    }

  });
