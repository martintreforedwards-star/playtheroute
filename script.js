let tickets = 5;

function submitStation() {
  const input = document.getElementById("stationInput").value;

  if (!input) return;

  tickets--;
  document.getElementById("tickets").innerText = tickets;

  alert("You entered: " + input);

  if (tickets <= 0) {
    alert("Out of tickets!");
  }
}
