(() => {
  const nav = document.querySelector('.nav');
  if (nav) {
    const update = () => nav.classList.toggle('scrolled', window.scrollY > 8);
    update();
    window.addEventListener('scroll', update, { passive: true });
  }
})();
