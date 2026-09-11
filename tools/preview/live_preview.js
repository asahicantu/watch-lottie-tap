// Live preview client: polls the dev server for the currently-built critter,
// renders it with lottie-web, and lets you browse + live-edit the animation's
// layers/groups/shapes in the browser. Edits only ever touch the in-memory
// copy of the JSON (`workingData`) - they never touch the .py source, and a
// rebuild from disk (editing the critter file) replaces them. Use "export
// json" to pull a snapshot out, or "reset edits" to throw them away.

let anim = null, animSmall = null, version = -1, playing = true, current = null;
let sourceData = null;   // last animation fetched from the server, untouched
let workingData = null;  // deep clone of sourceData that the inspector edits
let dirty = false;
let selectedPath = null; // e.g. ["layers", 0, "shapes", 2, "it", 0]
let selectedKind = null; // "layer" | "gr"
let applyTimer = null;

const stage = document.getElementById("stage");
const stageSmall = document.getElementById("stageSmall");
const pick = document.getElementById("pick");
const errBox = document.getElementById("err");
const status = document.getElementById("status");
const frame = document.getElementById("frame");
const frameLabel = document.getElementById("frameLabel");
const dirtyFlag = document.getElementById("dirtyFlag");

// --------------------------------------------------------------------------- //
// mounting / playback
// --------------------------------------------------------------------------- //

function mount(data, keepFrame) {
  [anim, animSmall].forEach(a => a && a.destroy());
  const opts = { renderer: "svg", loop: true, autoplay: playing, animationData: data };
  anim = lottie.loadAnimation(Object.assign({ container: stage }, opts));
  animSmall = lottie.loadAnimation(Object.assign({ container: stageSmall }, opts));
  frame.max = Math.max(0, Math.round(data.op) - 1);
  anim.addEventListener("enterFrame", () => {
    if (!playing) return;
    frame.value = Math.round(anim.currentFrame);
    frameLabel.textContent = "frame " + frame.value;
  });
  const target = keepFrame != null ? keepFrame : (!playing ? +frame.value : null);
  if (target != null) seek(target);
}

function seek(f) {
  frameLabel.textContent = "frame " + f;
  [anim, animSmall].forEach(a => a && a.goToAndStop(f, true));
}

function scheduleApply() {
  if (applyTimer) clearTimeout(applyTimer);
  applyTimer = setTimeout(() => { applyTimer = null; applyEdits(); }, 60);
}

function applyEdits() {
  if (!workingData) return;
  mount(workingData, anim ? anim.currentFrame : 0);
}

function markDirty() {
  dirty = true;
  dirtyFlag.style.display = "inline";
}

// --------------------------------------------------------------------------- //
// server polling
// --------------------------------------------------------------------------- //

async function refresh(state) {
  const data = await (await fetch("/api/animation?name=" + state.name)).json();
  current = state.name;
  pick.value = state.name;
  document.getElementById("path").textContent = "tools/critters/" + state.name + ".py";
  sourceData = data;
  workingData = JSON.parse(JSON.stringify(data));
  dirty = false;
  dirtyFlag.style.display = "none";
  selectedPath = null;
  selectedKind = null;
  buildTree();
  renderProps();
  mount(workingData);
}

async function poll() {
  try {
    const state = await (await fetch("/api/state")).json();
    if (state.error) {
      errBox.style.display = "block";
      errBox.textContent = state.error;
      status.className = "bad";
      status.textContent = "build failed — showing last good version";
    } else {
      errBox.style.display = "none";
      status.className = "ok";
      status.textContent = "built in " + state.ms + " ms";
    }
    if (state.version !== version || state.name !== current) {
      version = state.version;
      if (!state.error || !anim) await refresh(state);
      else { pick.value = state.name; current = state.name; }
    }
  } catch (e) {
    status.className = "bad";
    status.textContent = "server gone";
  }
  setTimeout(poll, 300);
}

// --------------------------------------------------------------------------- //
// outliner: walks layers -> groups -> nested groups
//
// Every meaningful "part" of a critter (an eye, a pupil, a tuft, a tooth) is
// already an explicitly named `group()` in critter_parts.py / lottie_kit.py,
// so mirroring the group nesting here gives a free decomposition of the
// figure. Raw fills/strokes/shapes are leaves shown in the properties panel
// of their enclosing group rather than as their own tree rows.
// --------------------------------------------------------------------------- //

function getNode(path) {
  let node = workingData;
  for (const step of path) node = node[step];
  return node;
}

function childGroupsOf(node, path, kind) {
  const arr = kind === "layer" ? (node.shapes || []) : (node.it || []);
  const key = kind === "layer" ? "shapes" : "it";
  const out = [];
  arr.forEach((c, i) => { if (c.ty === "gr") out.push({ node: c, path: path.concat([key, i]) }); });
  return out;
}

function renderNode(node, path, kind) {
  const li = document.createElement("li");
  const row = document.createElement("div");
  row.className = "node-row";
  if (path.join(",") === (selectedPath || []).join(",")) row.classList.add("selected");

  const kids = childGroupsOf(node, path, kind);

  const twirl = document.createElement("span");
  twirl.className = "twirl";
  twirl.textContent = kids.length ? "▾" : "";
  row.appendChild(twirl);

  const cb = document.createElement("input");
  cb.type = "checkbox";
  cb.checked = !node.hd;
  cb.title = "visible";
  cb.onclick = (e) => {
    e.stopPropagation();
    node.hd = !cb.checked;
    markDirty();
    applyEdits();
    row.classList.toggle("hidden-part", !!node.hd);
  };
  row.appendChild(cb);

  const icon = document.createElement("span");
  icon.className = "icon";
  icon.textContent = kind === "layer" ? "🏞" : "📦";
  row.appendChild(icon);

  const nm = document.createElement("span");
  nm.className = "nm";
  nm.textContent = node.nm || (kind === "layer" ? "layer" : "group");
  row.appendChild(nm);

  if (node.hd) row.classList.add("hidden-part");
  row.onclick = () => selectNode(path, kind);
  li.appendChild(row);

  if (kids.length) {
    const ul = document.createElement("ul");
    kids.forEach(({ node: c, path: p }) => ul.appendChild(renderNode(c, p, "gr")));
    li.appendChild(ul);
  }
  return li;
}

function buildTree() {
  const tree = document.getElementById("tree");
  tree.innerHTML = "";
  if (!workingData) {
    tree.innerHTML = '<div class="empty">nothing built yet</div>';
    return;
  }
  const ul = document.createElement("ul");
  (workingData.layers || []).forEach((layer, i) => {
    ul.appendChild(renderNode(layer, ["layers", i], "layer"));
  });
  tree.appendChild(ul);
}

function selectNode(path, kind) {
  selectedPath = path;
  selectedKind = kind;
  buildTree();
  renderProps();
}

// --------------------------------------------------------------------------- //
// properties panel: identity, transform, and any fill/stroke/shape leaves
// directly inside the selected group
// --------------------------------------------------------------------------- //

function rgbaToHex(c) {
  return "#" + [c[0], c[1], c[2]].map(v =>
    Math.round(Math.max(0, Math.min(1, v)) * 255).toString(16).padStart(2, "0")
  ).join("");
}

function hexToRgba(hex, alpha) {
  const h = hex.replace("#", "");
  return [parseInt(h.slice(0, 2), 16) / 255, parseInt(h.slice(2, 4), 16) / 255,
          parseInt(h.slice(4, 6), 16) / 255, alpha == null ? 1 : alpha];
}

function flattenValue(prop) {
  if (prop.a === 0) return prop.k;
  const first = prop.k[0].s;
  return first.length === 1 ? first[0] : first.slice();
}

function animatedBadge(container, prop, onFlatten) {
  const badge = document.createElement("span");
  badge.className = "anim-badge";
  badge.textContent = "animated · " + prop.k.length + " keys ";
  const btn = document.createElement("button");
  btn.className = "small";
  btn.textContent = "flatten";
  btn.title = "Convert to a static value (using the first keyframe) so it can be edited";
  btn.onclick = () => { onFlatten(); };
  badge.appendChild(btn);
  container.appendChild(badge);
}

function numberField(container, label, prop, dims) {
  const field = document.createElement("div");
  field.className = "field";
  const lab = document.createElement("label");
  lab.textContent = label;
  field.appendChild(lab);

  if (prop.a === 1) {
    animatedBadge(field, prop, () => {
      const v = flattenValue(prop);
      prop.a = 0;
      prop.k = v;
      markDirty();
      applyEdits();
      renderProps();
    });
  } else {
    const wrap = document.createElement("div");
    wrap.className = "field-row";
    const values = dims > 1 ? prop.k.slice(0, dims) : [prop.k];
    values.forEach((v, idx) => {
      const inp = document.createElement("input");
      inp.type = "number";
      inp.step = "any";
      inp.value = v;
      inp.oninput = () => {
        const nv = parseFloat(inp.value);
        if (Number.isNaN(nv)) return;
        if (dims > 1) prop.k[idx] = nv; else prop.k = nv;
        markDirty();
        scheduleApply();
      };
      wrap.appendChild(inp);
    });
    field.appendChild(wrap);
  }
  container.appendChild(field);
}

function colorField(container, label, prop) {
  const field = document.createElement("div");
  field.className = "field";
  const lab = document.createElement("label");
  lab.textContent = label;
  field.appendChild(lab);

  if (prop.a === 1) {
    animatedBadge(field, prop, () => {
      const v = flattenValue(prop);
      prop.a = 0;
      prop.k = v;
      markDirty();
      applyEdits();
      renderProps();
    });
  } else {
    const wrap = document.createElement("div");
    wrap.className = "swatch-row";
    const inp = document.createElement("input");
    inp.type = "color";
    inp.value = rgbaToHex(prop.k);
    inp.oninput = () => {
      prop.k = hexToRgba(inp.value, prop.k[3]);
      markDirty();
      scheduleApply();
    };
    wrap.appendChild(inp);
    field.appendChild(wrap);
  }
  container.appendChild(field);
}

function subcard(title) {
  const card = document.createElement("div");
  card.className = "subcard";
  const h = document.createElement("h4");
  h.textContent = title;
  card.appendChild(h);
  return card;
}

function buildIdentityCard(node) {
  const card = subcard("identity");

  const nameField = document.createElement("div");
  nameField.className = "field";
  const nameLabel = document.createElement("label");
  nameLabel.textContent = "name";
  nameField.appendChild(nameLabel);
  const nameInput = document.createElement("input");
  nameInput.type = "text";
  nameInput.value = node.nm || "";
  nameInput.oninput = () => { node.nm = nameInput.value; markDirty(); buildTree(); };
  nameField.appendChild(nameInput);
  card.appendChild(nameField);

  const visField = document.createElement("div");
  visField.className = "field";
  const visLabel = document.createElement("label");
  const visCb = document.createElement("input");
  visCb.type = "checkbox";
  visCb.checked = !node.hd;
  visCb.style.marginRight = "6px";
  visCb.onchange = () => { node.hd = !visCb.checked; markDirty(); applyEdits(); buildTree(); };
  visLabel.appendChild(visCb);
  visLabel.appendChild(document.createTextNode("visible"));
  visField.appendChild(visLabel);
  card.appendChild(visField);

  const btnRow = document.createElement("div");
  btnRow.className = "row";
  btnRow.style.marginTop = "0";
  const isolateBtn = document.createElement("button");
  isolateBtn.className = "small";
  isolateBtn.textContent = "isolate";
  isolateBtn.title = "Hide every other part so only this one (and its children) show";
  isolateBtn.onclick = () => isolate(selectedPath);
  btnRow.appendChild(isolateBtn);
  const showAllBtn2 = document.createElement("button");
  showAllBtn2.className = "small";
  showAllBtn2.textContent = "show all";
  showAllBtn2.onclick = () => showAllParts();
  btnRow.appendChild(showAllBtn2);
  card.appendChild(btnRow);

  return card;
}

function buildTransformCard(tr) {
  const card = subcard("transform");
  numberField(card, "position", tr.p, Array.isArray(tr.p.k) ? Math.min(2, tr.p.k.length) : 2);
  numberField(card, "scale %", tr.s, 2);
  numberField(card, "rotation °", tr.r, 1);
  numberField(card, "opacity %", tr.o, 1);
  return card;
}

function buildFillCard(fl) {
  const card = subcard("fill");
  colorField(card, "color", fl.c);
  numberField(card, "opacity %", fl.o, 1);
  return card;
}

function buildStrokeCard(st) {
  const card = subcard("stroke");
  colorField(card, "color", st.c);
  numberField(card, "width", st.w, 1);
  numberField(card, "opacity %", st.o, 1);
  return card;
}

function buildEllipseCard(el) {
  const card = subcard("ellipse");
  numberField(card, "size", el.s, 2);
  numberField(card, "position", el.p, 2);
  return card;
}

function buildRectCard(rc) {
  const card = subcard("rect");
  numberField(card, "size", rc.s, 2);
  numberField(card, "position", rc.p, 2);
  numberField(card, "corner radius", rc.r, 1);
  return card;
}

function buildPathCard(sh) {
  const card = subcard("path");
  const v = sh.ks.a === 0 ? sh.ks.k.v : sh.ks.k[0].s.v;
  const info = document.createElement("div");
  info.className = "muted";
  info.textContent = (v ? v.length : 0) + " points · shape editing isn't supported here";
  card.appendChild(info);
  return card;
}

function renderProps() {
  const body = document.getElementById("propsBody");
  const title = document.getElementById("propsTitle");
  body.innerHTML = "";

  if (!selectedPath) {
    title.textContent = "Properties";
    body.innerHTML = '<div class="empty">Select a part on the left to inspect and edit it.</div>';
    return;
  }
  const node = getNode(selectedPath);
  if (!node) {
    selectedPath = null;
    return renderProps();
  }
  title.textContent = node.nm || selectedKind;

  body.appendChild(buildIdentityCard(node));

  if (selectedKind === "gr") {
    const tr = (node.it || []).find(i => i.ty === "tr");
    if (tr) body.appendChild(buildTransformCard(tr));
    (node.it || []).forEach(child => {
      if (child.ty === "fl") body.appendChild(buildFillCard(child));
      else if (child.ty === "st") body.appendChild(buildStrokeCard(child));
      else if (child.ty === "el") body.appendChild(buildEllipseCard(child));
      else if (child.ty === "rc") body.appendChild(buildRectCard(child));
      else if (child.ty === "sh") body.appendChild(buildPathCard(child));
    });
  } else if (selectedKind === "layer" && node.ks) {
    body.appendChild(buildTransformCard(node.ks));
  }
}

// --------------------------------------------------------------------------- //
// isolate / show-all: walk every group in the tree, keep the ones on the
// selected node's ancestor-or-descendant chain, hide the rest
// --------------------------------------------------------------------------- //

function collectGroups(root) {
  const out = [];
  function walkItem(node, path) {
    if (node.ty === "gr") {
      out.push({ node, path });
      (node.it || []).forEach((c, i) => walkItem(c, path.concat(["it", i])));
    }
  }
  (root.layers || []).forEach((layer, i) => {
    (layer.shapes || []).forEach((c, j) => walkItem(c, ["layers", i, "shapes", j]));
  });
  return out;
}

function isPrefix(a, b) {
  if (a.length > b.length) return false;
  for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return false;
  return true;
}

function isolate(path) {
  if (!path) return;
  collectGroups(workingData).forEach(({ node, path: p }) => {
    node.hd = !(isPrefix(p, path) || isPrefix(path, p));
  });
  markDirty();
  applyEdits();
  buildTree();
  renderProps();
}

function showAllParts() {
  collectGroups(workingData).forEach(({ node }) => { node.hd = false; });
  markDirty();
  applyEdits();
  buildTree();
  renderProps();
}

// --------------------------------------------------------------------------- //
// header controls
// --------------------------------------------------------------------------- //

document.getElementById("playBtn").onclick = (e) => {
  playing = !playing;
  e.target.textContent = playing ? "pause" : "play";
  [anim, animSmall].forEach(a => a && (playing ? a.play() : a.pause()));
};
document.getElementById("shapeBtn").onclick = (e) => {
  stage.classList.toggle("square");
  e.target.textContent = stage.classList.contains("square") ? "round" : "square";
};
frame.oninput = () => {
  if (playing) document.getElementById("playBtn").click();
  seek(+frame.value);
};
pick.onchange = () => fetch("/api/select?name=" + pick.value);
document.getElementById("showAllBtn").onclick = () => showAllParts();

document.getElementById("exportBtn").onclick = () => {
  if (!workingData) return;
  const blob = new Blob([JSON.stringify(workingData, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = (current || "animation") + ".json";
  a.click();
  URL.revokeObjectURL(url);
};

document.getElementById("resetBtn").onclick = () => {
  if (!sourceData) return;
  workingData = JSON.parse(JSON.stringify(sourceData));
  dirty = false;
  dirtyFlag.style.display = "none";
  selectedPath = null;
  selectedKind = null;
  buildTree();
  renderProps();
  mount(workingData);
};

(async () => {
  const names = await (await fetch("/api/names")).json();
  pick.innerHTML = names.map(n => `<option>${n}</option>`).join("");
  poll();
})();
