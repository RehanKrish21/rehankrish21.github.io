// A soft ring that trails the cursor. It eases toward the pointer, grows over
// anything clickable and tightens on press. Mouse and trackpad only; it is off
// for touch screens and for anyone who has asked their device to reduce motion.
(() => {
  if (!matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const style = document.createElement('style');
  style.textContent =
    '.cursor-ring{position:fixed;left:0;top:0;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:50%;' +
    'border:1.5px solid var(--accent,#9E2A2B);pointer-events:none;z-index:9999;opacity:0;' +
    'transition:opacity .25s,width .22s,height .22s,margin .22s,background-color .22s,border-color .22s;will-change:transform}' +
    '.cursor-ring.on{opacity:.55}' +
    '.cursor-ring.over{width:46px;height:46px;margin:-23px 0 0 -23px;opacity:.8;background-color:color-mix(in srgb,var(--accent,#9E2A2B) 9%,transparent)}' +
    '.cursor-ring.down{width:22px;height:22px;margin:-11px 0 0 -11px;opacity:.9}';
  document.head.appendChild(style);
  const ring = document.createElement('div');
  ring.className = 'cursor-ring'; ring.setAttribute('aria-hidden', 'true');
  document.body.appendChild(ring);
  let tx = 0, ty = 0, x = 0, y = 0, raf = 0, placed = false;
  const CLICKABLE = 'a,button,.spike,[role="tab"],[role="link"],label,summary';
  function tick(){
    x += (tx - x) * 0.2; y += (ty - y) * 0.2;
    ring.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px,0)';
    raf = (Math.abs(tx - x) > 0.1 || Math.abs(ty - y) > 0.1) ? requestAnimationFrame(tick) : 0;
  }
  addEventListener('pointermove', e => {
    if (e.pointerType && e.pointerType !== 'mouse') return;
    tx = e.clientX; ty = e.clientY;
    if (!placed){ x = tx; y = ty; placed = true; }
    ring.classList.add('on');
    ring.classList.toggle('over', !!(e.target.closest && e.target.closest(CLICKABLE)));
    if (!raf) raf = requestAnimationFrame(tick);
  }, {passive: true});
  addEventListener('pointerdown', () => ring.classList.add('down'));
  addEventListener('pointerup', () => ring.classList.remove('down'));
  document.documentElement.addEventListener('mouseleave', () => ring.classList.remove('on'));
  addEventListener('blur', () => ring.classList.remove('on'));
})();
