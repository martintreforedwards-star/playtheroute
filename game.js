// FILE: game.js

// ========================================
// PUZZLE DATA
// ========================================

const puzzle = {
  answers: [
    ["Ramsgate", "Broadstairs"],
    ["Margate", "Dumpton Park"]
  ]
};

// ========================================
// STATION LIST
// ========================================

const stations = [
  "Ramsgate",
  "Broadstairs",
  "Margate",
  "Dumpton Park",
  "Canterbury West",
  "Ashford International",
  "Deal",
  "Sandwich",
  "Faversham",
  "Herne Bay",
  "Whitstable"
];

// ========================================
// GLOBALS
// ========================================

const grid = document.getElementById("grid");

const modal = document.getElementById("modal");

const stationSearch = document.getElementById("stationSearch");

const stationList = document.getElementById("stationList");

const closeModal = document.getElementById("closeModal");

let activeCell = null;

// ========================================
// BUILD GRID
// ========================================

function buildGrid() {

  puzzle.answers.forEach((row, rowIndex) => {

    row.forEach((answer, colIndex) => {

      const cell = document.createElement("div");

      cell.className = "cell";

      cell.dataset.answer = answer;

      cell.dataset.row = rowIndex;

      cell.dataset.col = colIndex;

      cell.textContent = "Select Station";

      cell.addEventListener("click", () => {

        if (cell.classList.contains("correct")) {
          return;
        }

        activeCell = cell;

        openModal();
      });

      grid.appendChild(cell);

    });

  });

}

// ========================================
// MODAL
// ========================================

function openModal() {

  modal.classList.remove("hidden");

  stationSearch.value = "";

  renderStationList(stations);

  stationSearch.focus();

}

function closeModalWindow() {

  modal.classList.add("hidden");

}

closeModal.addEventListener("click", closeModalWindow);

// ========================================
// STATION LIST
// ========================================

function renderStationList(list) {

  stationList.innerHTML = "";

  list.forEach(station => {

    const option = document.createElement("div");

    option.className = "station-option";

    option.textContent = station;

    option.addEventListener("click", () => {

      checkAnswer(station);

    });

    stationList.appendChild(option);

  });

}

// ========================================
// SEARCH
// ========================================

stationSearch.addEventListener("input", () => {

  const value = stationSearch.value.toLowerCase();

  const filtered = stations.filter(station =>
    station.toLowerCase().includes(value)
  );

  renderStationList(filtered);

});

// ========================================
// CHECK ANSWER
// ========================================

function checkAnswer(selectedStation) {

  const correctAnswer = activeCell.dataset.answer;

  if (selectedStation === correctAnswer) {

    activeCell.textContent = selectedStation;

    activeCell.classList.add("correct");

  } else {

    alert("Incorrect station");

  }

  closeModalWindow();

}

// ========================================
// START
// ========================================

buildGrid();
