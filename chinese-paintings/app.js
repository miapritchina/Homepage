/* Ink & Silk — gallery, filters and deep-zoom viewer. No build step. */
(() => {
'use strict';
const $ = s => document.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const store = {
  get(k, d) { try { return JSON.parse(localStorage.getItem('inksilk.' + k)) ?? d; } catch { return d; } },
  set(k, v) { try { localStorage.setItem('inksilk.' + k, JSON.stringify(v)); } catch {} }
};

const DYN = ['Six Dynasties','Sui','Tang','Five Dynasties','Liao','Northern Song','Song (general)','Jin','Southern Song','Yuan','Ming','Qing','Unknown'];
const DYN_ZH = {'Six Dynasties':'六朝','Sui':'隋','Tang':'唐','Five Dynasties':'五代','Liao':'遼','Northern Song':'北宋','Song (general)':'宋','Jin':'金','Southern Song':'南宋','Yuan':'元','Ming':'明','Qing':'清'};
const GENRE_ZH = {'Landscape':'山水','Bird-and-flower':'花鳥','Figure':'人物','Animals':'走獸','Other':'其他'};
const SCHOOL_ORDER = ['Six Dynasties & Tang masters','Five Dynasties masters','Northern Song landscape','Song Academy','Song literati','Jin dynasty','Southern Song Academy','Southern Song literati & Chan','Chan painting','Ningbo Buddhist workshops','Yuan literati','Four Yuan Masters','Ming court','Zhe school','Ming figure painting','Wu school','Songjiang school','Late Ming innovators','Anhui school','Nanjing school','Individualists','Orthodox school','Qing court','Yangzhou professionals','Yangzhou Eccentrics','Mid-late Qing','Lingnan precursors','Shanghai school'];

let ALL = [], NOTES = {}, ARTISTS = {}, VIEW = [], shown = 0;
const PAGE = 90;
const favs = new Set(store.get('favs', []));
const F = {}; // facet key -> Set
let yr = [300, 1912], q = '', sort = store.get('sort', 'chron'), seed = Math.random();

/* ---------- facet definitions ---------- */
const FACETS = [
  {k:'avail', label:'Availability', get:r => [r.lo ? 'Link only (no-copy museum)' : 'Zoomable here'], chips:true, open:false},
  {k:'fav', label:'My favourites', get:r => favs.has(r.i) ? ['♥ Favourites'] : [], chips:true},
  {k:'notes', label:'Guided notes', get:r => NOTES[r.i] ? ['With pinned notes'] : [], chips:true},
  {k:'dyn', label:'Era · dynasty', get:r => [r.d], order:DYN, zh:DYN_ZH, open:true},
  {k:'cent', label:'Century', get:r => r.c ? [r.c] : [], order:null, sortNum:true},
  {k:'genre', label:'Subject', get:r => r.g || [], zh:GENRE_ZH, open:true, chips:true},
  {k:'tags', label:'Theme', get:r => r.tg || []},
  {k:'season', label:'Season', get:r => r.se || [], chips:true, order:['Spring','Summer','Autumn','Winter']},
  {k:'painter', label:'Painter', get:r => [r.a], search:true, top:25},
  {k:'school', label:'School · movement', get:r => r.s ? [r.s] : ['Unassigned'], order:SCHOOL_ORDER.concat(['Unassigned'])},
  {k:'approach', label:'Approach', get:r => r.ap ? [r.ap] : [], chips:true},
  {k:'palette', label:'Ink & colour', get:r => r.p || [], chips:true},
  {k:'support', label:'Material', get:r => r.su ? [r.su] : [], chips:true},
  {k:'format', label:'Format', get:r => r.f ? [r.f] : [], chips:true},
  {k:'attr', label:'Attribution', get:r => r.at ? [r.at] : []},
  {k:'res', label:'Image detail', get:r => [resClass(r)], order:['Gigapixel-class (40 MP+)','Very high (15–40 MP)','High (5–15 MP)','Standard (under 5 MP)','Size unknown'], chips:false},
  {k:'museum', label:'Collection', get:r => [r.m], search:true, top:12},
];
function resClass(r){ if (r.lo) return 'Link only'; const m = r.mp; if (!m) return 'Size unknown'; if (m >= 40) return 'Gigapixel-class (40 MP+)'; if (m >= 15) return 'Very high (15–40 MP)'; if (m >= 5) return 'High (5–15 MP)'; return 'Standard (under 5 MP)'; }
const expanded = {}; const fsearch = {};

/* ---------- load ---------- */
Promise.all([
  fetch('data/paintings.json').then(r => r.json()),
  fetch('data/notes.json').then(r => r.ok ? r.json() : {}).catch(() => ({})),
  fetch('data/artists.json').then(r => r.ok ? r.json() : {}).catch(() => ({})),
]).then(([p, n, a]) => {
  ALL = p; NOTES = n; ARTISTS = a;
  ALL.forEach((r, ix) => { r._ix = ix; r._s = [r.t, r.z, r.a, r.az, r.m, r.s, (r.tg||[]).join(' '), r.md, r.d].join(' ').toLowerCase(); });
  readHash(true);
  $('#sort').value = sort;
  $('#sub').textContent = `${ALL.filter(r=>!r.lo).length.toLocaleString()} zoomable paintings · Chinese painting to 1912`;
  update();
  if (innerWidth <= 820) toggleFilters(false);
});

/* ---------- filtering ---------- */
function passes(r, skip) {
  if (q && !q.split(/\s+/).every(w => r._s.includes(w))) return false;
  if (skip !== 'yr' && r.y1 != null && (r.y2 < yr[0] || r.y1 > yr[1])) return false;
  for (const f of FACETS) {
    if (f.k === skip) continue;
    const s = F[f.k]; if (!s || !s.size) continue;
    const v = f.get(r) || [];
    if (!v.some(x => s.has(x))) return false;
  }
  return true;
}
function update(keepScroll) {
  VIEW = ALL.filter(r => passes(r));
  const by = {
    chron: (a, b) => (a.y1 ?? 9999) - (b.y1 ?? 9999) || (a.lo?1:0) - (b.lo?1:0),
    chronr: (a, b) => (b.y1 ?? -1) - (a.y1 ?? -1),
    artist: (a, b) => (a.a === 'Unidentified artist') - (b.a === 'Unidentified artist') || a.a.localeCompare(b.a) || (a.y1??0) - (b.y1??0),
    mp: (a, b) => (b.mp ?? 0) - (a.mp ?? 0),
    shuffle: (a, b) => hash(a.i) - hash(b.i),
  }[sort];
  VIEW.sort(by);
  $('#count').textContent = `${VIEW.length.toLocaleString()} paintings`;
  renderFacets(); renderActive();
  shown = 0; $('#grid').innerHTML = '';
  if (!VIEW.length) $('#grid').innerHTML = '<div class="empty">Nothing matches. Try removing a filter.</div>';
  more();
  if (!keepScroll) scrollTo({top: 0});
  writeHash();
}
function hash(s) { let h = Math.floor(seed * 1e9); for (const c of s) h = (h * 31 + c.charCodeAt(0)) | 0; return h; }

/* ---------- sidebar ---------- */
function counts(f) {
  const m = new Map();
  for (const r of ALL) { if (!passes(r, f.k)) continue; for (const v of (f.get(r) || [])) m.set(v, (m.get(v) || 0) + 1); }
  return m;
}
function renderFacets() {
  const open = {}; document.querySelectorAll('#facets details').forEach(d => open[d.dataset.k] = d.open);
  let h = '';
  // year range
  h += `<details class="facet" data-k="yr" ${open.yr ?? true ? 'open' : ''}><summary>Years<span class="n-on">${yr[0] > 300 || yr[1] < 1912 ? `${yr[0]}–${yr[1]}` : ''}</span></summary>
    <div class="range"><div class="vals"><span id="y0v">${fmtY(yr[0])}</span><span id="y1v">${fmtY(yr[1])}</span></div>
    <input id="y0" type="range" min="300" max="1912" step="10" value="${yr[0]}" aria-label="From year">
    <input id="y1" type="range" min="300" max="1912" step="10" value="${yr[1]}" aria-label="To year"></div></details>`;
  for (const f of FACETS) {
    const c = counts(f); const sel = F[f.k] || new Set();
    let vals = [...new Set([...c.keys(), ...sel])];
    if (f.order) vals.sort((a, b) => idx(f.order, a) - idx(f.order, b));
    else if (f.sortNum) vals.sort((a, b) => parseInt(a) - parseInt(b));
    else vals.sort((a, b) => (c.get(b) || 0) - (c.get(a) || 0) || a.localeCompare(b));
    if (f.k === 'painter') vals = vals.filter(v => v !== 'Unidentified artist').concat(vals.includes('Unidentified artist') ? ['Unidentified artist'] : []);
    if (f.search && fsearch[f.k]) { const s = fsearch[f.k].toLowerCase(); vals = vals.filter(v => (v + ' ' + (ARTISTS[v]?.zh || '')).toLowerCase().includes(s)); }
    const limit = f.top && !expanded[f.k] && !fsearch[f.k] ? f.top : 1e9;
    const list = vals.filter(v => sel.has(v) || (c.get(v) || 0) > 0 || f.order).slice(0, Math.max(limit, sel.size));
    if (!vals.length && !sel.size) continue;
    const isOpen = open[f.k] ?? !!f.open;
    h += `<details class="facet" data-k="${f.k}" ${isOpen ? 'open' : ''}><summary>${f.label}<span class="n-on">${sel.size || ''}</span></summary>`;
    if (f.search) h += `<input class="fsearch" data-k="${f.k}" placeholder="Find ${f.label.toLowerCase()}…" value="${esc(fsearch[f.k] || '')}">`;
    h += `<div class="opts ${f.chips ? 'chips' : ''}">`;
    for (const v of list) {
      const n = c.get(v) || 0; const z = f.zh?.[v] || (f.k === 'painter' ? ARTISTS[v]?.zh : '') || '';
      h += `<button class="opt ${sel.has(v) ? 'on' : ''} ${n ? '' : 'zero'}" data-k="${f.k}" data-v="${esc(v)}">${esc(v)}${z ? ` <span class="z">${esc(z)}</span>` : ''}<span class="c">${n}</span></button>`;
    }
    h += `</div>`;
    if (limit < vals.length) h += `<button class="showall" data-k="${f.k}">Show all ${vals.length}</button>`;
    h += `</details>`;
  }
  const fs = document.activeElement?.classList.contains('fsearch') ? document.activeElement.dataset.k : null;
  $('#facets').innerHTML = h;
  if (fs) { const el = document.querySelector(`.fsearch[data-k="${fs}"]`); el.focus(); el.setSelectionRange(el.value.length, el.value.length); }
}
const idx = (o, v) => { const i = o.indexOf(v); return i < 0 ? 999 : i; };
const fmtY = y => y < 0 ? `${-y} BCE` : `${y}`;
function renderActive() {
  let h = '';
  if (q) h += `<button data-clear="q">“${esc(q)}” ✕</button>`;
  if (yr[0] > 300 || yr[1] < 1912) h += `<button data-clear="yr">${yr[0]}–${yr[1]} ✕</button>`;
  for (const f of FACETS) for (const v of (F[f.k] || [])) h += `<button data-k="${f.k}" data-v="${esc(v)}">${esc(v)} ✕</button>`;
  $('#active').innerHTML = h;
}
function toggle(k, v) { const s = F[k] ||= new Set(); s.has(v) ? s.delete(v) : s.add(v); update(); }

$('#facets').addEventListener('click', e => {
  const b = e.target.closest('.opt'); if (b) return toggle(b.dataset.k, b.dataset.v);
  const s = e.target.closest('.showall'); if (s) { expanded[s.dataset.k] = true; renderFacets(); }
});
$('#facets').addEventListener('input', e => {
  if (e.target.classList.contains('fsearch')) { fsearch[e.target.dataset.k] = e.target.value; renderFacets(); return; }
  if (e.target.id === 'y0' || e.target.id === 'y1') {
    let a = +$('#y0').value, b = +$('#y1').value; if (a > b) [a, b] = [b, a];
    $('#y0v').textContent = fmtY(a); $('#y1v').textContent = fmtY(b);
  }
});
$('#facets').addEventListener('change', e => {
  if (e.target.id === 'y0' || e.target.id === 'y1') { let a = +$('#y0').value, b = +$('#y1').value; if (a > b) [a, b] = [b, a]; yr = [a, b]; update(); }
});
$('#active').addEventListener('click', e => {
  const b = e.target.closest('button'); if (!b) return;
  if (b.dataset.clear === 'q') { q = ''; $('#q').value = ''; } else if (b.dataset.clear === 'yr') yr = [300, 1912]; else F[b.dataset.k].delete(b.dataset.v);
  update();
});
$('#clear').onclick = () => { for (const k in F) F[k].clear(); q = ''; $('#q').value = ''; yr = [300, 1912]; update(); };
let qt; $('#q').addEventListener('input', e => { clearTimeout(qt); qt = setTimeout(() => { q = e.target.value.trim().toLowerCase(); update(); }, 220); });
$('#sort').onchange = e => { sort = e.target.value; store.set('sort', sort); if (sort === 'shuffle') seed = Math.random(); update(); };
function toggleFilters(force) {
  const on = force ?? $('.layout').classList.contains('nofilters');
  $('.layout').classList.toggle('nofilters', !on); $('#toggleFilters').setAttribute('aria-expanded', on);
}
$('#toggleFilters').onclick = () => toggleFilters();

/* ---------- grid ---------- */
function more() {
  const g = $('#grid'); const end = Math.min(VIEW.length, shown + PAGE); let h = '';
  for (let n = shown; n < end; n++) h += card(VIEW[n], n);
  g.insertAdjacentHTML('beforeend', h); shown = end;
  $('#more').textContent = shown < VIEW.length ? 'Loading more…' : (VIEW.length ? '— end —' : '');
}
function card(r, n) {
  if (r.lo) return `<button class="card lo" data-n="${n}" style="--ar:.75"><span class="seal">link</span><span class="vz">${esc(r.z || r.t)}</span><span class="lbl">${esc(r.a || '')}<br>${esc(r.m)}</span></button>`;
  const ar = r.ar || 0.62;
  return `<button class="card" data-n="${n}" style="--ar:${ar.toFixed(3)}"><img loading="lazy" decoding="async" src="${esc(r.th)}" alt="" onload="this.classList.add('ld');if(!${!!r.ar}){const a=this.naturalWidth/this.naturalHeight;if(a)this.parentNode.style.setProperty('--ar',Math.min(Math.max(a,.25),4).toFixed(3))}" onerror="this.style.display='none'">
    ${NOTES[r.i] ? '<span class="pin">notes</span>' : ''}${favs.has(r.i) ? '<span class="fav">♥</span>' : ''}
    <span class="cap"><b>${esc(r.t)}</b><span>${esc(r.a)} · ${esc(r.d)}</span></span></button>`;
}
new IntersectionObserver(es => { if (es[0].isIntersecting && shown < VIEW.length) more(); }, {rootMargin: '1200px'}).observe($('#more'));
$('#grid').addEventListener('click', e => { const c = e.target.closest('.card'); if (c) openViewer(+c.dataset.n); });

/* ---------- viewer ---------- */
let osd = null, cur = -1, curImg = 0, pinOn = -1;
function ensureOSD() {
  if (osd) return osd;
  osd = OpenSeadragon({
    element: $('#osd'), prefixUrl: 'https://cdn.jsdelivr.net/npm/openseadragon@4.1.1/build/openseadragon/images/',
    showNavigationControl: false, showNavigator: true, navigatorPosition: 'TOP_RIGHT', navigatorSizeRatio: 0.14, navigatorAutoFade: true,
    maxZoomPixelRatio: 3, visibilityRatio: 0.5, constrainDuringPan: false, animationTime: 0.9, springStiffness: 8,
    gestureSettingsTouch: {pinchRotate: false, flickEnabled: true}, crossOriginPolicy: false, immediateRender: false,
    preserveImageSizeOnResize: true, imageSmoothingEnabled: true,
  });
  osd.addHandler('open', () => { requestAnimationFrame(() => { osd.forceResize(); osd.viewport.goHome(true); addPins(); }); fadeHint(); });
  osd.addHandler('open-failed', () => { $('#osd').insertAdjacentHTML('beforeend', '<div class="loading">This image could not be loaded. Try the museum link in the notes.</div>'); });
  return osd;
}
function tileSource(im) {
  if (im.t === 'iiif') return im.u + '/info.json';
  if (im.t === 'dzi') return im.u;
  return {type: 'image', url: im.u, buildPyramid: false};
}
function openViewer(n, img = 0) {
  cur = n; curImg = img; const r = VIEW[n]; if (!r) return;
  $('#viewer').hidden = false; document.body.style.overflow = 'hidden';
  $('#vt').textContent = r.t; $('#vz').textContent = r.z || '';
  $('#vfav').classList.toggle('faved', favs.has(r.i)); $('#vfav').textContent = favs.has(r.i) ? '♥' : '♡';
  pinOn = -1;
  document.querySelectorAll('#osd .loading').forEach(e => e.remove());
  if (r.lo) {
    $('#osd').style.display = 'none'; $('#nolink').hidden = false; $('#strip').innerHTML = '';
    const href = r.l;
    $('#nolink').innerHTML = `<div><div class="big">${esc(r.z || r.t)}</div><p>${esc(r.m)} doesn't allow copies of its images, so this painting is shown here as a link only.</p>${href ? `<a href="${esc(href)}" target="_blank" rel="noopener">Read about it →</a>` : ''}</div>`;
  } else {
    $('#osd').style.display = ''; $('#nolink').hidden = true;
    ensureOSD().open(tileSource(r.im[img]));
    strip(r);
  }
  panel(r);
  writeHash();
}
function strip(r) {
  if (r.im.length < 2) { $('#strip').innerHTML = ''; return; }
  $('#strip').innerHTML = `<span class="lbl">${curImg + 1} / ${r.im.length}</span>` + r.im.map((im, k) =>
    `<button class="${k === curImg ? 'on' : ''}" data-k="${k}" aria-label="Image ${k + 1}" style="background-image:url('${esc(thumbOf(im, r))}')"></button>`).join('');
}
function thumbOf(im, r) {
  if (im.t === 'iiif') return im.u + '/full/!120,120/0/default.jpg';
  if (im.t === 'dzi') return im.u.replace(/\.dzi$/, '_files/') + '7/0_0.jpg';
  if (/images\.metmuseum\.org/.test(im.u)) return im.u.replace('/original/', '/web-additional/');
  if (/clevelandart/.test(im.u)) return im.u.replace('_print.jpg', '_web.jpg');
  return r.th;
}
$('#strip').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { curImg = +b.dataset.k; pinOn = -1; osd.open(tileSource(VIEW[cur].im[curImg])); strip(VIEW[cur]); panel(VIEW[cur]); } });
function closeViewer() { $('#viewer').hidden = true; document.body.style.overflow = ''; cur = -1; writeHash(); }
$('#vclose').onclick = closeViewer;
$('#vprev').onclick = () => cur > 0 && openViewer(cur - 1);
$('#vnext').onclick = () => { if (cur < VIEW.length - 1) { if (cur + 1 >= shown) more(); openViewer(cur + 1); } };
$('#vinfo').onclick = () => { $('#panel').classList.toggle('hide'); $('#vinfo').classList.toggle('on'); };
$('#vfav').onclick = () => {
  const r = VIEW[cur]; favs.has(r.i) ? favs.delete(r.i) : favs.add(r.i); store.set('favs', [...favs]);
  $('#vfav').classList.toggle('faved', favs.has(r.i)); $('#vfav').textContent = favs.has(r.i) ? '♥' : '♡';
};
addEventListener('keydown', e => {
  if ($('#viewer').hidden) return;
  if (e.key === 'Escape') closeViewer(); if (e.key === 'ArrowRight' && !e.target.closest('input')) $('#vnext').click(); if (e.key === 'ArrowLeft' && !e.target.closest('input')) $('#vprev').click();
});
let hintT; function fadeHint() { const z = $('#zoomhint'); z.style.opacity = 1; clearTimeout(hintT); hintT = setTimeout(() => z.style.opacity = 0, 2500); }

/* ---------- pins ---------- */
function pinsFor(r) { const n = NOTES[r.i]; return n ? (n.pins || []).filter(p => (p.img || 0) === curImg) : []; }
function addPins() {
  const r = VIEW[cur]; if (!r || !osd.world.getItemAt(0)) return;
  osd.clearOverlays();
  const item = osd.world.getItemAt(0); const sz = item.getContentSize();
  pinsFor(r).forEach((p, k) => {
    const box = document.createElement('div'); box.className = 'pinbox'; box.id = 'pb' + k;
    osd.addOverlay({element: box, location: item.imageToViewportRectangle(p.x * sz.x, p.y * sz.y, p.w * sz.x, p.h * sz.y)});
    const m = document.createElement('div'); m.className = 'pinmark'; m.textContent = k + 1; m.id = 'pm' + k;
    new OpenSeadragon.MouseTracker({element: m, clickHandler: () => goPin(k)});
    osd.addOverlay({element: m, location: item.imageToViewportCoordinates((p.x + p.w / 2) * sz.x, p.y * sz.y), placement: OpenSeadragon.Placement.CENTER});
  });
}
function goPin(k) {
  const r = VIEW[cur]; const p = pinsFor(r)[k]; if (!p) return;
  if (pinOn === k) { pinOn = -1; osd.viewport.goHome(); } else {
    pinOn = k; const item = osd.world.getItemAt(0); const sz = item.getContentSize();
    const rect = item.imageToViewportRectangle(p.x * sz.x, p.y * sz.y, p.w * sz.x, p.h * sz.y);
    osd.viewport.fitBoundsWithConstraints(rect.times ? rect : rect, false);
  }
  document.querySelectorAll('.pinmark').forEach((m, j) => m.classList.toggle('on', j === pinOn));
  document.querySelectorAll('.pinbox').forEach((m, j) => m.classList.toggle('on', j === pinOn));
  document.querySelectorAll('.pins li').forEach((m, j) => m.classList.toggle('on', j === pinOn));
  const li = document.querySelectorAll('.pins li')[k]; if (li && pinOn === k) li.scrollIntoView({block: 'nearest', behavior: 'smooth'});
}

/* ---------- info panel ---------- */
function panel(r) {
  const n = NOTES[r.i]; const art = ARTISTS[r.a];
  const pins = pinsFor(r);
  let h = `<h2>${esc(r.t)}</h2>${r.z ? `<div class="tz">${esc(r.z)}</div>` : ''}
  <div class="by"><b>${esc(r.a)}</b> ${r.az ? `<span class="zh">${esc(r.az)}</span>` : ''} ${r.ad ? `· ${esc(r.ad)}` : ''}<br>${esc(r.d)}${r.dt ? ` · ${esc(r.dt)}` : ''}</div>`;
  if (n?.intro) h += `<p>${esc(n.intro)}</p>`;
  if (pins.length) h += `<h3>Look closer</h3><ol class="pins">${pins.map((p, k) => `<li data-k="${k}"><span class="n">${k + 1}</span><span><b>${esc(p.title)}</b>${esc(p.text)}</span></li>`).join('')}</ol>
    <p class="conf">Tap a number to fly to that spot; tap again to zoom back out.</p>`;
  if (r.de) h += `<h3>From the museum</h3><p>${esc(r.de)}</p>`;
  if (r.dy) h += `<p><i>${esc(r.dy)}</i></p>`;
  if (r.ins) h += `<h3>Inscription</h3><p>${esc(r.ins.slice(0, 900))}${r.ins.length > 900 ? '…' : ''}</p>`;
  if (art?.note) h += `<h3>The painter</h3><p><b>${esc(r.a)}</b> ${art.zh ? `<span class="zh">${esc(art.zh)}</span>` : ''} (${esc(art.dates)}). ${esc(art.note)}</p>`;
  if (r.s) h += `<p class="conf">School: ${esc(r.s)}</p>`;
  h += `<h3>Details</h3><dl>
    ${r.f ? `<dt>Format</dt><dd>${esc(r.f)}</dd>` : ''}
    ${r.md ? `<dt>Medium</dt><dd>${esc(r.md)}</dd>` : ''}
    ${r.dm ? `<dt>Size</dt><dd>${esc(r.dm)}</dd>` : ''}
    ${r.at ? `<dt>Attribution</dt><dd>${esc(r.at)}</dd>` : ''}
    <dt>Collection</dt><dd>${esc(r.m)}${r.cr ? `<br><span class="conf">${esc(r.cr)}</span>` : ''}</dd>
    ${r.mp ? `<dt>Image</dt><dd>${r.mp} megapixels${r.im?.length > 1 ? ` · ${r.im.length} images` : ''}</dd>` : ''}
    ${r.lic ? `<dt>Rights</dt><dd>${esc(r.lic)}</dd>` : ''}
    ${r.l ? `<dt>Source</dt><dd><a href="${esc(r.l)}" target="_blank" rel="noopener">Museum record →</a>${r.cm ? `<br><a href="${esc(r.cm)}" target="_blank" rel="noopener">Wikimedia file →</a>` : ''}</dd>` : ''}
  </dl>`;
  const tags = [...(r.g || []), ...(r.tg || []), ...(r.se || []), ...(r.p || []), r.su, r.s].filter(Boolean);
  h += `<h3>Find similar</h3><div class="tagrow">
    ${r.a && r.a !== 'Unidentified artist' ? `<button data-k="painter" data-v="${esc(r.a)}">More by ${esc(r.a)}</button>` : ''}
    ${r.s ? `<button data-k="school" data-v="${esc(r.s)}">${esc(r.s)}</button>` : ''}
    ${(r.tg || []).slice(0, 6).map(t => `<button data-k="tags" data-v="${esc(t)}">${esc(t)}</button>`).join('')}
    <button data-k="dyn" data-v="${esc(r.d)}">${esc(r.d)}</button></div>`;
  $('#panel').innerHTML = h; $('#panel').scrollTop = 0;
}
$('#panel').addEventListener('click', e => {
  const li = e.target.closest('.pins li'); if (li) return goPin(+li.dataset.k);
  const b = e.target.closest('.tagrow button'); if (b) { for (const k in F) F[k].clear(); F[b.dataset.k] = new Set([b.dataset.v]); closeViewer(); update(); }
});

/* ---------- hash (open painting is shareable) ---------- */
function writeHash() {
  const id = cur >= 0 && VIEW[cur] ? VIEW[cur].i : '';
  const h = id ? '#' + id : ' ';
  if (location.hash !== h.trim()) history.replaceState(null, '', h === ' ' ? location.pathname : h);
}
function readHash(first) {
  const id = location.hash.slice(1); if (!id) return;
  setTimeout(() => { const n = VIEW.findIndex(r => r.i === id); if (n >= 0) { while (shown <= n) more(); openViewer(n); } }, first ? 50 : 0);
}
})();
