/* ===================================================
   AIVACS — animations.js
   IntersectionObserver scroll reveals + counter animation
   =================================================== */
(function () {

  /* ---- Scroll reveal ---- */
  const revealObs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('revealed');

      /* Trigger progress bar inside hero card when visible */
      const fill = entry.target.querySelector('.progress-fill');
      if (fill) setTimeout(() => { fill.style.width = '100%'; }, 700);

      /* Trigger the step connector line */
      if (entry.target.id === 'stepsContainer') {
        setTimeout(() => {
          const line = document.getElementById('stepsLineFill');
          if (line) line.classList.add('animated');
        }, 350);
      }

      revealObs.unobserve(entry.target);
    });
  }, { threshold: 0.12 });

  document.querySelectorAll(
    '.reveal, .reveal-up, .reveal-left, .reveal-right, .reveal-scale, .stagger, #stepsContainer'
  ).forEach(el => revealObs.observe(el));


  /* ---- Counter animation ---- */
  function animateCounter(el) {
    const target   = parseInt(el.getAttribute('data-target'), 10);
    const prefix   = el.getAttribute('data-prefix')  || '';
    const suffix   = el.getAttribute('data-suffix')  || '';
    const duration = 1800;
    const start    = performance.now();

    function tick(now) {
      const elapsed  = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased    = 1 - Math.pow(1 - progress, 3); /* cubic ease-out */
      el.textContent = prefix + Math.floor(eased * target) + suffix;
      if (progress < 1) requestAnimationFrame(tick);
    }

    requestAnimationFrame(tick);
  }

  const counterObs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      animateCounter(entry.target);
      counterObs.unobserve(entry.target);
    });
  }, { threshold: 0.6 });

  document.querySelectorAll('[data-target]').forEach(el => counterObs.observe(el));

})();
