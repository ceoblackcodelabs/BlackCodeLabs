/* Dashboard charts. Colours/specs follow the dataviz reference palette (dark mode):
   categorical slots 1-3 (blue, orange, aqua) validated all-pairs on surface #1a1a19. */
(function () {
  if (!window.Chart) return;
  const data = JSON.parse(document.getElementById('chart-data').textContent);
  const css = getComputedStyle(document.documentElement);
  const v = (n) => css.getPropertyValue(n).trim();
  const SURFACE = v('--surface-1'), TEXT = v('--text'), TEXT2 = v('--text-2'), MUTED = v('--text-3');
  const GRID = 'rgba(255,255,255,.07)';
  const SERIES = [v('--series-1'), v('--series-2'), v('--series-3')];
  const fmt = new Intl.NumberFormat('en-KE');
  const compact = (n) => (n >= 1e6 ? (n / 1e6).toFixed(n % 1e6 ? 1 : 0) + 'M' : n >= 1e3 ? (n / 1e3).toFixed(n % 1e3 ? 1 : 0) + 'K' : String(n));

  Chart.defaults.font.family = v('--font') || 'sans-serif';
  Chart.defaults.font.size = 12;
  Chart.defaults.color = MUTED;
  Chart.defaults.animation = { duration: 350 };

  // Tooltip: value leads (strong), label follows (secondary), line key not a box
  const tooltip = (valueFmt) => ({
    backgroundColor: '#0e0e0d', borderColor: '#3a3a36', borderWidth: 1, padding: 10, cornerRadius: 8,
    titleColor: TEXT2, titleFont: { weight: '400', size: 11 }, bodyColor: TEXT, boxPadding: 4,
    usePointStyle: true, callbacks: { label: (c) => ' ' + valueFmt(c.parsed.y ?? c.parsed.x) + '  ' + (c.dataset.label || '') }
  });
  const scaleY = (extra) => Object.assign({
    beginAtZero: true, border: { display: false }, grid: { color: GRID, lineWidth: 1, drawTicks: false },
    ticks: { color: MUTED, padding: 8, callback: (n) => compact(n) }
  }, extra || {});
  const scaleX = (extra) => Object.assign({ border: { color: GRID }, grid: { display: false }, ticks: { color: MUTED, maxRotation: 0, autoSkipPadding: 14 } }, extra || {});

  const table = (el, head, rows) => {
    const t = document.createElement('table');
    const hr = t.createTHead().insertRow();
    head.forEach((h, i) => { const th = document.createElement('th'); th.textContent = h; if (i) th.className = 'num'; hr.appendChild(th); });
    const tb = t.createTBody();
    rows.forEach((r) => { const tr = tb.insertRow(); r.forEach((c, i) => { const td = tr.insertCell(); td.textContent = c; if (i) td.className = 'num'; }); });
    el.appendChild(t);
  };

  // ---- 1. stacked columns: documents per month by type
  const m = data.by_month;
  const legend = document.getElementById('lg-month');
  m.series.forEach((s, i) => {
    const item = document.createElement('span');
    const sw = document.createElement('i'); sw.style.background = SERIES[i % 3];
    item.appendChild(sw); item.appendChild(document.createTextNode(s.label));
    legend.appendChild(item);
  });
  new Chart(document.getElementById('ch-month'), {
    type: 'bar',
    data: {
      labels: m.labels,
      datasets: m.series.map((s, i) => ({
        label: s.label, data: s.data, backgroundColor: SERIES[i % 3], hoverBackgroundColor: SERIES[i % 3],
        borderColor: SURFACE, borderWidth: 2, borderSkipped: false, maxBarThickness: 24,
        borderRadius: i === m.series.length - 1 ? { topLeft: 4, topRight: 4 } : 0
      }))
    },
    options: {
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      scales: { x: scaleX({ stacked: true }), y: scaleY({ stacked: true, ticks: { precision: 0, color: MUTED, padding: 8, callback: (n) => Number.isInteger(n) ? n : '' } }) },
      plugins: { legend: { display: false }, tooltip: tooltip((n) => n) }
    }
  });
  table(document.getElementById('tv-month'), ['Month'].concat(m.series.map((s) => s.label)),
    m.labels.map((l, i) => [l].concat(m.series.map((s) => s.data[i]))));

  // ---- 2. value by status (single measure, single hue)
  const s = data.by_status;
  new Chart(document.getElementById('ch-status'), {
    type: 'bar',
    data: { labels: s.labels, datasets: [{ label: 'KES', data: s.data, backgroundColor: SERIES[0], hoverBackgroundColor: '#5598e7', maxBarThickness: 22, borderRadius: { topRight: 4, bottomRight: 4 }, borderSkipped: 'start' }] },
    options: {
      indexAxis: 'y', maintainAspectRatio: false,
      layout: { padding: { right: 56 } },
      scales: { x: scaleY({ ticks: { color: MUTED, callback: (n) => compact(n) } }), y: { border: { display: false }, grid: { display: false }, ticks: { color: TEXT2 } } },
      plugins: { legend: { display: false }, tooltip: tooltip((n) => 'KES ' + fmt.format(n)) }
    },
    plugins: [{ // value at the tip of each bar (skipped when zero)
      id: 'tipLabels',
      afterDatasetsDraw(chart) {
        const { ctx } = chart; ctx.save(); ctx.fillStyle = TEXT; ctx.font = '500 12px ' + Chart.defaults.font.family; ctx.textBaseline = 'middle';
        chart.getDatasetMeta(0).data.forEach((bar, i) => { const val = s.data[i]; if (val) ctx.fillText('KES ' + compact(val), bar.x + 8, bar.y); });
        ctx.restore();
      }
    }]
  });
  table(document.getElementById('tv-status'), ['Status', 'Value (KES)'], s.labels.map((l, i) => [l, fmt.format(s.data[i])]));

  // ---- 3. inquiries per day (line, hairline crosshair)
  const q = data.inquiries;
  const crosshair = {
    id: 'crosshair',
    afterDraw(chart) {
      const a = chart.tooltip && chart.tooltip.getActiveElements && chart.tooltip.getActiveElements();
      if (!a || !a.length) return;
      const { ctx, chartArea: { top, bottom } } = chart; const x = a[0].element.x;
      ctx.save(); ctx.strokeStyle = 'rgba(255,255,255,.25)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(x, top); ctx.lineTo(x, bottom); ctx.stroke(); ctx.restore();
    }
  };
  const VIOLET = v('--series-7');
  new Chart(document.getElementById('ch-inq'), {
    type: 'line',
    data: { labels: q.labels, datasets: [{ label: 'Inquiries', data: q.data, borderColor: VIOLET, backgroundColor: 'rgba(144,133,233,.10)', fill: true, borderWidth: 2, tension: 0,
      pointRadius: 0, pointHoverRadius: 5, pointHitRadius: 24, pointHoverBackgroundColor: VIOLET, pointHoverBorderColor: SURFACE, pointHoverBorderWidth: 2 }] },
    options: {
      maintainAspectRatio: false, interaction: { mode: 'index', intersect: false },
      scales: { x: scaleX({ ticks: { color: MUTED, maxRotation: 0, autoSkip: true, maxTicksLimit: 10 } }), y: scaleY({ ticks: { precision: 0, color: MUTED, padding: 8, callback: (n) => Number.isInteger(n) ? n : '' } }) },
      plugins: { legend: { display: false }, tooltip: tooltip((n) => n) }
    },
    plugins: [crosshair]
  });
  table(document.getElementById('tv-inq'), ['Day', 'Inquiries'], q.labels.map((l, i) => [l, q.data[i]]));
})();
