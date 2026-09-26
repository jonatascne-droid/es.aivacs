/* ===================================================
   AIVACS — brilla-spotlight.js
   Hero animada do Brilla (mesma física de mola do app) dentro do card da
   home, guiada pelo scroll:
     1ª metade do palco: a foto se expande, o ícone brilha e "Brilla House"
                         entra voando com balanço;
     2ª metade:          a hero esmaece e o painel de informações do app sobe
                         por cima dela, ganhando opacidade.
   Com "reduzir movimento" (ou sem suporte a sticky) mostra só o painel.
   =================================================== */
(function () {
  var secao = document.getElementById('brilla-spotlight');
  if (!secao) return;

  var palco = secao.querySelector('.brilla-stage');
  var quadro = secao.querySelector('.brilla-frame');
  var img = secao.querySelector('.brilla-hero-img');
  var brilho = secao.querySelector('.brilla-glow');
  var icone = secao.querySelector('.brilla-icon');
  var palavraA = secao.querySelector('.brilla-word-a');
  var palavraB = secao.querySelector('.brilla-word-b');
  var dica = secao.querySelector('.brilla-hint');
  var info = secao.querySelector('.brilla-info');
  var nav = document.querySelector('nav');

  var semMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var temSticky = window.CSS && CSS.supports && (CSS.supports('position', 'sticky') || CSS.supports('position', '-webkit-sticky'));
  if (semMovimento || !temSticky) {
    secao.classList.add('brilla-sem-animacao');
    return;
  }

  function lerp(a, b, t) { return a + (b - a) * t; }
  function clamp01(n) { return Math.min(1, Math.max(0, n)); }
  function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }
  function easeInOut(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }

  // Mola leve: a posição "persegue" o alvo definido pelo scroll com inércia,
  // e o balanço (rotação) vem da velocidade — igual à hero do app.
  var RIGIDEZ = 140, AMORTECIMENTO = 13, BALANCO_MAX = 3, FATOR_BALANCO = 1.4;

  // O quadro fica preso logo abaixo da navbar fixa. Ela encolhe (com
  // transição) quando a página rola, então a altura é conferida a cada frame
  // e a variável CSS só muda quando a medida muda de fato.
  var topo = 72;
  function medirNav() {
    var h = nav ? Math.round(nav.getBoundingClientRect().height) : 0;
    if (Math.abs(h - topo) > 1) {
      topo = h;
      secao.style.setProperty('--brilla-top', topo + 'px');
    }
  }
  medirNav();

  function aplicarImagem(p) {
    var abre = easeOutCubic(clamp01(p / 0.4));
    img.style.clipPath = 'inset(' + lerp(9, 0, abre) + '% ' + lerp(11, 0, abre) + '% round ' + lerp(28, 0, abre) + 'px)';
    img.style.webkitClipPath = img.style.clipPath;
    img.style.transform = 'scale(' + lerp(1, 1.14, clamp01(p)) + ')';
  }

  function aplicarTexto(pos, balanco) {
    var opacidade = pos > 0 ? 1 : 0;
    var escala = lerp(0.7, 1, clamp01(pos));
    palavraA.style.opacity = opacidade;
    palavraA.style.transform = 'translate(' + lerp(-58, 0, pos) + 'vw, ' + lerp(-32, 0, pos) + 'vh) scale(' + escala + ') rotate(' + balanco + 'deg)';
    palavraB.style.opacity = opacidade;
    palavraB.style.transform = 'translate(' + lerp(58, 0, pos) + 'vw, ' + lerp(-32, 0, pos) + 'vh) scale(' + escala + ') rotate(' + -balanco + 'deg)';
  }

  function aplicarIcone(p, pos, balanco) {
    var opacidade = clamp01(p / 0.22);
    var escala = lerp(0.5, 1, clamp01(pos));
    icone.style.opacity = opacidade;
    icone.style.transform = 'translate(-50%, -50%) scale(' + escala + ') rotate(' + balanco * 1.3 + 'deg)';
    brilho.style.opacity = opacidade;
    brilho.style.transform = 'translate(-50%, -50%) scale(' + escala + ')';
  }

  function aplicarFade(f) {
    // A hero some e se afasta um pouco; o painel ganha opacidade enquanto
    // o próprio scroll o faz subir por cima do quadro.
    // A hero termina de sumir antes de o painel ficar opaco, para o texto
    // do painel não disputar com "Brilla House".
    var e = easeInOut(clamp01(f / 0.6));
    quadro.style.opacity = String(1 - e);
    quadro.style.transform = 'scale(' + lerp(1, 0.96, e) + ')';
    info.style.opacity = String(easeInOut(clamp01((f - 0.2) / 0.55)));
    info.style.transform = 'translateY(' + lerp(40, 0, easeOutCubic(f)) + 'px)';
  }

  function progresso() {
    var r = palco.getBoundingClientRect();
    var percurso = palco.offsetHeight - quadro.offsetHeight;
    return percurso > 0 ? clamp01((topo - r.top) / percurso) : 0;
  }

  var pos = 0, vel = 0, ultimo = performance.now(), raf = 0, ativo = false;

  function quadroAnim(agora) {
    var dt = Math.min(0.05, (agora - ultimo) / 1000);
    ultimo = agora;

    medirNav();
    var p = progresso();
    var hero = clamp01(p / 0.5);          // 1ª metade: animação da hero
    var fade = clamp01((p - 0.5) / 0.5);  // 2ª metade: fade para as informações

    aplicarImagem(hero);
    var alvo = clamp01((hero - 0.06) / 0.55);
    var acel = (alvo - pos) * RIGIDEZ - vel * AMORTECIMENTO;
    vel += acel * dt;
    pos += vel * dt;
    var balanco = Math.max(-BALANCO_MAX, Math.min(BALANCO_MAX, vel * FATOR_BALANCO));
    aplicarTexto(pos, balanco);
    aplicarIcone(hero, pos, balanco);
    dica.style.opacity = String(1 - clamp01(hero / 0.12));
    aplicarFade(fade);

    raf = ativo ? requestAnimationFrame(quadroAnim) : 0;
  }

  // Só anima enquanto a seção está perto da tela.
  var observador = new IntersectionObserver(function (entradas) {
    ativo = entradas[0].isIntersecting;
    if (ativo && !raf) {
      ultimo = performance.now();
      raf = requestAnimationFrame(quadroAnim);
    }
  }, { rootMargin: '200px 0px' });
  observador.observe(secao);

  // Estado inicial correto mesmo antes do primeiro frame (ex.: recarregar no meio).
  quadroAnim(performance.now());
})();
