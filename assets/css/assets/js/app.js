let selectedCell = null;

function selectCell(cell) {
  selectedCell = cell;

  document.querySelectorAll(".cell").forEach(c => {
    c.style.outline = "none";
  });

  cell.style.outline = "2px solid #2ecc71";
}

function placeStation() {
  const input = document.getElementById("stationInput").value;

  if (!selectedCell || !input) return;

  selectedCell.textContent = input.toUpperCase();
  document.getElementById("stationInput").value = "";
}
