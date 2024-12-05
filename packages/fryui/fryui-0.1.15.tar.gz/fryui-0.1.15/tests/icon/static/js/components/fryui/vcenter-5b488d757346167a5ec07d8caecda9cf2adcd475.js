import {
  hydrate
} from "../chunk-EPA2PB3C.js";

// static/js/components/.tmp/fryui/vcenter-5b488d757346167a5ec07d8caecda9cf2adcd475.js
var setup = async function() {
  let { grid, bottomGutter, topGutter } = this.fryargs;
  const numeric = (value, unit) => Number(value.slice(0, -1 * unit.length));
  const parseValue = function(value) {
    if (value.endsWith("px")) {
      return { value, type: "px", numeric: numeric(value, "px") };
    }
    if (value.endsWith("fr")) {
      return { value, type: "fr", numeric: numeric(value, "fr") };
    }
    if (value.endsWith("%")) {
      return { value, type: "%", numeric: numeric(value, "%") };
    }
    if (value === "auto") {
      return { value, type: "auto" };
    }
    return null;
  };
  const unparseValue = (v) => v.value ? v.value : `${v.numeric}${v.type}`;
  const parse = (rule) => rule.split(" ").map(parseValue);
  const unparse = (tracks) => tracks.map(unparseValue).join(" ");
  const step = 5;
  const rowPropName = "grid-template-rows";
  const firstNonZero = (tracks, type) => {
    for (let i = 0; i < tracks.length; i++) {
      if (tracks[i].type == type && tracks[i].numeric > 0) {
        return i;
      }
    }
    return null;
  };
  let rows = [];
  let pxrows = [];
  let rowfrs = [];
  let rowpercents = [];
  let rowfr2px = 0;
  let rowpercent2px = 0;
  const initialize = () => {
    rows = [];
    pxrows = [];
    rowfrs = [];
    rowpercents = [];
    rowfr2px = 0;
    rowpercent2px = 0;
    let prop = grid.style[rowPropName];
    if (prop) rows = parse(prop);
    prop = window.getComputedStyle(grid)[rowPropName];
    if (prop) pxrows = parse(prop);
    rowfrs = rows.filter((r) => r.type === "fr");
    if (rowfrs.length) {
      let r = firstNonZero(rows, "fr");
      if (r !== null)
        rowfr2px = pxrows[r].numeric / rows[r].numeric;
    }
    rowpercents = rows.filter((r) => r.type === "%");
    if (rowpercents.length) {
      let r = firstNonZero(rows, "%");
      if (r !== null)
        rowpercent2px = pxrows[r].numeric / rows[r].numeric;
    }
  };
  const setRowSize = (i, size) => {
    rows[i].value = null;
    if (rows[i].type === "px") {
      rows[i].numeric = size;
    } else if (rows[i].type === "fr") {
      if (rowfrs.length === 1) {
        rows[i].numeric = 1;
      } else if (rowfr2px !== 0) {
        rows[i].numeric = size / rowfr2px;
      }
    } else if (rows[i].type === "%" && rowpercent2px !== 0) {
      rows[i].numeric = size / rowpercent2px;
    }
  };
  this.broaden = () => {
    initialize();
    let topSize = pxrows[0].numeric;
    let centerSize = pxrows[2].numeric;
    let bottomSize = pxrows[4].numeric;
    if (topSize <= step || bottomSize <= step)
      return;
    topSize -= step;
    bottomSize -= step;
    centerSize += step + step;
    setRowSize(0, topSize);
    setRowSize(2, centerSize);
    setRowSize(4, bottomSize);
    grid.style[rowPropName] = unparse(rows);
  };
  this.narrow = () => {
    initialize();
    let topSize = pxrows[0].numeric;
    let centerSize = pxrows[2].numeric;
    let bottomSize = pxrows[4].numeric;
    if (centerSize <= step + step) return;
    topSize += step;
    bottomSize += step;
    centerSize -= step + step;
    setRowSize(0, topSize);
    setRowSize(2, centerSize);
    setRowSize(4, bottomSize);
    grid.style[rowPropName] = unparse(rows);
  };
  this.setCentered = (center) => {
    if (center && !topGutter.centered) {
      grid.style[rowPropName] = "1fr 1px 2fr 1px 1fr";
    }
    topGutter.centered = center;
    bottomGutter.centered = center;
  };
  this.isCentered = () => topGutter.centered;
  this.fryembeds = [];
};
export {
  hydrate,
  setup
};
