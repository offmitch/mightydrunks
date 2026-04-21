async function loadRoster() {
  const res = await fetch("http://127.0.0.1:5000/api/roster");
  const players = await res.json();

  const tbody = document.querySelector("#rosterTable tbody");
  tbody.innerHTML = "";

  players.forEach(player => {
    const row = document.createElement("tr");

    if(player.position === "0" || player.position === "1") {
      player.position = "G";
    }

    row.innerHTML = `
      <td>${player.number || "-"}</td>
      <td>${player.name}</td>
      <td>${player.position}</td>
    `;

    tbody.appendChild(row);
  });
}

loadRoster();