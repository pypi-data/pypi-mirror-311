export { hydrate } from "fryhcs";
export const setup = async function () {
    let { gutters, ncol, nrow, resizable } = this.fryargs;
    
      this.hgutters = (r) => {
        const gutters = [];
        for (let c=0; c<ncol; c++) {
            const n = r*ncol + c;
            const ch = this.fryelement.children.item(n);
            if (ch && ch.frycomponents && ch.frycomponents.length > 0) {
                const comp = ch.frycomponents[0];
                if (comp.fryname === 'Gutter') {
                    gutters.push(comp);
                }
            }
        }
        return gutters;
      }

      this.vgutters = (c) => {
        const gutters = [];
        for (let r=0; r<nrow; r++) {
            const n = r*ncol + c;
            const ch = this.fryelement.children.item(n);
            if (ch && ch.frycomponents && ch.frycomponents.length > 0) {
                const comp = ch.frycomponents[0];
                if (comp.fryname === 'Gutter') {
                    gutters.push(comp);
                }
            }
        }
        return gutters;
      }
    
    this.fryembeds = [];
};
