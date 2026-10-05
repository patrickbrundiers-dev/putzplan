/* Putzplan card – cleaning schedule for Home Assistant.
 * Usage:  type: custom:putzplan-card
 * Options: title (string), show_title (bool), rooms (list, order + filter),
 *          columns (number, default: auto)
 */
const PUTZPLAN_CARD_VERSION = "1.0.0";

const PUTZPLAN_TEXT = {
  de: {
    title: "Putzplan",
    every: (n) => (n === 1 ? "Jeden Tag" : n % 7 === 0 && n <= 28 ? (n === 7 ? "Jede Woche" : `Alle ${n / 7} Wochen`) : `Alle ${n} Tage`),
    as_needed: "Bei Bedarf",
    last_unknown: "Zuletzt unbekannt",
    last_today: "Zuletzt heute",
    last_yesterday: "Zuletzt gestern",
    last_ago: (n) => `Zuletzt vor ${n} Tagen`,
    done: "ERLEDIGT",
    overdue: "ÜBERFÄLLIG",
    soon: "BALD",
    mark_today: "Heute erledigt",
    mark_yesterday: "Gestern",
    undo: "Rückgängig",
    empty: "Keine Putzplan-Aufgaben gefunden. Ist die Integration eingerichtet?",
    overdue_count: (n) => `${n} überfällig`,
    all_good: "Alles im grünen Bereich",
  },
  en: {
    title: "Cleaning plan",
    every: (n) => (n === 1 ? "Every day" : n % 7 === 0 && n <= 28 ? (n === 7 ? "Every week" : `Every ${n / 7} weeks`) : `Every ${n} days`),
    as_needed: "As needed",
    last_unknown: "Last done unknown",
    last_today: "Last done today",
    last_yesterday: "Last done yesterday",
    last_ago: (n) => `Last done ${n} days ago`,
    done: "DONE",
    overdue: "OVERDUE",
    soon: "SOON",
    mark_today: "Done today",
    mark_yesterday: "Yesterday",
    undo: "Undo",
    empty: "No Putzplan tasks found. Is the integration set up?",
    overdue_count: (n) => `${n} overdue`,
    all_good: "All good",
  },
};

const putzplanEsc = (v) =>
  String(v ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

class PutzplanCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._expanded = null;
    this._signature = "";
    this._config = null;
    this._hass = null;
  }

  setConfig(config) {
    this._config = { show_title: true, ...config };
    this._signature = "";
    this._build();
    this._update();
  }

  set hass(hass) {
    this._hass = hass;
    this._update();
  }

  getCardSize() {
    return 8;
  }

  static getStubConfig() {
    return {};
  }

  get _t() {
    const lang = (this._hass?.locale?.language || this._hass?.language || "en").slice(0, 2);
    return PUTZPLAN_TEXT[lang] || PUTZPLAN_TEXT.en;
  }

  _build() {
    this.shadowRoot.innerHTML = `
      <style>
        :host { display: block; }
        ha-card { padding: 4px 0 8px; overflow: hidden; }
        .head { display: flex; align-items: center; justify-content: space-between;
                padding: 12px 16px 4px; gap: 8px; }
        .head h1 { margin: 0; font-size: 22px; font-weight: 500; color: var(--primary-text-color); }
        .pill { font-size: 12px; font-weight: 600; padding: 3px 10px; border-radius: 12px;
                background: rgba(67,160,71,.22); color: #66bb6a; white-space: nowrap; }
        .pill.bad { background: rgba(244,81,30,.25); color: #ff7043; }
        .grid { display: grid; gap: 8px; padding: 8px; grid-template-columns: repeat(var(--cols, 1), minmax(0, 1fr)); }
        .room { background: var(--secondary-background-color, rgba(127,127,127,.08));
                border-radius: 10px; padding: 6px 0 6px; }
        .room h2 { margin: 0; padding: 10px 16px 6px; font-size: 18px; font-weight: 500;
                   color: var(--primary-text-color); }
        .row { display: flex; align-items: center; gap: 14px; padding: 9px 16px; cursor: pointer;
               -webkit-tap-highlight-color: transparent; }
        .row:hover { background: rgba(127,127,127,.12); }
        .row ha-icon { --mdc-icon-size: 24px; flex: none; color: var(--primary-text-color); }
        .txt { flex: 1; min-width: 0; }
        .name { font-size: 15px; color: var(--primary-text-color); line-height: 1.25; }
        .sub { font-size: 13px; color: var(--secondary-text-color); line-height: 1.3;
               white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .badge { flex: none; font-size: 11px; font-weight: 700; letter-spacing: .3px;
                 padding: 2px 6px; border-radius: 4px; }
        .row.done { background: rgba(46,125,50,.35); }
        .row.done ha-icon { color: #4caf50; }
        .row.done .badge { background: rgba(76,175,80,.25); color: #66ff7a; }
        .row.overdue { background: rgba(216,67,21,.35); }
        .row.overdue ha-icon { color: #ff6e40; }
        .row.overdue .badge { background: rgba(255,112,67,.25); color: #ff8a65; }
        .row.soon { background: rgba(255,193,7,.16); }
        .row.soon ha-icon { color: #ffc107; }
        .row.soon .badge { background: rgba(255,193,7,.2); color: #ffd54f; }
        .actions { display: flex; flex-wrap: wrap; gap: 8px; padding: 2px 16px 10px 54px; }
        .actions button { font: inherit; font-size: 13px; cursor: pointer; border: 0;
                          padding: 7px 12px; border-radius: 16px;
                          background: var(--primary-color); color: var(--text-primary-color, #fff); }
        .actions button.sec { background: rgba(127,127,127,.25); color: var(--primary-text-color); }
        .empty { padding: 20px 16px; color: var(--secondary-text-color); }
      </style>
      <ha-card>
        <div class="head" id="head"></div>
        <div id="body"></div>
      </ha-card>`;
    this.shadowRoot.getElementById("body").addEventListener("click", (ev) => this._onClick(ev));
  }

  _tasks() {
    const states = this._hass?.states || {};
    const out = [];
    for (const [entityId, st] of Object.entries(states)) {
      if (!entityId.startsWith("sensor.") || st.attributes?.putzplan_task !== true) continue;
      out.push({ entityId, status: st.state, attr: st.attributes });
    }
    return out;
  }

  _update() {
    if (!this._hass || !this._config) return;
    const tasks = this._tasks();
    const lang = this._t === PUTZPLAN_TEXT.de ? "de" : "en";
    const signature = JSON.stringify([lang, this._expanded, this._config, tasks.map((t) => [t.entityId, t.status, t.attr])]);
    if (signature === this._signature) return;
    this._signature = signature;
    this._render(tasks);
  }

  _groupByRoom(tasks) {
    const rooms = new Map();
    for (const t of tasks) {
      const room = t.attr.room || "–";
      if (!rooms.has(room)) rooms.set(room, []);
      rooms.get(room).push(t);
    }
    const rank = (t) => (t.status === "overdue" ? 0 : t.status === "due_soon" ? 1 : 2);
    for (const list of rooms.values()) {
      list.sort((a, b) => rank(a) - rank(b) ||
        (rank(a) === 0 ? (b.attr.days_overdue || 0) - (a.attr.days_overdue || 0) : 0) ||
        String(a.attr.task_name).localeCompare(String(b.attr.task_name)));
    }
    let names = [...rooms.keys()];
    const wanted = this._config.rooms;
    if (Array.isArray(wanted) && wanted.length) {
      names = wanted.filter((r) => rooms.has(r));
    } else {
      names.sort((a, b) => a.localeCompare(b));
    }
    return names.map((name) => [name, rooms.get(name)]);
  }

  _subtitle(t) {
    const tx = this._t;
    const a = t.attr;
    const every = a.interval_days ? tx.every(a.interval_days) : tx.as_needed;
    let last;
    if (a.days_since_done === null || a.days_since_done === undefined) last = tx.last_unknown;
    else if (a.days_since_done === 0) last = tx.last_today;
    else if (a.days_since_done === 1) last = tx.last_yesterday;
    else last = tx.last_ago(a.days_since_done);
    return `${every} • ${last}`;
  }

  _render(tasks) {
    const tx = this._t;
    const head = this.shadowRoot.getElementById("head");
    const body = this.shadowRoot.getElementById("body");
    const overdue = tasks.filter((t) => t.status === "overdue").length;

    head.style.display = this._config.show_title === false ? "none" : "";
    head.innerHTML = `<h1>${putzplanEsc(this._config.title || tx.title)}</h1>` +
      (tasks.length ? `<span class="pill ${overdue ? "bad" : ""}">${putzplanEsc(overdue ? tx.overdue_count(overdue) : tx.all_good)}</span>` : "");

    if (!tasks.length) {
      body.innerHTML = `<div class="empty">${putzplanEsc(tx.empty)}</div>`;
      return;
    }

    const groups = this._groupByRoom(tasks);
    const cols = this._config.columns;
    const grid = `<div class="grid" style="--cols:${Number(cols) > 0 ? Number(cols) : 1}">` +
      groups.map(([room, list]) => `
        <div class="room">
          <h2>${putzplanEsc(room)}</h2>
          ${list.map((t) => this._rowHtml(t)).join("")}
        </div>`).join("") + `</div>`;
    body.innerHTML = grid;
  }

  _rowHtml(t) {
    const tx = this._t;
    const a = t.attr;
    let cls = "";
    let badge = "";
    if (a.done_today) { cls = "done"; badge = tx.done; }
    else if (t.status === "overdue") { cls = "overdue"; badge = tx.overdue; }
    else if (t.status === "due_soon") { cls = "soon"; badge = tx.soon; }

    const open = this._expanded === t.entityId;
    const actions = open ? `
      <div class="actions">
        <button data-act="done" data-id="${putzplanEsc(t.entityId)}">${putzplanEsc(tx.mark_today)}</button>
        <button class="sec" data-act="yesterday" data-id="${putzplanEsc(t.entityId)}">${putzplanEsc(tx.mark_yesterday)}</button>
        ${a.last_done ? `<button class="sec" data-act="undo" data-id="${putzplanEsc(t.entityId)}">${putzplanEsc(tx.undo)}</button>` : ""}
      </div>` : "";

    return `
      <div class="row ${cls}" data-toggle="${putzplanEsc(t.entityId)}">
        <ha-icon icon="${putzplanEsc(t.attr.icon || "mdi:broom")}"></ha-icon>
        <div class="txt">
          <div class="name">${putzplanEsc(a.task_name)}</div>
          <div class="sub">${putzplanEsc(this._subtitle(t))}</div>
        </div>
        ${badge ? `<span class="badge">${putzplanEsc(badge)}</span>` : ""}
      </div>${actions}`;
  }

  _localDate(offsetDays) {
    const d = new Date();
    d.setDate(d.getDate() + offsetDays);
    const p = (n) => String(n).padStart(2, "0");
    return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
  }

  _onClick(ev) {
    const btn = ev.target.closest("button[data-act]");
    if (btn) {
      const entity_id = btn.dataset.id;
      const act = btn.dataset.act;
      if (act === "done") this._hass.callService("putzplan", "mark_done", { entity_id });
      else if (act === "yesterday") this._hass.callService("putzplan", "mark_done", { entity_id, date: this._localDate(-1) });
      else if (act === "undo") this._hass.callService("putzplan", "undo_done", { entity_id });
      this._expanded = null;
      this._signature = "";
      this._update();
      return;
    }
    const row = ev.target.closest("[data-toggle]");
    if (row) {
      const id = row.dataset.toggle;
      this._expanded = this._expanded === id ? null : id;
      this._signature = "";
      this._update();
    }
  }
}

if (!customElements.get("putzplan-card")) {
  customElements.define("putzplan-card", PutzplanCard);
}
window.customCards = window.customCards || [];
if (!window.customCards.some((c) => c.type === "putzplan-card")) {
  window.customCards.push({
    type: "putzplan-card",
    name: "Putzplan",
    description: "Cleaning schedule grouped by room with overdue / done highlighting.",
    preview: false,
  });
}
console.info(`%c PUTZPLAN-CARD %c v${PUTZPLAN_CARD_VERSION} `, "background:#43a047;color:#fff;border-radius:3px 0 0 3px", "background:#333;color:#fff;border-radius:0 3px 3px 0");
