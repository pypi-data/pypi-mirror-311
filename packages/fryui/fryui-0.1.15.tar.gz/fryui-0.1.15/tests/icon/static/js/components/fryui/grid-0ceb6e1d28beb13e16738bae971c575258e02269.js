import {
  hydrate
} from "../chunk-EPA2PB3C.js";

// static/js/components/.tmp/fryui/grid-0ceb6e1d28beb13e16738bae971c575258e02269.js
var setup = async function() {
  let { gutters, ncol, nrow, resizable } = this.fryargs;
  this.hgutters = (r) => {
    const gutters2 = [];
    for (let c = 0; c < ncol; c++) {
      const n = r * ncol + c;
      const ch = this.fryelement.children.item(n);
      if (ch && ch.frycomponents && ch.frycomponents.length > 0) {
        const comp = ch.frycomponents[0];
        if (comp.fryname === "Gutter") {
          gutters2.push(comp);
        }
      }
    }
    return gutters2;
  };
  this.vgutters = (c) => {
    const gutters2 = [];
    for (let r = 0; r < nrow; r++) {
      const n = r * ncol + c;
      const ch = this.fryelement.children.item(n);
      if (ch && ch.frycomponents && ch.frycomponents.length > 0) {
        const comp = ch.frycomponents[0];
        if (comp.fryname === "Gutter") {
          gutters2.push(comp);
        }
      }
    }
    return gutters2;
  };
  this.fryembeds = [];
};
export {
  hydrate,
  setup
};
