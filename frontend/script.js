// ─────────────────────────────────────────────────────────────
//  script.js — API fetches + rendering
// ─────────────────────────────────────────────────────────────

const BASE = "https://mightydrunks-backend.onrender.com/api";

// Instagram SVG icon (inline, reusable)
const IG_SVG = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>`;

// ── helpers ──────────────────────────────────────────────────

function playerLookup(name) {
  return (typeof PLAYER_DATA !== "undefined" && PLAYER_DATA[name]) || {};
}

function showSpinner(containerId, label = "Loading...") {
  document.getElementById(containerId).innerHTML = `
    <div class="spinner-wrap">
      <div class="spinner"></div>
      <div class="spinner-label">${label}</div>
    </div>
  `;
}

function headshotEl(name, size = 80) {
  const p = playerLookup(name);
  if (p.headshot) {
    return `<img class="hero-headshot" src="${p.headshot}" alt="${name}" style="width:${size}px;height:${size}px">`;
  }
  return `<div class="hero-headshot-placeholder" style="width:${size}px;height:${size}px;font-size:${Math.round(size * 0.4)}px">🏒</div>`;
}

function profileHeadshotEl(name) {
  const p = playerLookup(name);
  if (p.headshot) {
    return `<img class="profile-headshot" src="${p.headshot}" alt="${name}">`;
  }
  return `<div class="profile-headshot-placeholder">🏒</div>`;
}

function formatDateTime(date, time) {
  const dt = new Date(`${date}T${time}`);
  const fDate = dt.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
  });
  const fTime = dt
    .toLocaleTimeString("en-US", {
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    })
    .toLowerCase();
  return { fDate, fTime };
}

// ── cached data (for profile overlay) ────────────────────────
let cachedStats = [];
let cachedRoster = [];

// ── home tab ─────────────────────────────────────────────────

async function loadHome() {
  showSpinner("heroContainer", "Loading stats...");
  showSpinner("nextGameCard", "Loading schedule...");
  showSpinner("prevGameCard", "Loading score...");
  // Top scorer
  try {
    const [statsRes, schedRes] = await Promise.all([
      fetch(`${BASE}/stats`),
      fetch(`${BASE}/schedule`),
    ]);
    const stats = await statsRes.json();
    const schedule = await schedRes.json();
    // Top scorer by points
    const sorted = [...stats].sort((a, b) => (b.points || 0) - (a.points || 0));
    const top = sorted[0];

    if (top) {
      document.getElementById("heroHeadshot").innerHTML = headshotEl(
        top.name,
        80,
      );
      document.getElementById("heroName").textContent = top.name;
      document.getElementById("heroPos").textContent = top.position || "";
      document.getElementById("heroGoals").textContent = top.goals ?? "-";
      document.getElementById("heroAssists").textContent = top.assists ?? "-";
      document.getElementById("heroPoints").textContent = top.points ?? "-";
      document.getElementById("heroGP").textContent = top.games_played ?? "-";
    }

    // Next upcoming game
    const now = new Date();
    const upcoming = schedule
      .map((g) => ({ ...g, _dt: new Date(`${g.date}T${g.time}`) }))
      .filter((g) => g._dt >= now)
      .sort((a, b) => a._dt - b._dt);

    const next = upcoming[0];
    if (next) {
      const { fDate, fTime } = formatDateTime(next.date, next.time);
      const homeTeam = next.home?.team || next.home || "-";
      const awayTeam = next.away?.team || next.away || "-";
      document.getElementById("nextGameHome").textContent = homeTeam;
      document.getElementById("nextGameHome").className =
        "next-game-team" + (homeTeam === OUR_TEAM ? " is-us" : "");
      document.getElementById("nextGameAway").textContent = awayTeam;
      document.getElementById("nextGameAway").className =
        "next-game-team right" + (awayTeam === OUR_TEAM ? " is-us" : "");
      document.getElementById("nextGameMeta").textContent =
        `${fDate} · ${fTime}`;
      document.getElementById("nextGameCard").style.display = "";
      document.getElementById("nextGameSpinner").innerHTML = "";
    } else {
      document.getElementById("nextGameCard").style.display = "none";
    }

    // Previous game
    const scoresRes = await fetch(`${BASE}/scores`);
    const scoresData = await scoresRes.json();

    const past = scoresData
      .map((g) => ({ ...g, _dt: new Date(`${g.date}T${g.time}`) }))
      .sort((a, b) => b._dt - a._dt);

    const prev = past[0];
    if (prev) {
      const { fDate } = formatDateTime(prev.date, prev.time);
      const homeTeam = prev.home?.team || prev.home || "-";
      const awayTeam = prev.away?.team || prev.away || "-";
      const homeScore = prev.home?.score ?? "-";
      const awayScore = prev.away?.score ?? "-";

      document.getElementById("prevGameHome").textContent = homeTeam;
      document.getElementById("prevGameHome").className =
        "next-game-team" + (homeTeam === OUR_TEAM ? " is-us" : "");
      document.getElementById("prevGameAway").textContent = awayTeam;
      document.getElementById("prevGameAway").className =
        "next-game-team right" + (awayTeam === OUR_TEAM ? " is-us" : "");
      document.getElementById("prevGameMeta").textContent = fDate;

      const isHome = homeTeam === OUR_TEAM;
      const ourScore = isHome ? homeScore : awayScore;
      const oppScore = isHome ? awayScore : homeScore;
      const result =
        ourScore > oppScore ? "win" : ourScore < oppScore ? "loss" : "";

      const scoreBadge = document.getElementById("prevGameScore");
      scoreBadge.textContent = `${homeScore} – ${awayScore}`;
      scoreBadge.className = `score-badge ${result}`;
      scoreBadge.style.display = "";

      document.getElementById("prevGameCard").style.display = "";
      document.getElementById("prevGameSpinner").innerHTML = "";
    } else {
      document.getElementById("prevGameCard").style.display = "none";
    }
  } catch (e) {
    console.error("Home load error:", e);
  }
}

// ── roster ────────────────────────────────────────────────────

async function loadRoster() {
  const tbody = document.querySelector("#rosterTable tbody");
  tbody.innerHTML = `
    <tr>
      <td colspan="3">
        <div class="spinner-wrap">
          <div class="spinner"></div>
          <div class="spinner-label">Loading roster...</div>
        </div>
      </td>
    </tr>
  `;

  const res = await fetch(`${BASE}/roster`);
  const players = await res.json();
  cachedRoster = players;

  tbody.innerHTML = ""; 

  players.forEach((player) => {
    if (player.position === "0" || player.position === "1")
      player.position = "G";

    const row = document.createElement("tr");
    row.className = "clickable";
    row.innerHTML = `
      <td>${player.number || "-"}</td>
      <td class="name-cell">${player.name}</td>
      <td>${player.position}</td>
    `;
    row.addEventListener("click", () => openProfile(player.name));
    tbody.appendChild(row);
  });
}

// ── stats ─────────────────────────────────────────────────────

async function loadStats() {
   const tbody = document.querySelector("#statsTable tbody");
  tbody.innerHTML = `
    <tr>
      <td colspan="6">
        <div class="spinner-wrap">
          <div class="spinner"></div>
          <div class="spinner-label">Loading stats...</div>
        </div>
      </td>
    </tr>
  `;

  const res = await fetch(`${BASE}/stats`);
  const players = await res.json();
  cachedStats = players;

  tbody.innerHTML = "";

  players.forEach((player) => {
    const row = document.createElement("tr");
    row.className = "clickable";
    row.innerHTML = `
      <td>${player.number || "-"}</td>
      <td class="name-cell">${player.name}</td>
      <td>${player.goals ?? "-"}</td>
      <td>${player.assists ?? "-"}</td>
      <td>${player.games_played ?? "-"}</td>
      <td class="pts-cell">${player.points ?? "-"}</td>
    `;
    row.addEventListener("click", () => openProfile(player.name));
    tbody.appendChild(row);
  });
}

// ── schedule ──────────────────────────────────────────────────

async function loadSchedule() {
   const tbody = document.querySelector("#scheduleTable tbody");
  tbody.innerHTML = `
    <tr>
      <td colspan="5">
        <div class="spinner-wrap">
          <div class="spinner"></div>
          <div class="spinner-label">Loading schedule...</div>
        </div>
      </td>
    </tr>
  `;

  const res = await fetch(`${BASE}/schedule`);
  const games = await res.json();

  tbody.innerHTML = "";

  games.forEach((game) => {
    const { fDate, fTime } = formatDateTime(game.date, game.time);
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${fDate || "-"}</td>
      <td>${fTime || "-"}</td>
      <td>${game.home?.team || game.home || "-"}</td>
      <td>vs</td>
      <td>${game.away?.team || game.away || "-"}</td>
    `;
    tbody.appendChild(row);
  });
}

// ── scores ────────────────────────────────────────────────────

async function loadScores() {
    const tbody = document.querySelector("#scoresTable tbody");
  tbody.innerHTML = `
    <tr>
      <td colspan="6">
        <div class="spinner-wrap">
          <div class="spinner"></div>
          <div class="spinner-label">Loading scores...</div>
        </div>
      </td>
    </tr>
  `;

  const res = await fetch(`${BASE}/scores`);
  const scores = await res.json();

  tbody.innerHTML = "";

  scores.forEach((score) => {
    const { fDate, fTime } = formatDateTime(score.date, score.time);
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${fDate || "-"}</td>
      <td>${fTime || "-"}</td>
      <td>${score.home?.team || score.home || "-"}</td>
      <td>vs</td>
      <td>${score.away?.team || score.away || "-"}</td>
      <td>${score.home?.score ?? "-"} – ${score.away?.score ?? "-"}</td>
    `;
    tbody.appendChild(row);
  });
}

// ── news ──────────────────────────────────────────────────────

function loadNews() {
  const list = document.getElementById("newsList");
  if (typeof NEWS_POSTS === "undefined" || !NEWS_POSTS.length) {
    list.innerHTML = `<div style="text-align:center;padding:40px;color:rgba(244,244,240,0.3);font-family:'Barlow Condensed',sans-serif;letter-spacing:1px;">No news yet</div>`;
    return;
  }
  list.innerHTML = NEWS_POSTS.map(
    (p) => `
    <div class="news-card">
      <div class="news-card-body">
        <span class="news-tag ${p.tagColor === "green" ? "green" : ""}">${p.tag}</span>
        <div class="news-title">${p.title}</div>
        <div class="news-excerpt">${p.excerpt}</div>
        <div class="news-date">${p.date}</div>
      </div>
    </div>
  `,
  ).join("");
}

// ── player profile overlay ────────────────────────────────────

function openProfile(name) {
  const statsPlayer = cachedStats.find((p) => p.name === name) || {};
  const rosterPlayer = cachedRoster.find((p) => p.name === name) || {};
  const extra = playerLookup(name);

  let position = rosterPlayer.position || statsPlayer.position || "";
  if (position === "0" || position === "1") position = "G";

  const number = rosterPlayer.number || statsPlayer.number || "-";
  const goals = statsPlayer.goals ?? "-";
  const assists = statsPlayer.assists ?? "-";
  const points = statsPlayer.points ?? "-";
  const gp = statsPlayer.games_played ?? "-";
  const bio = extra.bio || "Coming Soon";
  const igHandle = extra.instagram || "Coming Soon";

  document.getElementById("profileHeadshot").innerHTML =
    profileHeadshotEl(name);
  document.getElementById("profileNumber").textContent = `#${number}`;
  document.getElementById("profileName").textContent = name;
  document.getElementById("profilePos").textContent = position;
  document.getElementById("profileGoals").textContent = goals;
  document.getElementById("profileAssists").textContent = assists;
  document.getElementById("profilePoints").textContent = points;
  document.getElementById("profileGP").textContent = gp;
  document.getElementById("profileBio").textContent = bio;

  const igLink = document.getElementById("profileInstagram");
  if (igHandle) {
    igLink.href = `https://instagram.com/${igHandle}`;
    igLink.innerHTML = `${IG_SVG} @${igHandle}`;
    igLink.style.display = "inline-flex";
  } else {
    igLink.style.display = "none";
  }

  document.getElementById("playerProfileOverlay").classList.add("open");
  document.body.style.overflow = "hidden";
}

function closeProfile() {
  document.getElementById("playerProfileOverlay").classList.remove("open");
  document.body.style.overflow = "";
}

document
  .getElementById("playerProfileOverlay")
  .addEventListener("click", (e) => {
    if (e.target === e.currentTarget) closeProfile();
  });
document.getElementById("profileClose").addEventListener("click", closeProfile);

// ── init ──────────────────────────────────────────────────────

loadHome();
loadRoster();
loadStats();
loadSchedule();
loadScores();
loadNews();
