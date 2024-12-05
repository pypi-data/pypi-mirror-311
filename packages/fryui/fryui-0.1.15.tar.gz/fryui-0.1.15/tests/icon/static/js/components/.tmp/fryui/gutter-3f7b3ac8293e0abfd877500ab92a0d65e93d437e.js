export { hydrate } from "fryhcs";
export const setup = async function () {
    let { bar, el, ish, isv, cursor, col, row, ncol, nrow, resizable, center } = this.fryargs;
    
        let dragging = false;
        let cols = [];
        let rows = [];
        let pxcols = [];
        let pxrows = [];
        let colfr2px = 0;
        let rowfr2px = 0;
        let colpercent2px = 0;
        let rowpercent2px = 0;
        let colOffset1 = 0;
        let colOffset2 = 0;
        let colfrs = [];
        let colpercents = [];
        let rowOffset1 = 0;
        let rowOffset2 = 0;
        let rowfrs = [];
        let rowpercents = [];
        let colStart = 0;
        let colEnd = 0;
        let rowStart = 0;
        let rowEnd = 0;
        let contentSize = 0; // 除去gutter后的内容元素总px数，center中用
        let gridWidth, gridHeight, gridTop, gridBottom, gridLeft, gridRight;

        const columnPropName = 'grid-template-columns';
        const rowPropName = 'grid-template-rows';
        const bgColor = 'bg-primarya';
        const grid = el.parentElement;

        bar.classList.add('h-full');
        bar.classList.add('w-full');
        if (ish) {
            bar.classList.add('-top-3px');
            bar.classList.add('h-7px');
            bar.classList.remove('h-full');
        }
        if (isv) {
            bar.classList.add('-left-3px');
            bar.classList.add('w-7px');
            bar.classList.remove('w-full');
        }

        const numeric = (value, unit) => Number(value.slice(0, -1 * unit.length))
        const parseValue = function (value) {
            if (value.endsWith('px'))
                { return { value: value, type: 'px', numeric: numeric(value, 'px') } }
            if (value.endsWith('fr'))
                { return { value: value, type: 'fr', numeric: numeric(value, 'fr') } }
            if (value.endsWith('%'))
                { return { value: value, type: '%', numeric: numeric(value, '%') } }
            if (value === 'auto') { return { value: value, type: 'auto' } }
            return null
        }

        const unparseValue = v => v.value ? v.value : `${v.numeric}${v.type}`;
        const parse = rule => rule.split(' ').map(parseValue);
        const unparse = tracks => tracks.map(unparseValue).join(' ');

        const getColBegin = i => pxcols.slice(0,i).reduce((acc,v)=>acc+v.numeric, 0);
        const getColEnd = i => pxcols.slice(0,i+1).reduce((acc,v)=>acc+v.numeric, 0);
        const getRowBegin = i => pxrows.slice(0,i).reduce((acc,v)=>acc+v.numeric, 0);
        const getRowEnd = i => pxrows.slice(0,i+1).reduce((acc,v)=>acc+v.numeric, 0);
        const getMouseX = e => 'touches' in e ? e.touches[0].clientX : e.clientX;
        const getMouseY = e => 'touches' in e ? e.touches[0].clientY : e.clientY;

        const setColSize = (i, size) => {
            cols[i].value = null;
            if (cols[i].type === 'px') {
                cols[i].numeric = size;
            } else if (cols[i].type === 'fr') {
                if (colfrs.length === 1) {
                    cols[i].numeric = 1;
                } else if (colfr2px !== 0) {
                    cols[i].numeric = size / colfr2px;
                }
            } else if (cols[i].type === '%' && colpercent2px !== 0) {
                cols[i].numeric = size / colpercent2px;
            }
        }

        const setRowSize = (i, size) => {
            rows[i].value = null;
            if (rows[i].type === 'px') {
                rows[i].numeric = size;
            } else if (rows[i].type === 'fr') {
                if (rowfrs.length === 1) {
                    rows[i].numeric = 1;
                } else if (rowfr2px !== 0) {
                    rows[i].numeric = size / rowfr2px;
                }
            } else if (rows[i].type === '%' && rowpercent2px !== 0) {
                rows[i].numeric = size / rowpercent2px;
            }
        }

        const firstNonZero = (tracks, type) => {
            for (let i = 0; i < tracks.length; i++) {
                if (tracks[i].type == type && tracks[i].numeric > 0) {
                    return i
                }
            }
            return null
        }

        const NOOP = () => false

        const show = () => bar.classList.add(bgColor);
        const hide = () => bar.classList.remove(bgColor);

        const getGutterLine = () => {
            if (ncol === 1 || nrow === 1) {
                return [this];
            }
            const gutters = new Set();
            if (ish) for (let gutter of this.fryparent.hgutters(row)) {
                gutters.add(gutter);
            }
            if (isv) for (let gutter of this.fryparent.vgutters(col)) {
                gutters.add(gutter);
            }
            return gutters;
        }

        const setShow = () => {
            if (resizable) {
                const gutters = getGutterLine();
                gutters.forEach(gutter => gutter.show());
            }
        }
        const setHide = () => {
            if (!dragging && resizable) {
                const gutters = getGutterLine();
                gutters.forEach(gutter => gutter.hide());
            }
        }

        const initDrag = (e) => {
            const rect = grid.getBoundingClientRect();
            gridWidth = rect.width;
            gridHeight = rect.height;
            gridTop = rect.top;
            gridBottom = rect.bottom;
            gridLeft = rect.left;
            gridRight = rect.right;

            const mouseX = getMouseX(e);
            const mouseY = getMouseY(e);

            if (ish) {
                let prop = grid.style[rowPropName];
                if (prop) rows = parse(prop);

                prop = window.getComputedStyle(grid)[rowPropName];
                if (prop) {
                    pxrows = parse(prop);
                    if (this.centered) {
                        contentSize = pxrows[0].numeric + pxrows[2].numeric + pxrows[4].numeric;
                    }
                }

                rowOffset1 = mouseY - gridTop - getRowBegin(row);
                rowOffset2 = pxrows[row].numeric - rowOffset1;
                rowfrs = rows.filter(r => r.type === 'fr')
                rowpercents = rows.filter(r => r.type === '%')
                if (rowfrs.length) {
                    let r = firstNonZero(rows, 'fr')
                    if (r !== null)
                        rowfr2px = pxrows[r].numeric / rows[r].numeric;
                }
                if (rowpercents.length) {
                    let r = firstNonZero(rows, '%')
                    if (r !== null)
                        rowpercent2px = pxrows[r].numeric / rows[r].numeric;
                }
                rowStart = getRowBegin(row-1);
                rowEnd = getRowEnd(row+1);
            }

            if (isv) {
                let prop = grid.style[columnPropName];
                if (prop) cols = parse(prop);

                prop = window.getComputedStyle(grid)[columnPropName];
                if (prop) {
                    pxcols = parse(prop);
                    if (this.centered) {
                        contentSize = pxcols[0].numeric + pxcols[2].numeric + pxcols[4].numeric;
                    }
                }
                
                colOffset1 = mouseX - gridLeft - getColBegin(col);
                colOffset2 = pxcols[col].numeric - colOffset1;
                colfrs = cols.filter(c => c.type === 'fr')
                colpercents = cols.filter(c => c.type === '%')
                if (colfrs.length) {
                    let c = firstNonZero(cols, 'fr')
                    if (c !== null)
                        colfr2px = pxcols[c].numeric / cols[c].numeric;
                }
                if (colpercents.length) {
                    let c = firstNonZero(cols, '%')
                    if (c !== null)
                        colpercent2px = pxcols[c].numeric / cols[c].numeric;
                }
                colStart = getColBegin(col-1);
                colEnd = getColEnd(col+1);
            }
        }

        const startDrag = (e) => {
            if (!resizable) return
            if ('button' in e && e.button !== 0)
                return
            e.preventDefault();
            initDrag(e);
            dragging = true;
            window.addEventListener('mouseup', stopDrag);
            window.addEventListener('touchend', stopDrag);
            window.addEventListener('touchcancel', stopDrag);
            window.addEventListener('mousemove', drag);
            window.addEventListener('touchmove', drag);
            document.documentElement.classList.add(cursor)

            grid.addEventListener('selectstart', NOOP);
            grid.addEventListener('dragstart', NOOP);

            grid.style.userSelect = 'none';
            grid.style.webkitUserSelect = 'none';
            grid.style.MozUserSelect = 'none';
            grid.style.pointerEvents = 'none';
            setShow();
        }

        const drag = e => {
            if (ish) {
                let mouseY = getMouseY(e);
                const minPos = gridTop + rowStart + rowOffset1;
                const maxPos = gridTop + rowEnd - rowOffset2;
                if (mouseY < minPos) mouseY = minPos;
                if (mouseY > maxPos) mouseY = maxPos;
                if (this.centered) {
                    let sideSize = 0;
                    let centerSize = 0;
                    // row is 1 or row is 3
                    if (row === 1) {
                        sideSize = mouseY - minPos;
                    } else {
                        sideSize = maxPos - mouseY;
                    }
                    centerSize = contentSize - 2*sideSize;
                    setRowSize(0, sideSize);
                    setRowSize(2, centerSize);
                    setRowSize(4, sideSize);
                } else {
                    setRowSize(row-1, mouseY-minPos);
                    setRowSize(row+1, maxPos-mouseY);
                }
                grid.style[rowPropName] = unparse(rows);
            }
            if (isv) {
                let mouseX = getMouseX(e);
                const minPos = gridLeft + colStart + colOffset1;
                const maxPos = gridLeft + colEnd - colOffset2;
                if (mouseX < minPos) mouseX = minPos;
                if (mouseX > maxPos) mouseX = maxPos;
                if (this.centered) {
                    let sideSize = 0;
                    let centerSize = 0;
                    // col is 1 or col is 3
                    if (col === 1) {
                        sideSize = mouseX - minPos;
                    } else {
                        sideSize = maxPos - mouseX;
                    }
                    centerSize = contentSize - 2*sideSize;
                    setColSize(0, sideSize);
                    setColSize(2, centerSize);
                    setColSize(4, sideSize);
                } else {
                    setColSize(col-1, mouseX-minPos);
                    setColSize(col+1, maxPos-mouseX);
                }
                grid.style[columnPropName] = unparse(cols);
            }
        }

        const stopDrag = () => {
            dragging = false;
            window.removeEventListener('mouseup', stopDrag);
            window.removeEventListener('touchend', stopDrag);
            window.removeEventListener('touchcancel', stopDrag);
            window.removeEventListener('mousemove', drag);
            window.removeEventListener('touchmove', drag);
            document.documentElement.classList.remove(cursor)

            grid.removeEventListener('selectstart', NOOP);
            grid.removeEventListener('dragstart', NOOP);

            grid.style.userSelect = '';
            grid.style.webkitUserSelect = '';
            grid.style.MozUserSelect = '';
            grid.style.pointerEvents = '';
            setHide();
        }

        this.centered = center;
        this.show = show;
        this.hide = hide;
        this.col = col;
        this.row = row;
        this.ish = ish;
        this.isv = isv;
    
    this.fryembeds = [setShow, setHide, startDrag, startDrag];
};
