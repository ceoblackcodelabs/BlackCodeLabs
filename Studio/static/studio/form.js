/* Builds the document form from the server's schema and submits it as JSON.
   Everything the user types is read back through .value / textContent only (never innerHTML). */
(function () {
  const cfg = JSON.parse(document.getElementById('form-config').textContent);
  const root = document.getElementById('form-root');
  const banner = document.getElementById('banner');
  const saveBtn = document.getElementById('btn-save');
  let tree = [];          // top-level controls
  let dirty = false;

  const h = (tag, attrs, ...kids) => {
    const e = document.createElement(tag);
    Object.entries(attrs || {}).forEach(([k, v]) => { if (v === true) e.setAttribute(k, ''); else if (v !== false && v != null) e.setAttribute(k, v); });
    kids.flat().forEach((k) => k != null && e.append(k));
    return e;
  };
  const markDirty = () => { dirty = true; };

  // ---- a control = { node, get(), show(errors, path) }
  function leaf(spec, value, path) {
    let input;
    const ph = spec.placeholder || '';
    if (spec.kind === 'textarea') {
      input = h('textarea', { class: 'textarea', rows: 3, placeholder: ph });
      input.value = value || '';
      const grow = () => { input.style.height = 'auto'; input.style.height = Math.min(input.scrollHeight + 2, 360) + 'px'; };
      input.addEventListener('input', grow); setTimeout(grow, 0);
    } else if (spec.kind === 'select') {
      input = h('select', { class: 'select' }, h('option', { value: '' }, '—'), spec.choices.map((c) => h('option', { value: c }, c)));
      input.value = value || (spec.choices.length === 1 ? spec.choices[0] : '');
    } else {
      const type = spec.kind === 'date' ? 'date' : 'text';
      input = h('input', { class: 'input', type, placeholder: ph, inputmode: spec.kind === 'number' || spec.kind === 'money' ? 'decimal' : null, maxlength: spec.max_len || null });
      input.value = value == null ? '' : value;
    }
    input.addEventListener('input', markDirty);
    const err = h('div', { class: 'err', hidden: true });
    const node = h('div', { class: 'field' + (spec.kind === 'textarea' || spec.full ? ' full' : '') },
      h('label', null, spec.label, spec.required ? h('span', { class: 'req' }, ' *') : null), input, err,
      spec.help ? h('div', { class: 'help' }, spec.help) : null);
    return {
      node, get: () => input.value,
      show(errors, p) { const m = errors[p]; err.hidden = !m; err.textContent = m || ''; input.classList.toggle('invalid', !!m); return m ? input : null; },
      setLabelOnly(label) { node.querySelector('label').firstChild.textContent = label; }
    };
  }

  function groupControl(fields, value, path) {
    const kids = fields.map((f) => control(f, (value || {})[f.name], path + '.' + f.name));
    const node = h('div', { class: 'group' }, kids.map((k, i) => {
      if (fields[i].kind === 'list' || fields[i].kind === 'textarea') k.node.classList.add('full');
      return k.node;
    }));
    return {
      node,
      get: () => Object.fromEntries(fields.map((f, i) => [f.name, kids[i].get()])),
      show(errors, p) { let first = null; kids.forEach((k, i) => { const r = k.show(errors, p + '.' + fields[i].name); first = first || r; }); return first; }
    };
  }

  function listControl(spec, value, path) {
    const item = spec.item, rows = [];
    const wrap = h('div', { class: 'list' });
    const holder = h('div', { class: 'list' });
    const err = h('div', { class: 'err', hidden: true });
    const addBtn = h('button', { type: 'button', class: 'btn btn-sm add-row' }, '+ Add ' + (item.kind === 'group' ? 'row' : 'line'));

    const refresh = () => {
      holder.replaceChildren(...rows.map((r) => r.el));
      addBtn.hidden = !!(spec.max_items && rows.length >= spec.max_items);
      rows.forEach((r, i) => { r.up.disabled = i === 0; r.down.disabled = i === rows.length - 1; });
    };
    const addRow = (v, focus) => {
      const inner = item.kind === 'group' ? groupControl(item.fields, v, path + '.' + rows.length)
        : leaf(Object.assign({ label: '', placeholder: spec.placeholder }, item, { max_len: spec.max_len }), v, path);
      if (item.kind !== 'group') inner.node.querySelector('label').remove();
      const up = h('button', { type: 'button', class: 'icon-btn', title: 'Move up', 'aria-label': 'Move up' }, '↑');
      const down = h('button', { type: 'button', class: 'icon-btn', title: 'Move down', 'aria-label': 'Move down' }, '↓');
      const rm = h('button', { type: 'button', class: 'icon-btn rm', title: 'Remove', 'aria-label': 'Remove' }, '×');
      const el = h('div', { class: 'list-row' + (item.kind === 'group' ? '' : ' simple') }, inner.node, h('div', { class: 'row-tools' }, up, down, rm));
      const row = { el, inner, up, down };
      up.onclick = () => { const i = rows.indexOf(row); if (i > 0) { rows.splice(i - 1, 0, rows.splice(i, 1)[0]); refresh(); markDirty(); } };
      down.onclick = () => { const i = rows.indexOf(row); if (i < rows.length - 1) { rows.splice(i + 1, 0, rows.splice(i, 1)[0]); refresh(); markDirty(); } };
      rm.onclick = () => { rows.splice(rows.indexOf(row), 1); refresh(); markDirty(); };
      rows.push(row); refresh();
      if (focus) { const f = el.querySelector('input,textarea,select'); f && f.focus(); }
    };
    (Array.isArray(value) && value.length ? value : (spec.min_items ? [item.kind === 'group' ? {} : ''] : [])).forEach((v) => addRow(v));
    addBtn.onclick = () => { addRow(item.kind === 'group' ? {} : '', true); markDirty(); };

    const node = h('div', { class: 'field full' }, h('span', { class: 'lbl' }, spec.label, spec.min_items ? h('span', { class: 'req' }, ' *') : null), holder, err, addBtn,
      spec.help ? h('div', { class: 'help' }, spec.help) : null);
    return {
      node, get: () => rows.map((r) => r.inner.get()),
      show(errors, p) {
        const m = errors[p]; err.hidden = !m; err.textContent = m || '';
        let first = m ? node : null;
        rows.forEach((r, i) => { const x = r.inner.show(errors, p + '.' + i); first = first || x; });
        return first;
      }
    };
  }

  function control(spec, value, path) { return spec.kind === 'list' ? listControl(spec, value, path) : leaf(spec, value, path); }

  // ---- sections
  function build(values) {
    root.replaceChildren();
    tree = cfg.sections.map((sec, i) => {
      const kids = sec.fields.map((f) => control(f, values[f.name], f.name));
      const body = h('div', { class: 'fbody' }, kids.map((k, j) => { if (sec.fields[j].kind === 'list') k.node.classList.add('full'); return k.node; }));
      const det = h('details', { class: 'fsec', open: i < 3 || !cfg.sections.length }, h('summary', null, h('span', null, sec.title, sec.hint ? h('small', null, sec.hint) : null)), body);
      root.append(det);
      return { sec, kids, det };
    });
  }
  const collect = () => { const out = {}; tree.forEach((t) => t.sec.fields.forEach((f, i) => { out[f.name] = t.kids[i].get(); })); return out; };

  function showErrors(errors) {
    let first = null;
    tree.forEach((t) => t.sec.fields.forEach((f, i) => {
      const r = t.kids[i].show(errors, f.name);
      if (r && !first) first = r;
      if (r) t.det.open = true;
    }));
    const n = Object.keys(errors).length;
    banner.textContent = n ? 'Please fix ' + n + ' highlighted field' + (n > 1 ? 's' : '') + ' and try again.' : '';
    banner.classList.toggle('show', !!n);
    if (first) { const target = first.nodeType ? first : first; (target.scrollIntoView || (() => {})).call(target, { block: 'center', behavior: 'smooth' }); if (target.focus) target.focus({ preventScroll: true }); }
  }
  function showGeneral(msg) { banner.textContent = msg; banner.classList.add('show'); banner.scrollIntoView({ block: 'center', behavior: 'smooth' }); }

  // ---- toolbar
  const typeSelect = document.getElementById('type-select');
  if (!cfg.id) typeSelect.addEventListener('change', () => {
    if (!dirty || confirm('Switch document type? What you typed so far will be lost.')) { dirty = false; location.href = '?type=' + encodeURIComponent(typeSelect.value); }
    else typeSelect.value = cfg.type;
  });
  const sampleBtn = document.getElementById('btn-sample');
  if (cfg.sample && !cfg.id) {
    sampleBtn.hidden = false;
    sampleBtn.onclick = () => { if (!dirty || confirm('Replace the form with the example content?')) { build(cfg.sample); dirty = false; banner.classList.remove('show'); } };
  }
  document.getElementById('btn-reset').onclick = () => { if (!dirty || confirm('Discard your changes?')) { build(cfg.initial); dirty = false; banner.classList.remove('show'); } };
  window.addEventListener('beforeunload', (e) => { if (dirty) { e.preventDefault(); e.returnValue = ''; } });

  // ---- submit
  document.getElementById('doc-form').addEventListener('submit', async () => {
    saveBtn.disabled = true; const label = saveBtn.textContent; saveBtn.textContent = 'Generating…';
    banner.classList.remove('show');
    try {
      const res = await fetch(cfg.saveUrl, { method: 'POST', credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': window.STUDIO_CSRF },
        body: JSON.stringify({ type: cfg.type, id: cfg.id, data: collect() }) });
      const body = await res.json().catch(() => ({}));
      if (res.ok && body.ok) { dirty = false; location.href = body.url; return; }
      if (res.status === 422 && body.errors) showErrors(body.errors); else showGeneral(body.error || 'Something went wrong (' + res.status + ').');
    } catch (e) { showGeneral('Could not reach the server. Check your connection and try again.'); }
    saveBtn.disabled = false; saveBtn.textContent = label;
  });

  build(cfg.initial || {});
  dirty = false;
})();
