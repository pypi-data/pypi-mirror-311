const {
  SvelteComponent: v,
  append: c,
  attr: r,
  detach: d,
  element: u,
  init: g,
  insert: m,
  noop: f,
  safe_not_equal: j,
  set_data: p,
  text: y,
  toggle_class: a
} = window.__gradio__svelte__internal;
function b(t) {
  let e, s, i = _(
    /*value*/
    t[0]
  ) + "", o;
  return {
    c() {
      e = u("div"), s = u("pre"), o = y(i), r(s, "class", "svelte-4kwjdv"), r(e, "class", "svelte-4kwjdv"), a(
        e,
        "table",
        /*type*/
        t[1] === "table"
      ), a(
        e,
        "gallery",
        /*type*/
        t[1] === "gallery"
      ), a(
        e,
        "selected",
        /*selected*/
        t[2]
      );
    },
    m(n, l) {
      m(n, e, l), c(e, s), c(s, o);
    },
    p(n, [l]) {
      l & /*value*/
      1 && i !== (i = _(
        /*value*/
        n[0]
      ) + "") && p(o, i), l & /*type*/
      2 && a(
        e,
        "table",
        /*type*/
        n[1] === "table"
      ), l & /*type*/
      2 && a(
        e,
        "gallery",
        /*type*/
        n[1] === "gallery"
      ), l & /*selected*/
      4 && a(
        e,
        "selected",
        /*selected*/
        n[2]
      );
    },
    i: f,
    o: f,
    d(n) {
      n && d(e);
    }
  };
}
function _(t) {
  if (!t || !t.positions || !t.colors) return "Empty point cloud";
  const e = t.positions.map((s, i) => {
    const o = t.colors[i];
    return `(${s.join(", ")}) RGB(${o.join(", ")})`;
  });
  return e.length > 3 ? `${e.slice(0, 3).join(`
`)}...` : e.join(`
`);
}
function w(t, e, s) {
  let { value: i } = e, { type: o } = e, { selected: n = !1 } = e;
  return t.$$set = (l) => {
    "value" in l && s(0, i = l.value), "type" in l && s(1, o = l.type), "selected" in l && s(2, n = l.selected);
  }, [i, o, n];
}
class h extends v {
  constructor(e) {
    super(), g(this, e, w, b, j, { value: 0, type: 1, selected: 2 });
  }
}
export {
  h as default
};
