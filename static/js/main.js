const campaigns = [
  {
    title: "Promoción Verano 2024",
    platform: "TikTok",
    date: "May 02, 2024",
    reach: "35.0K",
    views: "6.5K",
    status: "Activa",
  },
  {
    title: "Lanzamiento Producto",
    platform: "Instagram",
    date: "May 06, 2024",
    reach: "12.0K",
    views: "9.5K",
    status: "Activa",
  },
  {
    title: "Black Friday Especial",
    platform: "YouTube",
    date: "Apr 12, 2024",
    reach: "18.4K",
    views: "9.5K",
    status: "Activa",
  },
  {
    title: "Black Friday 2024",
    platform: "Instagram",
    date: "Apr 22, 2024",
    reach: "65.0K",
    views: "9.5K",
    status: "Activa",
  },
];

const stats = {
  ctr: 42,
  plays: "8.2K",
  conversions: "125K",
};

const previewMessages = [
  "Listo para publicar en minutos",
  "Video personalizado según tu brief",
  "Copys y recursos optimizados",
  "Previsualización generada con IA",
];

function renderCampaigns(list = campaigns) {
  const grid = document.getElementById("campaignGrid");
  grid.innerHTML = "";

  list.forEach((campaign) => {
    const card = document.createElement("article");
    card.className = "campaign-card";
    card.innerHTML = `
      <div class="campaign-cover"></div>
      <div class="campaign-meta">
        <span class="badge">${campaign.platform}</span>
        <span class="muted small">${campaign.date}</span>
      </div>
      <h4>${campaign.title}</h4>
      <div class="campaign-meta">
        <span class="chip">${campaign.reach} Alcance</span>
        <span class="chip">${campaign.views} Visualizaciones</span>
      </div>
    `;
    grid.appendChild(card);
  });
}

function setStats() {
  document.getElementById("ctrStat").textContent = `${stats.ctr}%`;
  document.getElementById("playsStat").textContent = stats.plays;
  document.getElementById("convStat").textContent = stats.conversions;
}

function updateFormat(format) {
  const selected = document.getElementById("selectedFormat");
  const previewTitle = document.getElementById("previewTitle");
  selected.textContent = `${format} (${format === "TikTok" ? "9:16" : "16:9"})`;
  previewTitle.textContent = `${format} listo para publicar`;
}

function toggleChipSelection(containerId, activeClass = "active") {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.addEventListener("click", (event) => {
    const target = event.target;
    if (target.tagName === "BUTTON") {
      [...container.querySelectorAll("button")].forEach((btn) =>
        btn.classList.remove(activeClass)
      );
      target.classList.add(activeClass);
    }
  });
}

function toggleSelectablePills() {
  const platforms = document.getElementById("platformPills");
  platforms.addEventListener("click", (event) => {
    const target = event.target;
    if (target.tagName !== "BUTTON") return;
    target.classList.toggle("active");
  });
}

function handleSearch() {
  const searchInput = document.getElementById("searchInput");
  searchInput.addEventListener("input", () => {
    const term = searchInput.value.toLowerCase();
    const filtered = campaigns.filter(({ title, platform }) =>
      title.toLowerCase().includes(term) || platform.toLowerCase().includes(term)
    );
    renderCampaigns(filtered);
  });
}

function handleNewCampaign() {
  const form = document.getElementById("campaignForm");
  const button = document.getElementById("submitCampaign");

  const getSelected = (containerId) => {
    const active = document.querySelector(`#${containerId} .pill.active`);
    return active ? active.dataset.duration || active.dataset.resolution : "-";
  };

  button.addEventListener("click", (event) => {
    event.preventDefault();
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const name = document.getElementById("campaignName").value;
    const description = document.getElementById("campaignDescription").value;
    const duration = getSelected("durationPills");
    const resolution = getSelected("resolutionPills");
    const platforms = [...document.querySelectorAll("#platformPills .pill.active")].map((pill) => pill.dataset.platform);

    campaigns.unshift({
      title: name,
      platform: platforms.join(", ") || "Multi-Red",
      date: new Date().toLocaleDateString("es-ES", { month: "short", day: "2-digit", year: "numeric" }),
      reach: "—",
      views: `${duration}/${resolution}`,
      status: "Borrador",
    });

    renderCampaigns();
    form.reset();
    document.querySelectorAll(".pill.active").forEach((pill) => pill.classList.remove("active"));
    document.querySelector("#durationPills .pill").classList.add("active");
    document.querySelector("#resolutionPills .pill").classList.add("active");
    document.querySelector("#platformPills .pill").classList.add("active");
    document.getElementById("newCampaign").scrollIntoView({ behavior: "smooth" });
    alert(`Campaña "${name}" guardada como borrador`);
  });
}

function bindFormatChips() {
  const chips = document.getElementById("formatChips");
  chips.addEventListener("click", (event) => {
    if (event.target.tagName !== "BUTTON") return;
    chips.querySelectorAll("button").forEach((chip) => chip.classList.remove("active"));
    event.target.classList.add("active");
    updateFormat(event.target.dataset.format);
  });
}

function bindGeneratePreview() {
  const button = document.getElementById("generateVideo");
  button.addEventListener("click", () => {
    const message = previewMessages[Math.floor(Math.random() * previewMessages.length)];
    const frame = document.getElementById("videoFrame");
    frame.innerHTML = `<div class="play-icon">▶</div><p class="muted">${message}</p>`;
  });
}

function init() {
  renderCampaigns();
  setStats();
  toggleChipSelection("durationPills");
  toggleChipSelection("resolutionPills");
  toggleChipSelection("formatChips");
  toggleSelectablePills();
  handleSearch();
  handleNewCampaign();
  bindFormatChips();
  bindGeneratePreview();
}

window.addEventListener("DOMContentLoaded", init);
