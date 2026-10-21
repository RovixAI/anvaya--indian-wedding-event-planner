(function(){
  document.documentElement.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var btn = document.querySelector('.menu-btn'), list = document.querySelector('.nav ul');
  if (btn && list) btn.addEventListener('click', function(){
    var open = list.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // image slots: if a photo fails, show its brief instead
  document.querySelectorAll('.slot img').forEach(function(img){
    var mark = function(){ img.closest('.slot').classList.add('missing'); };
    if (img.complete && img.naturalWidth === 0) mark();
    img.addEventListener('error', mark);
  });

  // hero mosaic carousel
  document.querySelectorAll('.hero[data-carousel]').forEach(function(hero){
    var sets = hero.querySelectorAll('.mosaic .set'), caps = hero.querySelectorAll('.cap'), dots = hero.querySelectorAll('.dots button');
    var i = 0, t;
    function show(n){
      i = (n + sets.length) % sets.length;
      sets.forEach(function(s,k){ s.classList.toggle('on', k===i); });
      caps.forEach(function(c,k){ c.classList.toggle('on', k===i); });
      dots.forEach(function(d,k){ d.setAttribute('aria-selected', k===i ? 'true' : 'false'); });
    }
    function start(){ clearInterval(t); if (reduce || sets.length < 2) return; t = setInterval(function(){ show(i+1); }, 7000); }
    dots.forEach(function(d,k){ d.addEventListener('click', function(){ show(k); start(); }); });
    show(0); start();
  });

  // chips index for staggered confirmation
  document.querySelectorAll('.step').forEach(function(s){
    s.querySelectorAll('.falls li').forEach(function(li,k){ li.style.setProperty('--j', k); });
  });
  // image slots reveal individually, staggered within their group
  document.querySelectorAll('.trio, .row .art, .gallery, .mosaic .set, .portrait').forEach(function(g){
    g.querySelectorAll('.slot').forEach(function(sl,k){ sl.classList.add('reveal-img'); sl.style.setProperty('--i', k); });
  });
  // timeline line grows with scroll position
  var tls = document.querySelectorAll('.timeline');
  function lineProgress(){
    tls.forEach(function(tl){
      var r = tl.getBoundingClientRect(), vh = window.innerHeight;
      var p = (vh*0.72 - r.top) / r.height;
      tl.style.setProperty('--p', Math.max(0, Math.min(1, p)).toFixed(3));
    });
  }
  if (tls.length){ lineProgress(); window.addEventListener('scroll', lineProgress, {passive:true}); window.addEventListener('resize', lineProgress); }

  // reveal + timeline activation
  var io = ('IntersectionObserver' in window) ? new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      io.unobserve(e.target);
    });
  }, {threshold: 0.15, rootMargin: '0px 0px -8% 0px'}) : null;
  var targets = document.querySelectorAll('.reveal, .stagger, .step, .slot.reveal-img, .mapwrap, .mv .panel');
  if (io) targets.forEach(function(el){ io.observe(el); }); else targets.forEach(function(el){ el.classList.add('in'); });
  // hero images are above the fold: show at once
  document.querySelectorAll('.mosaic .slot, .trio .slot').forEach(function(el){ setTimeout(function(){ el.classList.add('in'); }, 150); });
  setTimeout(function(){ targets.forEach(function(el){ el.classList.add('in'); }); }, 4000);

  // vendor ledger
  document.querySelectorAll('.ledger').forEach(function(lg){
    var items = lg.querySelectorAll('li'), views = lg.querySelectorAll('.view .slot'), cap = lg.querySelector('.view .cap');
    function set(k){ items.forEach(function(it,i){ it.classList.toggle('on', i===k); }); views.forEach(function(v,i){ v.classList.toggle('on', i===k); }); if (cap) cap.textContent = items[k].querySelector('h3').textContent; }
    items.forEach(function(it,k){ it.addEventListener('mouseenter', function(){ set(k); }); it.addEventListener('focus', function(){ set(k); }); it.addEventListener('click', function(){ set(k); }); it.tabIndex = 0; });
    set(0);
  });

  // planning calendar: stacking cards
  document.querySelectorAll('.planner').forEach(function(pl){
    var data = JSON.parse(pl.getAttribute('data-plan')), tabs = pl.querySelectorAll('.horizons button'), deck = pl.querySelector('.deck'), note = pl.querySelector('.plan-note');
    var imgs = JSON.parse(pl.getAttribute('data-imgs') || '[]');
    function render(k){
      var h = data[k]; note.textContent = h.note;
      tabs.forEach(function(t,i){ t.setAttribute('aria-selected', i===k ? 'true' : 'false'); });
      deck.classList.add('swap'); deck.innerHTML = '';
      h.rows.forEach(function(r,i){
        var c = document.createElement('article'); c.className='pcard'; c.style.setProperty('--o', (i*14)+'px');
        var im = imgs[i % imgs.length] || null;
        c.innerHTML = '<div class="when"><span class="big">'+r.when+'</span><span class="unit">'+r.unit+'</span><span class="idx">'+(i+1)+' of '+h.rows.length+'</span></div>'+
          '<div class="what"><h3>'+r.title+'</h3><p>'+r.text+'</p><ul>'+r.items.map(function(x,j){ return '<li style="--k:'+j+'">'+x+'</li>'; }).join('')+'</ul></div>'+
          (im ? '<div class="pic"><figure class="slot"><img src="'+im[0]+'" alt="'+im[1]+'" loading="lazy"><figcaption>'+im[1]+'</figcaption></figure></div>' : '');
        deck.appendChild(c);
      });
      var end = document.createElement('div'); end.className='deck-end'; deck.appendChild(end);
      void deck.offsetWidth; deck.classList.remove('swap');
      deck.querySelectorAll('.pcard').forEach(function(el){ if (io) io.observe(el); else el.classList.add('in'); });
    }
    tabs.forEach(function(t,k){ t.addEventListener('click', function(){ render(k); pl.scrollIntoView({behavior: reduce ? 'auto':'smooth', block:'start'}); }); });
    render(0);
  });

  // story: sticky frame follows the chapter in view
  document.querySelectorAll('.story').forEach(function(st){
    var chapters = st.querySelectorAll('.chapter'), frames = st.querySelectorAll('.frame .slot');
    function set(k){ chapters.forEach(function(c,i){ c.classList.toggle('on', i===k); }); frames.forEach(function(f,i){ f.classList.toggle('on', i===k); }); }
    set(0);
    if ('IntersectionObserver' in window){
      var cio = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting) set([].indexOf.call(chapters, e.target)); }); }, {rootMargin:'-45% 0px -45% 0px', threshold:0});
      chapters.forEach(function(c){ cio.observe(c); });
    } else chapters.forEach(function(c){ c.classList.add('on'); });
  });
  document.querySelectorAll('.flmap .pin').forEach(function(p,k){ p.style.setProperty('--pd', (0.3 + k*0.17)+'s'); });

  // booking modal
  var modal = document.getElementById('book'), fabBtn = document.querySelector('.fab .book');
  if (modal && fabBtn){
    var panes = modal.querySelectorAll('.bk'), stepsUI = modal.querySelectorAll('.bk-steps span');
    var state = {type:'Wedding or Wedding Weekend', date:null, time:null, cur:0};
    var now = new Date(), view = new Date(now.getFullYear(), now.getMonth(), 1);
    function go(n){ state.cur=n; panes.forEach(function(p,i){ p.hidden = i!==n; }); stepsUI.forEach(function(s,i){ s.classList.toggle('on', i<=n); }); }
    function open(){ modal.classList.add('open'); document.body.style.overflow='hidden'; go(0); renderCal(); modal.querySelector('.close').focus(); }
    function close(){ modal.classList.remove('open'); document.body.style.overflow=''; }
    fabBtn.addEventListener('click', open);
    document.querySelectorAll('[data-book]').forEach(function(b){ b.addEventListener('click', function(e){ e.preventDefault(); open(); }); });
    modal.querySelector('.close').addEventListener('click', close);
    modal.addEventListener('click', function(e){ if (e.target===modal) close(); });
    document.addEventListener('keydown', function(e){ if (e.key==='Escape' && modal.classList.contains('open')) close(); });
    modal.querySelectorAll('input[name=bktype]').forEach(function(r){ r.addEventListener('change', function(){ state.type = r.value; }); });
    modal.querySelectorAll('[data-next]').forEach(function(b){ b.addEventListener('click', function(){
      if (state.cur===1 && !(state.date && state.time)) { modal.querySelector('.cal-note').textContent = 'Pick a day and a time to continue.'; return; }
      go(state.cur+1); if (state.cur===2) fillSummary();
    }); });
    modal.querySelectorAll('[data-prev]').forEach(function(b){ b.addEventListener('click', function(){ go(state.cur-1); }); });
    var months=['January','February','March','April','May','June','July','August','September','October','November','December'];
    function renderCal(){
      var head = modal.querySelector('.calhead span'), grid = modal.querySelector('.cal .grid');
      head.textContent = months[view.getMonth()]+' '+view.getFullYear();
      grid.innerHTML = '';
      ['S','M','T','W','T','F','S'].forEach(function(d){ var e=document.createElement('div'); e.className='dow'; e.textContent=d; grid.appendChild(e); });
      var first = new Date(view.getFullYear(), view.getMonth(), 1).getDay(), days = new Date(view.getFullYear(), view.getMonth()+1, 0).getDate();
      for (var i=0;i<first;i++){ grid.appendChild(document.createElement('div')); }
      var today = new Date(); today.setHours(0,0,0,0);
      for (var d=1; d<=days; d++){
        var dt = new Date(view.getFullYear(), view.getMonth(), d);
        var b = document.createElement('button'); b.type='button'; b.className='day'; b.textContent=d;
        if (dt < today || dt.getDay()===0) b.disabled = true;
        if (dt.getTime()===today.getTime()) b.classList.add('today');
        if (state.date && dt.getTime()===state.date.getTime()) b.classList.add('sel');
        (function(dt){ b.addEventListener('click', function(){ state.date = dt; renderCal(); modal.querySelector('.cal-note').textContent=''; }); })(dt);
        grid.appendChild(b);
      }
    }
    modal.querySelector('.cal .prev').addEventListener('click', function(){ view = new Date(view.getFullYear(), view.getMonth()-1, 1); renderCal(); });
    modal.querySelector('.cal .next').addEventListener('click', function(){ view = new Date(view.getFullYear(), view.getMonth()+1, 1); renderCal(); });
    modal.querySelectorAll('.slots button').forEach(function(b){ b.addEventListener('click', function(){ modal.querySelectorAll('.slots button').forEach(function(x){ x.classList.remove('sel'); }); b.classList.add('sel'); state.time = b.textContent; modal.querySelector('.cal-note').textContent=''; }); });
    function fmt(d){ return d.toLocaleDateString('en-US', {weekday:'long', month:'long', day:'numeric', year:'numeric'}); }
    function fillSummary(){ modal.querySelector('.summary').innerHTML = '<div><strong>'+state.type+'</strong></div><div>'+fmt(state.date)+' at '+state.time+'</div><div>Thirty minutes, by phone or video. We will confirm by email.</div>'; }
    modal.querySelector('#bkform').addEventListener('submit', function(e){
      e.preventDefault();
      var name = modal.querySelector('#bk-name').value.trim();
      modal.querySelector('.bk-done .who').textContent = name ? ', '+name : '';
      try { localStorage.setItem('anvaya-booking', JSON.stringify({type:state.type,date:state.date,time:state.time,name:name})); } catch(err){}
      go(3);
    });
  }

  // enquiry form (preview: no backend)
  var form = document.getElementById('enquiry');
  if (form) form.addEventListener('submit', function(ev){
    ev.preventDefault();
    var name = (form.querySelector('#f-name').value || '').trim();
    var sent = document.querySelector('.sent');
    sent.querySelector('.who').textContent = name ? ', ' + name : '';
    sent.classList.add('show');
    form.hidden = true;
    sent.scrollIntoView({behavior: reduce ? 'auto' : 'smooth', block: 'center'});
  });
})();
