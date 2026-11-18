/* Styles of the Tariffy panel (shadow DOM). Loaded by tariffy-panel.js. */

export const STYLE = `
:host {
  --bg: #0b0d12; --panel: #14171e; --panel2: #11141a;
  --tile: rgba(255,255,255,.032); --tile-line: rgba(255,255,255,.07); --line: rgba(255,255,255,.065);
  --text: #f3f5f9; --muted: #8b91a1; --dim: #5d6373;
  --green: #34d399; --red: #f87171; --orange: #fb923c; --blue: #60a5fa; --gold: #f7b733;
  display: block; min-height: 100%; box-sizing: border-box;
  background: var(--bg); color: var(--text); color-scheme: dark;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  container-type: inline-size;
}
* { box-sizing: border-box; }
/* use the whole width of the window; the cap only keeps ultra-wide monitors readable */
.wrap { max-width: 2400px; margin: 0 auto; padding: 16px 24px 40px; }
.top { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 18px; }
.brand { display: flex; align-items: center; gap: 10px; font-size: 20px; font-weight: 700; letter-spacing: .02em; }
.tabs { display: flex; gap: 2px; margin: 0 auto; padding: 4px; background: var(--panel2);
  border: 1px solid var(--line); border-radius: 12px; }
.tab { appearance: none; border: 0; background: transparent; color: var(--muted); font: inherit;
  font-size: 14px; font-weight: 600; padding: 8px 18px; border-radius: 9px; cursor: pointer; }
.tab:hover { color: var(--text); }
.tab[aria-selected="true"] { background: rgba(255,255,255,.09); color: var(--text); }
.tab:focus-visible, summary:focus-visible, a:focus-visible { outline: 2px solid var(--blue); outline-offset: 2px; }
.spacer { width: 90px; }

.summary { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; margin-bottom: 18px; }
@container (min-width: 1100px) { .summary { grid-template-columns: repeat(4, 1fr); } }
.sum { background: var(--panel); border: 1px solid var(--line); border-radius: 16px; padding: 14px 18px; min-width: 0; }
.label { font-size: 11px; font-weight: 600; letter-spacing: .09em; text-transform: uppercase; color: var(--muted); }
.sum .value { font-size: 26px; font-weight: 700; margin-top: 6px; font-variant-numeric: tabular-nums; }
.sum .sub { font-size: 12px; color: var(--muted); margin-top: 2px; }
.split { display: flex; height: 7px; margin-top: 12px; border-radius: 4px; overflow: hidden; gap: 2px; background: rgba(255,255,255,.07); }
.split span { display: block; height: 100%; }
.legend { display: flex; flex-wrap: wrap; gap: 2px 14px; margin-top: 8px; font-size: 12px; color: var(--muted); }
.legend b { color: var(--text); font-weight: 600; font-variant-numeric: tabular-nums; }
.legend i { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }
.mini { margin-top: 10px; display: grid; gap: 0; }
.mrow { display: flex; justify-content: space-between; gap: 10px; padding: 5px 0; border-top: 1px solid var(--line); font-size: 12px; color: var(--muted); }
.mrow .n { min-width: 0; }
.mrow .n b { color: var(--text); font-weight: 600; font-variant-numeric: tabular-nums; }
.mrow .v { flex: none; font-weight: 600; font-variant-numeric: tabular-nums; color: var(--text); }

/* two groups: metered contracts (big cards) and flat-rate contracts (slim cards), each in rows of equal height */
.group { margin-top: 22px; }
.group:first-of-type { margin-top: 0; }
.group-title { display: flex; align-items: center; gap: 8px; margin: 0 0 12px 2px; font-size: 11px; font-weight: 600;
  letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
/* the overall total is a row of its own in the same column grid as the tables above */
.grand-table { margin-top: 18px; table-layout: fixed; }
.grand-table td { font-weight: 700; border-bottom: 0; background: var(--panel2); }
.group-title .count { font-size: 11px; letter-spacing: 0; padding: 1px 8px; border-radius: 999px; background: rgba(255,255,255,.07); }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 16px; align-items: stretch; }
.grid.flat { grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); }
/* wide screens: three contracts per row in both groups, four on a very wide window */
@container (min-width: 1000px) { .grid.metered, .grid.flat { grid-template-columns: repeat(3, 1fr); } }
@container (min-width: 1500px) { .grid.flat { grid-template-columns: repeat(4, 1fr); } }
@container (min-width: 1750px) { .grid.metered, .grid.flat { grid-template-columns: repeat(4, 1fr); } }
section.card { display: flex; flex-direction: column; }
section.card .foot { padding-top: 12px; }
/* cards of one row share their rows: the header, the big figure, the tiles, the bars and the footer line up across the cards */
@supports (grid-template-rows: subgrid) {
  .grid > section.card { display: grid; grid-row: span 6; grid-template-rows: subgrid; row-gap: 0; align-content: start; }
}
.card.flat .big { font-size: 28px; }
.card { position: relative; background: var(--panel); border: 1px solid var(--line); border-radius: 18px; padding: 18px; }
.card.tone-green { background: linear-gradient(180deg, rgba(52,211,153,.085), var(--panel) 150px); }
.card.tone-red { background: linear-gradient(180deg, rgba(248,113,113,.085), var(--panel) 150px); }
.card.tone-orange { background: linear-gradient(180deg, rgba(251,146,60,.085), var(--panel) 150px); }
.card.alert { border-color: rgba(248,113,113,.35); }
.head { display: flex; align-items: flex-start; gap: 12px; }
.chips:empty { display: none; }
.head > .chips { margin-left: auto; flex: 0 1 auto; justify-content: flex-end; }
.card .title { font-size: 15px; letter-spacing: .07em; text-transform: uppercase; }
.icon-btn { appearance: none; flex: none; width: 34px; height: 34px; display: grid; place-items: center; padding: 0; border-radius: 10px;
  border: 1px solid var(--tile-line); background: var(--tile); color: var(--muted); cursor: pointer; }
.icon-btn:hover { color: var(--text); background: rgba(255,255,255,.09); }
.icon-btn:focus-visible { outline: 2px solid var(--blue); outline-offset: 2px; }
.icon-btn svg, .btn svg { width: 18px; height: 18px; fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
.row-actions { display: flex; gap: 6px; flex: none; }
.list-head { display: flex; justify-content: flex-end; margin: 0 0 12px; }
.list-head .btn { display: inline-flex; align-items: center; gap: 8px; }
.foot { margin-top: 12px; font-size: 12px; color: var(--muted); display: flex; flex-wrap: wrap; gap: 4px 10px; }
.foot b { color: var(--text); font-weight: 600; font-variant-numeric: tabular-nums; }
.badge { flex: none; width: 40px; height: 40px; border-radius: 12px; display: grid; place-items: center;
  background: var(--tile); border: 1px solid var(--tile-line); color: var(--blue); }
.badge ha-icon { --mdc-icon-size: 22px; width: 22px; height: 22px; display: block; }
.badge svg { width: 22px; height: 22px; fill: none; stroke: currentColor; stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round; }
.badge.gas { color: var(--orange); } .badge.water { color: #38bdf8; } .badge.electricity,
.badge.electricity_ht_nt { color: var(--gold); } .badge.internet { color: #a78bfa; } .badge.mobile { color: var(--green); } .badge.streaming { color: #f472b6; } .badge.loan { color: #fbbf24; } .badge.leasing { color: #38bdf8; }
.title { font-size: 17px; font-weight: 700; line-height: 1.2; }
.meta { font-size: 13px; color: var(--muted); margin-top: 2px; }
.who { min-width: 0; flex: 1; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; justify-content: flex-end; }
.chip { font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 999px; white-space: nowrap;
  background: rgba(255,255,255,.06); color: var(--muted); }
.chip.green { background: rgba(52,211,153,.14); color: var(--green); }
.chip.red { background: rgba(248,113,113,.14); color: var(--red); }
.chip.orange { background: rgba(251,146,60,.15); color: var(--orange); }
.chip.blue { background: rgba(96,165,250,.15); color: var(--blue); }

.hero { display: flex; align-items: flex-start; justify-content: space-between; gap: 14px; margin: 16px 0 14px; }
.hero > div:first-child { min-width: 0; }
.ring { position: relative; flex: none; width: 84px; height: 84px; }
.ring svg { width: 84px; height: 84px; transform: rotate(-90deg); }
.ring .track { stroke: rgba(255,255,255,.08); } .ring .arc { stroke: var(--blue); stroke-linecap: round; }
.ring .center { position: absolute; inset: 0; display: grid; place-content: center; text-align: center; }
.ring .pct { font-size: 17px; font-weight: 700; font-variant-numeric: tabular-nums; }
.ring .pcap { font-size: 9px; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); }
.big { font-size: 34px; font-weight: 700; font-variant-numeric: tabular-nums; line-height: 1.1; margin-top: 4px; }
.green-t { color: var(--green); } .red-t { color: var(--red); } .muted-t { color: var(--muted); }
.note { font-size: 13px; color: var(--muted); margin-top: 6px; }
.actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
.btn { appearance: none; font: inherit; font-size: 13px; font-weight: 700; padding: 8px 14px; border-radius: 10px;
  border: 1px solid var(--tile-line); background: var(--tile); color: var(--text); cursor: pointer; }
.btn:hover { background: rgba(255,255,255,.08); }
.btn[disabled] { opacity: .5; cursor: default; }
.btn:focus-visible { outline: 2px solid var(--blue); outline-offset: 2px; }
.btn.red { color: var(--red); border-color: rgba(248,113,113,.4); }
.btn.orange { color: var(--orange); border-color: rgba(251,146,60,.4); }
.btn.blue { color: var(--blue); border-color: rgba(96,165,250,.4); }
.btn.go { background: rgba(96,165,250,.18); color: var(--blue); border-color: rgba(96,165,250,.5); }
.overlay { position: fixed; inset: 0; z-index: 30; background: rgba(0,0,0,.62); display: flex; align-items: center; justify-content: center; padding: 16px; }
.dialog { background: var(--panel); border: 1px solid var(--line); border-radius: 16px; width: 100%; max-width: 620px; max-height: calc(100vh - 32px); overflow: auto; padding: 18px 20px; box-sizing: border-box; }
.dialog h2 { margin: 0 0 6px; font-size: 18px; }
.dialog .hint { color: var(--muted); font-size: 13px; margin: 0 0 8px; }
.fields { display: grid; grid-template-columns: 1fr 1fr; gap: 0 14px; }
.fld { display: block; margin: 8px 0; min-width: 0; }
.fld .lbl { display: block; font-size: 12px; color: var(--muted); margin-bottom: 4px; }
.fld input, .fld select { width: 100%; box-sizing: border-box; font: inherit; font-size: 14px; color: var(--text); background: var(--tile); border: 1px solid var(--tile-line); border-radius: 8px; padding: 8px 10px; color-scheme: dark; }
/* the list of a drop-down is drawn by the browser: some ignore color-scheme, so it gets its colours explicitly
   (otherwise light text on a white list) */
/* iOS draws a date field with its own intrinsic width and no height while empty: it stuck out of the dialog */
.fld input[type="date"] { appearance: none; -webkit-appearance: none; min-width: 0; max-width: 100%; min-height: 38px; text-align: left; }
.fld input[type="date"]::-webkit-date-and-time-value { text-align: left; min-height: 1.2em; }
.fld select option, .fld select optgroup { background: #1a1d25; color: var(--text); }
.fld input:focus-visible, .fld select:focus-visible { outline: 2px solid var(--blue); outline-offset: 1px; }
.confirm-name { width: 100%; font: inherit; font-size: 14px; color: var(--text); background: var(--tile); border: 1px solid var(--tile-line); border-radius: 8px; padding: 8px 10px; color-scheme: dark; }
.confirm-name:focus-visible { outline: 2px solid var(--red); outline-offset: 1px; }
.fld.bool { display: flex; gap: 8px; align-items: center; }
.fld.bool .lbl { margin: 0; font-size: 13px; color: var(--text); }
.fld.bool input { width: auto; }
.fld.bad input, .fld.bad select { border-color: var(--red); }
.ferr { color: var(--red); font-size: 12px; margin-top: 4px; }
.check { display: flex; gap: 8px; align-items: center; margin: 12px 0 0; font-size: 13px; }
.dialog .actions { margin-top: 16px; }
@media (max-width: 560px) { .fields { grid-template-columns: 1fr; } }
.ask { width: 100%; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; font-size: 13px; color: var(--muted); }
.ask span { flex-basis: 100%; }
.err { width: 100%; font-size: 13px; color: var(--red); }

.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(96px, 1fr)); gap: 8px; }
.tile { background: var(--tile); border: 1px solid var(--tile-line); border-radius: 12px; padding: 10px 12px; min-width: 0; }
.tile .label { overflow-wrap: anywhere; }
.tile .v { font-size: 16px; font-weight: 700; margin-top: 4px; font-variant-numeric: tabular-nums; }
.tile .s { font-size: 12px; color: var(--muted); margin-top: 1px; }
.tile .v small, .big small { font-size: 12px; font-weight: 500; color: var(--muted); margin-left: 3px; }

.bars { margin-top: 14px; display: grid; gap: 6px; }
.bar { display: grid; grid-template-columns: 1fr auto; gap: 2px 10px; align-items: center; font-size: 12px; color: var(--muted); }
.bar .tr { grid-column: 1 / -1; height: 7px; border-radius: 4px; background: rgba(255,255,255,.07); overflow: hidden; }
.bar .fl { display: block; height: 100%; border-radius: 4px; }
.bar b { color: var(--text); font-variant-numeric: tabular-nums; }

.notes { margin-top: 14px; display: grid; gap: 8px; }
.callout { font-size: 13px; line-height: 1.4; border-radius: 12px; padding: 10px 12px; background: var(--tile); border: 1px solid var(--tile-line); color: var(--muted); }
.callout.red { border-color: rgba(248,113,113,.35); background: rgba(248,113,113,.07); color: #fecaca; }
.callout.orange { border-color: rgba(251,146,60,.35); background: rgba(251,146,60,.07); color: #fed7aa; }
.callout.blue { border-color: rgba(96,165,250,.3); background: rgba(96,165,250,.06); color: #bfdbfe; }

.group table { table-layout: fixed; }
table { width: 100%; border-collapse: collapse; background: var(--panel); border: 1px solid var(--line); border-radius: 16px; overflow: hidden; }
th, td { padding: 12px 14px; text-align: right; font-variant-numeric: tabular-nums; border-bottom: 1px solid var(--line); }
th:first-child, td:first-child { text-align: left; }
th { font-size: 11px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); background: var(--panel2); }
tr.sub td { font-size: 13px; color: var(--muted); padding-top: 6px; padding-bottom: 6px; }
tr.sub td:first-child { padding-left: 32px; }
.hist { margin-bottom: 16px; }
.hist-head { display: flex; align-items: center; gap: 12px; margin: 0 0 10px; }
.hist-head .who { flex: 1; }
.hist .actions { margin-top: 10px; }
.hist-total { margin: 8px 2px 0; }
.once-row .t2 { display: block; }
.once-row .icon-btn { margin-left: 4px; flex: none; }
.once-row > span:first-child { min-width: 0; overflow-wrap: anywhere; }
.once-row > span:nth-child(2) { white-space: nowrap; }
.aussen-row { display: grid; grid-template-columns: minmax(0, 1fr) auto; column-gap: 8px; align-items: start; padding: 7px 0; border-bottom: 1px solid var(--line); font-size: 14px; }
.aussen-row .an { min-width: 0; overflow-wrap: anywhere; }
.aussen-row .t2 { display: block; font-size: 12px; color: var(--muted); }
.aussen-row .av { grid-column: 1; margin-top: 2px; font-variant-numeric: tabular-nums; }
.aussen-row .icon-btn { grid-column: 2; grid-row: 1 / span 2; }
.sec { min-width: 0; }
.aussen-sec { grid-column: 1 / -1; }
.aussen-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); column-gap: 18px; }
.once-add { margin-top: 8px; }
.chart { margin-bottom: 22px; }
.chart-ctl { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; margin: 0 0 14px; }
.yr-pick { display: inline-flex; align-items: center; gap: 8px; font-size: 13px; color: var(--muted); }
.yr-pick select { font: inherit; font-size: 13px; padding: 6px 10px; color: var(--text); background: var(--panel2); border: 1px solid var(--line); border-radius: 10px; }
.yr-pick select option { background: #14171e; color: #f3f5f9; }
.seg { display: inline-flex; gap: 2px; padding: 3px; margin: 0; background: var(--panel2); border: 1px solid var(--line); border-radius: 10px; }
.seg button { font: inherit; font-size: 13px; padding: 5px 12px; border: 0; border-radius: 7px; background: none; color: var(--muted); cursor: pointer; }
.seg button.on { background: var(--tile-line); color: var(--text); font-weight: 600; }
.chart-body { display: flex; align-items: center; gap: 28px; flex-wrap: wrap; }
.cs-ringwrap { position: relative; width: 190px; height: 190px; flex: none; }
.cs-ring { width: 100%; height: 100%; display: block; }
.cs-mid { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-size: 18px; }
.cs-legend { list-style: none; margin: 0; padding: 0; flex: 1 1 260px; min-width: 0; max-width: 560px; }
.cs-legend li { display: flex; align-items: baseline; gap: 10px; padding: 6px 0; border-bottom: 1px solid var(--line); font-size: 14px; }
.cs-legend .nm { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.cs-legend .val { font-variant-numeric: tabular-nums; }
.cs-legend .pct { width: 56px; text-align: right; color: var(--muted); font-variant-numeric: tabular-nums; }
.cs-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; flex: none; }
.kindbar { margin-top: 16px; }
.kindbar .cs-split { display: flex; height: 8px; border-radius: 99px; overflow: hidden; background: var(--tile-line); }
.cs-dot.k0, .cs-split .k0 { background: var(--blue); }
.cs-dot.k1, .cs-split .k1 { background: var(--orange); }
.kindleg { display: flex; gap: 16px; flex-wrap: wrap; margin-top: 8px; font-size: 13px; color: var(--muted); }
.kindleg .cs-dot { margin-right: 6px; }
.hist-total b { color: var(--text); }
.bk { background: var(--panel); border: 1px solid var(--line); border-radius: 16px; padding: 16px 18px; display: grid; gap: 12px; }
.bk p { margin: 0; font-size: 13px; color: var(--muted); }
.bk-row { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 14px; justify-content: space-between; }
.bk-row .who { flex: 1 1 200px; }
.bk-msg { margin: 0 0 12px; font-size: 13px; color: var(--green); }
.bk .file { font: inherit; font-size: 13px; color: var(--muted); max-width: 100%; }
.bk .file::file-selector-button { font: inherit; font-size: 13px; font-weight: 700; padding: 8px 14px; margin-right: 10px; border-radius: 10px;
  border: 1px solid var(--tile-line); background: var(--tile); color: var(--text); cursor: pointer; }
.bk .file::file-selector-button:hover { background: rgba(255,255,255,.09); }
td.act { width: 1%; white-space: nowrap; }
.fnote { font-size: 12px; color: var(--muted); margin-top: 4px; }
tr.total td { font-weight: 700; border-bottom: 0; background: var(--panel2); }
td .t2 { display: block; font-size: 12px; color: var(--muted); font-weight: 400; }
.hint { font-size: 12px; color: var(--muted); margin-top: 10px; }

details { background: var(--panel); border: 1px solid var(--line); border-radius: 16px; margin-bottom: 12px; overflow: hidden; }
summary { list-style: none; cursor: pointer; display: flex; align-items: center; gap: 12px; padding: 14px 18px; }
summary::-webkit-details-marker { display: none; }
summary .who { flex: 1; }
summary .end { text-align: right; font-weight: 700; font-variant-numeric: tabular-nums; white-space: nowrap; }
summary .caret { flex: none; width: 34px; height: 34px; display: grid; place-items: center; border-radius: 10px;
  border: 1px solid var(--tile-line); background: var(--tile); color: var(--muted); transition: color .15s; }
summary .caret svg { width: 18px; height: 18px; fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; transition: transform .15s; }
/* icons and arrow of a list row stay together when the row wraps */
.row-end { display: flex; align-items: center; gap: 6px; flex: none; margin-left: auto; }
summary:hover .caret { color: var(--text); }
summary .chips:empty { display: none; }
/* cards (overview): the chips get a line of their own below */
details.card > summary .chips { flex-basis: 100%; justify-content: flex-end; order: 5; }
/* rows of the contract list: name, chips, amount on one line, wrapping on narrow screens */
details:not(.card) > summary { flex-wrap: wrap; }
details:not(.card) > summary .who { flex: 1 1 150px; }
details:not(.card) > summary .chips { flex: 0 1 auto; justify-content: flex-end; }
details.card { padding: 0; }
details.card > summary { padding: 14px 16px; flex-wrap: wrap; }
details.card .body { padding: 0 16px 16px; }
details.card.alert { border-color: rgba(248,113,113,.35); }
details[open] summary .caret svg { transform: rotate(90deg); }
.detail { padding: 4px 18px 18px; display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 18px; }
.sec h4 { margin: 8px 0 6px; font-size: 11px; font-weight: 600; letter-spacing: .09em; text-transform: uppercase; color: var(--muted); }
.vgrid { display: grid; grid-template-columns: minmax(0, 1fr) auto auto; column-gap: 10px; font-size: 13.5px; border-bottom: 1px solid var(--line); }
.vgrid > span { padding: 7px 0; overflow-wrap: anywhere; border-bottom: 1px solid var(--line); }
.vgrid > span:nth-last-child(-n+3) { border-bottom: 0; }
.vgrid .n { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
.vgrid .h { color: var(--muted); font-size: 11px; white-space: nowrap; font-weight: 600; letter-spacing: .02em; }
.vgrid .b { font-weight: 600; }
.row .val { display: inline-flex; align-items: center; gap: 6px; flex: 0 0 auto; max-width: 66%; overflow-wrap: anywhere; text-align: right; }
.copy { flex: none; display: inline-grid; place-items: center; width: 24px; height: 24px; padding: 0; border: 0; border-radius: 6px; background: transparent; color: var(--muted); cursor: pointer; }
.copy:hover, .copy:focus-visible { background: var(--line); color: inherit; }
.copy svg { width: 15px; height: 15px; fill: none; stroke: currentColor; stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round; }
.copy.done { color: var(--green); }
.row { display: flex; justify-content: space-between; gap: 12px; padding: 7px 0; border-bottom: 1px solid var(--line); font-size: 14px; }
.row span:first-child { color: var(--muted); } .row span:last-child { text-align: right; font-variant-numeric: tabular-nums; }

.state { text-align: center; padding: 64px 16px; color: var(--muted); }
.state h2 { color: var(--text); margin: 0 0 6px; }
.state a { color: var(--blue); font-weight: 600; }

@container (max-width: 760px) {
  .wrap { padding: 12px 12px 32px; }
  .top { gap: 10px; }
  .tabs { order: 3; width: 100%; margin: 0; overflow-x: auto; scrollbar-width: none; }
  .tab { flex: 1; padding: 9px 6px; }
  .spacer { display: none; }
  .summary { grid-template-columns: 1fr; gap: 10px; }
  .sum { display: grid; grid-template-columns: 1fr auto; align-items: center; padding: 12px 14px; }
  .sum .value { font-size: 20px; margin: 0; grid-column: 2; grid-row: 1 / span 2; }
  .sum .sub { grid-column: 1; }
  .sum .split, .sum .legend, .sum .mini { grid-column: 1 / -1; }
  .tiles { grid-template-columns: 1fr 1fr; }
  .tiles .tile:last-child:nth-child(odd) { grid-column: 1 / -1; }
  .grid, .grid.flat { grid-template-columns: 1fr; gap: 12px; }
  summary .caret { width: 30px; height: 30px; }
  .group { margin-top: 18px; }
  .card { padding: 14px; }
  .big { font-size: 28px; }
  .ring, .ring svg { width: 76px; height: 76px; }
  table, thead, tbody, tr, td { display: block; }
  colgroup, td:empty { display: none; }
  thead { display: none; }
  table { background: transparent; border: 0; border-radius: 0; }
  tr { background: var(--panel); border: 1px solid var(--line); border-radius: 14px; margin-bottom: 10px; padding: 8px 14px; }
  tr.sub { margin: -6px 0 10px 14px; background: var(--panel2); padding: 6px 14px; }
  td { display: flex; justify-content: space-between; text-align: right; padding: 5px 0; border: 0; }
  td::before { content: attr(data-label); color: var(--muted); font-size: 12px; text-align: left; margin-right: 12px; }
  td:first-child { font-weight: 700; padding-bottom: 6px; }
  td:first-child::before { content: none; }
  tr.sub td:first-child { padding: 0 0 2px; font-weight: 600; color: var(--muted); }
  tr.total td:first-child { display: none; }
  td.empty { display: none; }
  td.rec { flex-wrap: wrap; }
  td.rec .t2 { flex-basis: 100%; text-align: right; margin-top: 2px; }
  .detail { grid-template-columns: 1fr; gap: 6px; padding: 0 14px 14px; }
  summary { padding: 12px 14px; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
`;
