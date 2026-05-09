let selectedCell = null;

let tickets = 3;

/* DAILY PUZZLE */

const puzzle = {

  cell1: "Brighton",
  cell2: "Blackfriars",
  cell3: "East Croydon",
  cell4: "London Bridge",

  cell5: "St Albans",
  cell6: "Brighton",
  cell7: "Blackfriars",
  cell8: "East Croydon"

};

/* SELECT CELL */

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

/* PLACE STATION */

function placeStation() {

  if (!selectedCell) {
    showMessage(
      "Select a square first.",
      "error"
    );
    return;
  }

  if (tickets <= 0) {
    return;
  }

  const input =
    document.getElementById("stationInput");

  const value =
    input.value.trim();

  const cellId =
    selectedCell.dataset.cell;

  const correctAnswer =
    puzzle[cellId];

  if (
    value.toLowerCase()
    ===
    correctAnswer.toLowerCase()
  ) {

    selectedCell.textContent =
      correctAnswer;

    selectedCell.classList.remove(
      "selected"
    );

    selectedCell.classList.add(
      "correct"
    );

    showMessage(
      "Correct station!",
      "success"
    );

  } else {

    selectedCell.classList.add(
      "incorrect"
    );

    setTimeout(() => {

      selectedCell.classList.remove(
        "incorrect"
      );

    }, 400);

    loseTicket();

    showMessage(
      "Incorrect station.",
      "error"
    );
  }

  input.value = "";
}

/* LOSE TICKET */

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

    document
      .getElementById("stationInput")
      .disabled = true;
  }
}

/* MESSAGE SYSTEM */

function showMessage(text, type) {

  const message =
    document.getElementById("message");

  message.textContent = text;

  message.className =
    "message " + type;

  setTimeout(() => {

    message.className =
      "message";

  }, 2000);
}

/* ENTER KEY */

document
  .getElementById("stationInput")
  .addEventListener(
    "keydown",
    function(event) {

      if (event.key === "Enter") {
        placeStation();
      }

    }
  );
