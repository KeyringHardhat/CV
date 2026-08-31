(() => {
  'use strict';

  // Optional controls for the decorative boot animation.
  const root = document.documentElement;
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const toggle = document.querySelector('.effects-toggle');
  const replay = document.querySelector('.boot-replay');
  let effects = !motion.matches;
  const syncEffects = () => {
    root.dataset.effects = effects && !motion.matches ? 'on' : 'off';
    toggle.textContent = `effects: ${root.dataset.effects}`;
    toggle.setAttribute('aria-pressed', String(root.dataset.effects === 'on'));
    toggle.disabled = motion.matches;
    toggle.title = motion.matches ? 'Reduced motion is enabled on your device' : 'Toggle terminal animation';
    replay.disabled = root.dataset.effects === 'off';
  };
  replay.hidden = false;
  replay.addEventListener('click', () => {
    root.dataset.effects = 'off';
    // Two frames let the browser discard the old animations before restarting.
    requestAnimationFrame(() => requestAnimationFrame(syncEffects));
  });
  toggle.hidden = false;
  toggle.addEventListener('click', () => { effects = !effects; syncEffects(); });
  motion.addEventListener('change', syncEffects);
  syncEffects();

})();
