import {
  hydrate
} from "../chunk-EPA2PB3C.js";

// static/js/components/.tmp/fryui/hcenter-790b10d21c6136bc7a2a52f7f4fd383a19b0c0c3.js
var setup = async function() {
  let { grid, rightGutter, leftGutter } = this.fryargs;
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
  const columnPropName = "grid-template-columns";
  const firstNonZero = (tracks, type) => {
    for (let i = 0; i < tracks.length; i++) {
      if (tracks[i].type == type && tracks[i].numeric > 0) {
        return i;
      }
    }
    return null;
  };
  let cols = [];
  let pxcols = [];
  let colfrs = [];
  let colpercents = [];
  let colfr2px = 0;
  let colpercent2px = 0;
  const initialize = () => {
    cols = [];
    pxcols = [];
    colfrs = [];
    colpercents = [];
    colfr2px = 0;
    colpercent2px = 0;
    let prop = grid.style[columnPropName];
    if (prop) cols = parse(prop);
    prop = window.getComputedStyle(grid)[columnPropName];
    if (prop) pxcols = parse(prop);
    colfrs = cols.filter((c) => c.type === "fr");
    if (colfrs.length) {
      let c = firstNonZero(cols, "fr");
      if (c !== null)
        colfr2px = pxcols[c].numeric / cols[c].numeric;
    }
    colpercents = cols.filter((c) => c.type === "%");
    if (colpercents.length) {
      let c = firstNonZero(cols, "%");
      if (c !== null)
        colpercent2px = pxcols[c].numeric / cols[c].numeric;
    }
  };
  const setColSize = (i, size) => {
    cols[i].value = null;
    if (cols[i].type === "px") {
      cols[i].numeric = size;
    } else if (cols[i].type === "fr") {
      if (colfrs.length === 1) {
        cols[i].numeric = 1;
      } else if (colfr2px !== 0) {
        cols[i].numeric = size / colfr2px;
      }
    } else if (cols[i].type === "%" && colpercent2px !== 0) {
      cols[i].numeric = size / colpercent2px;
    }
  };
  this.broaden = () => {
    initialize();
    let leftSize = pxcols[0].numeric;
    let centerSize = pxcols[2].numeric;
    let rightSize = pxcols[4].numeric;
    if (leftSize <= step || rightSize <= step)
      return;
    leftSize -= step;
    rightSize -= step;
    centerSize += step + step;
    setColSize(0, leftSize);
    setColSize(2, centerSize);
    setColSize(4, rightSize);
    grid.style[columnPropName] = unparse(cols);
  };
  this.narrow = () => {
    initialize();
    let leftSize = pxcols[0].numeric;
    let centerSize = pxcols[2].numeric;
    let rightSize = pxcols[4].numeric;
    if (centerSize <= step + step) return;
    leftSize += step;
    rightSize += step;
    centerSize -= step + step;
    setColSize(0, leftSize);
    setColSize(2, centerSize);
    setColSize(4, rightSize);
    grid.style[columnPropName] = unparse(cols);
  };
  this.setCentered = (center) => {
    if (center && !leftGutter.centered) {
      grid.style[columnPropName] = "1fr 1px 2fr 1px 1fr";
    }
    leftGutter.centered = center;
    rightGutter.centered = center;
  };
  this.isCentered = () => topGutter.centered;
  this.fryembeds = [];
};
export {
  hydrate,
  setup
};
