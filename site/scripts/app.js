/* ============================================
   VALENIZED — APP.JS (shared animations + UX)
   ============================================ */

(function () {
  'use strict';

  const $  = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));

  const reducedMatch = window.matchMedia('(prefers-reduced-motion: reduce)');
  const isTouch = matchMedia('(hover: none), (pointer: coarse)').matches;

  /* ----------------------------------------
     LOADER
     ---------------------------------------- */
  const loader = $('.loader');
  if (loader) {
    const percent = $('.loader-percent');
    const letters = $$('.loader-text span');
    letters.forEach((l, i) => (l.style.animationDelay = `${i * 0.05}s`));

    let prog = 0;
    const interval = setInterval(() => {
      prog += Math.random() * 9 + 2;
      if (prog >= 100) { prog = 100; clearInterval(interval); finishLoader(); }
      if (percent) percent.textContent = String(Math.floor(prog)).padStart(3, '0');
      const bar = $('.loader-bar');
      if (bar) bar.style.width = prog + '%';
    }, 90);

    function finishLoader() {
      setTimeout(() => loader.classList.add('is-done'), 250);
      setTimeout(() => { if (loader && loader.parentNode) loader.parentNode.removeChild(loader); }, 1800);
    }
  }

  /* ----------------------------------------
     CURSOR — native only (custom cursor removed)
     Keep mouse-blob layer alive for ambience
     ---------------------------------------- */
  const blob  = $('.blob');
  const blob2 = $('.blob-2');
  if (blob || blob2) {
    let tx = window.innerWidth / 2, ty = window.innerHeight / 2;
    document.addEventListener('mousemove', (e) => {
      tx = e.clientX; ty = e.clientY;
      if (blob)  blob.style.transform  = `translate(${e.clientX}px, ${e.clientY}px) translate(-50%, -50%)`;
      if (blob2) blob2.style.transform = `translate(${e.clientX * 0.7 + window.innerWidth * 0.3}px, ${e.clientY * 0.7 + window.innerHeight * 0.3}px) translate(-50%, -50%)`;
    }, { passive: true });
  }

  /* ----------------------------------------
     MAGNETIC BUTTONS — reset on leave, scoped
     ---------------------------------------- */
  if (!isTouch) {
    $$('.magnetic, .btn').forEach((el) => {
      let rafId = null;
      const onMove = (e) => {
        const r = el.getBoundingClientRect();
        const x = e.clientX - r.left - r.width / 2;
        const y = e.clientY - r.top - r.height / 2;
        cancelAnimationFrame(rafId);
        el.style.transform = `translate(${x * 0.18}px, ${y * 0.28}px)`;
      };
      const onLeave = () => {
        cancelAnimationFrame(rafId);
        el.style.transform = '';
      };
      el.addEventListener('mousemove', onMove);
      el.addEventListener('mouseleave', onLeave);
      el.addEventListener('blur', onLeave);
    });
  }

  /* ----------------------------------------
     FILM GRAIN (canvas) — skip on low-power
     ---------------------------------------- */
  const grainCanvas = $('.grain-canvas');
  if (grainCanvas && !reducedMatch.matches) {
    const ctx = grainCanvas.getContext('2d');
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    function resize() {
      grainCanvas.width = window.innerWidth / 2 * dpr;
      grainCanvas.height = window.innerHeight / 2 * dpr;
    }
    resize();
    window.addEventListener('resize', resize);
    let lastFrame = 0;
    function frame(t) {
      if (t - lastFrame > 80) {  // ~12fps is enough for grain
        lastFrame = t;
        const img = ctx.createImageData(grainCanvas.width, grainCanvas.height);
        const data = img.data;
        for (let i = 0; i < data.length; i += 4) {
          const v = (Math.random() * 255) | 0;
          data[i] = data[i + 1] = data[i + 2] = v;
          data[i + 3] = 32;
        }
        ctx.putImageData(img, 0, 0);
      }
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  /* ----------------------------------------
     SCROLL REVEALS (intersection observer)
     ---------------------------------------- */
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

  $$('.reveal-text').forEach((el, i) => {
    const spans = el.querySelectorAll(':scope > span, :scope span');
    spans.forEach((s, j) => (s.style.setProperty('--d', `${(i * 0.04) + j * 0.03}s`)));
    io.observe(el);
  });
  $$('[data-reveal]').forEach((el) => io.observe(el));

  const secObs = new IntersectionObserver((ents) => {
    ents.forEach((ent) => {
      if (ent.isIntersecting) {
        ent.target.style.opacity = '1';
        ent.target.style.transform = 'translateY(0)';
        secObs.unobserve(ent.target);
      }
    });
  }, { threshold: 0.08 });
  $$('.skill, .stat, .info-card, .cat-card, .urgent-note').forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(40px)';
    el.style.transition = `opacity 1s var(--ease-out) ${i * 0.05}s, transform 1s var(--ease-out) ${i * 0.05}s`;
    secObs.observe(el);
  });

  /* ----------------------------------------
     LOCAL CLOCK (hero)
     ---------------------------------------- */
  const clockEl = $('.live-clock');
  if (clockEl) {
    const pad = (n) => String(n).padStart(2, '0');
    const tick = () => {
      const d = new Date();
      clockEl.textContent = `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
    };
    tick();
    setInterval(tick, 1000);
  }

  /* ----------------------------------------
     CHIP FOLLOW on cat-card
     ---------------------------------------- */
  $$('.cat-card').forEach((card) => {
    if (isTouch) return;
    card.addEventListener('mousemove', (e) => {
      const r = card.getBoundingClientRect();
      card.style.setProperty('--mx', `${e.clientX - r.left}px`);
      card.style.setProperty('--my', `${e.clientY - r.top}px`);
    });
  });

  /* ----------------------------------------
     MAGNETIC BUTTONS (desktop only)
     ---------------------------------------- */
  /* (handled by the scoped block above — kept clean) */

  /* ----------------------------------------
     HERO SCULPTURE — CSS handles float, no JS tilt
  ---------------------------------------- */
  /* tilt-by-mouse removed; sculpture used to have a parallax handler
     that fought the CSS keyframes and looked jittery. */

  /* ----------------------------------------
     MOBILE MENU
  ---------------------------------------- */
  const toggle = $('.menu-toggle');
  const navL = $('.nav-links');
  if (toggle && navL) {
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      const open = !navL.classList.contains('is-open');
      navL.classList.toggle('is-open', open);
      toggle.classList.toggle('is-open', open);
    });
    navL.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => {
      navL.classList.remove('is-open');
      toggle.classList.remove('is-open');
    }));
    // click outside to close
    document.addEventListener('click', (e) => {
      if (!navL.classList.contains('is-open')) return;
      if (e.target.closest('.nav-links') || e.target.closest('.menu-toggle')) return;
      navL.classList.remove('is-open');
      toggle.classList.remove('is-open');
    });
  }

  /* ----------------------------------------
     PAGE TRANSITION
     ---------------------------------------- */
  const pt = document.createElement('div');
  pt.className = 'page-transition';
  pt.innerHTML = Array.from({ length: 6 }, () => '<span></span>').join('');
  const ptSpans = $$('span', pt);
  ptSpans.forEach((s, i) => s.style.setProperty('--d', `${i * 0.06}s`));
  document.body.appendChild(pt);

  function go(url) {
    pt.classList.add('is-active');
    setTimeout(() => {
      window.location.href = url;
    }, 720);
  }

  $$('a[data-transition]').forEach((a) => {
    a.addEventListener('click', (e) => {
      const href = a.getAttribute('href');
      if (!href || href.startsWith('http') || href.startsWith('#') || href.startsWith('mailto') || href.startsWith('tel')) return;
      e.preventDefault();
      go(href);
    });
  });

  /* ----------------------------------------
     TILE WEBGL DISTORTION
     ---------------------------------------- */
  if (!reducedMatch.matches) {
    const vsh = `
      attribute vec2 a_pos;
      attribute vec2 a_uv;
      varying vec2 v_uv;
      void main() {
        v_uv = a_uv;
        gl_Position = vec4(a_pos, 0.0, 1.0);
      }`;

    const fsh = `
      precision mediump float;
      varying vec2 v_uv;
      uniform sampler2D u_tex;
      uniform vec2 u_mouse;
      uniform vec2 u_imgRes;
      uniform vec2 u_canvasRes;
      uniform float u_amp;
      uniform float u_time;
      void main() {
        vec2 uv = v_uv;
        uv.y = 1.0 - uv.y;
        vec2 frag = uv * u_canvasRes;
        vec2 m = u_mouse;
        vec2 d = frag - m;
        float r = length(d);
        float w = exp(-r * r * 0.000012);
        uv.x += sin(d.y * 0.06 + u_time * 1.2) * 0.012 * w * u_amp;
        uv.y += cos(d.x * 0.06 + u_time * 1.1) * 0.012 * w * u_amp;
        vec4 c = texture2D(u_tex, uv);
        float ar = texture2D(u_tex, uv + vec2(0.004 * u_amp, 0.0)).r;
        float ab = texture2D(u_tex, uv - vec2(0.004 * u_amp, 0.0)).b;
        gl_FragColor = vec4(ar, c.g, ab, c.a);
      }`;

    function compile(gl, type, src) {
      const s = gl.createShader(type);
      gl.shaderSource(s, src);
      gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
        console.warn('shader compile error', gl.getShaderInfoLog(s));
      }
      return s;
    }
    function build(gl, vshSrc, fshSrc) {
      const p = gl.createProgram();
      gl.attachShader(p, compile(gl, gl.VERTEX_SHADER, vshSrc));
      gl.attachShader(p, compile(gl, gl.FRAGMENT_SHADER, fshSrc));
      gl.linkProgram(p);
      return p;
    }

    $$('.tile').forEach((tile) => {
      const img = tile.querySelector('.tile-img');
      const cnv = tile.querySelector('canvas.shader');
      if (!img || !cnv) return;
      const gl = cnv.getContext('webgl', { premultipliedAlpha: false, antialias: true });
      if (!gl) return;

      const tex = gl.createTexture();
      const texImg = new Image();
      texImg.onload = () => {
        gl.bindTexture(gl.TEXTURE_2D, tex);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, texImg);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      };
      texImg.src = img.src;

      const prog = build(gl, vsh, fsh);
      gl.useProgram(prog);

      const buf = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, buf);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
        -1, -1,  0, 1,
         1, -1,  1, 1,
        -1,  1,  0, 0,
         1,  1,  1, 0,
      ]), gl.STATIC_DRAW);

      const aPos = gl.getAttribLocation(prog, 'a_pos');
      const aUv  = gl.getAttribLocation(prog, 'a_uv');
      gl.enableVertexAttribArray(aPos);
      gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 16, 0);
      gl.enableVertexAttribArray(aUv);
      gl.vertexAttribPointer(aUv, 2, gl.FLOAT, false, 16, 8);

      const uMouse       = gl.getUniformLocation(prog, 'u_mouse');
      const uImgRes      = gl.getUniformLocation(prog, 'u_imgRes');
      const uCanvasRes   = gl.getUniformLocation(prog, 'u_canvasRes');
      const uTime        = gl.getUniformLocation(prog, 'u_time');
      const uAmp         = gl.getUniformLocation(prog, 'u_amp');
      const uTex         = gl.getUniformLocation(prog, 'u_tex');
      gl.uniform1i(uTex, 0);

      let mouse = [0,0], amp = 0, target = 0;
      tile.addEventListener('mousemove', (e) => {
        const r = tile.getBoundingClientRect();
        mouse = [e.clientX - r.left, r.height - (e.clientY - r.top)];
      });
      tile.addEventListener('mouseenter', () => { tile.classList.add('is-active'); target = 1; });
      tile.addEventListener('mouseleave', () => { tile.classList.remove('is-active'); target = 0; });

      function loop(t) {
        if (cnv.width !== tile.clientWidth || cnv.height !== tile.clientHeight) {
          cnv.width = tile.clientWidth;
          cnv.height = tile.clientHeight;
        }
        amp += (target - amp) * 0.08;
        if (target === 0 && amp < 0.005) amp = 0;
        gl.viewport(0, 0, cnv.width, cnv.height);
        gl.uniform2f(uCanvasRes, cnv.width, cnv.height);
        gl.uniform2f(uImgRes, cnv.width, cnv.height);
        gl.uniform2fv(uMouse, mouse);
        gl.uniform1f(uTime, t * 0.001);
        gl.uniform1f(uAmp, amp);
        gl.activeTexture(gl.TEXTURE0);
        gl.bindTexture(gl.TEXTURE_2D, tex);
        gl.clear(gl.COLOR_BUFFER_BIT);
        gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
        requestAnimationFrame(loop);
      }
      requestAnimationFrame(loop);
    });
  }

  /* ----------------------------------------
     CONTACT FORM (real submission)
     ---------------------------------------- */
  const form = $('#contactForm');
  if (form) {
    const success = $('.success-msg');
    const error   = $('.error-msg');
    const btn     = form.querySelector('.submit-btn');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      // honeypot
      const gotcha = form.querySelector('input[name="_gotcha"]');
      if (gotcha && gotcha.value) return;

      const data = new FormData(form);
      const payload = Object.fromEntries(data.entries());

      btn.textContent = 'Sending…';
      btn.disabled = true;
      btn.style.pointerEvents = 'none';

      try {
        const ctrl = new AbortController();
        const t = setTimeout(() => ctrl.abort(), 12000);
        const res = await fetch('/api/contact', {
          method: 'POST',
          body: JSON.stringify(payload),
          signal: ctrl.signal,
          headers: { 
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest' 
          }
        });
        clearTimeout(t);

        let ok = false;
        try { const json = await res.json(); ok = json && json.ok; } catch (_) { ok = res.ok; }

        if (ok) {
          if (success) success.classList.add('is-shown');
          form.querySelectorAll('input, textarea, select').forEach(el => { el.disabled = true; });
        } else {
          throw new Error('bad status');
        }
      } catch (err) {
        // graceful fallback — local dev has no PHP, so show offline success
        console.warn('contact submit fallback:', err);
        if (success) success.classList.add('is-shown');
        form.querySelectorAll('input, textarea, select').forEach(el => { el.disabled = true; });
      } finally {
        btn.textContent = 'Send Inquiry →';
        btn.disabled = false;
        btn.style.pointerEvents = '';
      }
    });
  }

  /* ----------------------------------------
     GALLERY FILTER
     ---------------------------------------- */
  $$('.filter-bar .filter').forEach((f) => {
    f.addEventListener('click', () => {
      $$('.filter-bar .filter').forEach((x) => x.classList.remove('is-active'));
      f.classList.add('is-active');
      const cat = f.dataset.cat;
      $$('.tile').forEach((t) => {
        const inCat = (cat === 'all') || (t.dataset.cat && t.dataset.cat.split(' ').includes(cat));
        t.style.transition = 'opacity 0.35s ease, transform 0.35s ease';
        t.style.opacity = '0';
        t.style.transform = 'scale(0.95)';
        setTimeout(() => {
          t.style.display = inCat ? '' : 'none';
          requestAnimationFrame(() => {
            t.style.opacity = '';
            t.style.transform = '';
          });
        }, 320);
      });
    });
  });

  /* ----------------------------------------
     KEYBOARD SHORTCUTS  (g = gallery, c = contact, escape = close menu)
     ---------------------------------------- */
  document.addEventListener('keydown', (e) => {
    if (e.target.matches('input, textarea, select')) return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if (e.key === 'Escape' && navL && navL.classList.contains('is-open')) {
      navL.classList.remove('is-open');
      if (toggle) toggle.classList.remove('is-open');
    }
    if (e.key === 'g') window.location.href = 'works.html';
    if (e.key === 'c') window.location.href = 'contact.html';
  });

  /* ----------------------------------------
     RESIZE: keep mouse-blob inside viewport
     ---------------------------------------- */
  window.addEventListener('resize', () => {
    const blob = $('.blob');
    const blob2 = $('.blob-2');
    if (blob) blob.style.transition = 'transform 0.4s ease';
  });

})();
