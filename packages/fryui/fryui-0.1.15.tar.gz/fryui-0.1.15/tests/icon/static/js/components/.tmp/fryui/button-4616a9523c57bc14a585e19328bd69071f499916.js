export { hydrate } from "fryhcs";
export const setup = async function () {
    let { dom } = this.fryargs;
    
      this.focus = () => { dom.focus(); };
    
    this.fryembeds = [];
};
