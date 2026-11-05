/* Tariffy panel (beta). Placeholder until the final design lands: lists the
 * contracts delivered by the backend. User controlled text is only ever set
 * through textContent, never innerHTML. */
class TariffyPanel extends HTMLElement {
  constructor() {
    super();
    this._hass = null;
    this._unsub = null;
    this._contracts = [];
    this.attachShadow({ mode: "open" });
  }

  set hass(hass) {
    const first = !this._hass;
    this._hass = hass;
    if (first) this._subscribe();
  }

  set narrow(value) {
    this._narrow = value;
  }

  set panel(value) {
    this._panel = value;
  }

  disconnectedCallback() {
    if (this._unsub) {
      this._unsub();
      this._unsub = null;
    }
    this._hass = null;
  }

  async _subscribe() {
    try {
      this._unsub = await this._hass.connection.subscribeMessage(
        (event) => {
          this._contracts = event.contracts || [];
          this._render();
        },
        { type: "tariffy/subscribe" }
      );
    } catch (err) {
      this._error = String(err && err.message ? err.message : err);
      this._render();
    }
  }

  _render() {
    const root = this.shadowRoot;
    root.replaceChildren();

    const style = document.createElement("style");
    style.textContent =
      ":host{display:block;padding:16px;color:var(--primary-text-color);font-family:system-ui,sans-serif}" +
      "h1{font-size:20px;margin:0 0 4px}.beta{color:var(--secondary-text-color);margin:0 0 16px}" +
      ".card{border:1px solid var(--divider-color);border-radius:14px;padding:12px 16px;margin:0 0 12px}" +
      ".muted{color:var(--secondary-text-color)}";
    root.appendChild(style);

    const title = document.createElement("h1");
    title.textContent = "Tariffy";
    root.appendChild(title);
    const beta = document.createElement("p");
    beta.className = "beta";
    beta.textContent = "Beta: the panel is under construction.";
    root.appendChild(beta);

    if (this._error) {
      const err = document.createElement("p");
      err.textContent = this._error;
      root.appendChild(err);
      return;
    }

    for (const contract of this._contracts) {
      const card = document.createElement("div");
      card.className = "card";
      const name = document.createElement("strong");
      name.textContent = contract.title;
      card.appendChild(name);
      const meta = document.createElement("div");
      meta.className = "muted";
      meta.textContent = [contract.anbieter, contract.tarif].filter(Boolean).join(" · ");
      card.appendChild(meta);
      if (contract.prognose_real !== null && contract.prognose_real !== undefined) {
        const line = document.createElement("div");
        line.textContent =
          "Forecast at contract end: " + contract.prognose_real + " " + (contract.currency || "");
        card.appendChild(line);
      }
      root.appendChild(card);
    }
  }
}

customElements.define("tariffy-panel", TariffyPanel);
