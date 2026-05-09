let selectedCell = null;

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

  if (selectedCell) {
    selectedCell.classList.remove("selected");
  }

  selectedCell = cell;

  selectedCell.classList.add("selected");
}

/* PLACE STATION */

function placeStation() {

  const input =
    document.getElementById("stationInput");

  const value =
    input.value.trim();

  if (!selectedCell) {
    return;
  }

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

  } else {

    selectedCell.classList.add(
      "incorrect"
    );

    setTimeout(() => {

      selectedCell.classList.remove(
        "incorrect"
      );

    }, 400);
  }

  input.value = "";
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
