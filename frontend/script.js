async function loadRoster() {
  const res = await fetch("data/roster.json");
  const players = await res.json();

  renderRoster(players);
}

function renderRoster(players) {
  const tbody = document.querySelector("#rosterTable tbody");
  tbody.innerHTML = "";

  players.forEach((player) => {
    let position = player.position;
    if (position === "0" || position === "1") {
      position = "G";
    }

    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${player.number || "-"}</td>
      <td>${player.name}</td>
      <td>${position}</td>
    `;

    tbody.appendChild(row);
  });
}

async function loadStats() {
  const tbody = document.querySelector("#statsTable tbody");

  // Show loading row
  tbody.innerHTML = `
  <tr>
    <td colspan="6" style="text-align:center;">
      <span class="loader"></span>
    </td>
  </tr>
`;

  try {
    const res = await fetch("https://mightydrunks-backend.onrender.com/api/stats");
    const players = await res.json();

    tbody.innerHTML = "";

    players.forEach((player) => {
      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${player.number || "-"}</td>
        <td>${player.name}</td>
        <td>${player.goals || "-"}</td>
        <td>${player.assists || "-"}</td>
        <td>${player.games_played || "-"}</td>
        <td>${player.points || "-"}</td>
      `;

      tbody.appendChild(row);
    });

  } catch (err) {
    // Show error state
    tbody.innerHTML = `
      <tr>
        <td colspan="6" style="text-align:center;">Failed to load stats.</td>
      </tr>
    `;
    console.error(err);
  }
}

async function loadSchedule() {
  const res = await fetch("https://mightydrunks-backend.onrender.com/api/schedule");
  const games = await res.json();

  const tbody = document.querySelector("#scheduleTable tbody");
  tbody.innerHTML = "";

  games.forEach((game) => {
    const row = document.createElement("tr");

    const dateTime = new Date(`${game.date}T${game.time}`);

    const formattedDate = dateTime.toLocaleDateString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric",
    });

    const formattedTime = dateTime
      .toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
      })
      .toLowerCase();

    console.log(`${formattedDate} and ${formattedTime}`);

    row.innerHTML = `
      <td>${formattedDate || "-"}</td>
      <td>${formattedTime || "-"}</td>
      <td>${game.home.team || "-"}</td>
      <td>vs</td>
      <td>${game.away.team || "-"}</td>     

    `;

    tbody.appendChild(row);
  });
}

async function loadScores() {
  const res = await fetch("https://mightydrunks-backend.onrender.com/api/scores");
  const scores = await res.json();

  const tbody = document.querySelector("#scoresTable tbody");
  tbody.innerHTML = "";

  scores.forEach((score) => {
    const row = document.createElement("tr");

    const dateTime = new Date(`${score.date}T${score.time}`);

    const formattedDate = dateTime.toLocaleDateString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric",
    });

    const formattedTime = dateTime
      .toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
      })
      .toLowerCase();

    console.log(`${formattedDate} and ${formattedTime}`);

    row.innerHTML = `
      <td>${formattedDate || "-"}</td>
      <td>${formattedTime || "-"}</td>
      <td>${score.home.team || "-"}</td>
      <td>vs</td>
      <td>${score.away.team || "-"}</td>    
      <td>${score.home.score || "-"} - ${score.away.score || "-"}</td>

    `;

    tbody.appendChild(row);
  });
}

loadRoster();
loadStats();
loadSchedule();
loadScores();
