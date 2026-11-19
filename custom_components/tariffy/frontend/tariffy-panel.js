/* Tariffy panel.
 *
 * Overview of all contracts, fed by the integration's websocket API
 * (tariffy/subscribe); administrators can also maintain the contracts. Plain web
 * component, no build step, system font.
 *
 * Security: text that comes from the user (contract names, providers, tariffs)
 * is only ever written with textContent / text nodes, never as HTML.
 */

/* The texts, icons and styles are in their own files next to this one. They are loaded with the version of this
 * file in the URL (?v=...): the static path is cached for a long time, so a browser must never combine new code
 * with old texts or styles after an update. */
const VERSION = new URL(import.meta.url).search;
let I18N;
let ICONS;
let STYLE;
/* No top-level await: the element must be defined the moment this file has run. Home Assistant may create the
 * element and hand it `hass` before it is defined (the properties then shadow the setters), and a module that is
 * still waiting for its parts defines it too late. The parts arrive a moment later and the panel draws itself then. */
const PARTS = Promise.all([
  import(`./tariffy-i18n.js${VERSION}`),
  import(`./tariffy-icons.js${VERSION}`),
  import(`./tariffy-style.js${VERSION}`),
]).then(([i18n, icons, style]) => {
  ({ I18N } = i18n);
  ({ ICONS } = icons);
  ({ STYLE } = style);
});

const SVG_NS = "http://www.w3.org/2000/svg";
const TABS = ["overview", "costs", "contracts", "history", "backup"];
// contracts that are billed by consumption; everything else (internet, mobile, ...) is a flat rate
// column widths shared by the cost tables, so that their columns line up
const GRID = ["24%", "15.2%", "15.2%", "15.2%", "15.2%", "15.2%"];
const INTERVAL_MONTHS = { monthly: 1, quarterly: 3, halfyearly: 6, yearly: 12 };
const METERED = new Set(["electricity", "electricity_ht_nt", "gas", "water"]);
const TAB_KEY = "tariffy-panel-tab";

/* ---------- DOM helpers (text only, never HTML) ---------- */

function h(tag, props, ...children) {
  const el = document.createElement(tag);
  for (const [key, value] of Object.entries(props || {})) {
    if (value === null || value === undefined || value === false) continue;
    if (key === "class") el.className = value;
    else if (key === "text") el.textContent = value;
    else if (key.startsWith("on")) el.addEventListener(key.slice(2), value);
    else el.setAttribute(key, value);
  }
  for (const child of children.flat(Infinity)) {
    if (child === null || child === undefined || child === false) continue;
    el.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
  }
  return el;
}

function svg(tag, attrs, ...children) {
  const el = document.createElementNS(SVG_NS, tag);
  for (const [key, value] of Object.entries(attrs || {})) el.setAttribute(key, value);
  for (const child of children.flat()) if (child) el.appendChild(child);
  return el;
}

function icon(sparte) {
  const parts = ICONS[sparte] || ICONS.other;
  return svg(
    "svg", { viewBox: "0 0 24 24", "aria-hidden": "true" },
    parts.map(([tag, attrs]) => svg(tag, attrs))
  );
}

const FLOWS = {
  // the integration's "Configure" dialog (next contract) and its "Reconfigure" dialog (the contract itself)
  next: { api: "config/config_entries/options/flow", body: (c) => ({ handler: c.entry_id }), category: "options" },
  edit: { api: "config/config_entries/flow", body: (c) => ({ handler: "tariffy", entry_id: c.entry_id }), category: "config" },
  // the integration's "Add entry" dialog
  create: { api: "config/config_entries/flow", body: () => ({ handler: "tariffy" }), category: "config" },
};

const CHART_COLORS = ["#4e79a7", "#f28e2b", "#59a14f", "#e15759", "#76b7b2", "#b07aa1", "#edc948", "#9c755f"];

const isNum = (v) => typeof v === "number" && Number.isFinite(v);

/* ---------- the panel ---------- */

class TariffyPanel extends HTMLElement {
  constructor() {
    super();
    this._hass = null;
    this._unsub = null;
    this._contracts = null; // null = loading
    this._error = null;
    this._narrow = false;
    this._tab = this._loadTab();
    this._open = new Set();
    this._compact = false;
    this._confirming = null;
    this._busy = null;
    this._actionError = null;
    this._bk = { deleted: null, loading: false, plan: null, backup: null, file: null, message: null, error: null, busy: false, asking: null };
    this.attachShadow({ mode: "open" });
    // values set before the element was defined (Home Assistant creates it first) sit on the object itself and
    // hide the setters: take them back through the setters
    for (const prop of ["hass", "narrow", "panel"]) {
      if (Object.prototype.hasOwnProperty.call(this, prop)) {
        const value = this[prop];
        delete this[prop];
        this[prop] = value;
      }
    }
    PARTS.then(() => { if (this._hass) this._render(); }, (err) => {
      this.shadowRoot.replaceChildren(Object.assign(document.createElement("pre"), {
        textContent: `Tariffy: ${(err && err.message) || err}`, style: "color:#f87171;padding:16px",
      }));
    });
  }

  set hass(hass) {
    const first = !this._hass;
    const languageChanged = this._hass && this._hass.language !== hass.language;
    this._hass = hass;
    this._applyTheme();
    if (first) {
      this._subscribe();
      this._render();
    } else if (languageChanged) {
      this._render();
    }
  }

  // the light or the dark colours: whatever Home Assistant shows (its own light/dark/auto setting), else the system's
  _applyTheme() {
    const ha = this._hass && this._hass.themes && this._hass.themes.darkMode;
    const dark = typeof ha === "boolean" ? ha
      : !(window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches);
    this.classList.toggle("light", !dark);
  }

  set narrow(value) {
    this._narrow = Boolean(value);
    if (this._hass) this._render();
  }

  set panel(value) {
    this._panel = value;
  }

  connectedCallback() {
    if (this._hass && !this._unsub) this._subscribe();
    if (typeof ResizeObserver === "function" && !this._observer) {
      this._observer = new ResizeObserver((entries) => {
        const width = entries[entries.length - 1].contentRect.width;
        const compact = width > 0 && width <= 760;
        if (compact !== this._compact) {
          this._compact = compact;
          if (this._hass) this._render();
        }
      });
    }
    if (this._observer) this._observer.observe(this);
  }

  disconnectedCallback() {
    if (this._observer) this._observer.disconnect();
    this._closeFlow();
    if (this._unsub) {
      this._unsub();
      this._unsub = null;
    }
  }

  async _subscribe() {
    try {
      this._unsub = await this._hass.connection.subscribeMessage(
        (event) => {
          this._contracts = Array.isArray(event.contracts) ? event.contracts : [];
          this._error = null;
          this._render();
        },
        { type: "tariffy/subscribe" }
      );
    } catch (err) {
      this._error = String((err && err.message) || err);
      this._render();
    }
  }

  _loadTab() {
    try {
      const tab = window.localStorage.getItem(TAB_KEY);
      return TABS.includes(tab) ? tab : "overview";
    } catch (_err) {
      return "overview";
    }
  }

  _saveTab(tab) {
    try {
      window.localStorage.setItem(TAB_KEY, tab);
    } catch (_err) { /* private mode */ }
  }

  /* ----- language, numbers, dates ----- */

  get _lang() {
    const code = String((this._hass && this._hass.language) || "en").toLowerCase();
    return code.startsWith("de") ? "de" : "en";
  }

  _t(key, vars) {
    let text = I18N[this._lang][key] ?? I18N.en[key] ?? key;
    for (const [name, value] of Object.entries(vars || {})) text = text.replace(`{${name}}`, value);
    return text;
  }

  // a text that depends on the contract: a streaming subscription has a price, not an instalment (key + "_streaming")
  _tc(key, c, vars) {
    const alt = `${key}_streaming`;
    return c && c.sparte === "streaming" && (I18N[this._lang][alt] || I18N.en[alt]) ? this._t(alt, vars) : this._t(key, vars);
  }

  get _locale() {
    return (this._hass && this._hass.locale && this._hass.locale.language) ||
      (this._hass && this._hass.language) || "en";
  }

  _money(value, currency, { sign = false, digits = 0 } = {}) {
    if (!isNum(value)) return "–";
    let text;
    try {
      text = new Intl.NumberFormat(this._locale, {
        style: "currency", currency: currency || "EUR",
        minimumFractionDigits: digits, maximumFractionDigits: digits,
      }).format(Math.abs(value));
    } catch (_err) {
      text = `${Math.abs(value).toFixed(digits)} ${currency || ""}`;
    }
    if (value < 0) return `−${text}`;
    return sign && value > 0 ? `+${text}` : text;
  }

  _num(value, digits = 0) {
    if (!isNum(value)) return "–";
    return new Intl.NumberFormat(this._locale, {
      minimumFractionDigits: digits, maximumFractionDigits: digits,
    }).format(value);
  }

  _price(value, currency, unit) {
    if (!isNum(value)) return "–";
    return `${this._money(value, currency, { digits: 4 })} / ${unit}`;
  }

  /* A negative recommended instalment means the credit already covers the costs
   * until the end of the contract: show 0 instead of a negative instalment. */
  _instalment(value, currency) {
    return isNum(value) ? this._money(Math.max(0, value), currency, { digits: 2 }) : "–";
  }

  /* What the recommended instalment means for the current one: raise it, lower it, none needed, or fine as it is. */
  _advice(c) {
    const rec = c.abschlag_anpassung_empfohlen;
    if (!isNum(rec)) return null;
    if (rec < 0) return this._t("adviceNone");
    const v = this._money(rec, c.currency, { digits: 2 });
    if (!isNum(c.abschlag) || Math.abs(rec - c.abschlag) < 0.5) return this._t("adviceOk");
    return this._t(rec > c.abschlag ? "adviceRaise" : "adviceLower", { v });
  }

  _covered(value) {
    return isNum(value) && value < 0;
  }

  _parse(iso) {
    if (typeof iso !== "string") return null;
    const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso);
    return m ? new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3])) : null;
  }

  _date(iso) {
    const d = this._parse(iso);
    return d
      ? new Intl.DateTimeFormat(this._locale, { day: "2-digit", month: "2-digit", year: "numeric" }).format(d)
      : "–";
  }

  _isoLocal(d) {
    const two = (n) => String(n).padStart(2, "0");
    return `${d.getFullYear()}-${two(d.getMonth() + 1)}-${two(d.getDate())}`;
  }

  _today() {
    const n = new Date();
    return new Date(n.getFullYear(), n.getMonth(), n.getDate());
  }

  _days(iso) {
    const d = this._parse(iso);
    return d ? Math.round((d - this._today()) / 86400000) : null;
  }

  _insuranceType(key) {
    const labels = (I18N[this._lang] && I18N[this._lang].versicherungsart) || I18N.en.versicherungsart;
    return labels[key] || key;
  }

  _unit(contract) {
    if (contract.verbrauch_einheit) return contract.verbrauch_einheit;
    return contract.sparte === "gas" || contract.sparte === "water" ? "m³" : "kWh";
  }

  _priceUnit(contract) {
    return contract.sparte === "water" ? this._unit(contract) : "kWh";
  }

  /* ----- derived values per contract ----- */

  _derive(c) {
    const begin = this._parse(c.beginn);
    const end = this._parse(c.ende);
    let elapsed = null;
    if (begin && end && end > begin) {
      elapsed = Math.min(1, Math.max(0, (this._today() - begin) / (end - begin)));
    }
    const paid = isNum(c.kosten_bisher) && isNum(c.guthaben_bisher) ? c.kosten_bisher + c.guthaben_bisher : null;
    const hasMetering = isNum(c.prognose_real);
    // consumption already measured (also on the first day, before there is a forecast)
    const measured = isNum(c.kosten_bisher) || isNum(c.verbrauch_bisher);
    // the state (credit / balance due / warning) always comes last, so it sits at the far right
    // of every card; further badges (cancel now, switch on ...) stand to its left
    const chips = [];
    if (c.archivierbar) chips.push({ text: this._t("expired"), tone: "muted" });
    if (c.erinnerung_aktiv) chips.push({ text: this._t("cancelDue"), tone: "orange" });
    if (c.wechsel) chips.push({ text: this._t("switchOn", { d: this._date(c.wechsel) }), tone: "blue" });
    if (c.abschlag_warnung_aktiv) chips.push({ text: this._t("warning"), tone: "red" });
    else if (hasMetering) {
      chips.push(c.prognose_real >= 0
        ? { text: this._t("credit"), tone: "green" }
        : { text: this._t("balanceDue"), tone: "red" });
    }
    return { elapsed, paid, hasMetering, measured, chips };
  }

  /* ----- rendering ----- */

  _render() {
    if (!STYLE) return; // the texts and styles are still loading: PARTS draws the panel when they are here
    const root = this.shadowRoot;
    root.replaceChildren(h("style", { text: STYLE }));
    const wrap = h("div", { class: "wrap" });
    wrap.appendChild(this._top());

    if (this._error) {
      wrap.appendChild(h("div", { class: "state" }, h("h2", { text: this._t("error" ) }), h("div", { text: this._error })));
    } else if (this._contracts === null) {
      wrap.appendChild(h("div", { class: "state", text: this._t("loading") }));
    } else if (this._tab === "backup" && this._isAdmin) {
      wrap.appendChild(this._backup());
    } else if (this._contracts.length === 0) {
      wrap.appendChild(this._empty());
    } else if (this._tab === "history") {
      wrap.appendChild(this._history());
    } else if (this._live.length === 0 && this._loans.length === 0) {
      wrap.appendChild(h("div", { class: "state", text: this._t("allArchived") }));
    } else if (this._tab === "costs") {
      wrap.appendChild(this._costs());
    } else if (this._tab === "contracts") {
      wrap.appendChild(this._contractList());
    } else {
      if (this._live.length) wrap.appendChild(this._summary());
      const group = (key, list, extra) => (list.length ? h("section", { class: "group" },
        h("h3", { class: "group-title" }, h("span", { text: this._t(key) }), h("span", { class: "count", text: String(list.length) })),
        h("div", { class: `grid ${extra}` }, list.map((c) => this._card(c)))) : null);
      // a group is null when there is no contract of that kind: skip it (appendChild(null) throws
      // and leaves the whole panel empty for anyone who has only metered or only flat-rate contracts)
      for (const section of [
        group("groupMetered", this._live.filter((c) => METERED.has(c.sparte)), "metered"),
        group("groupFlat", this._live.filter((c) => !METERED.has(c.sparte) && c.sparte !== "leasing"), "flat"),
        group("groupLoans", this._financing, "flat"),
      ]) {
        if (section) wrap.appendChild(section);
      }
    }
    root.appendChild(wrap);
    if (this._dlgEl) root.appendChild(this._dlgEl);
  }

  _top() {
    const menu = this._narrow && customElements.get("ha-menu-button")
      ? Object.assign(document.createElement("ha-menu-button"), { hass: this._hass, narrow: this._narrow })
      : null;
    const tabs = h(
      "div", { class: "tabs", role: "tablist" },
      TABS.filter((tab) => tab !== "backup" || this._isAdmin).map((tab) => h("button", {
        class: "tab", role: "tab", "aria-selected": String(this._tab === tab), text: this._t(tab),
        onclick: () => { this._tab = tab; this._saveTab(tab); this._render(); },
      }))
    );
    return h(
      "div", { class: "top" },
      menu,
      h("div", { class: "brand" }, "Tariffy"),
      tabs,
      h("div", { class: "spacer" })
    );
  }

  _empty() {
    return h(
      "div", { class: "state" },
      h("h2", { text: this._t("emptyTitle") }),
      h("p", { text: this._t("emptyText") }),
      h("a", { href: "/config/integrations/dashboard/add?domain=tariffy", text: this._t("emptyLink") })
    );
  }

  /* the group "Loans / financing" of the overview and the list: the loans (kept apart from the totals) and the
     leases, which stand there too but count in the totals like any flat-rate contract */
  get _financing() {
    return [...this._loans, ...this._live.filter((c) => c.sparte === "leasing")];
  }

  /* ----- loans / financing (kept apart from the contracts and their totals) ----- */
  get _loans() {
    return (this._contracts || []).filter((c) => c.sparte === "loan" && !c.archiviert);
  }

  /* the badge icon: the own icon of the contract (mdi:...) when HA can draw it, else the one of the category */
  _icon(c) {
    const own = typeof c.icon === "string" && /^[a-z0-9_-]+:[a-z0-9_-]+$/i.test(c.icon) ? c.icon : null;
    if (own && customElements.get("ha-icon")) {
      return Object.assign(document.createElement("ha-icon"), { icon: own, className: "own-icon" });
    }
    return icon(c.sparte);
  }

  _loanSub(c) {
    const iv = this._t("interval")[c.zahlweise] || this._t("interval").monthly;
    const rates = [
      isNum(c.kredit_rate) ? `${this._money(c.kredit_rate, c.currency, { digits: 2 })} ${iv}` : null,
      isNum(c.kredit_sollzins) ? `${this._num(c.kredit_sollzins, 2)} %` : null,
      isNum(c.kredit_effektivzins) ? this._t("loanEffective", { v: this._num(c.kredit_effektivzins, 2) }) : null,
    ].filter(Boolean);
    return rates.join(" · ") || null;
  }

  _loanNote(c) {
    if (c.kredit_rate_passt !== false || !isNum(c.kredit_rate_abweichung)) return null;
    return this._t("loanMismatch", {
      p: this._num(Math.abs(c.kredit_rate_abweichung), 1),
      r: this._money(c.kredit_rate_berechnet, c.currency, { digits: 2 }),
    });
  }

  _loanCard(c) {
    const d = this._derive(c);
    const money = (v) => this._money(v, c.currency, { digits: 2 });
    const next = isNum(c.kredit_naechste_betrag);
    const tiles = [
      this._tile(this._t("loanPaid"), money(c.kredit_gezahlt),
        isNum(c.kredit_zinsen_bisher) ? this._t("loanInterestOf", { v: money(c.kredit_zinsen_bisher) }) : null),
      this._tile(this._t("loanRemainingSum"), money(c.kredit_restsumme),
        isNum(c.kredit_zinsen_gesamt) ? this._t("loanInterestTotalOf", { v: money(c.kredit_zinsen_gesamt) }) : null),
      next ? this._tile(this._t("loanNext"), money(c.kredit_naechste_betrag),
        c.kredit_naechste_zahlung ? this._date(c.kredit_naechste_zahlung) : null) : null,
    ];
    const repaid = isNum(c.kredit_tilgung_prozent) ? c.kredit_tilgung_prozent : 0;
    const bar = h("div", { class: "bars" }, h("div", { class: "bar" },
      h("span", { text: this._t("loanRepaid") }), h("b", { text: `${this._num(repaid, 0)} %` }),
      h("span", { class: "tr" }, h("span", { class: "fl", style: `width:${Math.max(2, repaid).toFixed(1)}%;background:var(--green)` }))));
    const foot = [];
    if (isNum(c.restlaufzeit)) {
      foot.push(h("span", {}, `${this._t("remaining")} `, h("b", { text: this._t("daysLeft", { n: c.restlaufzeit }) }),
        c.ende ? ` · ${this._t("until", { d: this._date(c.ende) })}` : ""));
    }
    if (isNum(c.kredit_zahlungen_gesamt)) {
      foot.push(h("span", {}, `${this._t("loanPayments")} `, h("b", { text: `${c.kredit_zahlungen_geleistet} / ${c.kredit_zahlungen_gesamt}` })));
    }
    if (next) { // how the next rate is made up
      foot.push(h("span", {}, `${this._t("loanNext")} `, h("b", { text: this._t("loanSplit", { z: money(c.kredit_zins_anteil), t: money(c.kredit_tilgung_anteil) }) })));
    }
    const notes = [];
    if (this._loanNote(c)) notes.push(h("div", { class: "callout orange", text: this._loanNote(c) }));
    if (c.archivierbar) notes.push(h("div", { class: "callout", text: this._t("noteExpired") }));
    if (c.erinnerung_aktiv) notes.push(h("div", { class: "callout orange", text: this._t("noteCancel", { d: this._date(c.ende) }) }));
    if (!isNum(c.kredit_restschuld)) notes.push(h("div", { class: "callout", text: this._t("loanIncomplete") }));
    const hero = h("div", { class: "hero" },
      h("div", {},
        h("div", { class: "label", text: this._t("loanDebt") }),
        h("div", { class: "big", text: isNum(c.kredit_restschuld) ? money(c.kredit_restschuld) : "–" }),
        this._loanSub(c) ? h("div", { class: "note", text: this._loanSub(c) }) : null));
    const body = [hero, h("div", { class: "tiles" }, tiles.filter(Boolean)), bar,
      foot.length ? h("div", { class: "foot" }, foot) : null,
      notes.length ? h("div", { class: "notes" }, notes) : null];
    if (this._compact) {
      const card = h("details", { class: "card compact tone-none".replace(" tone-none", ""), "data-id": c.entry_id },
        h("summary", {},
          h("div", { class: `badge ${c.sparte}` }, this._icon(c)),
          this._who(c),
          h("div", { class: "end", text: isNum(c.kredit_restschuld) ? this._money(c.kredit_restschuld, c.currency) : "–" }),
          h("span", { class: "caret", "aria-hidden": "true" }, icon("chevron")),
          this._chips(d.chips)),
        h("div", { class: "body" }, body));
      if (this._open.has(c.entry_id)) card.setAttribute("open", "");
      card.addEventListener("toggle", () => {
        if (card.open) this._open.add(c.entry_id);
        else this._open.delete(c.entry_id);
      });
      return card;
    }
    return h("section", { class: "card flat", "data-id": c.entry_id },
      h("div", { class: "head" }, h("div", { class: `badge ${c.sparte}` }, this._icon(c)), this._who(c), this._chips(d.chips)),
      body.map((part) => part || h("div", { class: "slot" })));
  }

  /* the "loan" block of the contract details */
  _kreditSection(c) {
    if (c.sparte !== "loan") return null;
    const money = (v) => (isNum(v) ? this._money(v, c.currency, { digits: 2 }) : null);
    const pct = (v) => (isNum(v) ? `${this._num(v, 2)} %` : null);
    const row = (label, value) => (value === null || value === undefined ? null
      : h("div", { class: "row" }, h("span", { text: label }), h("span", { text: value })));
    const iv = this._t("interval")[c.zahlweise] || this._t("interval").monthly;
    const rows = [
      row(this._t("loanAmount"), money(c.kredit_summe)),
      row(this._t("loanNominal"), pct(c.kredit_sollzins)),
      row(this._t("loanEffectiveRow"), pct(c.kredit_effektivzins)),
      row(this._t("loanTerm"), isNum(c.laufzeit_monate) ? this._t("months", { n: c.laufzeit_monate }) : null),
      row(this._t("loanRatePaid"), isNum(c.kredit_rate) ? `${money(c.kredit_rate)} ${iv}` : null),
      row(this._t("loanRateCalc"), c.kredit_rate_passt === false ? money(c.kredit_rate_berechnet) : null),
      row(this._t("loanFinal"), isNum(c.kredit_schlussrate) && c.kredit_schlussrate > 0 ? money(c.kredit_schlussrate) : null),
      row(this._t("firstPayment"), c.kredit_erste_zahlung ? this._date(c.kredit_erste_zahlung) : null),
      row(this._t("loanPayments"), isNum(c.kredit_zahlungen_gesamt) ? `${c.kredit_zahlungen_geleistet} / ${c.kredit_zahlungen_gesamt}` : null),
      row(this._t("loanDebt"), money(c.kredit_restschuld)),
      row(this._t("loanPaid"), money(c.kredit_gezahlt)),
      row(this._t("loanInterestPaid"), money(c.kredit_zinsen_bisher)),
      row(this._t("loanPrincipalPaid"), money(c.kredit_tilgung_bisher)),
      row(this._t("loanRemainingSum"), money(c.kredit_restsumme)),
      row(this._t("loanInterestTotal"), money(c.kredit_zinsen_gesamt)),
      row(this._t("loanTotalCost"), money(c.kredit_gesamtkosten)),
      row(this._t("nextPayment"), c.kredit_naechste_zahlung ? `${this._date(c.kredit_naechste_zahlung)} · ${this._t("loanSplit", { z: money(c.kredit_zins_anteil), t: money(c.kredit_tilgung_anteil) })}` : null),
    ].filter(Boolean);
    return rows.length ? h("div", { class: "sec" }, h("h4", { text: this._t("secLoan") }), rows,
      this._loanNote(c) ? h("div", { class: "hint", text: this._loanNote(c) }) : null) : null;
  }

  /* the "leasing" block of the contract details: kilometres against the allowance */
  _leasingSection(c) {
    if (c.sparte !== "leasing") return null;
    const km = (v) => (isNum(v) ? `${this._num(v, 0)} km` : null);
    const sgn = (v) => (isNum(v) ? `${v > 0 ? "+" : ""}${this._num(v, 0)} km` : null);
    const money = (v) => (isNum(v) ? this._money(v, c.currency, { digits: 2 }) : null);
    const row = (label, value) => (value === null || value === undefined ? null
      : h("div", { class: "row" }, h("span", { text: label }), h("span", { text: value })));
    let note = null;
    if (!isNum(c.leasing_km_gefahren)) note = this._t("leasingNoOdo");
    else if (!isNum(c.leasing_km_hochgerechnet)) note = this._t("leasingEarly");
    else if (c.leasing_mehr_km > 0) note = this._t("leasingOver", { k: this._num(c.leasing_km_abweichung_ende, 0) });
    else if (c.leasing_minder_km > 0) note = this._t("leasingUnder", { k: this._num(-c.leasing_km_abweichung_ende, 0) });
    else note = this._t("leasingFine");
    const rows = [
      row(this._t("leasingOdo"), km(c.leasing_km_stand)),
      row(this._t("leasingDriven"), km(c.leasing_km_gefahren)),
      row(this._t("leasingAllowed"), km(c.leasing_km_erlaubt)),
      row(this._t("leasingTarget"), km(c.leasing_km_soll)),
      row(this._t("leasingDiff"), sgn(c.leasing_km_abweichung)),
      row(this._t("leasingLeft"), km(c.leasing_km_rest)),
      row(this._t("leasingPerDay"), isNum(c.leasing_km_rest_je_tag) ? `${this._num(c.leasing_km_rest_je_tag, 1)} km` : null),
      row(this._t("leasingAvg"), isNum(c.leasing_km_je_tag) ? `${this._num(c.leasing_km_je_tag, 1)} km` : null),
      row(this._t("leasingForecast"), km(c.leasing_km_hochgerechnet)),
      row(this._t("leasingEndDiff"), sgn(c.leasing_km_abweichung_ende)),
      row(this._t("leasingToleranceUp"), km(c.km_toleranz_oben)),
      row(this._t("leasingToleranceDown"), km(c.km_toleranz_unten)),
      row(this._t("leasingExtra"), c.leasing_mehr_km > 0 ? km(c.leasing_mehr_km) : null),
      row(this._t("leasingShort"), c.leasing_minder_km > 0 ? km(c.leasing_minder_km) : null),
      row(this._t("leasingPriceExtra"), money(c.preis_mehrkm)),
      row(this._t("leasingPriceShort"), money(c.preis_minderkm)),
      row(this._t("leasingCostExtra"), c.leasing_nachzahlung > 0 ? money(c.leasing_nachzahlung) : null),
      row(this._t("leasingCostCredit"), c.leasing_gutschrift > 0 ? money(c.leasing_gutschrift) : null),
      row(this._t("leasingCostBalance"), isNum(c.leasing_km_kosten) ? money(c.leasing_km_kosten) : null),
    ].filter(Boolean);
    return h("div", { class: "sec" }, h("h4", { text: this._t("secLeasing") }), rows,
      note ? h("div", { class: "hint", text: note }) : null);
  }

  _loanTable(loans) {
    if (!loans.length) return null;
    const money = (v, c) => this._money(v, c.currency, { digits: 2 });
    const cell = (label, value) => h("td", { "data-label": label, class: value === "–" ? "empty" : null, text: value });
    const rows = loans.map((c) => h("tr", {},
      h("td", {}, c.title, h("span", { class: "t2", text: c.anbieter || this._t("sparte").loan })),
      cell(this._t("loanPaid"), money(c.kredit_gezahlt, c)),
      cell(this._t("loanDebt"), money(c.kredit_restschuld, c)),
      cell(this._t("loanRemainingSum"), money(c.kredit_restsumme, c)),
      cell(this._t("colInstalment"), isNum(c.kredit_rate) ? money(c.kredit_rate, c) : "–"),
      cell(this._t("loanInterestTotal"), money(c.kredit_zinsen_gesamt, c))));
    return h("section", { class: "group" },
      h("h3", { class: "group-title" }, h("span", { text: this._t("groupLoans") }), h("span", { class: "count", text: String(loans.length) })),
      h("table", {},
        h("colgroup", {}, GRID.map((width) => h("col", { style: `width:${width}` }))),
        h("thead", {}, h("tr", {}, [this._t("colContract"), this._t("loanPaid"), this._t("loanDebt"), this._t("loanRemainingSum"),
          this._t("colInstalment"), this._t("loanInterestTotal")].map((label) => h("th", { text: label })))),
        h("tbody", {}, rows)),
      h("div", { class: "hint", text: this._t("loansHint") }));
  }

  /* Contracts that are not archived (loans are kept apart): the overview, the costs and the list only show these. */
  get _live() {
    return (this._contracts || []).filter((c) => !c.archiviert && c.sparte !== "loan");
  }

  _summary() {
    const contracts = this._live;
    const currency = contracts[0].currency || "EUR";
    const metered = contracts.filter((c) => METERED.has(c.sparte));
    const flat = contracts.filter((c) => !METERED.has(c.sparte));
    const sum = (list, fn) => list.reduce((s, c) => s + (fn(c) || 0), 0);
    const money = (v, o = {}) => this._money(v, currency, o);
    const tone = (value) => (value < 0 ? "red-t" : value > 0 ? "green-t" : "");

    // instalments: per month, split by kind of contract, and what that makes per year
    const monthlyMetered = sum(metered, (c) => c.abschlag);
    const monthlyFlat = sum(flat, (c) => c.abschlag);
    const monthly = monthlyMetered + monthlyFlat;

    // costs so far: measured for metered contracts, instalments due for flat-rate ones
    const costs = sum(contracts, (c) => this._costSoFar(c));
    const due = sum(metered, (c) => (isNum(c.kosten_bisher) && isNum(c.guthaben_bisher) ? c.kosten_bisher + c.guthaben_bisher : 0))
      + sum(flat, (c) => c.abschlag_bisher_gezahlt);
    const withBalance = metered.filter((c) => isNum(c.guthaben_bisher));
    const balance = sum(withBalance, (c) => c.guthaben_bisher);

    // forecast at contract end, worst first
    const withMetering = contracts.filter((c) => isNum(c.prognose_real));
    const forecast = sum(withMetering, (c) => c.prognose_real);
    const worstFirst = [...withMetering].sort((a, b) => a.prognose_real - b.prognose_real).slice(0, 4);

    // the next dates: cancellation deadline, switch, contract end; one entry per contract and date
    const candidates = [];
    for (const c of contracts) {
      const endDays = this._days(c.ende);
      if (c.erinnerung_aktiv && endDays !== null && endDays >= 0) {
        candidates.push({ days: endDays, rank: 0, key: `${c.entry_id}${c.ende}`, text: `${this._t("cancelDue")} · ${c.title}`, date: c.ende });
      }
      const switchDays = this._days(c.wechsel);
      if (switchDays !== null && switchDays >= 0) {
        candidates.push({ days: switchDays, rank: 1, key: `${c.entry_id}${c.wechsel}`, text: this._t("switchOn", { d: this._date(c.wechsel) }) + ` · ${c.title}`, date: c.wechsel });
      }
      if (endDays !== null && endDays >= 0) {
        candidates.push({ days: endDays, rank: 2, key: `${c.entry_id}${c.ende}`, text: `${this._t("contractEnd")} · ${c.title}`, date: c.ende });
      }
    }
    candidates.sort((a, b) => a.days - b.days || a.rank - b.rank);
    const seen = new Set();
    const dates = candidates.filter((x) => (seen.has(x.key) ? false : seen.add(x.key))).slice(0, 3);
    const rel = (days) => (days === 0 ? this._t("today") : days === 1 ? this._t("tomorrow") : this._t("inDays", { n: days }));

    const row = (name, value, cls) => h("div", { class: "mrow" },
      h("span", { class: "n" }, name), h("span", { class: `v ${cls || ""}`, text: value }));
    const segment = (value, color) => (value > 0 ? h("span", { style: `width:${(value / monthly * 100).toFixed(1)}%;background:${color}` }) : null);
    const legend = (color, label, value) => (value > 0 ? h("span", {}, h("i", { style: `background:${color}` }), `${label} `, h("b", { text: money(value, { digits: 2 }) })) : null);

    return h(
      "div", { class: "summary" },
      h("div", { class: "sum" },
        h("div", { class: "label", text: this._t("monthlyTotal") }),
        h("div", { class: "value", text: money(monthly, { digits: 2 }) }),
        h("div", { class: "sub", text: this._t("perYear", { v: money(monthly * 12) }) }),
        monthly > 0 ? h("div", { class: "split" }, segment(monthlyMetered, "var(--blue)"), segment(monthlyFlat, "var(--c-flat)")) : null,
        monthly > 0 ? h("div", { class: "legend" },
          legend("var(--blue)", this._t("shortMetered"), monthlyMetered), legend("var(--c-flat)", this._t("shortFlat"), monthlyFlat)) : null),
      h("div", { class: "sum" },
        h("div", { class: "label", text: this._t("colCost") }),
        h("div", { class: "value", text: money(costs, { digits: 2 }) }),
        h("div", { class: "sub", text: this._t("dueSoFar", { v: money(due) }) }),
        withBalance.length ? h("div", { class: "mini" }, row(this._t("saldoShort"), money(balance, { sign: true, digits: 2 }), tone(balance))) : null),
      h("div", { class: "sum" },
        h("div", { class: "label", text: this._t("forecastTotal") }),
        h("div", { class: `value ${withMetering.length ? tone(forecast) : "muted-t"}`,
          text: withMetering.length ? money(forecast, { sign: true }) : "–" }),
        h("div", { class: "sub", text: this._t("forecastSub", { n: withMetering.length, m: contracts.length }) }),
        worstFirst.length ? h("div", { class: "mini" }, worstFirst.map((c) => row(c.title, money(c.prognose_real, { sign: true }), tone(c.prognose_real)))) : null),
      h("div", { class: "sum" },
        h("div", { class: "label", text: this._t("nextDates") }),
        h("div", { class: "value", text: dates.length ? this._date(dates[0].date) : "–" }),
        h("div", { class: "sub", text: dates.length ? `${dates[0].text} · ${rel(dates[0].days)}` : this._t("nothingPlanned") }),
        dates.length > 1 ? h("div", { class: "mini" }, dates.slice(1).map((x) => row(
          h("span", {}, h("b", { text: this._date(x.date) }), ` ${x.text}`), rel(x.days)))) : null)
    );
  }


  _chips(chips) {
    return h("div", { class: "chips" }, chips.map((chip) => h("span", { class: `chip ${chip.tone}`, text: chip.text })));
  }

  _who(c) {
    return h(
      "div", { class: "who" },
      h("div", { class: "title", text: c.title }),
      h("div", { class: "meta", text: [c.anbieter, c.tarif].filter(Boolean).join(" · ") })
    );
  }

  /* Cost over all terms of a contract (earlier ones from the history plus the running one): value and
   * "since 01.06.2024 · 3 terms". Only for contracts that have a history; the sum is a lower bound when a
   * term has no cost. */
  _total(c) {
    if (!((c.historie || []).length || (c.einmalposten || []).length) || !isNum(c.kosten_gesamt)) return null;
    const value = this._money(c.kosten_gesamt, c.currency, { digits: 2 });
    const n = c.laufzeiten_anzahl;
    const since = [c.seit ? this._t("totalSince", { d: this._date(c.seit) }) : null,
      isNum(n) ? this._t(n === 1 ? "termsOne" : "termsMany", { n }) : null].filter(Boolean).join(" · ");
    return { value: c.kosten_gesamt_vollstaendig === false ? this._t("atLeast", { v: value }) : value, since };
  }

  /* Cost so far: measured for metered contracts, the instalments due until today for flat-rate ones. */
  _costSoFar(c) {
    if (isNum(c.kosten_bisher)) return c.kosten_bisher;
    return !METERED.has(c.sparte) && isNum(c.abschlag_bisher_gezahlt) ? c.abschlag_bisher_gezahlt : null;
  }

  _tile(label, value, sub, tone) {
    return h(
      "div", { class: "tile" },
      h("div", { class: "label", text: label }),
      h("div", { class: `v ${tone || ""}`, text: value }),
      sub ? h("div", { class: "s", text: sub }) : null
    );
  }

  _ring(elapsed) {
    if (elapsed === null) return null; // no start and end date: nothing to draw
    const radius = 38;
    const circumference = 2 * Math.PI * radius;
    const pct = elapsed === null ? null : Math.round(elapsed * 100);
    return h(
      "div", { class: "ring", role: "img", "aria-label": `${this._t("term")}: ${pct === null ? "–" : pct + " %"}` },
      svg("svg", { viewBox: "0 0 96 96" },
        svg("circle", { class: "track", cx: 48, cy: 48, r: radius, fill: "none", "stroke-width": 8 }),
        pct === null ? null : svg("circle", {
          class: "arc", cx: 48, cy: 48, r: radius, fill: "none", "stroke-width": 8,
          "stroke-dasharray": `${(circumference * elapsed).toFixed(2)} ${circumference.toFixed(2)}`,
        })),
      h("div", { class: "center" },
        h("div", { class: "pct", text: pct === null ? "–" : `${pct} %` }),
        h("div", { class: "pcap", text: this._t("term") }))
    );
  }

  _bars(c, d) {
    if (d.paid === null || !isNum(c.kosten_bisher)) return null;
    const max = Math.max(d.paid, c.kosten_bisher, 1);
    const over = c.kosten_bisher > d.paid;
    const bar = (label, value, color) => h(
      "div", { class: "bar" },
      h("span", { text: label }),
      h("b", { text: this._money(value, c.currency) }),
      h("span", { class: "tr" }, h("span", { class: "fl", style: `width:${Math.max(2, (value / max) * 100).toFixed(1)}%;background:${color}` }))
    );
    return h("div", { class: "bars" },
      bar(this._t("paid"), d.paid, "var(--blue)"),
      bar(this._t("cost"), c.kosten_bisher, over ? "var(--red)" : "var(--green)"));
  }

  _card(c) {
    if (c.sparte === "loan") return this._loanCard(c);
    const d = this._derive(c);
    const unit = this._unit(c);
    const alert = c.abschlag_warnung_aktiv;
    const flat = !METERED.has(c.sparte); // no consumption, often no end date
    // the colour that tints the top of the card
    const tone = alert || (d.hasMetering && c.prognose_real < 0) ? "red"
      : c.erinnerung_aktiv ? "orange" : d.hasMetering ? "green" : "none";

    // flat-rate contracts lead with the monthly amount: it exists always, a total over the term only with an end date
    const heroValue = flat ? c.abschlag : d.hasMetering ? c.prognose_real : c.jahreskosten;
    const heroLabel = flat ? this._tc("instalment", c) : d.hasMetering ? this._t("forecastTotal") : this._t("endTotal");
    const heroTone = !flat && d.hasMetering ? (heroValue < 0 ? "red-t" : "green-t") : "";
    const heroSub = flat
      ? [
        c.zahlweise && c.zahlweise !== "monthly" && isNum(c.abschlag_je_zahlung)
          ? `${this._money(c.abschlag_je_zahlung, c.currency, { digits: 2 })} ${this._t("interval")[c.zahlweise] || c.zahlweise}` : null,
        isNum(c.abschlag_jahr) && c.zahlweise !== "yearly" ? this._t("perYearShort", { v: this._money(c.abschlag_jahr, c.currency) }) : null,
        c.ende && isNum(c.jahreskosten) ? this._t("overTerm", { v: this._money(c.jahreskosten, c.currency) }) : null,
      ].filter(Boolean).join(" · ") || null
      : isNum(c.abschlag)
      ? `${this._tc("instalment", c)}: ${this._money(c.abschlag, c.currency, { digits: 2 })}` +
        (isNum(c.abschlag_anpassung_empfohlen)
          ? ` · ${this._advice(c)}`
          : "")
      : null;

    // the balance today and the forecast can point in different directions: say why
    let hint = null;
    if (!flat && d.measured && isNum(c.guthaben_bisher) && isNum(c.prognose_real) && Math.abs(c.guthaben_bisher) >= 0.5) {
      const v = this._money(Math.abs(c.guthaben_bisher), c.currency, { digits: 2 });
      if (c.guthaben_bisher < 0 && c.prognose_real >= 0) hint = this._t("hintCatchUp", { v });
      else if (c.guthaben_bisher > 0 && c.prognose_real < 0) hint = this._t("hintUsedUp", { v });
    }

    // three figures at most; the remaining term goes into the footer line
    const tiles = flat ? [
      isNum(this._costSoFar(c)) ? this._tile(this._t("costSoFar"), this._money(this._costSoFar(c), c.currency, { digits: 2 })) : null,
      this._total(c) ? this._tile(this._t("totalCost"), this._total(c).value, this._total(c).since) : null,
      c.ende ? this._tile(this._t("contractEnd"), this._date(c.ende)) : null,
    ] : d.measured
      ? [
        this._tile(this._t("costSoFar"), this._money(c.kosten_bisher, c.currency, { digits: 2 })),
        isNum(c.guthaben_bisher)
          ? this._tile(this._t("saldoShort"), this._money(c.guthaben_bisher, c.currency, { sign: true, digits: 2 }), null,
            c.guthaben_bisher < 0 ? "red-t" : "green-t")
          : null,
        this._tile(this._t("consumption"), `${this._num(c.verbrauch_bisher, 0)} ${unit}`,
          isNum(c.verbrauch_hochgerechnet) ? this._t("projected", { v: `${this._num(c.verbrauch_hochgerechnet, 0)} ${unit}` }) : null),
      ]
      : [
        this._tile(this._tc("instalment", c), this._money(c.abschlag, c.currency, { digits: 2 })),
        c.ende ? this._tile(this._t("contractEnd"), this._date(c.ende)) : null,
      ];
    const foot = [];
    if (isNum(c.restlaufzeit)) {
      foot.push(h("span", {}, `${this._t("remaining")} `, h("b", { text: this._t("daysLeft", { n: c.restlaufzeit }) }),
        c.ende ? ` · ${this._t("until", { d: this._date(c.ende) })}` : ""));
    } else if (flat) {
      foot.push(h("span", { text: this._t("noEnd") }));
    }
    if (!flat && this._total(c)) { // the flat-rate cards have a tile for it
      foot.push(h("span", {}, `${this._t("totalCost")} `, h("b", { text: this._total(c).value }), ` · ${this._total(c).since}`));
    }
    if (flat || !d.measured) {
      foot.push(h("span", {}, `${this._t("reminder")} `, h("b", { text: c.erinnerung_datum ? this._date(c.erinnerung_datum) : this._t("reminderOff") })));
    }

    const notes = [];
    if (c.abschlag_warnung_zu_bestaetigen) {
      const value = this._money(Math.abs(c.prognose_real), c.currency);
      notes.push(h("div", { class: "callout red", text: isNum(c.abschlag_anpassung_empfohlen) && c.abschlag_anpassung_empfohlen > 0
        ? this._t("noteWarning", { v: value, a: this._money(c.abschlag_anpassung_empfohlen, c.currency) })
        : this._t("noteWarningShort", { v: value }) }));
    }
    if (c.archivierbar) {
      notes.push(h("div", { class: "callout", text: this._t("noteExpired") }));
    }
    if (c.erinnerung_aktiv) {
      notes.push(h("div", { class: "callout orange", text: this._t("noteCancel", { d: this._date(c.ende) }) }));
    }
    if (c.sparte === "leasing" && isNum(c.leasing_km_gefahren)) { // kilometres against the allowance
      const km = `${this._num(c.leasing_km_gefahren, 0)} km`;
      const over = isNum(c.leasing_mehr_km) && c.leasing_mehr_km > 0;
      const text = !isNum(c.leasing_km_hochgerechnet) ? this._t("leasingEarly")
        : over ? this._t("leasingOver", { k: this._num(c.leasing_km_abweichung_ende, 0) })
        : c.leasing_minder_km > 0 ? this._t("leasingUnder", { k: this._num(-c.leasing_km_abweichung_ende, 0) })
        : this._t("leasingFine");
      notes.push(h("div", { class: `callout ${over ? "orange" : "blue"}`, text: `${km} · ${text}` }));
    }
    if (c.next && c.next.beginn) {
      const name = [c.next.anbieter, c.next.tarif].filter(Boolean).join(" · ") || "–";
      notes.push(h("div", { class: "callout blue", text: this._t("noteNext", { d: this._date(c.next.beginn), name }) }));
    }

    const hero = h("div", { class: "hero" },
      h("div", {},
        h("div", { class: "label", text: heroLabel }),
        h("div", { class: `big ${heroTone}`, text: this._money(heroValue, c.currency, { sign: !flat && d.hasMetering, digits: flat ? 2 : undefined }) }),
        heroSub ? h("div", { class: "note", text: heroSub }) : null,
        hint ? h("div", { class: "note", text: hint }) : null),
      flat ? null : this._ring(d.elapsed));
    // how far the term has come, for contracts that have both dates
    const termBar = flat && d.elapsed !== null ? h("div", { class: "bars" }, h("div", { class: "bar" },
      h("span", { text: this._t("term") }), h("b", { text: `${Math.round(d.elapsed * 100)} %` }),
      h("span", { class: "tr" }, h("span", { class: "fl", style: `width:${Math.max(2, d.elapsed * 100).toFixed(1)}%;background:var(--blue)` })))) : null;
    const body = [hero, tiles.filter(Boolean).length ? h("div", { class: "tiles" }, tiles.filter(Boolean)) : null, this._bars(c, d) || termBar,
      foot.length ? h("div", { class: "foot" }, foot) : null,
      notes.length ? h("div", { class: "notes" }, notes) : null];

    if (this._compact) {
      const card = h(
        "details", { class: `card compact${alert ? " alert" : ""} tone-${tone}`.replace(" tone-none", ""), "data-id": c.entry_id },
        h("summary", {},
          h("div", { class: `badge ${c.sparte}` }, this._icon(c)),
          this._who(c),
          h("div", { class: `end ${heroTone}`, text: flat
            ? `${this._money(heroValue, c.currency, { digits: 2 })} ${this._t("perMonth")}`
            : this._money(heroValue, c.currency, { sign: d.hasMetering }) }),
          h("span", { class: "caret", "aria-hidden": "true" }, icon("chevron")),
          this._chips(d.chips)),
        h("div", { class: "body" }, body));
      if (this._open.has(c.entry_id)) card.setAttribute("open", "");
      card.addEventListener("toggle", () => {
        if (card.open) this._open.add(c.entry_id);
        else this._open.delete(c.entry_id);
      });
      return card;
    }
    return h(
      "section", { class: `card${flat ? " flat" : ""}${alert ? " alert" : ""} tone-${tone}`.replace(" tone-none", "") },
      h("div", { class: "head" },
        h("div", { class: `badge ${c.sparte}` }, this._icon(c)),
        this._who(c),
        this._chips(d.chips)),
      // always six blocks: cards in one row share their rows (subgrid), so the figures line up across the cards
      body.map((part) => part || h("div", { class: "slot" }))
    );
  }

  get _isAdmin() {
    return Boolean(this._hass && this._hass.user && this._hass.user.is_admin);
  }

  /* Actions are only offered to administrators; the backend checks it again. */
  _actions(c, only = null) {
    if (!this._isAdmin) return null;
    const list = [];
    if (c.abschlag_warnung_zu_bestaetigen) {
      list.push({ key: "confirm_abschlag_warning", label: this._t("actConfirmWarning"), tone: "red", ask: "actAskWarning", yes: "actYesAck" });
    }
    if (c.erinnerung_aktiv) {
      list.push({ key: "confirm_cancellation", label: this._t("actConfirmCancel"), tone: "orange", ask: "actAskCancel", yes: "actYesAck" });
    }
    if (c.archivierbar) {
      list.push({ key: "archive_contract", label: this._t("actArchive"), tone: "orange", ask: "actAskArchive", yes: "actYesArchive" });
    }
    if (c.archiviert) {
      list.push({ key: "restore_contract", label: this._t("actRestore"), tone: "blue", ask: "actAskRestore", yes: "actYesRestore" });
    }
    if (only) list.splice(0, list.length, ...list.filter((a) => only.includes(a.key)));
    if (!list.length) return null;

    const id = c.entry_id;
    const busy = this._busy === id;
    const children = [];
    const pending = this._confirming && this._confirming.id === id
      ? list.find((a) => a.key === this._confirming.key) : null;
    if (pending) {
      children.push(h("div", { class: "ask" },
        h("span", { text: this._t(pending.ask) }),
        h("button", { class: "btn go", type: "button", disabled: busy ? "" : null, text: this._t(pending.yes),
          onclick: () => this._run(c, pending.key) }),
        h("button", { class: "btn", type: "button", text: this._t("actCancel"),
          onclick: () => { this._confirming = null; this._render(); } })));
    } else {
      for (const action of list) {
        children.push(h("button", {
          class: `btn ${action.tone}`, type: "button", disabled: busy ? "" : null, text: action.label,
          onclick: () => {
            if (action.open) { this._openFlow(c, action.open); return; }
            this._confirming = { id, key: action.key };
            this._actionError = null;
            this._render();
          },
        }));
      }
    }
    if (this._actionError && this._actionError.id === id) {
      children.push(h("div", { class: "err", role: "alert", text: this._t("actFailed", { m: this._actionError.message }) }));
    }
    return h("div", { class: "actions" }, children);
  }

  async _run(c, action) {
    this._busy = c.entry_id;
    this._confirming = null;
    this._actionError = null;
    this._render();
    try {
      await this._hass.callWS({ type: "tariffy/action", entry_id: c.entry_id, action });
    } catch (err) {
      this._actionError = { id: c.entry_id, message: String((err && err.message) || err) };
    } finally {
      this._busy = null;
      this._render();
    }
  }

  /* ---------- forms of the integration: next contract and contract data ----------
     Renders the flows of Home Assistant from its REST API (the "Configure" dialog for the
     next contract, the "Reconfigure" dialog for the contract itself), so validation and
     storage stay in the integration. Empty optional fields are left out, exactly as Home
     Assistant's own form does. */

  _errorText(err) {
    return String((err && ((err.body && err.body.message) || err.message || err.error)) || err);
  }

  _fieldSpec(raw, dlg, step) {
    const kind = ["date", "text", "number", "select", "entity", "boolean", "icon"].find((k) => raw.selector && k in raw.selector) || null;
    const sel = kind === "select" ? raw.selector.select : {};
    const suggested = raw.description && raw.description.suggested_value;
    const initial = suggested !== undefined && suggested !== null ? suggested : raw.default;
    const label = dlg.localize(`component.tariffy.${dlg.category}.step.${step}.data.${raw.name}`) ||
      raw.name.replace(/^next_/, "").replace(/_/g, " ");
    const optionLabel = (value, fallback) => (sel.translation_key
      ? dlg.localize(`component.tariffy.selector.${sel.translation_key}.options.${value}`) : "") || fallback;
    return {
      name: raw.name, kind, label, required: Boolean(raw.required),
      min: kind === "number" && isNum(raw.selector.number.min) ? raw.selector.number.min : null,
      domains: kind === "entity" ? [].concat(raw.selector.entity.domain || []) : [],
      custom: Boolean(sel.custom_value),
      options: (sel.options || []).map((o) => {
        const value = typeof o === "string" ? o : o.value;
        return { value, label: optionLabel(value, typeof o === "string" ? o : o.label || o.value) };
      }),
      initial: kind === "boolean" ? Boolean(initial) : (initial === undefined || initial === null ? "" : String(initial)),
    };
  }

  async _flowLocalize(category) {
    try {
      if (typeof this._hass.loadBackendTranslation === "function") {
        await this._hass.loadBackendTranslation("selector", "tariffy"); // labels of the drop-downs
        const localize = await this._hass.loadBackendTranslation(category, "tariffy");
        if (typeof localize === "function") return localize;
      }
    } catch (_err) { /* fall back to the field names */ }
    return typeof this._hass.localize === "function" ? this._hass.localize : () => "";
  }

  _applyForm(dlg, form) {
    if (form.type === "create_entry" || (form.type === "abort" && form.reason === "reconfigure_successful")) {
      dlg.stage = "saved";
      return;
    }
    if (form.type === "abort") {
      dlg.stage = "error";
      dlg.message = this._t("dlgAborted", { m: form.reason || "" });
      return;
    }
    dlg.flowId = form.flow_id;
    dlg.stage = "form";
    if (dlg.step !== form.step_id) { // a new step starts with its own values
      dlg.step = form.step_id;
      dlg.values = {};
      dlg.refocus = true;
    }
    // Home Assistant says whether a step is the last one; without it every step after the first is
    dlg.final = dlg.mode === "next" || (typeof form.last_step === "boolean" ? form.last_step
      : form.step_id !== (dlg.mode === "create" ? "user" : "reconfigure"));
    dlg.fields = (form.data_schema || []).map((f) => this._fieldSpec(f, dlg, form.step_id));
    dlg.unsupported = dlg.fields.some((f) => !f.kind);
    dlg.hint = dlg.localize(`component.tariffy.${dlg.category}.step.${form.step_id}.description`) || "";
    dlg.fieldErrors = {};
    dlg.message = null;
    for (const [name, code] of Object.entries(form.errors || {})) {
      const text = dlg.localize(`component.tariffy.${dlg.category}.error.${code}`) || String(code);
      if (name === "base") dlg.message = text;
      else dlg.fieldErrors[name] = text;
    }
    for (const f of dlg.fields) if (!(f.name in dlg.values)) dlg.values[f.name] = f.initial;
  }

  async _openFlow(c, mode) {
    this._closeFlow();
    const flow = FLOWS[mode];
    const dlg = {
      mode, api: flow.api, category: flow.category, id: c ? c.entry_id : null, name: c ? c.title : "", stage: "loading", flowId: null,
      step: null, final: true, fields: [], values: {}, fieldErrors: {}, message: null, hint: "", unsupported: false,
      asking: null, localize: () => "", refocus: false,
      hasNext: mode === "next" && Boolean(c.next && c.next.beginn),
      reminder: mode === "next" && Boolean(c.erinnerung_aktiv), markDone: true, note: null, info: null, doneKey: "dlgSaved",
    };
    this._dlg = dlg;
    this._renderDialog();
    try {
      const [form, localize] = await Promise.all([
        this._hass.callApi("POST", flow.api, flow.body(c)),
        this._flowLocalize(flow.category),
      ]);
      if (this._dlg !== dlg) {
        if (form && form.flow_id) this._abortFlow(flow.api, form.flow_id);
        return;
      }
      dlg.localize = localize;
      this._applyForm(dlg, form);
    } catch (err) {
      dlg.stage = "error";
      dlg.message = this._t("dlgLoadFailed", { m: this._errorText(err) });
    }
    if (this._dlg === dlg) this._renderDialog();
  }

  _abortFlow(api, flowId) {
    try {
      Promise.resolve(this._hass.callApi("DELETE", `${api}/${flowId}`)).catch(() => {});
    } catch (_err) { /* the flow expires by itself */ }
  }

  _closeFlow() {
    const dlg = this._dlg;
    this._dlg = null;
    if (dlg && dlg.flowId && dlg.stage !== "saved") this._abortFlow(dlg.api, dlg.flowId);
    if (this._dlgEl) {
      this._dlgEl.remove();
      this._dlgEl = null;
    }
  }

  _collectFlow(dlg) {
    const values = {};
    const errors = {};
    for (const f of dlg.fields) {
      if (f.kind === "boolean") {
        values[f.name] = Boolean(dlg.values[f.name]);
        continue;
      }
      const raw = String(dlg.values[f.name] ?? "").trim();
      if (raw === "") {
        if (f.required) errors[f.name] = this._t("dlgRequired");
        continue;
      }
      if (f.kind === "number") {
        const n = Number(raw.replace(",", "."));
        if (!Number.isFinite(n) || (f.min !== null && n < f.min)) errors[f.name] = this._t("dlgInvalidNumber");
        else values[f.name] = n;
      } else {
        values[f.name] = raw;
      }
    }
    return { values, errors };
  }

  async _sendFlow(dlg, values, removed) {
    dlg.stage = "saving";
    dlg.message = null;
    this._renderDialog();
    let result;
    try {
      result = await this._hass.callApi("POST", `${dlg.api}/${dlg.flowId}`, values);
    } catch (err) {
      if (this._dlg !== dlg) return;
      dlg.stage = "form";
      dlg.asking = null;
      dlg.message = this._t("dlgSaveFailed", { m: this._errorText(err) });
      this._renderDialog();
      return;
    }
    if (this._dlg !== dlg) return;
    dlg.asking = null;
    this._applyForm(dlg, result);
    if (dlg.stage !== "saved") {
      this._renderDialog();
      return;
    }
    dlg.doneKey = removed ? "dlgRemoved" : dlg.mode === "create" ? "dlgCreated" : "dlgSaved";
    dlg.note = null;
    this._renderDialog();
    if (!removed && dlg.reminder && dlg.markDone) {
      const done = await this._markCancellationDone(dlg.id);
      if (this._dlg !== dlg) return;
      if (!done) dlg.note = this._t("dlgMarkDoneFailed");
      this._renderDialog();
    }
  }

  /* Saving reloads the contract, so the action may answer "not_found" for a moment. */
  async _markCancellationDone(entryId) {
    for (let attempt = 0; attempt < 12; attempt++) {
      await new Promise((resolve) => setTimeout(resolve, attempt === 0 ? 700 : 600));
      try {
        await this._hass.callWS({ type: "tariffy/action", entry_id: entryId, action: "confirm_cancellation" });
        return true;
      } catch (err) {
        if (err && err.code === "not_available") return true; // nothing left to acknowledge
        if (!err || err.code !== "not_found") return false;
      }
    }
    return false;
  }

  /* Deleting is Home Assistant's own "remove entry"; the open form is closed first. */
  async _deleteContract(dlg) {
    dlg.stage = "saving";
    dlg.message = null;
    this._renderDialog();
    if (dlg.flowId) this._abortFlow(dlg.api, dlg.flowId);
    dlg.flowId = null;
    try {
      await this._hass.callApi("DELETE", `config/config_entries/entry/${dlg.id}`);
    } catch (err) {
      if (this._dlg !== dlg) return;
      dlg.stage = "error";
      dlg.message = this._t("dlgDeleteFailed", { m: this._errorText(err) });
      this._renderDialog();
      return;
    }
    if (this._dlg !== dlg) return;
    dlg.stage = "saved";
    dlg.doneKey = "dlgDeleted";
    dlg.info = this._t("dlgDeleteNote");
    this._renderDialog();
  }

  /* Validates the form; the last step of editing a contract asks once more before it is sent. */
  _submitFlow(confirmed) {
    const dlg = this._dlg;
    if (!dlg || dlg.stage !== "form") return;
    const { values, errors } = this._collectFlow(dlg);
    dlg.fieldErrors = errors;
    if (Object.keys(errors).length) {
      dlg.message = null;
      dlg.asking = null;
      this._renderDialog();
      return;
    }
    if (dlg.mode === "edit" && dlg.final && !confirmed) {
      dlg.asking = "save";
      this._renderDialog();
      return;
    }
    this._sendFlow(dlg, values, false);
  }

  _fieldInput(dlg, f) {
    const forget = (target) => { // an error message is outdated as soon as its field is edited
      if (!dlg.fieldErrors[f.name]) return;
      delete dlg.fieldErrors[f.name];
      const label = target.closest("label");
      if (label) {
        label.classList.remove("bad");
        const note = label.querySelector(".ferr");
        if (note) note.remove();
      }
      target.removeAttribute("aria-invalid");
    };
    const common = {
      id: `f-${f.name}`, name: f.name, "aria-invalid": dlg.fieldErrors[f.name] ? "true" : null,
      oninput: (ev) => { dlg.values[f.name] = ev.target.value; forget(ev.target); },
    };
    if (f.kind === "boolean") {
      return [h("input", { id: common.id, name: f.name, type: "checkbox",
        onchange: (ev) => { dlg.values[f.name] = ev.target.checked; } })];
    }
    if (f.kind === "select" && !f.custom) {
      return [h("select", { ...common, onchange: (ev) => { dlg.values[f.name] = ev.target.value; } },
        f.options.map((o) => h("option", { value: o.value, text: o.label })))];
    }
    if (f.kind === "entity" || f.kind === "select") { // free text with suggestions
      const list = `dl-${f.name}`;
      const ids = f.kind === "select" ? f.options.map((o) => o.value)
        : Object.keys((this._hass && this._hass.states) || {})
          .filter((id) => !f.domains.length || f.domains.includes(id.split(".")[0])).sort();
      return [
        h("input", { ...common, type: "text", list, autocomplete: "off", spellcheck: "false" }),
        h("datalist", { id: list }, ids.map((id) => h("option", { value: id }))),
      ];
    }
    const type = f.kind === "date" ? "date" : "text";
    return [h("input", { ...common, type, inputmode: f.kind === "number" ? "decimal" : null, autocomplete: "off" })];
  }

  _renderDialog() {
    const dlg = this._dlg;
    if (!dlg) return;
    if (dlg.mode === "term") { this._renderTermDialog(); return; }
    if (dlg.mode === "renew") { this._renderRenewDialog(); return; }
    if (dlg.mode === "once") { this._renderOnceDialog(); return; }
    if (dlg.mode === "instal") { this._renderInstalDialog(); return; }
    if (dlg.mode === "aussen") { this._renderAussenDialog(); return; }
    const busy = dlg.stage === "saving";
    const body = [h("h2", { id: "dlg-title", text: this._t({ edit: "dlgTitleEdit", create: "dlgTitleCreate", next: "dlgTitle" }[dlg.mode], { name: dlg.name }) })];
    const buttons = [];
    const ask = (text, yes, tone, onYes) => h("div", { class: "ask" },
      h("span", { text }),
      h("button", { class: `btn ${tone}`, type: "button", disabled: busy ? "" : null, text: yes, onclick: onYes }),
      h("button", { class: "btn", type: "button", text: this._t("actCancel"),
        onclick: () => { dlg.asking = null; this._renderDialog(); } }));

    if (dlg.stage === "loading") {
      body.push(h("p", { class: "hint", text: this._t("dlgLoading") }));
    } else if (dlg.stage === "error") {
      body.push(h("div", { class: "err", role: "alert", text: dlg.message }));
      buttons.push(h("button", { class: "btn", type: "button", text: this._t("dlgClose"), onclick: () => this._closeFlow() }));
    } else if (dlg.stage === "saved") {
      body.push(h("p", { class: "hint", text: this._t(dlg.doneKey) }));
      if (dlg.info) body.push(h("p", { class: "hint", text: dlg.info }));
      if (dlg.note) body.push(h("div", { class: "err", role: "alert", text: dlg.note }));
      buttons.push(h("button", { class: "btn go", type: "button", text: this._t("dlgClose"), onclick: () => this._closeFlow() }));
    } else {
      if (dlg.hint) body.push(h("p", { class: "hint", text: dlg.hint }));
      if (dlg.unsupported) {
        body.push(h("div", { class: "err", role: "alert", text: this._t("dlgUnsupported") }));
      } else {
        body.push(h("div", { class: "fields" }, dlg.fields.map((f) => {
          const error = dlg.fieldErrors[f.name];
          const input = this._fieldInput(dlg, f);
          const text = h("span", { class: "lbl", text: f.label });
          return h("label", { class: `fld${f.kind === "boolean" ? " bool" : ""}${error ? " bad" : ""}`, for: `f-${f.name}` },
            f.kind === "boolean" ? [input, text] : [text, input],
            error ? h("div", { class: "ferr", text: error }) : null);
        })));
      }
      if (dlg.message) body.push(h("div", { class: "err", role: "alert", text: dlg.message }));
      if (dlg.reminder && !dlg.unsupported) {
        body.push(h("label", { class: "check" },
          h("input", { type: "checkbox", checked: dlg.markDone ? "" : null, onchange: (ev) => { dlg.markDone = ev.target.checked; } }),
          h("span", { text: this._t("dlgMarkDone") })));
      }
      if (dlg.asking === "remove") {
        buttons.push(ask(this._t("dlgRemoveAsk"), this._t("dlgRemoveYes"), "red", () => this._sendFlow(dlg, {}, true)));
      } else if (dlg.asking === "delete") {
        const go = h("button", { class: "btn red", type: "button", disabled: "", text: this._t("dlgDeleteYes"),
          onclick: () => this._deleteContract(dlg) });
        buttons.push(h("div", { class: "ask" },
          h("span", { text: this._t("dlgDeleteAsk", { name: dlg.name }) }),
          h("input", { class: "confirm-name", type: "text", autocomplete: "off", spellcheck: "false", placeholder: dlg.name,
            "aria-label": this._t("dlgDeleteAsk", { name: dlg.name }),
            oninput: (ev) => { go.disabled = ev.target.value.trim() !== dlg.name; } }),
          go,
          h("button", { class: "btn", type: "button", text: this._t("actCancel"),
            onclick: () => { dlg.asking = null; this._renderDialog(); } })));
      } else if (dlg.asking === "save") {
        buttons.push(ask(this._t("dlgSaveAsk"), this._t("dlgSaveYes"), "go", () => this._submitFlow(true)));
      } else {
        if (!dlg.unsupported) {
          buttons.push(h("button", { class: "btn go", type: "button", disabled: busy ? "" : null,
            text: this._t(busy ? "dlgSaving" : dlg.final ? "dlgSave" : "dlgContinue"), onclick: () => this._submitFlow(false) }));
        }
        buttons.push(h("button", { class: "btn", type: "button", disabled: busy ? "" : null, text: this._t("actCancel"),
          onclick: () => this._closeFlow() }));
        if (dlg.mode === "edit") {
          buttons.push(h("button", { class: "btn red", type: "button", disabled: busy ? "" : null, text: this._t("dlgDelete"),
            onclick: () => { dlg.asking = "delete"; this._renderDialog(); } }));
        }
        if (dlg.hasNext && !dlg.unsupported) {
          buttons.push(h("button", { class: "btn red", type: "button", disabled: busy ? "" : null, text: this._t("dlgRemove"),
            onclick: () => { dlg.asking = "remove"; this._renderDialog(); } }));
        }
      }
    }
    body.push(h("div", { class: "actions" }, buttons));
    this._mountDialog(dlg, body, busy);
  }

  _mountDialog(dlg, body, busy) {
    const el = this._dlgEl || (this._dlgEl = h("div", { class: "overlay" }));
    el.onkeydown = (ev) => { if (ev.key === "Escape" && !busy) this._closeFlow(); };
    el.replaceChildren(h("div", { class: "dialog", role: "dialog", "aria-modal": "true", "aria-labelledby": "dlg-title" }, body));
    if (!el.isConnected) this.shadowRoot.appendChild(el);

    // the inputs are filled through properties, attributes would not follow later changes
    for (const f of dlg.fields) {
      const input = el.querySelector(`[name="${f.name}"]`);
      if (!input) continue;
      if (f.kind === "boolean") input.checked = Boolean(dlg.values[f.name]);
      else input.value = dlg.values[f.name] ?? "";
    }
    const confirmName = el.querySelector(".confirm-name");
    if (confirmName) confirmName.focus();
    if (dlg.refocus && dlg.stage === "form") {
      dlg.refocus = false;
      const first = el.querySelector("input, select");
      if (first) first.focus();
    }
  }

  /* ----- backup: export, restore from a file, deleted contracts (administrators only) ----- */

  _bkError(err) {
    const code = String((err && (err.code || (err.body && err.body.code))) || "");
    const key = `bkErr_${code}`;
    return I18N[this._lang][key] || I18N.en[key] ? this._t(key) : this._t("bkErr_invalid_backup");
  }

  async _bkLoad() {
    const bk = this._bk;
    bk.loading = true;
    try {
      bk.deleted = (await this._hass.callWS({ type: "tariffy/deleted_list" })).deleted || [];
    } catch (_err) {
      bk.deleted = [];
    }
    bk.loading = false;
    this._render();
  }

  async _bkDownload() {
    const bk = this._bk;
    bk.message = null;
    bk.error = null;
    try {
      const { backup } = await this._hass.callWS({ type: "tariffy/backup_export" });
      const url = URL.createObjectURL(new Blob([JSON.stringify(backup, null, 2)], { type: "application/json" }));
      const link = h("a", { href: url, download: `tariffy-backup-${new Date().toISOString().slice(0, 10)}.json` });
      this.shadowRoot.appendChild(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      bk.message = this._t("bkDownloaded", { n: backup.contracts.length });
    } catch (err) {
      bk.error = this._bkError(err);
    }
    this._render();
  }

  async _bkPick(file) {
    const bk = this._bk;
    Object.assign(bk, { plan: null, backup: null, file: null, message: null, error: null, asking: null });
    if (file && file.size > 1048576) {
      bk.error = this._t("bkErrBig");
    } else if (file) {
      try {
        const backup = JSON.parse(await file.text());
        bk.plan = (await this._hass.callWS({ type: "tariffy/backup_preview", backup })).contracts;
        bk.backup = backup;
        bk.file = file.name;
      } catch (err) {
        bk.error = this._bkError(err);
      }
    }
    this._render();
  }

  async _bkRun(task, done) {
    const bk = this._bk;
    Object.assign(bk, { busy: true, asking: null, message: null, error: null });
    this._render();
    try {
      bk.message = done(await task());
    } catch (err) {
      bk.error = this._bkError(err);
    }
    bk.busy = false;
    await this._bkLoad();
  }

  _bkRestore() {
    const bk = this._bk;
    return this._bkRun(() => this._hass.callWS({ type: "tariffy/backup_restore", backup: bk.backup }), (r) => {
      bk.plan = null;
      bk.backup = null;
      return this._t("bkDone", { c: r.created.length, s: r.skipped.length });
    });
  }

  _bkDiscard(item) {
    return this._bkRun(() => this._hass.callWS({ type: "tariffy/deleted_discard", item_id: item.id }),
      () => this._t("bkDiscarded", { name: item.title }));
  }

  _bkRestoreOne(item) {
    return this._bkRun(() => this._hass.callWS({ type: "tariffy/deleted_restore", item_id: item.id }),
      (r) => this._t("bkRestoredOne", { name: r.title }));
  }

  _backup() {
    const bk = this._bk;
    if (bk.deleted === null && !bk.loading) this._bkLoad();
    const ask = (text, yes, onYes) => h("div", { class: "ask" }, h("span", { text }),
      h("button", { class: "btn go", type: "button", disabled: bk.busy ? "" : null, text: yes, onclick: onYes }),
      h("button", { class: "btn", type: "button", text: this._t("actCancel"), onclick: () => { bk.asking = null; this._render(); } }));
    const section = (title, ...children) => h("section", { class: "group" },
      h("h3", { class: "group-title" }, h("span", { text: this._t(title) })), h("div", { class: "bk" }, children));
    const text = (key) => h("p", { text: this._t(key) });

    const creating = (bk.plan || []).filter((step) => step.action === "create").length;
    const plan = bk.plan ? [
      h("table", {}, h("thead", {}, h("tr", {}, [this._t("colContract"), ""].map((label) => h("th", { text: label })))),
        h("tbody", {}, bk.plan.map((step) => h("tr", {},
          h("td", {}, step.title, h("span", { class: "t2", text: this._t("sparte")[step.sparte] || step.sparte })),
          h("td", { class: step.action === "create" ? "green-t" : "muted-t", text: this._t(step.action === "create" ? "bkPlanCreate" : "bkPlanSkip") }))))),
      creating === 0 ? h("p", { text: this._t("bkNothing") }) : null,
      creating > 0 && bk.asking === "restore"
        ? ask(this._t("bkAskRestore", { n: creating }), this._t("bkYesRestore"), () => this._bkRestore())
        : creating > 0 ? h("div", { class: "actions" }, h("button", { class: "btn go", type: "button", disabled: bk.busy ? "" : null,
          text: this._t("bkRestoreGo", { n: creating }), onclick: () => { bk.asking = "restore"; this._render(); } })) : null,
    ] : [];

    const deleted = (bk.deleted || []).map((item) => h("div", { class: "bk-row" },
      h("div", { class: "who" }, h("div", { class: "title", text: item.title }),
        h("div", { class: "meta", text: `${this._t("sparte")[item.sparte] || item.sparte} · ${this._t("bkDeletedOn", { d: this._date(item.deleted) })}` })),
      bk.asking === item.id
        ? ask(this._t("bkAskOne", { name: item.title }), this._t("bkYesOne"), () => this._bkRestoreOne(item))
        : bk.asking === `discard:${item.id}`
          ? ask(this._t("bkAskDiscard", { name: item.title }), this._t("bkYesDiscard"), () => this._bkDiscard(item))
          : h("div", { class: "actions" },
            h("button", { class: "btn blue", type: "button", disabled: bk.busy ? "" : null, text: this._t("bkRestoreOne"),
              onclick: () => { bk.asking = item.id; this._render(); } }),
            h("button", { class: "btn red", type: "button", disabled: bk.busy ? "" : null, text: this._t("bkDiscard"),
              onclick: () => { bk.asking = `discard:${item.id}`; this._render(); } }))));

    return h("div", {},
      bk.message ? h("p", { class: "bk-msg", role: "status", text: bk.message }) : null,
      bk.error ? h("div", { class: "err", role: "alert", text: bk.error }) : null,
      section("bkTitleExport", text("bkExportText"),
        h("div", { class: "actions" }, h("button", { class: "btn blue", type: "button", disabled: bk.busy ? "" : null,
          text: this._t("bkDownload"), onclick: () => this._bkDownload() }))),
      section("bkTitleRestore", text("bkRestoreText"),
        h("input", { class: "file", type: "file", accept: ".json,application/json", "aria-label": this._t("bkTitleRestore"),
          onchange: (ev) => this._bkPick(ev.target.files && ev.target.files[0]) }),
        plan),
      section("bkTitleDeleted", text("bkDeletedText"),
        deleted.length ? deleted : (bk.deleted === null ? null : h("p", { text: this._t("bkDeletedEmpty") }))));
  }

  /* ----- renew a flat-rate contract: new start, end and amount; the old term goes to the history ----- */

  _isoShift(iso, { days = 0, years = 0 }) {
    const date = this._parse(iso);
    if (!date) return "";
    date.setFullYear(date.getFullYear() + years);
    date.setDate(date.getDate() + days);
    const two = (n) => String(n).padStart(2, "0");
    return `${date.getFullYear()}-${two(date.getMonth() + 1)}-${two(date.getDate())}`;
  }

  /* follow-up financing: the remaining debt becomes the new loan amount */
  _openRenewLoan(c) {
    this._closeFlow();
    const spec = (name, kind, label, extra = {}) => ({
      name, kind, label, required: false, min: null, domains: [], custom: false, options: [], initial: "", ...extra,
    });
    const zahlweise = c.zahlweise && INTERVAL_MONTHS[c.zahlweise] ? c.zahlweise : "monthly";
    const text = (v) => (isNum(v) ? String(v) : "");
    this._dlg = {
      mode: "renew", kredit: true, stage: "form", id: c.entry_id, name: c.title, contract: c, flowId: null, localize: () => "",
      fields: [
        spec("beginn", "date", this._t("tf_beginn"), { required: true }),
        spec("kredit_summe", "number", this._t("lf_summe"), { required: true, min: 0.01 }),
        spec("sollzins", "number", this._t("lf_soll"), { min: 0 }),
        spec("effektivzins", "number", this._t("lf_effektiv"), { min: 0 }),
        spec("laufzeit_monate", "number", this._t("lf_laufzeit"), { required: true, min: 1 }),
        spec("zahlweise", "select", this._t("rf_zahlweise"), { options: Object.keys(INTERVAL_MONTHS).map((k) => ({ value: k, label: this._t("interval")[k] })) }),
        spec("kredit_rate", "number", this._t("lf_rate"), { min: 0 }),
        spec("schlussrate", "number", this._t("lf_schluss"), { min: 0 }),
        spec("erste_zahlung", "date", this._t("rf_erste")),
      ],
      values: {
        beginn: c.ende || "", kredit_summe: text(c.kredit_restschuld), sollzins: text(c.kredit_sollzins),
        effektivzins: text(c.kredit_effektivzins), laufzeit_monate: text(c.laufzeit_monate), zahlweise,
        kredit_rate: "", schlussrate: "", erste_zahlung: "",
      },
      fieldErrors: {}, message: null,
    };
    this._renderRenewDialog();
  }

  _openRenew(c) {
    if (c.sparte === "loan") { this._openRenewLoan(c); return; }
    this._closeFlow();
    const spec = (name, kind, label, extra = {}) => ({
      name, kind, label, required: false, min: null, domains: [], custom: false, options: [], initial: "", ...extra,
    });
    const zahlweise = c.zahlweise && INTERVAL_MONTHS[c.zahlweise] ? c.zahlweise : "monthly";
    const dlg = {
      mode: "renew", stage: "form", id: c.entry_id, name: c.title, contract: c, flowId: null, localize: () => "",
      fields: [
        spec("beginn", "date", this._t("tf_beginn"), { required: true }),
        spec("ende", "date", this._t("tf_ende")),
        spec("zahlweise", "select", this._t("rf_zahlweise"), { options: Object.keys(INTERVAL_MONTHS).map((k) => ({ value: k, label: this._t("interval")[k] })) }),
        spec("abschlag", "number", this._t("rf_abschlag"), { required: true, min: 0.01 }),
        spec("erste_zahlung", "date", this._t("rf_erste")),
      ],
      values: {
        beginn: c.ende ? this._isoShift(c.ende, { days: 1 }) : this._isoLocal(this._today()), ende: c.ende ? this._isoShift(c.ende, { years: 1 }) : "", zahlweise,
        abschlag: String(isNum(c.abschlag_je_zahlung) ? c.abschlag_je_zahlung : (c.abschlag ?? "")),
      },
      fieldErrors: {}, message: null,
    };
    this._dlg = dlg;
    this._renderRenewDialog();
  }

  /* "5 % dearer": what the new amount means compared with the current one */
  _renewChange(dlg) {
    const amount = Number(String(dlg.values.abschlag ?? "").replace(",", "."));
    const months = INTERVAL_MONTHS[dlg.values.zahlweise] || 1;
    const old = dlg.contract.abschlag;
    if (!Number.isFinite(amount) || amount <= 0 || !isNum(old) || old <= 0) return "";
    const monthly = amount / months;
    const percent = ((monthly - old) / old) * 100;
    if (Math.abs(percent) < 0.05) return this._t("renewSame");
    return this._t(percent > 0 ? "renewUp" : "renewDown", {
      p: this._num(Math.abs(percent), 1), n: this._money(monthly, dlg.contract.currency, { digits: 2 }), o: this._money(old, dlg.contract.currency, { digits: 2 }),
    });
  }

  async _saveRenew() {
    const dlg = this._dlg;
    const { values, errors } = this._collectFlow(dlg);
    dlg.fieldErrors = errors;
    dlg.message = null;
    if (Object.keys(errors).length) {
      this._renderRenewDialog();
      return;
    }
    dlg.stage = "saving";
    this._renderRenewDialog();
    try {
      await this._hass.callWS({ type: "tariffy/renew", entry_id: dlg.id, values });
    } catch (err) {
      if (this._dlg !== dlg) return;
      dlg.stage = "form";
      dlg.message = this._termError(err);
      this._renderRenewDialog();
      return;
    }
    if (this._dlg === dlg) this._closeFlow();
    this._render();
  }

  _renderRenewDialog() {
    const dlg = this._dlg;
    if (!dlg) return;
    const busy = dlg.stage === "saving";
    const body = [
      h("h2", { id: "dlg-title", text: this._t(dlg.kredit ? "loanRenewTitle" : "renewTitle") }),
      h("p", { class: "hint", text: dlg.name }),
      h("p", { class: "hint", text: this._t(dlg.kredit ? "loanRenewHint" : "renewHint") }),
      h("div", { class: "fields" }, dlg.fields.map((f) => {
        const error = dlg.fieldErrors[f.name];
        return h("label", { class: `fld${error ? " bad" : ""}`, for: `f-${f.name}` },
          h("span", { class: "lbl", text: f.label }), this._fieldInput(dlg, f),
          f.name === "abschlag" ? h("div", { class: "fnote", "data-note": "change", text: this._renewChange(dlg) }) : null,
          error ? h("div", { class: "ferr", text: error }) : null);
      })),
    ];
    if (dlg.message) body.push(h("div", { class: "err", role: "alert", text: dlg.message }));
    body.push(h("div", { class: "actions" },
      h("button", { class: "btn go", type: "button", disabled: busy ? "" : null, text: this._t(busy ? "dlgSaving" : "renewGo"), onclick: () => this._saveRenew() }),
      h("button", { class: "btn", type: "button", disabled: busy ? "" : null, text: this._t("actCancel"), onclick: () => this._closeFlow() })));
    this._mountDialog(dlg, body, busy);
    const el = this._dlgEl;
    // a finished edit of the amount or the interval updates the note under the amount
    el.onchange = () => {
      const note = el.querySelector('[data-note="change"]');
      if (note) note.textContent = this._renewChange(dlg);
    };
    el.oninput = el.onchange;
    if (!dlg.focused) {
      dlg.focused = true;
      const first = el.querySelector("input, select");
      if (first) first.focus();
    }
  }

  /* ----- one-time items of a contract: bonus (+) or bill (-), administrators only ----- */
  _openOnce(c, index) {
    this._closeFlow();
    const spec = (name, kind, label, extra = {}) => ({
      name, kind, label, required: false, min: null, domains: [], custom: false, options: [], initial: "", ...extra,
    });
    const item = index === null ? {} : (c.einmalposten || [])[index] || {};
    this._dlg = {
      mode: "once", stage: "form", id: c.entry_id, name: c.title, index, flowId: null, localize: () => "", asking: null,
      fields: [
        spec("bezeichnung", "text", this._t("onceName"), { required: true }),
        spec("betrag", "number", this._t("onceAmount"), { required: true }),
        spec("datum", "date", this._t("onceDate")),
      ],
      values: { bezeichnung: item.bezeichnung || "", betrag: isNum(item.betrag) ? String(item.betrag) : "", datum: item.datum || "" },
      fieldErrors: {}, message: null,
    };
    this._renderOnceDialog();
  }

  async _saveOnce() {
    const dlg = this._dlg;
    const { values, errors } = this._collectFlow(dlg);
    dlg.fieldErrors = errors;
    dlg.message = null;
    if (Object.keys(errors).length) { this._renderOnceDialog(); return; }
    await this._callOnce(dlg, { type: "tariffy/einmal_save", entry_id: dlg.id, values, ...(dlg.index === null ? {} : { index: dlg.index }) });
  }

  async _deleteOnce() {
    const dlg = this._dlg;
    await this._callOnce(dlg, { type: "tariffy/einmal_delete", entry_id: dlg.id, index: dlg.index });
  }

  async _callOnce(dlg, message) {
    dlg.stage = "saving";
    this._renderOnceDialog();
    try {
      await this._hass.callWS(message);
    } catch (err) {
      if (this._dlg !== dlg) return;
      dlg.stage = "form";
      dlg.asking = null;
      dlg.message = this._termError(err);
      this._renderOnceDialog();
      return;
    }
    if (this._dlg === dlg) this._closeFlow();
    this._render();
  }

  _renderOnceDialog() {
    const dlg = this._dlg;
    if (!dlg) return;
    const busy = dlg.stage === "saving";
    const body = [
      h("h2", { id: "dlg-title", text: this._t(dlg.index === null ? "onceTitleAdd" : "onceTitleEdit") }),
      h("p", { class: "hint", text: dlg.name }),
      h("p", { class: "hint", text: this._t("onceHint") }),
      h("div", { class: "fields" }, dlg.fields.map((f) => {
        const error = dlg.fieldErrors[f.name];
        return h("label", { class: `fld${error ? " bad" : ""}`, for: `f-${f.name}` },
          h("span", { class: "lbl", text: f.label }), this._fieldInput(dlg, f),
          error ? h("div", { class: "ferr", text: error }) : null);
      })),
    ];
    if (dlg.message) body.push(h("div", { class: "err", role: "alert", text: dlg.message }));
    const buttons = [];
    if (dlg.asking === "delete") {
      buttons.push(h("div", { class: "ask" },
        h("span", { text: this._t("onceDeleteAsk") }),
        h("button", { class: "btn red", type: "button", disabled: busy ? "" : null, text: this._t("onceDeleteYes"), onclick: () => this._deleteOnce() }),
        h("button", { class: "btn", type: "button", text: this._t("actCancel"), onclick: () => { dlg.asking = null; this._renderOnceDialog(); } })));
    } else {
      buttons.push(h("button", { class: "btn go", type: "button", disabled: busy ? "" : null,
        text: this._t(busy ? "dlgSaving" : "dlgSave"), onclick: () => this._saveOnce() }));
      buttons.push(h("button", { class: "btn", type: "button", disabled: busy ? "" : null, text: this._t("actCancel"), onclick: () => this._closeFlow() }));
      if (dlg.index !== null) {
        buttons.push(h("button", { class: "btn red", type: "button", disabled: busy ? "" : null, text: this._t("onceDelete"),
          onclick: () => { dlg.asking = "delete"; this._renderOnceDialog(); } }));
      }
    }
    body.push(h("div", { class: "actions" }, buttons));
    this._mountDialog(dlg, body, busy);
    if (!dlg.focused) {
      dlg.focused = true;
      const first = this._dlgEl.querySelector("input, select");
      if (first) first.focus();
    }
  }

  /* the "one-time items" block of a contract */
  _onceSection(c) {
    const items = c.einmalposten || [];
    if (!items.length && !this._isAdmin) return null;
    if (!items.length && c.sparte === "streaming") return null; // a streaming subscription has none; one that already has items keeps the block
    const rows = items.map((item, index) => h("div", { class: "row once-row" },
      h("span", {}, item.bezeichnung, item.datum ? h("span", { class: "t2", text: this._date(item.datum) }) : null),
      h("span", { class: item.betrag < 0 ? "red-t" : "green-t", text: this._money(item.betrag, c.currency, { sign: true, digits: 2 }) }),
      this._isAdmin ? h("button", {
        class: "icon-btn", type: "button", title: this._t("onceEdit"), "aria-label": this._t("onceEdit"),
        onclick: () => this._openOnce(c, index),
      }, icon("edit")) : null));
    return h("div", { class: "sec" }, h("h4", { text: this._t("secOnce") }), rows,
      items.length > 1 && isNum(c.einmal_summe)
        ? h("div", { class: "row" }, h("span", { text: this._t("onceSum") }),
          h("span", { text: this._money(c.einmal_summe, c.currency, { sign: true, digits: 2 }) })) : null,
      this._isAdmin ? h("div", { class: "once-add" }, h("button", {
        class: "btn", type: "button", onclick: () => this._openOnce(c, null),
      }, icon("plus"), this._t("onceAdd"))) : null);
  }

  /* ----- instalments paid: one amount per payment of the term, administrators only ----- */
  // the payments of a term, one per payment interval (monthly: a field per month, quarterly four a year, half-yearly two,
  // yearly one); a payment that has not come yet is locked. Without an end the payments up to today.
  _payRange(beginn, ende, first, interval) {
    const parse = (iso) => { const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso || ""); return m ? [Number(m[1]), Number(m[2]), Number(m[3])] : null; };
    const start = parse(first) || parse(beginn);
    if (!start) return [];
    const pad = (n) => String(n).padStart(2, "0");
    const now = new Date();
    const todayIso = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
    const end = parse(ende);
    const endIso = end ? `${end[0]}-${pad(end[1])}-${pad(end[2])}` : todayIso;
    const months = [];
    if (interval === 1) { // monthly: the months, from the month of the start
      const here = now.getFullYear() * 12 + now.getMonth();
      const last = end ? end[0] * 12 + end[1] - 1 : here;
      for (let k = parse(beginn || first)[0] * 12 + parse(beginn || first)[1] - 1; k <= last && months.length < 600; k += 1) {
        const y = Math.floor(k / 12);
        const m = k % 12 + 1;
        months.push({ iso: `${y}-${pad(m)}-01`, upto: `${y}-${pad(m)}-31`, future: k > here,
          label: new Intl.DateTimeFormat(this._locale, { month: "long", year: "numeric" }).format(new Date(y, m - 1, 1)) });
      }
      return months;
    }
    for (let n = 0; n < 200; n += 1) {
      const k = start[0] * 12 + start[1] - 1 + n * interval;
      const y = Math.floor(k / 12);
      const m = k % 12 + 1;
      const day = Math.min(start[2], new Date(y, m, 0).getDate());
      const iso = `${y}-${pad(m)}-${pad(day)}`;
      if (iso > endIso) break;
      months.push({ iso, upto: iso, future: iso > todayIso, label: this._date(iso) });
    }
    return months;
  }

  // fills the amounts: the entry that applied at the payment, the current instalment for the ones that have not come yet
  _instalFill(range, entries, current) {
    for (const x of range) {
      const valid = entries.filter((e) => e.ab <= x.upto);
      const value = x.future ? current : entries.length ? (valid.length ? valid[valid.length - 1] : entries[0]).betrag_je_zahlung : current;
      x.betrag = isNum(value) ? String(value) : "";
    }
    return range;
  }

  _instalMonths(c) {
    const interval = INTERVAL_MONTHS[c.zahlweise] || 1;
    return this._instalFill(this._payRange(c.beginn, c.ende, c.erste_zahlung, interval), c.abschlagsverlauf || [],
      isNum(c.abschlag_je_zahlung) ? c.abschlag_je_zahlung : null);
  }

  // the changes to send: a blank amount takes the one before, only the payments where the amount changes; null = the first one is missing
  _instalRows(months) {
    const rows = [];
    let before = null;
    for (const month of months.filter((x) => !x.future)) {
      const text = String(month.betrag || "").trim();
      const value = text === "" ? before : text;
      if (value === null) return null;
      if (before === null || Number(value) !== Number(before) || Number.isNaN(Number(value))) rows.push({ ab: month.iso, betrag: value });
      before = value;
    }
    return rows;
  }

  // the grid of amounts shared by the dialog of a contract and the one of an earlier term
  _instalGrid(months, busy, interval, c) {
    const inputs = [];
    // the payments that have not come yet show the instalment of the last one that has (the current one)
    const syncFuture = () => {
      const began = months.filter((x) => !x.future);
      const now = began.length ? began[began.length - 1].betrag : null;
      months.forEach((x, j) => { if (x.future && now !== null) { x.betrag = now; if (inputs[j]) inputs[j].value = now; } });
    };
    const rows = months.map((month, i) => {
      const input = h("input", { type: "text", inputmode: "decimal", autocomplete: "off", value: month.betrag, "aria-label": `${month.label}: ${this._tc("instalAmount", c)}`,
        disabled: busy || month.future ? "" : null, oninput: (ev) => { month.betrag = ev.target.value.replace(",", "."); },
        // a finished edit also applies to the following payments that still had the old amount
        onchange: (ev) => {
          ev.target.value = month.betrag; // a comma typed as decimal separator is shown as the dot that is stored
          const old = month.before;
          month.before = month.betrag;
          for (let j = i + 1; j < months.length; j += 1) {
            if (months[j].future || months[j].betrag !== old) continue;
            months[j].betrag = month.betrag;
            months[j].before = month.betrag;
            inputs[j].value = month.betrag;
          }
          syncFuture();
        } });
      month.before = month.betrag;
      inputs.push(input);
      return h("label", { class: `instal-row${month.future ? " instal-future" : ""}` }, h("span", { text: month.label }), h("span", { class: "fld" }, input));
    });
    syncFuture();
    return h("div", { class: "instal-grid" },
      h("div", { class: "instal-head" }, h("span", { text: this._t(interval === 1 ? "instalMonth" : "instalPayment") }),
        h("span", { text: interval === 1 ? this._tc("instalAmount", c) : this._t("instalAmountPay") })),
      rows);
  }

  _openInstal(c) {
    this._closeFlow();
    const months = this._instalMonths(c);
    this._dlg = { mode: "instal", stage: "form", id: c.entry_id, name: c.title, flowId: null, localize: () => "", fields: [], values: {},
      months, interval: INTERVAL_MONTHS[c.zahlweise] || 1, sparte: c.sparte, message: null };
    this._renderInstalDialog();
  }

  async _saveInstal() {
    const dlg = this._dlg;
    const rows = this._instalRows(dlg.months);
    if (rows === null) { dlg.message = this._t("instalErr_first"); this._renderInstalDialog(); return; }
    dlg.stage = "saving";
    dlg.message = null;
    this._renderInstalDialog();
    try {
      await this._hass.callWS({ type: "tariffy/abschlag_verlauf_save", entry_id: dlg.id, rows });
    } catch (err) {
      if (this._dlg !== dlg) return;
      const code = String((err && (err.code || (err.body && err.body.code))) || "");
      const key = `instalErr_${code}`;
      dlg.stage = "form";
      dlg.message = I18N[this._lang][key] || I18N.en[key] ? this._t(key) : this._termError(err);
      this._renderInstalDialog();
      return;
    }
    if (this._dlg === dlg) this._closeFlow();
    this._render();
  }

  _renderInstalDialog() {
    const dlg = this._dlg;
    if (!dlg) return;
    const busy = dlg.stage === "saving";
    const body = [
      h("h2", { id: "dlg-title", text: this._tc("instalTitle", dlg) }),
      h("p", { class: "hint", text: dlg.name }),
      h("p", { class: "hint", text: this._tc("instalHint", dlg) }),
      dlg.months.length ? this._instalGrid(dlg.months, busy, dlg.interval, dlg) : h("p", { class: "hint", text: this._t("instalNoStart") }),
    ];
    if (dlg.message) body.push(h("div", { class: "err", role: "alert", text: dlg.message }));
    body.push(h("div", { class: "actions" },
      h("button", { class: "btn go", type: "button", disabled: busy || !dlg.months.some((x) => !x.future) ? "" : null, text: this._t(busy ? "dlgSaving" : "dlgSave"), onclick: () => this._saveInstal() }),
      h("button", { class: "btn", type: "button", disabled: busy ? "" : null, text: this._t("actCancel"), onclick: () => this._closeFlow() })));
    this._mountDialog(dlg, body, busy);
  }

  /* the "instalments paid" block of a contract */
  _instalSection(c) {
    if (c.sparte === "loan" || !isNum(c.abschlag)) return null;
    const items = c.abschlagsverlauf || [];
    if (!items.length && !this._isAdmin) return null;
    // monthly (the usual case) needs no word, another interval is named
    const iv = c.zahlweise && c.zahlweise !== "monthly" ? this._t("interval")[c.zahlweise] || "" : "";
    const rows = items.map((e, i) => h("div", { class: "row once-row" },
      h("span", {}, `${this._t("instalFrom")} ${this._date(e.ab)}`, i === items.length - 1 ? h("span", { class: "t2", text: this._t("instalNow") }) : null),
      h("span", { text: `${this._money(e.betrag_je_zahlung, c.currency, { digits: 2 })}${iv ? ` ${iv}` : ""}` })));
    return h("div", { class: "sec" }, h("h4", { text: this._tc("secInstal", c) }),
      rows.length ? rows : h("div", { class: "hint", text: this._tc("instalNone", c) }),
      this._isAdmin ? h("div", { class: "once-add" }, h("button", { class: "btn", type: "button", onclick: () => this._openInstal(c) },
        icon("edit"), this._tc(items.length ? "instalEdit" : "instalEnter", c))) : null);
  }

  /* ----- outdoor meters of a water contract (garden, pool, ...): not charged wastewater, administrators only ----- */
  _openAussen(c, index) {
    this._closeFlow();
    const spec = (name, kind, label, extra = {}) => ({
      name, kind, label, required: false, min: null, domains: [], custom: false, options: [], initial: "", ...extra,
    });
    const item = index === null ? {} : (c.aussenzaehler || [])[index] || {};
    this._dlg = {
      mode: "aussen", stage: "form", id: c.entry_id, name: c.title, index, flowId: null, localize: () => "", asking: null,
      fields: [
        spec("name", "text", this._t("aussenName"), { required: true }),
        spec("sensor", "entity", this._t("aussenSensor"), { required: true, domains: ["sensor"] }),
        spec("start_wert", "number", this._t("aussenStart"), { min: 0 }),
        spec("preis", "number", this._t("aussenPrice"), { min: 0 }),
      ],
      values: {
        name: item.name || "", sensor: item.sensor || "",
        start_wert: isNum(item.start_wert) ? String(item.start_wert) : "", preis: isNum(item.preis) ? String(item.preis) : "",
      },
      fieldErrors: {}, message: null,
    };
    this._renderAussenDialog();
  }

  async _saveAussen() {
    const dlg = this._dlg;
    const { values, errors } = this._collectFlow(dlg);
    dlg.fieldErrors = errors;
    dlg.message = null;
    if (Object.keys(errors).length) { this._renderAussenDialog(); return; }
    await this._callAussen(dlg, { type: "tariffy/aussen_save", entry_id: dlg.id, values, ...(dlg.index === null ? {} : { index: dlg.index }) });
  }

  async _deleteAussen() {
    const dlg = this._dlg;
    await this._callAussen(dlg, { type: "tariffy/aussen_delete", entry_id: dlg.id, index: dlg.index });
  }

  async _callAussen(dlg, message) {
    dlg.stage = "saving";
    this._renderAussenDialog();
    try {
      await this._hass.callWS(message);
    } catch (err) {
      if (this._dlg !== dlg) return;
      dlg.stage = "form";
      dlg.asking = null;
      const code = String((err && (err.code || (err.body && err.body.code))) || "");
      dlg.message = code === "too_many" ? this._t("aussenTooMany") : this._termError(err);
      this._renderAussenDialog();
      return;
    }
    if (this._dlg === dlg) this._closeFlow();
    this._render();
  }

  _renderAussenDialog() {
    const dlg = this._dlg;
    if (!dlg) return;
    const busy = dlg.stage === "saving";
    const body = [
      h("h2", { id: "dlg-title", text: this._t(dlg.index === null ? "aussenTitleAdd" : "aussenTitleEdit") }),
      h("p", { class: "hint", text: dlg.name }),
      h("p", { class: "hint", text: this._t("aussenHint") }),
      h("div", { class: "fields" }, dlg.fields.map((f) => {
        const error = dlg.fieldErrors[f.name];
        return h("label", { class: `fld${error ? " bad" : ""}`, for: `f-${f.name}` },
          h("span", { class: "lbl", text: f.label }), this._fieldInput(dlg, f),
          error ? h("div", { class: "ferr", text: error }) : null);
      })),
    ];
    if (dlg.message) body.push(h("div", { class: "err", role: "alert", text: dlg.message }));
    const buttons = [];
    if (dlg.asking === "delete") {
      buttons.push(h("div", { class: "ask" },
        h("span", { text: this._t("aussenDeleteAsk") }),
        h("button", { class: "btn red", type: "button", disabled: busy ? "" : null, text: this._t("onceDeleteYes"), onclick: () => this._deleteAussen() }),
        h("button", { class: "btn", type: "button", text: this._t("actCancel"), onclick: () => { dlg.asking = null; this._renderAussenDialog(); } })));
    } else {
      buttons.push(h("button", { class: "btn go", type: "button", disabled: busy ? "" : null,
        text: this._t(busy ? "dlgSaving" : "dlgSave"), onclick: () => this._saveAussen() }));
      buttons.push(h("button", { class: "btn", type: "button", disabled: busy ? "" : null, text: this._t("actCancel"), onclick: () => this._closeFlow() }));
      if (dlg.index !== null) {
        buttons.push(h("button", { class: "btn red", type: "button", disabled: busy ? "" : null, text: this._t("aussenDelete"),
          onclick: () => { dlg.asking = "delete"; this._renderAussenDialog(); } }));
      }
    }
    body.push(h("div", { class: "actions" }, buttons));
    this._mountDialog(dlg, body, busy);
    if (!dlg.focused) {
      dlg.focused = true;
      const first = this._dlgEl.querySelector("input, select");
      if (first) first.focus();
    }
  }

  /* the "outdoor meters" block of a water contract */
  _aussenSection(c) {
    if (c.sparte !== "water") return null;
    const items = c.aussenzaehler || [];
    if (!items.length && !this._isAdmin) return null;
    const unit = this._unit(c);
    const amount = (v) => (isNum(v) ? `${this._num(v, 1)} ${unit}` : "–");
    // name and sensor on top (a long entity id wraps), the figures below, the pencil at the right
    const rows = items.map((item, index) => h("div", { class: "aussen-row" },
      h("div", { class: "an" }, item.name, h("span", { class: "t2", text: item.sensor })),
      h("div", { class: "av", text: isNum(item.verbrauch) ? `${amount(item.verbrauch)}${isNum(item.kosten) ? ` · ${this._money(item.kosten, c.currency, { digits: 2 })}` : ""}` : "–" }),
      this._isAdmin ? h("button", {
        class: "icon-btn", type: "button", title: this._t("aussenEdit"), "aria-label": this._t("aussenEdit"),
        onclick: () => this._openAussen(c, index),
      }, icon("edit")) : null));
    return h("div", { class: "sec aussen-sec" }, h("h4", { text: this._t("secAussen") }),
      rows.length ? h("div", { class: "aussen-list" }, rows) : null,
      this._isAdmin ? h("div", { class: "once-add" }, h("button", {
        class: "btn", type: "button", onclick: () => this._openAussen(c, null),
      }, icon("plus"), this._t("aussenAdd"))) : null);
  }

  /* ----- old contracts: a term entered by hand (administrators only) ----- */

  _openTerm(c, index) {
    this._closeFlow();
    const target = c || this._live[0] || this._contracts[0];
    const term = c && index !== null ? (c.historie || [])[index] : null;
    const AUTO = ["verbrauch", "kosten", "abschlag_gezahlt", "saldo"];
    const spec = (name, kind, extra = {}) => ({
      name, kind, label: this._t(`tf_${name}`), required: false, min: kind === "number" ? 0 : null,
      domains: [], custom: false, options: [], initial: "", ...extra,
    });
    const fields = [
      spec("entry_id", "select", { options: this._contracts.map((x) => ({ value: x.entry_id, label: x.title })) }),
      spec("beginn", "date", { required: true }), spec("ende", "date", { required: true }),
      spec("anbieter", "text"), spec("tarif", "text"),
      spec("arbeitspreis", "number"), spec("grundpreis", "number"), spec("abschlag", "number"),
      spec("verbrauch", "number", { auto: true }), spec("kosten", "number", { auto: true }),
      spec("abschlag_gezahlt", "number", { auto: true }), spec("saldo", "number", { auto: true, min: null }),
    ];
    const values = { entry_id: target.entry_id };
    if (term) {
      // the values the user typed in stay filled in; the ones that were worked out are worked out again
      const own = Array.isArray(term.eigene) ? term.eigene : AUTO;
      for (const f of fields) {
        const stored = term[f.name];
        if (f.name === "entry_id" || stored === undefined || stored === null) continue;
        if (!f.auto || own.includes(f.name)) values[f.name] = String(stored);
      }
    }
    const dlg = {
      mode: "term", stage: "form", id: target.entry_id, name: target.title, index: term ? index : null, fields, values,
      fieldErrors: {}, message: null, asking: null, calc: null, calcSeq: 0, flowId: null, localize: () => "",
      termMonths: [], termOpen: false,
    };
    // the instalments by payment of the term, when it has them: the amounts show again for editing
    const stored = term && Array.isArray(term.abschlag_verlauf) ? term.abschlag_verlauf : [];
    if (stored.length) {
      dlg.termOpen = true;
      this._termRebuild(dlg, stored);
    }
    this._dlg = dlg;
    this._renderTermDialog();
    this._termCalc(dlg);
  }

  // the payments of the term (from its two dates and the payment interval of the contract); amounts already typed stay
  _termRebuild(dlg, stored) {
    const contract = (this._contracts || []).find((x) => x.entry_id === dlg.values.entry_id);
    const interval = (contract && INTERVAL_MONTHS[contract.zahlweise]) || 1;
    const range = this._payRange(dlg.values.beginn, dlg.values.ende, dlg.values.beginn, interval);
    const typed = new Map((dlg.termMonths || []).map((x) => [x.iso, x.betrag]));
    const entries = (stored || []).map((e) => ({ ab: e.ab, betrag_je_zahlung: Math.round(e.betrag * interval * 100) / 100 }));
    dlg.termInterval = interval;
    dlg.termMonths = stored ? this._instalFill(range, entries, null) : range.map((x) => ({ ...x, betrag: typed.get(x.iso) || "" }));
    for (const x of dlg.termMonths) x.future = false; // an earlier term is over
  }

  // the instalments of the term as the changes to send (nothing when no amount was typed); null = the first one is missing
  _termRows(dlg) {
    if (!(dlg.termMonths || []).some((x) => String(x.betrag || "").trim() !== "")) return [];
    return this._instalRows(dlg.termMonths);
  }

  async _termCalc(dlg) {
    const { values } = this._collectFlow(dlg);
    if (!values.beginn || !values.ende) {
      dlg.calc = null;
      this._termPaint(dlg);
      return;
    }
    const seq = ++dlg.calcSeq;
    const { entry_id: _id, ...rest } = values;
    const rows = this._termRows(dlg) || [];
    let calc = null;
    try {
      calc = await this._hass.callWS({ type: "tariffy/history_calc", entry_id: dlg.values.entry_id, values: rest, ...(rows.length ? { rows } : {}) });
    } catch (_err) { /* invalid dates and the like: nothing to show yet */ }
    if (this._dlg !== dlg || seq !== dlg.calcSeq) return;
    dlg.calc = calc;
    this._termPaint(dlg);
  }

  /* Shows the worked-out values as grey placeholders and says where each one comes from. */
  _termPaint(dlg) {
    const el = this._dlgEl;
    if (!el || this._dlg !== dlg) return;
    const calc = dlg.calc;
    const contract = (this._contracts || []).find((c) => c.entry_id === dlg.values.entry_id);
    for (const f of dlg.fields.filter((x) => x.auto)) {
      const typed = String(dlg.values[f.name] ?? "").trim() !== "";
      const computed = calc ? calc.values[f.name] : null;
      const input = el.querySelector(`[name="${f.name}"]`);
      const note = el.querySelector(`[data-note="${f.name}"]`);
      if (input) input.placeholder = isNum(computed) ? this._num(computed, 2) : "";
      let text;
      if (typed) text = this._t("autoOwn");
      else if (f.name === "verbrauch") {
        if (!calc) text = this._t("autoWait");
        else if (isNum(computed)) text = this._t("autoStat", { s: (calc.sensors || []).join(", ") });
        else if (contract && !METERED.has(contract.sparte)) text = this._t("autoFlat");
        else if (!(calc.sensors || []).length) text = this._t("autoNoSensor");
        else text = this._t("autoNoStat");
      } else text = isNum(computed) ? this._t("autoCalc") : this._t("autoWait");
      if (note) note.textContent = text;
    }
  }

  _termError(err) {
    const code = String((err && (err.code || (err.body && err.body.code))) || "");
    const specific = `termErr_${code}`;
    const has = (key) => Boolean(I18N[this._lang][key] || I18N.en[key]);
    const key = has(specific) ? specific : (code.startsWith("invalid_") ? "termErr_invalid" : specific);
    return has(key) ? this._t(key) : this._t("dlgSaveFailed", { m: this._errorText(err) });
  }

  async _saveTerm() {
    const dlg = this._dlg;
    const { values, errors } = this._collectFlow(dlg);
    dlg.fieldErrors = errors;
    dlg.message = null;
    if (Object.keys(errors).length) {
      this._renderTermDialog();
      return;
    }
    const rows = this._termRows(dlg);
    if (rows === null) { dlg.message = this._t("instalErr_first"); this._renderTermDialog(); return; }
    dlg.stage = "saving";
    this._renderTermDialog();
    const { entry_id: _id, ...rest } = values;
    const message = { type: "tariffy/history_save", entry_id: dlg.values.entry_id, values: rest };
    if (rows.length) message.rows = rows;
    if (dlg.index !== null) message.index = dlg.index;
    try {
      await this._hass.callWS(message);
    } catch (err) {
      if (this._dlg !== dlg) return;
      dlg.stage = "form";
      dlg.message = this._termError(err);
      this._renderTermDialog();
      return;
    }
    if (this._dlg === dlg) this._closeFlow();
    this._render();
  }

  async _deleteTerm() {
    const dlg = this._dlg;
    dlg.stage = "saving";
    this._renderTermDialog();
    try {
      await this._hass.callWS({ type: "tariffy/history_delete", entry_id: dlg.values.entry_id, index: dlg.index });
    } catch (err) {
      if (this._dlg !== dlg) return;
      dlg.stage = "form";
      dlg.asking = null;
      dlg.message = this._termError(err);
      this._renderTermDialog();
      return;
    }
    if (this._dlg === dlg) this._closeFlow();
    this._render();
  }

  _termGrid(dlg, busy) {
    return dlg.termMonths.length ? this._instalGrid(dlg.termMonths, busy, dlg.termInterval || 1, (this._contracts || []).find((x) => x.entry_id === dlg.values.entry_id)) : h("p", { class: "hint", text: this._t("termInstalWait") });
  }

  _renderTermDialog() {
    const dlg = this._dlg;
    if (!dlg) return;
    const busy = dlg.stage === "saving";
    const body = [
      h("h2", { id: "dlg-title", text: this._t(dlg.index === null ? "termTitleAdd" : "termTitleEdit") }),
      h("p", { class: "hint", text: this._t("termHint") }),
      h("div", { class: "fields" }, dlg.fields.map((f) => {
        const error = dlg.fieldErrors[f.name];
        return h("label", { class: `fld${error ? " bad" : ""}`, for: `f-${f.name}` },
          h("span", { class: "lbl", text: f.label }), this._fieldInput(dlg, f),
          f.auto ? h("div", { class: "fnote", "data-note": f.name }) : null,
          error ? h("div", { class: "ferr", text: error }) : null);
      })),
      h("details", { class: "term-instal", open: dlg.termOpen ? "" : null, ontoggle: (ev) => { dlg.termOpen = ev.target.open; } },
        h("summary", { text: this._t("termInstal") }),
        h("p", { class: "hint", text: this._t("termInstalHint") }),
        h("div", { class: "term-grid" }, this._termGrid(dlg, busy))),
    ];
    if (dlg.message) body.push(h("div", { class: "err", role: "alert", text: dlg.message }));
    const buttons = [];
    if (dlg.asking === "delete") {
      buttons.push(h("div", { class: "ask" },
        h("span", { text: this._t("termDeleteAsk") }),
        h("button", { class: "btn red", type: "button", disabled: busy ? "" : null, text: this._t("termDeleteYes"), onclick: () => this._deleteTerm() }),
        h("button", { class: "btn", type: "button", text: this._t("actCancel"), onclick: () => { dlg.asking = null; this._renderTermDialog(); } })));
    } else {
      buttons.push(h("button", { class: "btn go", type: "button", disabled: busy ? "" : null,
        text: this._t(busy ? "dlgSaving" : "dlgSave"), onclick: () => this._saveTerm() }));
      buttons.push(h("button", { class: "btn", type: "button", disabled: busy ? "" : null, text: this._t("actCancel"), onclick: () => this._closeFlow() }));
      if (dlg.index !== null) {
        buttons.push(h("button", { class: "btn red", type: "button", disabled: busy ? "" : null, text: this._t("termDelete"),
          onclick: () => { dlg.asking = "delete"; this._renderTermDialog(); } }));
      }
    }
    body.push(h("div", { class: "actions" }, buttons));
    this._mountDialog(dlg, body, busy);
    const el = this._dlgEl;
    // a finished edit of any field (blur, drop-down) works the automatic values out again
    el.onchange = (ev) => {
      const name = ev && ev.target && ev.target.name;
      if (name === "beginn" || name === "ende" || name === "entry_id") {
        if (name === "entry_id") dlg.values.entry_id = ev.target.value;
        this._termRebuild(dlg, null);
        const grid = el.querySelector(".term-grid");
        if (grid) grid.replaceChildren(this._termGrid(dlg, false));
      }
      this._termCalc(dlg);
    };
    if (dlg.index !== null) {
      const select = el.querySelector('[name="entry_id"]');
      if (select) select.disabled = true; // a term stays with its contract
    }
    this._termPaint(dlg);
    if (!dlg.focused) { // keyboard users start in the dialog (Escape closes it)
      dlg.focused = true;
      const first = el.querySelector("select:not(:disabled), input");
      if (first) first.focus();
    }
  }

  _recommendedCell(c) {
    const raw = c.empfohlener_abschlag ?? c.abschlag_anpassung_empfohlen;
    return h("td", {
      "data-label": this._t("colRecommended"), class: isNum(raw) ? "rec" : "rec empty",
    }, this._instalment(raw, c.currency),
    this._covered(raw) ? h("span", { class: "t2", text: this._t("coveredHint") }) : null);
  }

  /* Cost split: a ring with one slice per contract, switchable between what has been paid so far and a year */
  /* the cost of one calendar year: every term (earlier ones and the running one) counts for the days it has in that year */
  _yearTerms(c) {
    const today = new Date().toISOString().slice(0, 10);
    const terms = (c.historie || []).map((t) => ({ from: t.beginn, to: t.ende, cost: isNum(t.kosten) ? t.kosten : t.abschlag_gezahlt }));
    if (!c.archiviert && c.beginn) {
      const end = c.ende && c.ende < today ? c.ende : today; // the running term counts up to today
      terms.push({ from: c.beginn, to: end, cost: this._costSoFar(c) });
    }
    return terms.filter((t) => t.from && t.to && isNum(t.cost) && t.to >= t.from);
  }

  _costYears(contracts) {
    const years = new Set();
    for (const c of contracts) {
      for (const t of this._yearTerms(c)) for (let y = Number(t.from.slice(0, 4)); y <= Number(t.to.slice(0, 4)); y += 1) years.add(y);
    }
    return [...years].sort((a, b) => b - a);
  }

  _yearCost(c, year) {
    const day = (iso) => Date.UTC(Number(iso.slice(0, 4)), Number(iso.slice(5, 7)) - 1, Number(iso.slice(8, 10))) / 86400000;
    const start = Date.UTC(year, 0, 1) / 86400000;
    const end = Date.UTC(year, 11, 31) / 86400000;
    let sum = 0;
    for (const t of this._yearTerms(c)) {
      const from = day(t.from);
      const to = day(t.to);
      const overlap = Math.min(to, end) - Math.max(from, start) + 1;
      if (overlap > 0) sum += t.cost * (overlap / (to - from + 1));
    }
    return sum;
  }

  _costChart(live) {
    const years = this._costYears(this._contracts.filter((c) => c.sparte !== "loan"));
    const year = years.includes(this._costYear) ? this._costYear : null;
    const contracts = year === null ? live : this._contracts.filter((c) => c.sparte !== "loan");
    const basis = this._costBasis || "sofar";
    const value = (c) => {
      if (year !== null) return this._yearCost(c, year);
      const v = basis === "year" ? (isNum(c.abschlag_jahr) ? c.abschlag_jahr : isNum(c.abschlag) ? c.abschlag * 12 : null) : this._costSoFar(c);
      return isNum(v) && v > 0 ? v : 0;
    };
    const currency = contracts[0].currency || "EUR";
    const grouped = this._costGroup !== "contract"; // by category unless "per contract" is chosen
    const perContract = contracts.map((c) => ({ label: c.title, sparte: c.sparte, currency: c.currency, n: 1, v: value(c) }))
      .filter((it) => it.v > 0.005);
    const merged = new Map(); // contracts of one category count together
    for (const it of perContract) {
      const old = merged.get(it.sparte);
      if (old) { old.v += it.v; old.n += 1; } else merged.set(it.sparte, { ...it, label: this._t("sparte")[it.sparte] || it.sparte });
    }
    const items = (grouped ? [...merged.values()] : perContract).sort((a, b) => b.v - a.v)
      .map((it, i) => ({ ...it, color: CHART_COLORS[i % CHART_COLORS.length] }));
    const total = items.reduce((s, it) => s + it.v, 0);
    const toggle = h("div", { class: "seg", role: "group" }, [["sofar", "chartSoFar"], ["year", "chartYear"]].map(([key, label]) => h("button", {
      class: year === null && basis === key ? "on" : "", type: "button", "aria-pressed": String(year === null && basis === key), text: this._t(label),
      onclick: () => { this._costBasis = key; this._costYear = null; this._render(); },
    })));
    // the years with data: the cost of that calendar year (earlier terms count for their days in it)
    const picker = years.length ? h("label", { class: "yr-pick" }, h("span", { text: this._t("chartYearLabel") }),
      h("select", {
        "aria-label": this._t("chartYearLabel"),
        onchange: (ev) => { this._costYear = ev.target.value ? Number(ev.target.value) : null; this._render(); },
      }, [h("option", { value: "", text: this._t("chartYearAll") })].concat(
        years.map((y) => h("option", { value: String(y), text: String(y), selected: y === year ? "" : null }))))) : null;
    const groupToggle = h("div", { class: "seg", role: "group" }, [["sparte", "chartBySparte"], ["contract", "chartByContract"]].map(([key, label]) => h("button", {
      class: (grouped ? "sparte" : "contract") === key ? "on" : "", type: "button", "aria-pressed": String((grouped ? "sparte" : "contract") === key), text: this._t(label),
      onclick: () => { this._costGroup = key; this._render(); },
    })));
    const card = h("section", { class: "chart" },
      h("h3", { class: "group-title" }, h("span", { text: this._t("chartTitle") })),
      h("div", { class: "chart-ctl" }, toggle, picker, groupToggle),
      year !== null ? h("p", { class: "hint", text: this._t("chartYearHint") }) : null);
    if (!total) {
      card.appendChild(h("div", { class: "hint", text: this._t("chartEmpty") }));
      return card;
    }
    const percent = (v) => `${this._num((v / total) * 100, 1)} %`;
    let offset = 0;
    const slices = items.map((it) => {
      const part = (it.v / total) * 100;
      const slice = svg("circle", {
        cx: "21", cy: "21", r: "15.9155", fill: "none", stroke: it.color, "stroke-width": "6",
        "stroke-dasharray": `${Math.max(part - 0.4, 0.01)} ${100 - Math.max(part - 0.4, 0.01)}`, "stroke-dashoffset": String(-offset),
        transform: "rotate(-90 21 21)",
      });
      offset += part;
      return slice;
    });
    const ring = svg("svg", { viewBox: "0 0 42 42", class: "cs-ring", role: "img", "aria-label": this._t("chartTitle") },
      svg("circle", { cx: "21", cy: "21", r: "15.9155", fill: "none", stroke: "rgba(255,255,255,.06)", "stroke-width": "6" }), slices);
    const kinds = [["chartMetered", (c) => METERED.has(c.sparte)], ["chartFlat", (c) => !METERED.has(c.sparte)]]
      .map(([label, test]) => ({ label, v: items.filter((it) => test(it)).reduce((s, it) => s + it.v, 0) })).filter((k) => k.v > 0);
    card.appendChild(h("div", { class: "chart-body" },
      h("div", { class: "cs-ringwrap" }, ring,
        h("div", { class: "cs-mid" }, h("b", { text: this._money(total, currency, { digits: 0 }) }))),
      h("ul", { class: "cs-legend" }, items.map((it) => h("li", {},
        h("span", { class: "cs-dot", style: `background:${it.color}` }),
        h("span", { class: "nm", text: it.n > 1 ? `${it.label} (${it.n})` : it.label }),
        h("span", { class: "val", text: this._money(it.v, it.currency, { digits: 2 }) }),
        h("span", { class: "pct", text: percent(it.v) }))))));
    if (kinds.length > 1) {
      card.appendChild(h("div", { class: "kindbar" },
        h("div", { class: "cs-split" }, kinds.map((k, i) => h("span", { class: `k${i}`, style: `width:${(k.v / total) * 100}%` }))),
        h("div", { class: "kindleg" }, kinds.map((k, i) => h("span", {}, h("span", { class: `cs-dot k${i}` }),
          `${this._t(k.label)} ${percent(k.v)}`)))));
    }
    return card;
  }

  _costs() {
    const contracts = this._live;
    const loans = this._loans;
    const currency = (contracts[0] || loans[0] || {}).currency || "EUR";
    const tone = (v) => (isNum(v) ? (v < 0 ? "red-t" : v > 0 ? "green-t" : "") : "muted-t");
    const cell = (label, value, cls) => h("td", { "data-label": label, class: [cls, value === "–" ? "empty" : ""].filter(Boolean).join(" ") || null, text: value });
    const sum = (list, key) => list.reduce((s, c) => s + (isNum(c[key]) ? c[key] : 0), 0);
    const sumCost = (list) => list.reduce((s, c) => s + (this._costSoFar(c) || 0), 0);
    const money = (v, digits = 2, o = {}) => this._money(v, currency, { digits, ...o });
    const metered = contracts.filter((c) => METERED.has(c.sparte));
    const flat = contracts.filter((c) => !METERED.has(c.sparte));
    const name = (c) => h("td", {}, c.title, h("span", { class: "t2", text: c.anbieter || this._t("sparte")[c.sparte] || c.sparte }));

    // metered contracts: what the consumption cost, the balance against the instalments, the forecast
    const meteredRows = [];
    for (const c of metered) {
      meteredRows.push(h("tr", {},
        name(c),
        cell(this._t("colCost"), this._money(this._costSoFar(c), c.currency, { digits: 2 })),
        cell(this._t("colBalance"), this._money(c.guthaben_bisher, c.currency, { sign: true, digits: 2 }), tone(c.guthaben_bisher)),
        cell(this._t("colForecast"), this._money(c.prognose_real, c.currency, { sign: true }), tone(c.prognose_real)),
        cell(this._t("colInstalment"), this._money(c.abschlag, c.currency, { digits: 2 })),
        this._recommendedCell(c)));
      if (isNum(c.kosten_ht_bisher) || isNum(c.kosten_nt_bisher)) {
        for (const [label, key, vkey] of [["highTariff", "kosten_ht_bisher", "verbrauch_bisher_ht"], ["lowTariff", "kosten_nt_bisher", "verbrauch_bisher_nt"]]) {
          meteredRows.push(h("tr", { class: "sub" },
            h("td", { text: `${this._t(label)} · ${this._num(c[vkey], 0)} ${this._unit(c)}` }),
            cell(this._t("colCost"), this._money(c[key], c.currency, { digits: 2 }))));
        }
      }
    }
    meteredRows.push(h("tr", { class: "total" },
      h("td", { text: this._t("total") }),
      cell(this._t("colCost"), money(sumCost(metered))),
      cell(this._t("colBalance"), money(sum(metered, "guthaben_bisher"), 2, { sign: true }), tone(sum(metered, "guthaben_bisher"))),
      cell(this._t("colForecast"), money(sum(metered, "prognose_real"), 0, { sign: true }), tone(sum(metered, "prognose_real"))),
      cell(this._t("colInstalment"), money(sum(metered, "abschlag"))),
      h("td", { text: "" })));

    // flat-rate contracts: no consumption, so the cost so far is what was due, and the term.
    // Cost so far (2nd column) and instalment (5th column) sit exactly below those of the table above.
    const flatRows = flat.map((c) => h("tr", {},
      name(c),
      cell(this._t("colCost"), this._money(this._costSoFar(c), c.currency, { digits: 2 })),
      cell(this._t("remaining"), isNum(c.restlaufzeit) ? this._t("daysLeft", { n: c.restlaufzeit }) : "–"),
      cell(this._t("contractEnd"), c.ende ? this._date(c.ende) : this._t("noEnd")),
      h("td", { "data-label": this._t("colInstalment") }, this._money(c.abschlag, c.currency, { digits: 2 }),
        isNum(c.abschlag_jahr) ? h("span", { class: "t2", text: this._t("perYearShort", { v: this._money(c.abschlag_jahr, c.currency) }) }) : null),
      h("td", { class: "empty" })));
    flatRows.push(h("tr", { class: "total" },
      h("td", { text: this._t("total") }),
      cell(this._t("colCost"), money(sumCost(flat))),
      h("td", { text: "" }), h("td", { text: "" }),
      cell(this._t("colInstalment"), money(sum(flat, "abschlag"))),
      h("td", { text: "" })));

    const group = (key, list, heads, rows) => (list.length ? h("section", { class: "group" },
      h("h3", { class: "group-title" }, h("span", { text: this._t(key) }), h("span", { class: "count", text: String(list.length) })),
      h("table", {},
        // both tables share one column grid (the 6th column is empty in the flat-rate table)
        h("colgroup", {}, GRID.map((width) => h("col", { style: `width:${width}` }))),
        h("thead", {}, h("tr", {}, heads.map((label) => h("th", { text: label })))),
        h("tbody", {}, rows))) : null);

    return h(
      "div", {},
      contracts.length ? this._costChart(contracts) : null,
      group("groupMetered", metered, [
        this._t("colContract"), this._t("colCost"), this._t("colBalance"),
        this._t("colForecast"), this._t("colInstalment"), this._t("colRecommended"),
      ], meteredRows),
      group("groupFlat", flat, [
        this._t("colContract"), this._t("colCost"), this._t("remaining"), this._t("contractEnd"), this._t("colInstalment"), "",
      ], flatRows),
      contracts.length ? h("table", { class: "grand-table" },
        h("colgroup", {}, GRID.map((width) => h("col", { style: `width:${width}` }))),
        h("tbody", {}, h("tr", { class: "grandrow" },
          h("td", { text: this._t("grandTotal") }),
          cell(this._t("colCost"), money(sumCost(contracts))),
          h("td", { text: "" }), h("td", { text: "" }),
          cell(this._t("colInstalment"), money(sum(contracts, "abschlag"))),
          h("td", { text: "" })))) : null,
      contracts.length ? h("div", { class: "hint", text: this._t("costsHint") }) : null,
      this._loanTable(loans)
    );
  }


  /* History: archived contracts and the earlier terms of every contract. */
  _history() {
    const archived = this._contracts.filter((c) => c.archiviert).sort((a, b) => a.title.localeCompare(b.title));
    const earlier = this._contracts.filter((c) => !c.archiviert && (c.historie || []).length)
      .sort((a, b) => a.title.localeCompare(b.title));
    const toolbar = this._isAdmin
      ? h("div", { class: "list-head" },
        h("button", { class: "btn blue", type: "button", onclick: () => this._openTerm(null, null) }, icon("plus"), this._t("termAdd")))
      : null;
    if (!archived.length && !earlier.length) {
      return h("div", {}, toolbar,
        h("div", { class: "state" }, h("h2", { text: this._t("histEmptyTitle") }), h("div", { text: this._t("histEmpty") })));
    }
    const tone = (v) => (isNum(v) ? (v < 0 ? "red-t" : v > 0 ? "green-t" : "") : "muted-t");
    const cell = (label, value, cls) => h("td", { "data-label": label, class: cls || null, text: value });
    const termRow = (c, t, index) => h("tr", {},
      h("td", {}, `${this._date(t.beginn)} – ${t.ende ? this._date(t.ende) : "–"}`,
        h("span", { class: "t2", text: [t.anbieter, t.tarif].filter(Boolean).join(" · ") || "–" })),
      cell(this._t("colInstalment"), isNum(t.abschlag) ? this._money(t.abschlag, c.currency, { digits: 2 }) : "–"),
      cell(this._t("colTermCost"), this._money(isNum(t.kosten) ? t.kosten : t.abschlag_gezahlt, c.currency, { digits: 2 })),
      cell(this._t("colUsage"), isNum(t.verbrauch) ? `${this._num(t.verbrauch, 0)} ${this._unit(c)}` : "–"),
      cell(this._t("colTermBalance"), isNum(t.saldo) ? this._money(t.saldo, c.currency, { sign: true, digits: 2 }) : "–", tone(t.saldo)),
      this._isAdmin ? h("td", { class: "act" }, h("button", {
        class: "icon-btn", type: "button", title: this._t("termEdit"), "aria-label": this._t("termEdit"),
        onclick: () => this._openTerm(c, index),
      }, icon("edit"))) : null);
    const contractBlock = (c) => h("div", { class: "hist", "data-id": c.entry_id },
      h("div", { class: "hist-head" },
        h("div", { class: `badge ${c.sparte}` }, this._icon(c)),
        this._who(c),
        c.archiviert ? h("span", { class: "chip", text: this._t("archived") }) : null),
      h("table", {},
        h("thead", {}, h("tr", {}, [this._t("colTerm"), this._t("colInstalment"), this._t("colTermCost"), this._t("colUsage"), this._t("colTermBalance")]
          .concat(this._isAdmin ? [""] : []).map((label) => h("th", { text: label })))),
        // newest first; `index` is the position in the stored list (oldest first), needed to edit a term
        h("tbody", {}, (c.historie || []).map((t, index) => [t, index]).reverse().map(([t, index]) => termRow(c, t, index)))),
      this._total(c) ? h("p", { class: "hint hist-total" }, `${this._t("totalCost")}: `,
        h("b", { text: this._total(c).value }), ` · ${this._total(c).since}`) : null,
      // the acknowledgements belong to the contract list; here only archiving and restoring
      this._actions(c, ["archive_contract", "restore_contract"]));
    const group = (key, list) => (list.length ? h("section", { class: "group" },
      h("h3", { class: "group-title" }, h("span", { text: this._t(key) }), h("span", { class: "count", text: String(list.length) })),
      list.map(contractBlock)) : null);
    return h("div", {}, toolbar, group("groupArchived", archived), group("groupEarlier", earlier));
  }

  _contractList() {
    const head = this._isAdmin
      ? h("div", { class: "list-head" },
        h("button", { class: "btn blue", type: "button", onclick: () => this._openFlow(null, "create") }, icon("plus"), this._t("actNew")))
      : null;
    // the same two groups as in the overview
    const group = (key, list) => (list.length ? h("section", { class: "group" },
      h("h3", { class: "group-title" }, h("span", { text: this._t(key) }), h("span", { class: "count", text: String(list.length) })),
      list.map((c) => this._detail(c))) : null);
    return h("div", {}, head,
      group("groupMetered", this._live.filter((c) => METERED.has(c.sparte))),
      group("groupFlat", this._live.filter((c) => !METERED.has(c.sparte) && c.sparte !== "leasing")),
      group("groupLoans", this._financing));
  }

  /* Everything that changes a contract lives here, in the list of contracts (administrators only). */
  _rowActions(c) {
    if (!this._isAdmin) return null;
    const button = (flow, label, name) => h("button", {
      class: "icon-btn", type: "button", title: label, "aria-label": label,
      // the row is a <summary>: a click on the icon must not open or close it
      onclick: (ev) => { ev.preventDefault(); ev.stopPropagation(); this._openFlow(c, flow); },
    }, icon(name));
    return h("div", { class: "row-actions" },
      c.verlaengerbar ? h("button", {
        class: "icon-btn", type: "button", title: this._t("actRenew"), "aria-label": this._t("actRenew"),
        onclick: (ev) => { ev.preventDefault(); ev.stopPropagation(); this._openRenew(c); },
      }, icon("renew")) : null,
      c.sparte === "loan" ? null : button("next", this._t(c.next && c.next.beginn ? "actNextEdit" : "actNextPlan"), "plan"),
      button("edit", this._t("actEdit"), "edit"));
  }

  /* copies a value to the clipboard (HA may be opened over plain http, where the clipboard API is missing) */
  async _copy(text, button) {
    let ok = false;
    try {
      if (navigator.clipboard && window.isSecureContext) { await navigator.clipboard.writeText(text); ok = true; }
    } catch (_err) { /* fall back below */ }
    if (!ok) {
      const area = document.createElement("textarea");
      area.value = text;
      area.setAttribute("readonly", "");
      area.style.cssText = "position:fixed;top:-1000px;opacity:0";
      document.body.appendChild(area);
      area.select();
      try { ok = document.execCommand("copy"); } catch (_err) { ok = false; }
      area.remove();
    }
    if (ok && button) {
      button.classList.add("done");
      button.title = this._t("copied");
      setTimeout(() => { button.classList.remove("done"); button.title = this._t("copyValue"); }, 1600);
    }
  }

  _detail(c) {
    const d = this._derive(c);
    const unit = this._unit(c);
    const pu = this._priceUnit(c);
    const row = (label, value) => (value === null || value === undefined || value === "–" ? null
      : h("div", { class: "row" }, h("span", { text: label }), h("span", { text: value })));
    // personal details (only administrators receive them): the value with a button to copy it
    const copyRow = (label, value) => (!value ? null
      : h("div", { class: "row" }, h("span", { text: label }),
        h("span", { class: "val" }, h("span", { text: value }),
          h("button", { class: "copy", type: "button", title: this._t("copyValue"), "aria-label": `${this._t("copyValue")}: ${label}`,
            onclick: (ev) => this._copy(value, ev.currentTarget) }, icon("copy")))));
    const section = (title, rows) => {
      const filled = rows.filter(Boolean);
      return filled.length ? h("div", { class: "sec" }, h("h4", { text: title }), filled) : null;
    };
    const money = (v, digits = 2) => (isNum(v) ? this._money(v, c.currency, { digits }) : null);
    const amount = (v) => (isNum(v) ? `${this._num(v, 0)} ${unit}` : null);
    const amount1 = (v) => (isNum(v) ? `${this._num(v, 1)} ${unit}` : null); // small amounts (outdoor water) need a decimal
    const nxt = c.next || {};
    const sameAsYearCost = !METERED.has(c.sparte) && isNum(c.kosten_jahr) && isNum(c.abschlag_jahr) && Math.abs(c.kosten_jahr - c.abschlag_jahr) < 0.005;
    // with a total-consumption sensor (PV self-sufficiency): total, covered by PV and billed grid draw, so far and projected
    const usageGrid = c.autarkie_aktiv && isNum(c.verbrauch_gesamt_bisher) && isNum(c.verbrauch_gesamt_hochgerechnet)
      ? h("div", { class: "vgrid" },
        h("span", { class: "h", text: unit }), h("span", { class: "h n", text: this._t("gridColNow") }), h("span", { class: "h n", text: this._t("gridColEnd") }),
        h("span", { text: this._t("totalUse") }), h("span", { class: "n", text: this._num(c.verbrauch_gesamt_bisher, 0) }), h("span", { class: "n", text: this._num(c.verbrauch_gesamt_hochgerechnet, 0) }),
        h("span", { text: this._t("pvCovered") }), h("span", { class: "n", text: this._num(c.verbrauch_pv_gedeckt_bisher, 0) }), h("span", { class: "n", text: this._num(c.verbrauch_pv_gedeckt_hochgerechnet, 0) }),
        h("span", { class: "b", text: this._t("gridDraw") }), h("span", { class: "n b", text: this._num(c.verbrauch_bisher, 0) }), h("span", { class: "n b", text: this._num(c.verbrauch_hochgerechnet, 0) }))
      : null;

    const sections = [
      section(this._t("secContract"), [
        row(this._t("provider"), c.anbieter), row(this._t("tariff"), c.tarif),
        copyRow(this._t("customerNo"), c.kundennummer),
        copyRow(this._t("meterNo"), c.zaehlernummer), copyRow(this._t("meterNoLow"), c.zaehlernummer_nt),
        copyRow(this._t("maloId"), c.marktlokation),
        row(this._t("insuranceType"), c.versicherungsart ? this._insuranceType(c.versicherungsart) : null),
        row(this._t("kmStart"), isNum(c.km_start) ? `${this._num(c.km_start, 0)} km` : null),
        row(this._t("kmPerYear"), isNum(c.km_pro_jahr) ? `${this._num(c.km_pro_jahr, 0)} km` : null),
        row(this._t("start"), c.beginn ? this._date(c.beginn) : null),
        row(this._t("end"), c.ende ? this._date(c.ende) : null),
        row(this._t("remaining"), isNum(c.restlaufzeit) ? this._t("daysLeft", { n: c.restlaufzeit }) : null),
        row(this._t("minTerm"), isNum(c.mindestlaufzeit)
          ? `${this._t("months", { n: c.mindestlaufzeit })}${c.mindestlaufzeit_bis ? ` · ${this._t("untilDate", { d: this._date(c.mindestlaufzeit_bis) })}` : ""}` : null),
        row(this._t("noticePeriod"), isNum(c.kuendigungsfrist) ? this._t("months", { n: c.kuendigungsfrist }) : null),
        row(this._t("cancelBy"), c.kuendigung_bis ? this._date(c.kuendigung_bis) : null),
        row(this._t("reminderDate"), c.erinnerung_datum
          ? `${this._date(c.erinnerung_datum)} · ${c.erinnerung_bestaetigt ? this._t("reminderDone") : c.erinnerung_aktiv ? this._t("reminderActive") : this._t("months", { n: c.erinnerung_monate })}`
          : null),
      ]),
      this._kreditSection(c),
      this._leasingSection(c),
      section(this._t("secPrices"), [
        row(this._t("unitPrice"), isNum(c.arbeitspreis) ? this._price(c.arbeitspreis, c.currency, pu) : null),
        row(this._t("unitPriceLow"), isNum(c.arbeitspreis_nt) ? this._price(c.arbeitspreis_nt, c.currency, pu) : null),
        row(this._t("unitPriceNight"), isNum(c.arbeitspreis_nacht) ? this._price(c.arbeitspreis_nacht, c.currency, pu) : null),
        row(this._t("unitPriceEff"), isNum(c.effektiver_arbeitspreis) ? this._price(c.effektiver_arbeitspreis, c.currency, pu) : null),
        row(this._t("unitPriceWater"), isNum(c.arbeitspreis_gesamt_wasser) ? this._price(c.arbeitspreis_gesamt_wasser, c.currency, pu) : null),
        row(this._t("basePrice"), isNum(c.grundpreis) ? `${money(c.grundpreis)} ${this._t("perMonth")}` : null),
        row(this._tc("instalment", c), isNum(c.abschlag) ? `${money(c.abschlag)} ${this._t("perMonth")}` : null),
        // a flat-rate contract with one amount: the instalment per year is the same figure as "cost per year" right below
        // (they differ only when there is a base price, and a metered contract has no "cost per year" row)
        row(this._tc("instalmentYear", c), isNum(c.abschlag_jahr) && !sameAsYearCost ? money(c.abschlag_jahr) : null),
        // flat-rate contracts: what the contract costs a year, and how it is paid when not monthly
        row(this._t("costYear"), !METERED.has(c.sparte) && isNum(c.kosten_jahr) ? money(c.kosten_jahr) : null),
        row(this._t("payment"), c.zahlweise && c.zahlweise !== "monthly" && isNum(c.abschlag_je_zahlung)
          ? `${money(c.abschlag_je_zahlung)} ${this._t("interval")[c.zahlweise] || c.zahlweise}` : null),
        row(this._t("firstDebit"), c.zahlweise && c.zahlweise !== "monthly" && c.erste_zahlung ? this._date(c.erste_zahlung) : null),
        row(this._t("nextPayment"), c.naechste_zahlung ? this._date(c.naechste_zahlung) : null),
        row(this._t("costSoFar"), !METERED.has(c.sparte) && isNum(this._costSoFar(c)) ? money(this._costSoFar(c)) : null),
        row(this._t("totalCost"), this._total(c) ? `${this._total(c).value} · ${this._total(c).since}` : null),
      ]),
      this._onceSection(c),
      this._instalSection(c),
      d.measured || d.hasMetering || isNum(c.verbrauch_letzte_laufzeit) ? section(this._t("secConsumption"), [
        usageGrid || row(this._t("soFar"), amount(c.verbrauch_bisher)),
        row(this._t("gardenUse"), amount1(c.garten_verbrauch)),
        row(this._t("wwUse"), amount1(c.abwasserpflichtiger_verbrauch)),
        row(this._t("soFarHigh"), amount(c.verbrauch_bisher_ht)),
        row(this._t("soFarLow"), amount(c.verbrauch_bisher_nt)),
        usageGrid ? null : row(this._t("projectedTerm"), amount(c.verbrauch_hochgerechnet)),
        row(this._t("lastPeriod"), amount(c.verbrauch_letzte_laufzeit)),
        row(this._t("costSoFar"), money(c.kosten_bisher)),
        row(this._t("gardenCost"), money(c.garten_kosten)),
        row(this._t("wwCost"), money(c.abwasser_kosten)),
        row(this._t("balanceSoFar"), isNum(c.guthaben_bisher) ? this._money(c.guthaben_bisher, c.currency, { sign: true, digits: 2 }) : null),
        row(this._t("endForecast"), isNum(c.prognose_real) ? this._money(c.prognose_real, c.currency, { sign: true, digits: 2 }) : null),
        row(this._t("pvWithout"), c.autarkie_aktiv && isNum(c.prognose_ohne_autarkie) ? this._money(c.prognose_ohne_autarkie, c.currency, { sign: true, digits: 2 }) : null),
        row(this._t("pvSoFar"), c.autarkie_aktiv && isNum(c.autarkie_bisher)
          ? `${this._num(c.autarkie_bisher, 0)} %${isNum(c.autarkie_bisher_nt) ? ` · ${this._t("pvLowTariff", { v: this._num(c.autarkie_bisher_nt, 0) })}` : ""}` : null),
        row(this._t("pvSource"), c.autarkie_aktiv && c.autarkie_variante ? this._t("pvSrc")[c.autarkie_variante] || c.autarkie_variante : null),
        row(this._t("pvApprox"), c.autarkie_aktiv && c.autarkie_naeherung ? this._t("yes") : null),
      ]) : null,
      section(this._t("secAdvice"), [
        row(this._t("recommended"), isNum(c.empfohlener_abschlag) ? `${money(c.empfohlener_abschlag)} ${this._t("perMonth")}` : null),
        row(this._t("adjustment"), this._advice(c)),
      ]),
      c.next ? section(this._t("secNext"), [
        row(this._t("nextStart"), nxt.beginn ? this._date(nxt.beginn) : null),
        row(this._t("nextEnd"), nxt.ende ? this._date(nxt.ende) : null),
        row(this._t("nextProvider"), nxt.anbieter), row(this._t("nextTariff"), nxt.tarif),
        row(this._t("nextPrice"), isNum(nxt.arbeitspreis) ? this._price(nxt.arbeitspreis, c.currency, pu) : null),
        row(this._tc("nextInstalment", c), isNum(nxt.abschlag) ? `${money(nxt.abschlag)} ${this._t("perMonth")}` : null),
      ]) : null,
      this._aussenSection(c), // over the whole width below the other blocks: up to ten meters fit side by side
    ];

    const flat = !METERED.has(c.sparte);
    const endValue = c.sparte === "loan" ? (isNum(c.kredit_restschuld) ? this._money(c.kredit_restschuld, c.currency, { digits: 2 }) : "–")
      : flat ? `${this._money(c.abschlag, c.currency, { digits: 2 })} ${this._t("perMonth")}`
      : d.hasMetering ? this._money(c.prognose_real, c.currency, { sign: true }) : this._money(c.jahreskosten, c.currency);
    const details = h(
      "details", { "data-id": c.entry_id },
      h("summary", {},
        h("div", { class: `badge ${c.sparte}` }, this._icon(c)),
        this._who(c),
        this._chips(d.chips),
        h("div", { class: `end ${!flat && d.hasMetering ? (c.prognose_real < 0 ? "red-t" : "green-t") : ""}`, text: endValue }),
        h("div", { class: "row-end" },
          this._rowActions(c),
          h("span", { class: "caret", "aria-hidden": "true" }, icon("chevron")))),
      h("div", { class: "detail" }, sections, this._actions(c))
    );
    if (this._open.has(c.entry_id)) details.setAttribute("open", "");
    details.addEventListener("toggle", () => {
      if (details.open) this._open.add(c.entry_id);
      else this._open.delete(c.entry_id);
    });
    return details;
  }
}

if (!customElements.get("tariffy-panel")) {
  customElements.define("tariffy-panel", TariffyPanel);
}
