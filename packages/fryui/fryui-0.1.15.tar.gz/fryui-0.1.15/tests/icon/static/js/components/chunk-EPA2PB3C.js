// ../../../fryhcs/src/fryhcs/static/js/fryhcs.js
var activeEffectStack = [];
var Signal = class {
  constructor(rawValue) {
    this.rawValue = rawValue;
    this.effectSet = /* @__PURE__ */ new Set();
  }
  addEffect(effect2) {
    this.effectSet.add(effect2);
  }
  removeEffect(effect2) {
    this.effectSet.delete(effect2);
  }
  hasEffect(effect2) {
    return this.effectSet.has(effect2);
  }
  peek() {
    return this.rawValue;
  }
  get value() {
    const len = activeEffectStack.length;
    if (len === 0) {
      return this.rawValue;
    }
    const currentEffect = activeEffectStack[len - 1];
    if (!this.hasEffect(currentEffect)) {
      this.effectSet.add(currentEffect);
      currentEffect.addSignal(this);
    }
    return this.rawValue;
  }
  set value(rawValue) {
    if (this.rawValue !== rawValue) {
      this.rawValue = rawValue;
      const errs = [];
      for (const effect2 of this.effectSet) {
        try {
          effect2.callback();
        } catch (err) {
          errs.push([effect2, err]);
        }
      }
      if (errs.length > 0) {
        throw errs;
      }
    }
  }
};
var Effect = class {
  constructor(fn) {
    this.fn = fn;
    this.active = false;
    this.todispose = false;
    this.disposed = false;
    this.signalSet = /* @__PURE__ */ new Set();
  }
  addSignal(signal) {
    this.signalSet.add(signal);
  }
  removeSignal(signal) {
    this.signalSet.delete(signal);
  }
  callback() {
    if (this.active === true || this.disposed === true) {
      return;
    }
    activeEffectStack.push(this);
    this.active = true;
    this.signalSet.clear();
    try {
      this.fn();
    } finally {
      this.active = false;
      activeEffectStack.pop();
      if (this.todispose) {
        this.dispose();
      }
    }
  }
  dispose() {
    if (this.disposed) {
      return;
    }
    if (this.active) {
      this.todispose = true;
      return;
    }
    for (const signal of this.signalSet) {
      signal.removeEffect(this);
    }
    this.signalSet.clear();
    this.todispose = false;
    this.disposed = true;
  }
};
function effect(fn) {
  const e = new Effect(fn);
  try {
    e.callback();
  } catch (err) {
    e.dispose();
    throw err;
  }
  return e.dispose.bind(e);
}
var Computed = class {
  constructor(fn) {
    this.fn = fn;
    this.rawValue = void 0;
    this.active = false;
    this.todispose = false;
    this.disposed = false;
    this.effectSet = /* @__PURE__ */ new Set();
    this.signalSet = /* @__PURE__ */ new Set();
  }
  addEffect(effect2) {
    this.effectSet.add(effect2);
  }
  removeEffect(effect2) {
    this.effectSet.delete(effect2);
  }
  hasEffect(effect2) {
    return this.effectSet.has(effect2);
  }
  peek() {
    return this.rawValue;
  }
  get value() {
    this.rawValue = this.fn();
    const len = activeEffectStack.length;
    if (len === 0) {
      return this.rawValue;
    }
    const currentEffect = activeEffectStack[len - 1];
    if (!this.hasEffect(currentEffect)) {
      this.effectSet.add(currentEffect);
      currentEffect.addSignal(this);
    }
    return this.rawValue;
  }
  addSignal(signal) {
    this.signalSet.add(signal);
  }
  removeSignal(signal) {
    this.signalSet.delete(signal);
  }
  callback() {
    if (this.active === true || this.disposed === true) {
      return;
    }
    activeEffectStack.push(this);
    this.active = true;
    this.signalSet.clear();
    let rawValue;
    try {
      rawValue = this.fn();
      if (rawValue != this.rawValue) {
        this.rawValue = rawValue;
        const errs = [];
        for (const effect2 of this.effectSet) {
          try {
            effect2.callback();
          } catch (err) {
            errs.push([effect2, err]);
          }
        }
        if (errs.length > 0) {
          throw errs;
        }
      }
    } finally {
      this.active = false;
      activeEffectStack.pop();
      if (this.todispose) {
        this.dispose();
      }
    }
  }
  dispose() {
    if (this.disposed) {
      return;
    }
    if (this.active) {
      this.todispose = true;
      return;
    }
    for (const signal of this.signalSet) {
      signal.removeEffect(this);
    }
    this.signalSet.clear();
    for (const effect2 of this.effectSet) {
      effect2.removeSignal(this);
    }
    this.effectSet.clear();
    this.todispose = false;
    this.disposed = true;
  }
};
var Component = class {
  constructor({ cid, name, url, args, refs, element, g }) {
    this.fryid = cid;
    const names = name.split(":");
    if (names.length == 1) {
      this.fryapp = "";
      this.fryname = name;
    } else {
      this.fryapp = names[0];
      this.fryname = names[1];
    }
    this.fryurl = url;
    this.fryargs = args;
    this.fryrefs = refs;
    this.fryelement = element;
    this.fryg = g;
    this._fryparent = null;
    this._fryroot = null;
  }
  ready(fn) {
    this.fryg.readyFns.push(fn);
  }
  get g() {
    return this.fryg.g;
  }
  get isReady() {
    return this.fryg.isReady;
  }
  get fryparent() {
    if (this._fryparent) return this._fryparent;
    let element = this.fryelement;
    let components = element.frycomponents;
    const index = components.indexOf(this);
    if (index > 0) {
      this._fryparent = components[index - 1];
      return this._fryparent;
    }
    element = element.parentElement;
    while (element) {
      if ("frycomponents" in element) {
        components = element.frycomponents;
        this._fryparent = components[components.length - 1];
        return this._fryparent;
      }
      element = element.parentElement;
    }
  }
  get fryroot() {
    let element = this.fryelement;
    let component = this;
    if (!element.isConnected) {
      this._fryroot = null;
      return null;
    }
    if (this._fryroot) return this._fryroot;
    while (element) {
      if ("frycomponents" in element) {
        component = element.frycomponents[0];
      }
      element = element.parentElement;
    }
    this._fryroot = component;
    return component;
  }
};
async function hydrate(domContainer, rootArgs) {
  const g = {
    readyFns: [],
    isReady: false,
    g: {}
  };
  const components = {};
  const complist = [];
  const scripts = {};
  for (const script of document.querySelectorAll("script[data-fryid]")) {
    scripts[script.dataset.fryid] = script;
  }
  function collect(element) {
    if (element.tagName === "SCRIPT") {
      return;
    } else if (element.tagName === "TEMPLATE") {
      return;
    } else {
      if (element.dataset && "fryid" in element.dataset) {
        for (const cid of element.dataset.fryid.split(" ")) {
          if (cid in components) {
            throw `duplicate component id ${cid}`;
          }
          if (!(cid in scripts)) {
            throw `unknown component id ${cid}`;
          }
          const script = scripts[cid];
          const { args, refs } = JSON.parse(script.textContent);
          const { fryname: name, fryurl: url } = script.dataset;
          if (complist.length === 0 && args) {
            Object.assign(args, rootArgs);
          }
          let comp = components[cid] = new Component({ cid, name, url, args, refs, element, g });
          complist.push(comp);
          if (!("frycomponents" in element)) {
            element.frycomponents = [comp];
          } else {
            element.frycomponents.push(comp);
          }
        }
      }
      for (const child of element.children) {
        collect(child);
      }
    }
  }
  collect(domContainer);
  const embedElements = domContainer.querySelectorAll("[data-fryref]:not(script)");
  for (const element of embedElements) {
    const refs = element.dataset.fryref;
    for (const ref of refs.split(" ")) {
      const [name, cid] = ref.split("-");
      const component = components[cid];
      if (name.endsWith(":a")) {
        const rname = name.slice(0, -2);
        if (rname in component.fryargs) {
          component.fryargs[rname].push(element);
        } else {
          component.fryargs[rname] = [element];
        }
      } else {
        component.fryargs[name] = element;
      }
    }
  }
  for (const comp of complist) {
    let templator = function(subid) {
      const template = domContainer.querySelector(`[data-frytid="${subid}"]`);
      const create = async (args) => {
        let clone = template.content.cloneNode(true);
        await hydrate(clone, args);
        return clone.firstElementChild.frycomponents[0];
      };
      return { template, create };
    };
    for (const name in comp.fryrefs) {
      const value = comp.fryrefs[name];
      let rname = name;
      let f = (subid) => components[subid];
      if (name.startsWith("t:")) {
        rname = name.slice(2);
        f = templator;
      }
      if (Array.isArray(value)) {
        comp.fryargs[rname] = value.map((subid) => f(subid));
      } else {
        comp.fryargs[rname] = f(value);
      }
    }
  }
  function doHydrate(component) {
    const prefix = "" + component.fryid + "/";
    const embedValues = component.fryembeds;
    function handle(element) {
      if ("fryembed" in element.dataset) {
        const embeds = element.dataset.fryembed;
        for (const embed of embeds.split(" ")) {
          if (!embed.startsWith(prefix)) {
            continue;
          }
          const [embedId, atype, ...args] = embed.substr(prefix.length).split("-");
          const index = parseInt(embedId);
          const arg = args.join("-");
          if (index >= embedValues.length) {
            console.log("invalid embed id: ", embedId);
            continue;
          }
          const value = embedValues[index];
          if (atype === "text") {
            if (value instanceof Signal || value instanceof Computed) {
              effect(() => element.textContent = value.value);
            } else {
              element.textContent = value;
            }
          } else if (atype === "html") {
            if (value instanceof Signal || value instanceof Computed) {
              effect(() => element.innerHTML = value.value);
            } else {
              element.innerHTML = value;
            }
          } else if (atype === "event") {
            element.addEventListener(arg, value);
          } else if (atype === "attr") {
            if (value instanceof Signal || value instanceof Computed) {
              effect(() => element.setAttribute(arg, value.value));
            } else {
              element.setAttribute(arg, value);
            }
          } else if (atype === "object") {
            if (!("frydata" in element)) {
              element.frydata = {};
            }
            element.frydata[arg] = value;
          } else {
            console.log("invalid attribute type: ", atype);
          }
        }
      }
      for (const child of element.children) {
        handle(child);
      }
    }
    handle(component.fryelement);
  }
  for (const comp of complist) {
    if (typeof comp.fryurl === "undefined") {
      continue;
    }
    const { setup } = await import(comp.fryurl);
    const boundSetup = setup.bind(comp);
    await boundSetup();
    doHydrate(comp);
  }
  for (const fn of g.readyFns) {
    fn();
  }
  g.readyFns.length = 0;
  g.isReady = true;
}

export {
  hydrate
};
