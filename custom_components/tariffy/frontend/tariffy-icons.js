/* Icons of the Tariffy panel. Loaded by tariffy-panel.js. */

/* Simple outline icons per contract type (24x24, stroke). */
export const ICONS = {
  electricity: [["path", { d: "M13 2 4 14h7l-1 8 9-12h-7z" }]],
  electricity_ht_nt: [["path", { d: "M13 2 4 14h7l-1 8 9-12h-7z" }]],
  gas: [["path", { d: "M12 2c.5 4 5 6 5 11a5 5 0 0 1-10 0c0-2 1-3.500 2-4.500.2 2 1 3 2 3 .5-3-1-5 1-9.500z" }]],
  water: [["path", { d: "M12 2s6.500 7 6.500 12a6.500 6.500 0 0 1-13 0C5.500 9 12 2 12 2z" }]],
  internet: [
    ["path", { d: "M2.500 9a14 14 0 0 1 19 0" }],
    ["path", { d: "M5.500 12.500a9.500 9.500 0 0 1 13 0" }],
    ["path", { d: "M8.600 16a5 5 0 0 1 6.800 0" }],
    ["circle", { cx: "12", cy: "19.500", r: "1", fill: "currentColor" }],
  ],
  mobile: [
    ["rect", { x: "7", y: "2.500", width: "10", height: "19", rx: "2.500" }],
    ["path", { d: "M11 18.500h2" }],
  ],
  streaming: [
    ["rect", { x: "3", y: "5", width: "18", height: "14", rx: "3" }],
    ["path", { d: "M10 9.500v5l4.500-2.500z" }],
  ],
  loan: [
    ["rect", { x: "3", y: "6", width: "18", height: "12", rx: "2" }],
    ["circle", { cx: "12", cy: "12", r: "2.500" }],
    ["path", { d: "M6.500 9.500v.01M17.500 14.500v.01" }],
  ],
  leasing: [
    ["path", { d: "M5 16.500h14l1.500-4.500-2-4.500H5.500l-2 4.500z" }],
    ["circle", { cx: "8", cy: "17", r: "1.600" }],
    ["circle", { cx: "16", cy: "17", r: "1.600" }],
  ],
  insurance: [["path", { d: "M12 2.500 20 5.500v6c0 5-3.500 8.500-8 10.500-4.500-2-8-5.500-8-10.500v-6z" }]],
  // actions of the contract list
  copy: [["rect", { x: "9", y: "9", width: "11", height: "11", rx: "2" }], ["path", { d: "M5 15V6a2 2 0 0 1 2-2h8" }]],
  edit: [["path", { d: "M12 20h9" }], ["path", { d: "M16.500 3.500a2.100 2.100 0 0 1 3 3L7 19l-4 1 1-4z" }]],
  plan: [
    ["rect", { x: "3", y: "4", width: "18", height: "18", rx: "2" }],
    ["path", { d: "M16 2v4M8 2v4M3 10h18M12 13.500v5M9.500 16h5" }],
  ],
  plus: [["path", { d: "M12 5v14M5 12h14" }]],
  close: [["path", { d: "M6 6l12 12M18 6 6 18" }]],
  chevron: [["path", { d: "M9 6l6 6-6 6" }]],
  renew: [["path", { d: "M20 11a8 8 0 0 0-14.500-3.500M4 5v4h4" }], ["path", { d: "M4 13a8 8 0 0 0 14.500 3.500M20 19v-4h-4" }]],
  other: [
    ["circle", { cx: "6", cy: "12", r: "1.600", fill: "currentColor" }],
    ["circle", { cx: "12", cy: "12", r: "1.600", fill: "currentColor" }],
    ["circle", { cx: "18", cy: "12", r: "1.600", fill: "currentColor" }],
  ],
};
