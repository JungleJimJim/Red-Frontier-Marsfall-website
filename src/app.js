import { catalogue, gallery } from './content.js';

const root = new URL('../', import.meta.url);
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const $ = (selector, parent = document) => parent.querySelector(selector);
const $$ = (selector, parent = document) => [...parent.querySelectorAll(selector)];
document.documentElement.classList.add('js');

// Native cross-document transitions are defined in CSS; ordinary links still
// work in browsers without that feature, and every route is a real HTML page.
function transition(update) {
  // Commit controls immediately, so rapid filter changes cannot race a deferred
  // whole-document snapshot. Animate only the surface that actually changed.
  update();
  if (!reducedMotion.matches) {
    const surface = $('.catalogue-grid') || $('.gallery-grid') || $('#mode-image');
    surface?.animate?.([{ opacity:0.65, transform:'translateY(6px)' }, { opacity:1, transform:'translateY(0)' }], { duration:260, easing:'ease-out' });
  }
}

const menu = $('.menu-toggle');
const nav = $('#site-nav');
function closeMenu() {
  menu?.setAttribute('aria-expanded', 'false');
  nav?.classList.remove('open');
  menu?.setAttribute('aria-label', 'Open navigation');
}
menu?.addEventListener('click', () => {
  const opening = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(opening));
  menu.setAttribute('aria-label', opening ? 'Close navigation' : 'Open navigation');
  nav.classList.toggle('open', opening);
});
nav?.addEventListener('click', event => {
  if (event.target.closest('a')) closeMenu();
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menu.focus();
  }
});
document.addEventListener('click', event => {
  if (!event.target.closest('.site-header')) closeMenu();
});

const revealElements = $$('[data-reveal]');
if ('IntersectionObserver' in window && !reducedMotion.matches) {
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    }
  }, { threshold: 0.08 });
  revealElements.forEach((el, index) => {
    el.style.setProperty('--reveal-delay', `${Math.min(index % 4 * 65, 195)}ms`);
    observer.observe(el);
  });
} else revealElements.forEach(el => el.classList.add('visible'));
reducedMotion.addEventListener('change', event => {
  if (event.matches) revealElements.forEach(el => el.classList.add('visible'));
});

// Small ambient particles and a restrained pointer response, only in the hero.
const hero = $('.hero');
if (hero && !reducedMotion.matches) {
  const grid = $('.hero-grid');
  for (let i = 0; i < 16; i++) {
    const particle = document.createElement('span');
    particle.className = 'dust';
    particle.style.cssText = `--x:${(i * 37 + 11) % 100}%;--y:${(i * 23 + 9) % 100}%;--duration:${14 + i % 8}s;--delay:-${i * 1.4}s`;
    grid.append(particle);
  }
  let frame = 0;
  let x = 0, y = 0;
  hero.addEventListener('pointermove', event => {
    if (event.pointerType !== 'mouse' || reducedMotion.matches) return;
    const box = hero.getBoundingClientRect();
    x = (event.clientX - box.left - box.width / 2) / box.width * 10;
    y = (event.clientY - box.top - box.height / 2) / box.height * 6;
    if (!frame) frame = requestAnimationFrame(() => {
      hero.style.setProperty('--pointer-x', `${x}px`);
      hero.style.setProperty('--pointer-y', `${y}px`);
      frame = 0;
    });
  });
  hero.addEventListener('pointerleave', () => {
    hero.style.setProperty('--pointer-x', '0px');
    hero.style.setProperty('--pointer-y', '0px');
  });
}

const modes = {
  strategy: { image:'ares-gameplay', alt:'Ares army seen from the strategy camera', label:'STRATEGY CAMERA', caption:'Command the army from above.', title:'The whole battlefield is yours.', text:'Build a base, manage your resources, form an army, and coordinate your attack from the strategy camera.' },
  direct: { image:'direct-control', alt:'First-person gameplay view beside an Ares hovertank', label:'DIRECT UNIT CONTROL', caption:'Step into the same battle.', title:'Take the front line into your own hands.', text:'Select a friendly unit and press Tab. Move, aim, and fight from its perspective while the rest of your army continues the battle.' },
};
$$('[data-mode]').forEach(button => button.addEventListener('click', () => {
  const data = modes[button.dataset.mode];
  $$('[data-mode]').forEach(b => {
    const selected = b === button;
    b.classList.toggle('active', selected);
    b.setAttribute('aria-pressed', String(selected));
  });
  transition(() => {
    $('#mode-image').src = new URL(`assets/${data.image}.webp`, root).href;
    $('#mode-image').alt = data.alt;
    $('#mode-frame-label').textContent = data.label;
    $('#mode-caption').textContent = data.caption;
    $('#mode-copy h3').textContent = data.title;
    $('#mode-copy p').textContent = data.text;
  });
}));

const catalogueCards = $$('.catalogue-grid .unit-card');
const filters = { faction:'all', kind:'all', search:'' };
function applyCatalogueFilters() {
  let count = 0;
  catalogueCards.forEach(card => {
    const show = (filters.faction === 'all' || card.dataset.faction === filters.faction)
      && (filters.kind === 'all' || card.dataset.kind === filters.kind)
      && (!filters.search || card.dataset.search.includes(filters.search));
    card.hidden = !show;
    if (show) count++;
  });
  if ($('#catalogue-count')) $('#catalogue-count').textContent = `${count} ${count === 1 ? 'entry' : 'entries'}`;
  if ($('#catalogue-empty')) $('#catalogue-empty').hidden = count !== 0;
  const url = new URL(location.href);
  if (filters.faction !== 'all') url.searchParams.set('faction', filters.faction);
  else url.searchParams.delete('faction');
  if (filters.kind !== 'all') url.searchParams.set('kind', filters.kind);
  else url.searchParams.delete('kind');
  if (filters.search) url.searchParams.set('q', filters.search);
  else url.searchParams.delete('q');
  history.replaceState(null, '', url);
}
function syncFilterButtons(attribute, selected) {
  $$(`[${attribute}]`).forEach(button => {
    const active = button.getAttribute(attribute) === selected;
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
  });
}
$$('[data-faction-filter]').forEach(button => button.addEventListener('click', () => {
  filters.faction = button.dataset.factionFilter;
  syncFilterButtons('data-faction-filter', filters.faction);
  transition(applyCatalogueFilters);
}));
$$('[data-kind-filter]').forEach(button => button.addEventListener('click', () => {
  filters.kind = button.dataset.kindFilter;
  syncFilterButtons('data-kind-filter', filters.kind);
  transition(applyCatalogueFilters);
}));
$('#catalogue-search')?.addEventListener('input', event => {
  filters.search = event.target.value.trim().toLowerCase();
  applyCatalogueFilters();
});
$('#reset-filters')?.addEventListener('click', () => {
  Object.assign(filters, { faction:'all', kind:'all', search:'' });
  syncFilterButtons('data-faction-filter','all');
  syncFilterButtons('data-kind-filter','all');
  $('#catalogue-search').value = '';
  transition(applyCatalogueFilters);
  $('#catalogue-search').focus();
});
if (catalogueCards.length) {
  const params = new URLSearchParams(location.search);
  if (['ares','xenaari','wildlife'].includes(params.get('faction'))) filters.faction = params.get('faction');
  if (['unit','building','creature'].includes(params.get('kind'))) filters.kind = params.get('kind');
  filters.search = (params.get('q') || '').trim().toLowerCase();
  $('#catalogue-search').value = filters.search;
  syncFilterButtons('data-faction-filter',filters.faction);
  syncFilterButtons('data-kind-filter',filters.kind);
  applyCatalogueFilters();
}

let galleryFilter = 'all';
$$('[data-gallery-filter]').forEach(button => button.addEventListener('click', () => {
  galleryFilter = button.dataset.galleryFilter;
  syncFilterButtons('data-gallery-filter', galleryFilter);
  transition(() => {
    let count = 0;
    $$('.gallery-grid .gallery-card').forEach(card => {
      card.hidden = galleryFilter !== 'all' && card.dataset.category !== galleryFilter;
      if (!card.hidden) count++;
    });
    $('#gallery-count').textContent = `${count} ${count === 1 ? 'piece' : 'pieces'}`;
  });
}));

// One keyboard-accessible native dialog handles both visual archives.
const dialog = $('#art-viewer');
const viewerImage = $('#viewer-image');
let viewerItems = [], viewerIndex = 0;
let previousBodyOverflow = '';
const factionNames = {ares:'Ares Expedition',xenaari:'Xenaari Brood',wildlife:'Martian wildlife'};
function updateViewer() {
  const item = viewerItems[viewerIndex];
  if (!item) return;
  viewerImage.classList.remove('loaded');
  viewerImage.src = new URL(item.image, root).href;
  viewerImage.alt = item.name ? `${item.name} — ${item.artType}` : `${item.title} — ${item.category}`;
  if (viewerImage.complete) viewerImage.classList.add('loaded');
  $('#viewer-title').textContent = item.name || item.title;
  $('#viewer-category').textContent = item.name ? `${factionNames[item.faction]} / ${item.role} / ${item.artType}` : item.category;
  $('#viewer-description').textContent = item.description;
  $('#viewer-position').textContent = `${viewerIndex + 1} / ${viewerItems.length}`;
  $('#viewer-prev').disabled = viewerItems.length < 2;
  $('#viewer-next').disabled = viewerItems.length < 2;
}
viewerImage?.addEventListener('load', () => viewerImage.classList.add('loaded'));
viewerImage?.addEventListener('error', () => {
  $('.viewer-loading').textContent = 'This artwork could not load. Please try again.';
});
function stepViewer(direction) {
  viewerIndex = (viewerIndex + direction + viewerItems.length) % viewerItems.length;
  $('.viewer-loading').textContent = 'Loading artwork…';
  updateViewer();
}
document.addEventListener('click', event => {
  const button = event.target.closest('[data-view]');
  if (!button) return;
  if (button.dataset.collection === 'catalogue') {
    const visibleIds = catalogueCards.length
      ? catalogueCards.filter(c => !c.hidden).map(c => c.dataset.entry)
      : $$('.arsenal-preview .unit-card').map(c => c.dataset.entry);
    viewerItems = catalogue.filter(item => visibleIds.includes(item.id));
  } else {
    viewerItems = gallery.filter(item => galleryFilter === 'all' || item.category === galleryFilter);
    // The featured render remains inspectable when a different gallery filter is active.
    if (!viewerItems.some(item => item.id === button.dataset.view)) viewerItems = gallery;
  }
  viewerIndex = viewerItems.findIndex(item => item.id === button.dataset.view);
  if (viewerIndex < 0) return;
  $('.viewer-loading').textContent = 'Loading artwork…';
  updateViewer();
  previousBodyOverflow = document.body.style.overflow;
  document.body.style.overflow = 'hidden';
  dialog.showModal();
});
$('.viewer-close')?.addEventListener('click', () => dialog.close());
$('#viewer-prev')?.addEventListener('click', () => stepViewer(-1));
$('#viewer-next')?.addEventListener('click', () => stepViewer(1));
dialog?.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
dialog?.addEventListener('keydown', event => {
  if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
    event.preventDefault();
    stepViewer(event.key === 'ArrowLeft' ? -1 : 1);
  }
});
dialog?.addEventListener('close', () => { document.body.style.overflow = previousBodyOverflow; });
