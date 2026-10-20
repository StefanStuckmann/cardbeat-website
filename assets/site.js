// Drag the hero's index cards around, the way you would in the app.
// Purely decorative: the page works the same without it.
(() => {
  const board = document.querySelector('.board');
  if (board) {
    // Cards may roam the whole hero, not just their row.
    const area = board.closest('section') || board;
    let z = 1;
    for (const card of board.querySelectorAll('.card')) {
      let x = 0, y = 0, startX = 0, startY = 0, min, max;
      card.addEventListener('pointerdown', (e) => {
        card.setPointerCapture(e.pointerId);
        const b = area.getBoundingClientRect(), c = card.getBoundingClientRect();
        // Limits for the translation, relative to where the card is now.
        min = { x: x - (c.left - b.left), y: y - (c.top - b.top) };
        max = { x: x + (b.right - c.right), y: y + (b.bottom - c.bottom) };
        startX = e.clientX - x;
        startY = e.clientY - y;
        card.style.zIndex = ++z;
        card.classList.add('lifted');
      });
      card.addEventListener('pointermove', (e) => {
        if (!card.hasPointerCapture(e.pointerId)) return;
        x = Math.min(max.x, Math.max(min.x, e.clientX - startX));
        y = Math.min(max.y, Math.max(min.y, e.clientY - startY));
        card.style.translate = `${x}px ${y}px`;
      });
      const drop = () => card.classList.remove('lifted');
      card.addEventListener('pointerup', drop);
      card.addEventListener('pointercancel', drop);
    }
  }

  const nav = document.querySelector('.nav');
  if (nav) {
    const update = () => nav.classList.toggle('scrolled', window.scrollY > 8);
    update();
    window.addEventListener('scroll', update, { passive: true });
  }
})();
