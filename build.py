#!/usr/bin/env python3
"""Builds the Anvaya site into dist/ with shared CSS/JS inlined into every page."""
import pathlib, json, html, re

def keep_whole(s):
    """Keep hyphenated words (Multi-Day, First-Rice) on one line in headings."""
    return re.sub(r"(\S+-\S+)", r'<span style="white-space:nowrap">\1</span>', s)

ROOT = pathlib.Path(__file__).parent
DIST = ROOT / "dist"
SRC = ROOT / "src" if (ROOT / "src").exists() else DIST / "src"  # src/ currently ships inside dist/
IMG = "img"
CSS = (SRC / "style.css").read_text(encoding="utf-8")
JS = (SRC / "main.js").read_text(encoding="utf-8")
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Jost:wght@300;400&family=Pinyon+Script&display=swap">')
ARROW = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M4 12h16M14 6l6 6-6 6"/></svg>'
SITE = "https://anvaya-events.vercel.app"
PHONE_TEL = "+1XXXXXXXXXX"      # fill in: digits only after +1
WHATSAPP = "1XXXXXXXXXX"        # fill in: country code + number, digits only

PAGES = [("index","Home"),("about","About"),("weddings","Weddings"),("milestones","Milestones"),("traditions","Traditions"),("corporate","Corporate"),("contact","Contact")]

def slot(src, brief, cls="", lazy=True):
    load = ' loading="lazy"' if lazy else ''  # first-screen photos load straight away
    return f'<figure class="slot {cls}"><img src="{IMG}/{src}" alt="{brief}"{load}><figcaption>{brief}</figcaption></figure>'

def nav(active):
    items = "".join(f'<li><a href="{s}.html"{" aria-current=page" if s==active else ""}>{l}</a></li>' for s,l in PAGES)
    return f'''<nav class="nav" aria-label="Main"><div class="wrap">
<a class="brand" href="index.html" aria-label="Anvaya home"><img src="{IMG}/logo-dark.webp" alt="Anvaya" onerror="this.closest('.brand').classList.add('nologo')"><span class="wordmark">Anvaya</span></a>
<button class="menu-btn" aria-label="Open menu" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
<ul>{items}</ul></div></nav>'''

FAB = f'''<div class="fab" aria-label="Quick contact">
<a href="tel:{PHONE_TEL}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg><span>Call</span></a>
<a href="https://wa.me/{WHATSAPP}?text=Hello%20Anvaya%2C%20I%20would%20love%20to%20talk%20about%20a%20celebration." target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 20l1.3-3.8A8 8 0 1 1 8 19.2L4 20z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5l1-1.5-2-1-1 1a4 4 0 0 1-2-2l1-1-1-2-1.5 1z"/></svg><span>WhatsApp</span></a>
<button type="button" class="book"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="5" width="18" height="16" rx="1"/><path d="M3 10h18M8 3v4M16 3v4"/></svg><span>Book a conversation</span></button>
</div>

<div class="modal" id="book" role="dialog" aria-modal="true" aria-label="Book a conversation">
<div class="card">
<button type="button" class="close" aria-label="Close">×</button>
<div class="head"><p class="kicker">Book a conversation</p><h2 class="h-display">Let’s Talk About Your Celebration</h2><p class="lede" style="font-size:.98rem">Choose the type of event and a convenient time to discuss your vision, priorities and next steps.</p></div>
<div class="bk-steps"><span class="on">Occasion</span><span>·</span><span>Day &amp; time</span><span>·</span><span>Your details</span></div>

<div class="bk">
<div class="chooser" style="justify-content:center">
<label><input type="radio" name="bktype" value="Wedding or Wedding Weekend" id="bk-w" checked><span>Wedding or Wedding Weekend</span></label>
<label><input type="radio" name="bktype" value="Milestone Celebration" id="bk-m"><span>Milestone Celebration</span></label>
<label><input type="radio" name="bktype" value="Traditional Ceremony" id="bk-t"><span>Traditional Ceremony</span></label>
<label><input type="radio" name="bktype" value="Corporate Event" id="bk-c"><span>Corporate Event</span></label>
<label><input type="radio" name="bktype" value="Something Else" id="bk-o"><span>Something Else</span></label>
</div>
<div class="bk-nav"><span></span><button type="button" class="btn fill" data-next>Choose a day {ARROW}</button></div>
</div>

<div class="bk" hidden>
<div class="cal"><div class="calhead"><button type="button" class="prev" aria-label="Previous month">‹</button><span></span><button type="button" class="next" aria-label="Next month">›</button></div><div class="grid"></div></div>
<p class="kicker" style="margin-top:.4rem">A time that suits you (Eastern)</p>
<div class="slots"><button type="button">10:00 AM</button><button type="button">11:00 AM</button><button type="button">12:30 PM</button><button type="button">2:00 PM</button><button type="button">3:30 PM</button><button type="button">5:00 PM</button><button type="button">6:30 PM</button></div>
<p class="note cal-note" aria-live="polite"></p>
<div class="bk-nav"><button type="button" class="btn" data-prev>Back</button><button type="button" class="btn fill" data-next>Your details {ARROW}</button></div>
</div>

<div class="bk" hidden>
<div class="summary"></div>
<form id="bkform">
<div class="row2"><label for="bk-name">Your name<input id="bk-name" type="text" autocomplete="name" required></label><label for="bk-phone">Phone<input id="bk-phone" type="tel" autocomplete="tel" required></label></div>
<label for="bk-email">Email<input id="bk-email" type="email" autocomplete="email" required></label>
<label for="bk-note">Anything we should know before we call?<textarea id="bk-note" style="min-height:80px" placeholder="Rough date, guest count, traditions, anything already booked"></textarea></label>
<div class="bk-nav"><button type="button" class="btn" data-prev>Back</button><button type="submit" class="btn fill">Confirm the call {ARROW}</button></div>
</form>
</div>

<div class="bk bk-done" hidden>
<div class="head"><span class="script">received</span><h3 class="h-serif">Thank you<span class="who"></span>.</h3><p class="lede" style="font-size:1rem">Your booking request has been received.</p></div>
</div>
</div></div>'''

FOOTER = f'''<footer><div class="wrap">
<div class="top">
<div style="display:grid;gap:1rem"><a class="brand" href="index.html"><img src="{IMG}/logo-dark.webp" alt="Anvaya" onerror="this.closest('.brand').classList.add('nologo')"><span class="wordmark">Anvaya</span></a><p>Anvaya plans weddings, traditional ceremonies, milestones and corporate events across South Florida and beyond. Eight years of team experience, culturally informed planning and considered vendor choices. Seamless Planning. Timeless Celebrations.</p></div>
<div><h4>Celebrations</h4><ul><li><a href="weddings.html">Weddings</a></li><li><a href="milestones.html">Milestones</a></li><li><a href="traditions.html">Traditions</a></li><li><a href="corporate.html">Corporate</a></li></ul></div>
<div><h4>Anvaya</h4><ul><li><a href="about.html">Our Story</a></li><li><a href="index.html#unfolds">How We Work</a></li><li><a href="blog/index.html">Blog</a></li><li><a href="contact.html">Contact Us</a></li><li><a href="#0" data-book>Book a Conversation</a></li></ul></div>
<div><h4>Find Us</h4><ul><li><span class="placeholder">[Phone]</span></li><li><span class="placeholder">[Email]</span></li><li>Miami · Fort Lauderdale · Palm Beach</li><li><a href="#0">Instagram</a></li></ul></div>
</div>
<div class="bottom"><span>© 2026 Anvaya. All rights reserved.</span><span>Privacy · Terms</span></div>
</div></footer>'''

def cta(kicker, h, p, label="Book a Conversation", label2="Contact Us"):
    return f'''<section class="cta sage"><div class="wrap reveal">
<p class="kicker">{kicker}</p><h2 class="h-display">{h}</h2><p class="lede">{p}</p>
<div style="display:flex;gap:1rem;flex-wrap:wrap;justify-content:center"><a class="btn on-sage" href="#0" data-book>{label} {ARROW}</a><a class="btn on-sage" href="contact.html" style="border-color:rgba(244,241,234,.45)">{label2}</a></div></div></section>'''

def banner(kicker, h, lede, trio):
    ledes = "".join(f'<p class="lede">{p}</p>' for p in (lede if isinstance(lede, (list, tuple)) else [lede]))  # one paragraph, or several
    return f'''<header class="banner"><div class="wrap">
<div class="copy"><p class="kicker">{kicker}</p><h1 class="h-display">{h}</h1><div class="rule"></div>{ledes}</div>
<div class="trio">{"".join(slot(s,b,lazy=False) for s,b in trio)}</div>
</div></header>'''

def timeline(steps, note):
    """steps: (title, text, [falls], (img, brief) or None)"""
    out = []
    for k,(t,x,falls,pic) in enumerate(steps):
        p = f'<div class="pic" style="--src:url({IMG}/{pic[0]})">{slot(pic[0],pic[1])}</div>' if pic else ''  # --src: the black-and-white preview copy
        out.append(f'<li class="step" style="--i:{k}"><span class="num">{k+1:02}</span>{p}<div class="body"><h3>{t}</h3><p>{x}</p><ul class="falls">{"".join(f"<li>{f}</li>" for f in falls)}</ul><span class="state"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3.2 3.2L13 4.5"/></svg>Confirmed</span></div></li>')
    nav = f'<div class="tl-nav"><button type="button" class="prev" aria-label="Previous step">{ARROW}</button><span class="tl-count" aria-hidden="true"><b>01</b><i></i>{len(steps):02}</span><button type="button" class="next" aria-label="Next step">{ARROW}</button></div>'
    return f'<div class="tl-pin"><div class="tl-stage"><ol class="timeline" style="--n:{len(steps)-1}">{"".join(out)}</ol></div></div>{nav}<div class="timeline-note reveal"><p>{note}</p></div>'

def faq(items):
    return '<div class="faq reveal">' + "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in items) + '</div>'

def story(frames, chapters):
    """frames: [(img, brief)]; chapters: [(script, h, p)]"""
    f = "".join(f'<figure class="slot{" on" if k==0 else ""}"><img src="{IMG}/{s}" alt="{b}" loading="lazy"><figcaption>{b}</figcaption></figure>' for k,(s,b) in enumerate(frames))
    c = "".join(f'<div class="chapter"><span class="script">{sc}</span><h3>{h}</h3><p>{p}</p></div>' for sc,h,p in chapters)
    return f'<div class="story"><div class="frame">{f}</div><div class="chapters">{c}</div></div>'

FLMAP = '''<svg class="flmap" viewBox="0 0 530 540" role="img" aria-label="Map of Florida showing where Anvaya plans celebrations, with South Florida at its heart">
<path class="land" d="M19.2 89.6 L23.8 52.4 L138.8 52.4 L143.4 71.0 L276.8 77.2 L304.4 71.0 L309.0 114.4 L322.8 164.0 L341.2 213.6 L355.0 269.4 L368.8 312.8 L364.2 362.4 L359.6 399.6 L350.4 412.0 L327.4 415.1 L313.6 381.0 L290.6 362.4 L276.8 331.4 L263.0 300.4 L244.6 250.8 L244.6 213.6 L235.4 176.4 L212.4 145.4 L184.8 108.2 L166.4 117.5 L125.0 133.0 L102.0 102.0 L69.8 89.6 L37.6 95.8 Z"/>
<path class="land" d="M348.1 415.1 L336.6 427.5 L322.8 439.9 L304.4 446.1 L286.0 452.3" fill="none" stroke-width="5" stroke-linecap="round" style="fill:none;stroke:var(--ivory-2)"/>
<circle class="home-ring" cx="355.0" cy="337.6" r="78"/>
<path class="route" d="M364.7 304.7 L367.0 319.0 L365.1 339.5 L362.4 355.0 L360.1 376.7"/>
<text class="label" x="315.0" y="437.6" text-anchor="middle">our home, South Florida</text>
<g class="pin far" transform="translate(37.6 89.6)"><g><circle class="pulse" r="4"/><circle class="ring" r="9"/><circle class="dot" r="3"/><text x="0" y="22" text-anchor="middle">Pensacola</text></g></g><g class="pin far" transform="translate(171.0 86.5)"><g><circle class="pulse" r="4"/><circle class="ring" r="9"/><circle class="dot" r="3"/><text x="-14" y="4" text-anchor="end">Tallahassee</text></g></g><g class="pin far" transform="translate(292.4 93.9)"><g><circle class="pulse" r="4"/><circle class="ring" r="9"/><circle class="dot" r="3"/><text x="-14" y="4" text-anchor="end">Jacksonville</text></g></g><g class="pin far" transform="translate(305.3 204.9)"><g><circle class="pulse" r="4"/><circle class="ring" r="9"/><circle class="dot" r="3"/><text x="-14" y="4" text-anchor="end">Orlando</text></g></g><g class="pin far" transform="translate(255.6 241.5)"><g><circle class="pulse" r="4"/><circle class="ring" r="9"/><circle class="dot" r="3"/><text x="-14" y="4" text-anchor="end">Tampa</text></g></g><g class="pin far" transform="translate(252.4 279.3)"><g><circle class="pulse" r="4"/><circle class="ring" r="9"/><circle class="dot" r="3"/><text x="-14" y="4" text-anchor="end">Sarasota</text></g></g><g class="pin far" transform="translate(282.8 322.7)"><g><circle class="pulse" r="4"/><circle class="ring" r="9"/><circle class="dot" r="3"/><text x="-14" y="4" text-anchor="end">Fort Myers</text></g></g><g class="pin far" transform="translate(286.0 353.7)"><g><circle class="pulse" r="4"/><circle class="ring" r="9"/><circle class="dot" r="3"/><text x="-14" y="4" text-anchor="end">Naples</text></g></g><g class="pin far" transform="translate(286.9 451.7)"><g><circle class="pulse" r="4"/><circle class="ring" r="9"/><circle class="dot" r="3"/><text x="14" y="4" text-anchor="start">Key West</text></g></g><g class="pin " transform="translate(364.7 304.7)"><g><circle class="pulse" r="4"/><circle class="ring" r="9"/><circle class="dot" r="3"/><text x="14" y="-1" text-anchor="start">Jupiter</text></g></g><g class="pin " transform="translate(367.0 319.0)"><g><circle class="pulse" r="4"/><circle class="ring" r="9"/><circle class="dot" r="3"/><text x="14" y="9" text-anchor="start">Palm Beach</text></g></g><g class="pin " transform="translate(365.1 339.5)"><g><circle class="pulse" r="4"/><circle class="ring" r="9"/><circle class="dot" r="3"/><text x="14" y="4" text-anchor="start">Boca Raton</text></g></g><g class="pin " transform="translate(362.4 355.0)"><g><circle class="pulse" r="4"/><circle class="ring" r="9"/><circle class="dot" r="3"/><text x="14" y="8" text-anchor="start">Fort Lauderdale</text></g></g><g class="pin home" transform="translate(360.1 376.7)"><g><circle class="pulse" r="4"/><circle class="ring" r="9"/><circle class="dot" r="3"/><text x="14" y="10" text-anchor="start">Miami &amp; Coral Gables</text></g></g>
</svg>'''

REGIONS = ["home", "central", "gulf", "beyond"]
REGION_NAMES = ["Miami, Fort Lauderdale &amp; Palm Beach", "Orlando &amp; Tampa", "Naples, Sarasota &amp; Fort Myers", "Jacksonville, the Panhandle &amp; the Keys"]

def mapsection(h, lede, texts, band="ivory"):
    """texts: one paragraph per region, in REGIONS order"""
    cols = "".join(f'<div><span class="script">{s}</span><h3>{n}</h3><p>{t}</p></div>' for s,n,t in zip(REGIONS, REGION_NAMES, texts))
    return f'''<section class="{band} mapsec"><div class="wrap">
<div class="head reveal"><p class="kicker">Where We Work</p><h2 class="h-display">{h}</h2><div class="rule"></div><p class="lede">{lede}</p></div>
<div class="mapwrap" style="grid-template-columns:1fr;justify-items:center">{FLMAP}</div>
<div class="mapcols stagger">{cols}</div></div></section>'''

def ledger(items):
    """items: (title, text, (img, brief))"""
    li = "".join(f'<li><span class="n">{"abcdefghijkl"[k]}.</span><h3>{keep_whole(t)}</h3><svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M4 12h16M14 6l6 6-6 6"/></svg><p>{x}</p></li>' for k,(t,x,pic) in enumerate(items))
    views = "".join(f'<figure class="slot{" on" if k==0 else ""}"><img src="{IMG}/{pic[0]}" alt="{pic[1]}" loading="lazy"><figcaption>{pic[1]}</figcaption></figure>' for k,(t,x,pic) in enumerate(items))
    return f'<div class="ledger reveal"><ol>{li}</ol><div class="view">{views}<span class="cap"></span></div></div>'

def pace_id(label):  # "Nine Months" -> "nine-months": the anchor each preview links to
    return label.lower().replace(" ", "-")

def planner(data, imgs, band="white"):
    tabs = "".join(f'<button type="button" role="tab" id="{pace_id(d["label"])}" aria-selected="{"true" if k==0 else "false"}">{d["label"]}</button>' for k,d in enumerate(data))
    return f'''<section class="{band}"><div class="wrap">
<div class="planner" data-plan='{json.dumps(data).replace("'", "&#39;")}' data-imgs='{json.dumps([[f"{IMG}/{a}",b] for a,b in imgs]).replace("'", "&#39;")}'>
<div class="horizons" role="tablist">{tabs}</div>
<p class="plan-note"></p>
<div class="deck"></div>
</div></div></section>'''

CAL_PAGE = {"weddings":"blog/indian-wedding-planning-timeline/index","milestones":"milestone-planning-calendar","traditions":"traditions-planning-calendar","corporate":"corporate-planning-calendar"}  # each calendar has its own page; the wedding one is a blog resource

def plan_link(sid, data, kicker, h, lede, band="ivory"):
    """the calendar lives on its own page; this preview lists each pace and links straight to it"""
    url = CAL_PAGE[sid] + ".html"
    paces = "".join(f'<li><a href="{url}#{pace_id(d["label"])}"><span class="label">{d["label"]}</span><span class="note">{d["note"]}</span>{ARROW}</a></li>' for d in data)
    return f'''<section class="{band}"><div class="wrap"><div class="plan-link reveal">
<div class="copy"><p class="kicker">{kicker}</p><h2 class="h-serif">{h}</h2><p class="lede">{lede}</p><a class="btn fill" href="{url}">View the Full Calendar {ARROW}</a></div>
<ol class="paces">{paces}</ol>
</div></div></section>'''

# image shorthands
W = [("weddings/mandap.jpg","South Indian mandap at Biscayne Bay"),("weddings/baraat.jpg","Baraat arriving under royal palms"),("weddings/sangeet.jpg","Sangeet night, marigold stage")]
M = [("milestones/anniversary.jpg","Fiftieth anniversary dinner, Palm Beach"),("milestones/first-birthday.jpg","First birthday with grandparents"),("milestones/baby-shower.jpg","Baby shower brunch on the terrace")]
C = [("corporate/gala.jpg","Awards gala, Miami ballroom"),("corporate/launch.jpg","Product launch, Wynwood"),("corporate/dinner.jpg","Leadership dinner, Brickell")]
def mosaic_set(trio, on):
    return f'<div class="set{" on" if on else ""}">{"".join(slot(s,b,lazy=not on) for s,b in trio)}</div>'

WED_PLAN = [{"label": "Fourteen Months", "note": "The unhurried version. Plenty of time to visit venues twice, taste menus slowly and let both families weigh in.", "rows": [{"when": "14", "unit": "months out", "title": "We sit down together", "text": "The first conversation, both families if you wish. Every event goes on the list with a guest count and a budget.", "items": ["Event list", "Budget", "Guest estimate", "Priest or officiant's dates"]}, {"when": "13", "unit": "months out", "title": "Your venues are held", "text": "Ceremony, reception and the hotel block, walked and contracted before anything else.", "items": ["Ceremony venue", "Reception venue", "Hotel block", "Save-the-dates"]}, {"when": "11", "unit": "months out", "title": "Your vendor family", "text": "Caterer, d\u00e9cor, photo and film, music and hair and makeup, each chosen from two or three we trust.", "items": ["Caterer", "D\u00e9cor &amp; florals", "Photographer", "Videographer", "DJ &amp; dhol", "Hair &amp; makeup"]}, {"when": "8", "unit": "months out", "title": "Design and stationery", "text": "Mandap, linens, lighting and the invitation suite, tasted and proofed.", "items": ["Design story", "Menu tasting", "Invitations", "Outfits calendar"]}, {"when": "4", "unit": "months out", "title": "Guests and logistics", "text": "Invitations out, replies tracked, transport and the baraat route agreed with the venue.", "items": ["Invitations sent", "Transport", "Baraat route", "Welcome bags"]}, {"when": "6", "unit": "weeks out", "title": "The timeline", "text": "Minute by minute for each day, shared with every vendor. Seating, final counts, weather plan.", "items": ["Day timelines", "Seating", "Final counts", "Weather plan"]}, {"when": "The", "unit": "weekend", "title": "You are guests", "text": "We are there before the first florist and after the last car.", "items": ["On-site team", "Vendor care", "Send-off"]}]}, {"label": "Nine Months", "note": "Comfortable. Venues go first within the first fortnight, then the rest follows at a steady pace.", "rows": [{"when": "9", "unit": "months out", "title": "We sit down, venues held", "text": "The first conversation and the venue walkthroughs happen in the same fortnight.", "items": ["Event list", "Budget", "Ceremony venue", "Reception venue", "Hotel block"]}, {"when": "8", "unit": "months out", "title": "Your vendor family", "text": "The full team booked within a month of the venues.", "items": ["Caterer", "D\u00e9cor &amp; florals", "Photo &amp; film", "Music", "Hair &amp; makeup", "Officiant"]}, {"when": "6", "unit": "months out", "title": "Design and stationery", "text": "Tasting, design board and invitations in one stretch.", "items": ["Design story", "Tasting", "Invitations"]}, {"when": "3", "unit": "months out", "title": "Guests and logistics", "text": "Replies tracked, transport and welcome bags arranged.", "items": ["Invitations sent", "Transport", "Welcome bags"]}, {"when": "5", "unit": "weeks out", "title": "The timeline", "text": "Every day written down, every vendor briefed.", "items": ["Day timelines", "Seating", "Final counts"]}, {"when": "The", "unit": "weekend", "title": "You are guests", "text": "We hold it. You live it.", "items": ["On-site team", "Send-off"]}]}, {"label": "Six Months", "note": "Yes, it can be done beautifully. We move fast in the first three weeks, and the order never changes: venues first, always.", "rows": [{"when": "6", "unit": "months out", "title": "Week one: we meet, venues held", "text": "We talk on day one and walk venues the same week. Contracts signed before the month is out.", "items": ["Event list", "Budget", "Ceremony venue", "Reception venue"]}, {"when": "5", "unit": "months out", "title": "The team, booked together", "text": "Caterer, d\u00e9cor, photo, music, hair and makeup and officiant confirmed in a single push.", "items": ["Caterer", "D\u00e9cor", "Photo &amp; film", "Music", "Hair &amp; makeup", "Officiant", "Hotel block"]}, {"when": "4", "unit": "months out", "title": "Design, tasting, invitations", "text": "Decisions made in one sitting where possible. Digital invitations if print timelines are tight.", "items": ["Design story", "Tasting", "Invitations out"]}, {"when": "2", "unit": "months out", "title": "Guests and logistics", "text": "Replies, transport, baraat route, outfits.", "items": ["Replies", "Transport", "Baraat route"]}, {"when": "3", "unit": "weeks out", "title": "The timeline", "text": "Written, shared and rehearsed.", "items": ["Day timelines", "Seating", "Final counts"]}, {"when": "The", "unit": "weekend", "title": "You are guests", "text": "Same care, same calm.", "items": ["On-site team", "Send-off"]}]}]
MS_PLAN = [{"label": "Three Months", "note": "Room to breathe. Good for a fiftieth anniversary or a first birthday with family flying in.", "rows": [{"when": "12", "unit": "weeks out", "title": "We listen, the room is held", "text": "Who it is for, who is coming, and the venue chosen from two or three we show you.", "items": ["Guest of honor", "Guest list", "Budget", "Venue held"]}, {"when": "9", "unit": "weeks out", "title": "Your people", "text": "Caterer or restaurant, florist, photographer, music, cake.", "items": ["Catering", "Flowers", "Photographer", "Music", "Cake"]}, {"when": "6", "unit": "weeks out", "title": "Invitations and design", "text": "Invitations out, a design story for the room, the program sketched with the family.", "items": ["Invitations", "Design story", "Menu", "Program"]}, {"when": "1", "unit": "week out", "title": "Final numbers", "text": "Counts to the kitchen, run-of-show for toasts and slideshows, call times.", "items": ["Final count", "Run-of-show", "Call times"]}, {"when": "The", "unit": "day", "title": "You host", "text": "We set the room and keep the evening flowing.", "items": ["Room set", "Evening held"]}]}, {"label": "Six Weeks", "note": "Our usual rhythm for most milestones. Brisk, but nothing is rushed.", "rows": [{"when": "6", "unit": "weeks out", "title": "We listen, the room is held", "text": "One call, two or three venues, the one you love held by the end of the week.", "items": ["Guest of honor", "Guest list", "Venue held"]}, {"when": "5", "unit": "weeks out", "title": "Your people", "text": "Catering, flowers, photographer, music and cake booked together.", "items": ["Catering", "Flowers", "Photographer", "Music", "Cake"]}, {"when": "4", "unit": "weeks out", "title": "Invitations out", "text": "Digital or printed, replies tracked for you.", "items": ["Invitations", "Replies", "Design story"]}, {"when": "1", "unit": "week out", "title": "Final numbers", "text": "Counts, run-of-show, call times.", "items": ["Final count", "Run-of-show"]}, {"when": "The", "unit": "day", "title": "You host", "text": "We are there first and leave last.", "items": ["Room set", "Evening held"]}]}, {"label": "Three Weeks", "note": "A surprise party, a last-minute visit from family abroad. A short runway, planned with the same care.", "rows": [{"when": "3", "unit": "weeks out", "title": "Everything in week one", "text": "Room held, caterer and florist booked, invitations out, all within seven days.", "items": ["Venue held", "Catering", "Flowers", "Invitations out"]}, {"when": "2", "unit": "weeks out", "title": "The details", "text": "Photographer, music, cake, a short program.", "items": ["Photographer", "Music", "Cake", "Program"]}, {"when": "3", "unit": "days out", "title": "Final numbers", "text": "Counts and call times.", "items": ["Final count", "Call times"]}, {"when": "The", "unit": "day", "title": "You host", "text": "Same calm, shorter runway.", "items": ["Room set", "Evening held"]}]}]
CORP_PLAN = [{"label": "Twelve Weeks", "note": "Ideal for a gala, a launch or anything with a stage and a program.", "rows": [{"when": "12", "unit": "weeks out", "title": "Brief and venue", "text": "You brief us, we return a one-page plan and a cost estimate, and hold the venue.", "items": ["Brief", "One-page plan", "Estimate", "Venue held", "COI"]}, {"when": "9", "unit": "weeks out", "title": "Production team", "text": "Staging and AV, catering, d\u00e9cor, photographer, entertainment and registration.", "items": ["AV &amp; staging", "Catering", "D\u00e9cor", "Photographer", "Entertainment", "Registration"]}, {"when": "6", "unit": "weeks out", "title": "Brand and invitations", "text": "Signage, screens, stationery and gifting proofed against your guidelines. Invitations out.", "items": ["Signage proofs", "Screens", "Invitations", "Gifting"]}, {"when": "3", "unit": "weeks out", "title": "Run-of-show", "text": "Minute by minute, speaker briefings, rehearsal slots, seating, contingency.", "items": ["Run-of-show", "Rehearsal", "Seating", "Contingency"]}, {"when": "1", "unit": "week out", "title": "Final confirmations", "text": "Headcount to the caterer, badges printed, call sheet issued, your team briefed.", "items": ["Final count", "Badges", "Call sheet", "Team brief"]}, {"when": "Event", "unit": "day", "title": "We run the floor", "text": "Your team hosts. Afterwards, one debrief.", "items": ["Floor held", "Debrief"]}]}, {"label": "Eight Weeks", "note": "Our standard runway. Everything above, in a tighter sequence.", "rows": [{"when": "8", "unit": "weeks out", "title": "Brief and venue", "text": "Plan, estimate and venue in the first week.", "items": ["Brief", "Plan", "Venue held", "COI"]}, {"when": "6", "unit": "weeks out", "title": "Production team", "text": "Booked together.", "items": ["AV &amp; staging", "Catering", "D\u00e9cor", "Photographer", "Registration"]}, {"when": "4", "unit": "weeks out", "title": "Brand and invitations", "text": "Proofs and invitations out.", "items": ["Signage proofs", "Invitations"]}, {"when": "2", "unit": "weeks out", "title": "Run-of-show", "text": "Written and rehearsed.", "items": ["Run-of-show", "Rehearsal", "Seating"]}, {"when": "Event", "unit": "day", "title": "We run the floor", "text": "Followed by one debrief.", "items": ["Floor held", "Debrief"]}]}, {"label": "Four Weeks", "note": "A client dinner, a holiday party, a team offsite. Quick, and still on brand.", "rows": [{"when": "4", "unit": "weeks out", "title": "Brief, venue, team", "text": "All three in the first week.", "items": ["Brief", "Venue held", "Catering", "AV"]}, {"when": "2", "unit": "weeks out", "title": "Invitations and run-of-show", "text": "Out and written.", "items": ["Invitations", "Run-of-show"]}, {"when": "3", "unit": "days out", "title": "Final confirmations", "text": "Counts and call sheet.", "items": ["Final count", "Call sheet"]}, {"when": "Event", "unit": "day", "title": "We run the floor", "text": "Your team hosts.", "items": ["Floor held", "Debrief"]}]}]

TR_PLAN = [{"label": "Three Months", "note": "Time to settle the date with your officiant, prepare the home or venue and bring everyone in without hurry.", "rows": [{"when": "12", "unit": "weeks out", "title": "We learn the tradition", "text": "The occasion, your family\u2019s customs, the officiant\u2019s needs, the guest count and the budget, written into one plan.", "items": ["Customs", "Officiant", "Guest count", "Budget"]}, {"when": "10", "unit": "weeks out", "title": "The setting is chosen", "text": "Your home or a venue, assessed for ceremony space, seating, catering and comfortable guest flow.", "items": ["Venue or home", "Layout", "Timing"]}, {"when": "8", "unit": "weeks out", "title": "Your partners", "text": "D\u00e9cor, catering, photography and other needs, including vendors you already prefer.", "items": ["D\u00e9cor", "Catering", "Photography", "Officiant coordination"]}, {"when": "4", "unit": "weeks out", "title": "Ceremony and design", "text": "Ritual order, supplies, d\u00e9cor, outfits and hospitality agreed with your family and officiant.", "items": ["Ritual sequence", "Supplies", "D\u00e9cor", "Menu"]}, {"when": "1", "unit": "week out", "title": "The day confirmed", "text": "Vendors, delivery times, family responsibilities, guest movement and the schedule, finalized.", "items": ["Timeline", "Vendor calls", "Guest flow"]}, {"when": "The", "unit": "day", "title": "Your family is present", "text": "We manage the setup, transitions and vendors while you take part.", "items": ["On-site team", "Celebration"]}]}, {"label": "Six Weeks", "note": "A comfortable runway for most ceremonies. Priorities are set in the first week.", "rows": [{"when": "6", "unit": "weeks out", "title": "The tradition and the setting", "text": "Customs, officiant, guest count and the home or venue, settled in the first week.", "items": ["Customs", "Guest count", "Venue or home"]}, {"when": "5", "unit": "weeks out", "title": "Your partners", "text": "D\u00e9cor, catering and photography chosen together, with the vendors you prefer.", "items": ["D\u00e9cor", "Catering", "Photography"]}, {"when": "3", "unit": "weeks out", "title": "Ceremony and design", "text": "Ritual order, supplies and hospitality agreed with your family and officiant.", "items": ["Ritual sequence", "Supplies", "Menu"]}, {"when": "1", "unit": "week out", "title": "The day confirmed", "text": "Delivery times, family responsibilities and the schedule.", "items": ["Timeline", "Guest flow"]}, {"when": "The", "unit": "day", "title": "Your family is present", "text": "We hold the day so you can be part of it.", "items": ["On-site team", "Celebration"]}]}, {"label": "Three Weeks", "note": "When the date is close, we set clear priorities in the first few days and focus on what the ceremony needs most.", "rows": [{"when": "3", "unit": "weeks out", "title": "Essentials first", "text": "Customs, the setting and key partners confirmed in the first week.", "items": ["Customs", "Venue or home", "Catering", "Officiant coordination"]}, {"when": "2", "unit": "weeks out", "title": "Ceremony and design", "text": "Ritual order, supplies and d\u00e9cor agreed with your family.", "items": ["Ritual sequence", "Supplies", "D\u00e9cor"]}, {"when": "3", "unit": "days out", "title": "The day confirmed", "text": "Final counts, delivery times and the schedule.", "items": ["Final count", "Timeline"]}, {"when": "The", "unit": "day", "title": "Your family is present", "text": "Same care, shorter runway.", "items": ["On-site team", "Celebration"]}]}]

# ------------------------------------------------------------------ HOME
home = f'''<header class="hero" data-carousel><div class="wrap">
<div class="copy">
<div class="cap on"><p class="kicker">Indian &amp; South Asian Wedding &amp; Event Planning · South Florida</p><h1 class="h-display">Seamless Planning. Timeless Celebrations.</h1><div class="rule left"></div><p class="lede">Eight years of team experience. Cultural understanding. Trusted vendor relationships. One thoughtful plan—so you can enjoy every moment.</p><div class="actions"><a class="btn fill" href="#0" data-book>Plan Your Celebration {ARROW}</a><a class="btn" href="#unfolds">How We Plan</a></div></div>
<div class="cap"><p class="kicker">Indian &amp; South Asian Weddings</p><h2 class="h-display">Every Tradition Honored. Every Detail Thoughtfully Planned.</h2><div class="rule left"></div><p class="lede">Indian, Pakistani, Sikh, South Indian and multicultural celebrations—every ritual and wedding event connected through one clear plan.</p><div class="actions"><a class="btn fill" href="weddings.html">Explore Wedding Planning {ARROW}</a></div></div>
<div class="cap"><p class="kicker">Milestones · Traditions · Corporate</p><h2 class="h-display">Meaningful Moments. Beautifully Brought Together.</h2><div class="rule left"></div><p class="lede">From meaningful traditions and milestone celebrations to company gatherings, we handle the details so you can enjoy the occasion.</p><div class="actions"><a class="btn fill" href="traditions.html">Explore Traditions {ARROW}</a><a class="btn" href="#services">View All Services</a></div></div>
<div class="dots" role="tablist" aria-label="Celebrations"><button role="tab" aria-selected="true">Anvaya</button><button role="tab" aria-selected="false">Weddings</button><button role="tab" aria-selected="false">Milestones, Traditions &amp; Corporate</button></div>
</div>
<div class="mosaic">{mosaic_set([W[0],M[0],C[0]],True)}{mosaic_set(W,False)}{mosaic_set([M[0],C[0],M[1]],False)}</div>
</div></header>

<section><div class="wrap"><div class="letter reveal">
<div class="photo">{slot("about/kitchen.jpg","Garlands on the kitchen floor, wedding morning")}<span class="plate">Est. Miami</span></div>
<div>
<p class="kicker">About Anvaya</p><h2 class="h-serif" style="margin:.6rem 0 1.4rem"><span style="display:inline-block">Experienced Planning.</span> <span style="display:inline-block">Thoughtful Celebrations.</span></h2>
<div class="text">
<p>At Anvaya, every celebration begins with your story, your family, and your traditions. We bring everything together through thoughtful planning, ensuring every detail is considered and every tradition is&nbsp;honored.</p>
<p>Our team brings eight years of experience through JRN Events, having worked on hundreds of weddings and celebrations across different cultures. With deep South Florida knowledge and strong vendor relationships, we help you find quality services at competitive&nbsp;prices.</p>
<p>From venue selection and vendor negotiations to timelines and on-site coordination, we take care of the details so you and your family can be fully present and enjoy every&nbsp;moment.</p>
<p class="sign">Anvaya</p>
</div></div></div></div></section>

<section class="ivory" id="services"><div class="wrap">
<div class="head reveal"><p class="kicker">What We Plan</p><h2 class="h-display">Celebrations We Plan</h2><div class="rule"></div></div>

<div class="row reveal">
<div class="art">{"".join(slot(s,b) for s,b in W)}</div>
<div class="copy"><span class="script">weddings</span><h2 class="h-serif"><span style="display:inline-block">Every Tradition Honored.</span> <span style="display:inline-block">Every Wedding Thoughtfully Planned.</span></h2><p class="lede">From Indian and Pakistani weddings to Bangladeshi, Sikh, South Indian, Christian and interfaith celebrations, we understand how rituals, families and multiple events fit together. One team plans every part of the weekend.</p>
<ul><li>Venue selection and wedding-weekend logistics</li><li>Curated vendor options across styles and budgets</li><li>Cultural ceremonies and coordinated timelines</li><li>On-site management from welcome to farewell</li></ul>
<a class="textlink" href="weddings.html">Our Wedding Planning</a></div>
</div>

<div class="row flip reveal">
<div class="art">{"".join(slot(s,b) for s,b in M)}</div>
<div class="copy"><span class="script">milestones</span><h2 class="h-serif">Your Milestones. Beautifully Celebrated.</h2><p class="lede">Milestone birthdays, anniversaries, baby showers and achievements deserve thoughtful celebrations. We bring the setting, vendors and details together so you can enjoy the people who matter most.</p>
<ul><li>Venues suited to your guest list</li><li>Personalized décor, dining and entertainment</li><li>Invitations, RSVPs and guest experience</li><li>Seamless celebration-day coordination</li></ul>
<a class="textlink" href="milestones.html">Our Milestone Planning</a></div>
</div>

<div class="row reveal">
<div class="art">{slot("weddings/ceremony.jpg","A priest-led ritual by the sacred fire")}{slot("milestones/vow-renewal.jpg","Garlands exchanged, family gathered")}{slot("about/evening.jpg","Lanterns lit for an evening at home")}</div>
<div class="copy"><span class="script">traditions</span><h2 class="h-serif">Meaningful Traditions. Thoughtfully Planned.</h2><p class="lede">From dhoti and half-saree ceremonies to naming celebrations and housewarmings, we plan the rituals, décor, hospitality and flow with care for what each occasion means to your family.</p>
<ul><li>Ceremony timing and family customs</li><li>Décor, catering and seating</li><li>Priest/officiant and vendor coordination</li><li>Thoughtful hosting and on-site management</li></ul>
<a class="textlink" href="traditions.html">Explore Traditional Celebrations</a></div>
</div>

<div class="row flip reveal">
<div class="art">{"".join(slot(s,b) for s,b in C)}</div>
<div class="copy"><span class="script">corporate</span><h2 class="h-serif">Corporate Events Planned with Purpose.</h2><p class="lede">From executive dinners and galas to company celebrations and product launches, we create polished experiences that reflect your brand, engage guests and stay organized behind the scenes.</p>
<ul><li>Venue sourcing and supplier coordination</li><li>Brand-aligned event design and production</li><li>Guest registration and event logistics</li><li>Detailed schedules and on-site delivery</li></ul>
<a class="textlink" href="corporate.html">Our Corporate Events</a></div>
</div>
</div></section>

<section id="unfolds"><div class="wrap">
<div class="head reveal"><p class="kicker">How We Work</p><h2 class="h-display">How We Bring Your Celebration Together</h2><div class="rule"></div><p class="lede">Good planning gives creativity room to shine. Our five steps keep your vision, budget, vendors and event experience moving together.</p></div>
{timeline([
 ("We Understand Your Story","We begin with your occasion, priorities, family traditions, guest count and budget. What matters to you becomes the starting point of every decision.",["Your vision","Guest count","Budget"],("studio/listening.jpg","The first conversation")),
 ("We Find the Right Setting","We shortlist venues that fit your events, guests and overall vision—considering ceremony needs, access, logistics and the experience you want to create.",["Venue options","Dates confirmed"],("studio/walkthrough.jpg","Walking the ballroom together")),
 ("We Curate Your Vendor Team","Explore options for catering, décor, photography, music and more. We help compare proposals, coordinate decisions and bring your chosen partners into one plan.",["Vendor options","Proposals","Contracts"],("studio/tasting.jpg","Menu tasting with the family")),
 ("We Shape Every Detail","Design, menus, schedules and traditions come together in a considered experience. Every supplier knows what is expected and when.",["Event design","Menus","Ceremony details"],("studio/design-board.jpg","Swatches, garlands, stationery")),
 ("We Bring It All Together","On celebration day, our team coordinates deliveries, vendors, transitions and timing so the event unfolds with confidence and care.",["On-site coordination","Event timeline"],("studio/timeline.jpg","The day, in our hands")),
], "One vision. Connected details. Memories that stay with you.")}
</div></section>

<section class="sage"><div class="wrap">
<div class="head reveal"><p class="kicker">The Anvaya Difference</p><h2 class="h-display">Why Families Choose Anvaya</h2><div class="rule"></div><p class="lede">The experience should feel just as considered as the celebration itself.</p></div>
<div class="cols four stagger">
<div><span class="script">i.</span><h3>Cultural Understanding</h3><p>We plan around the meaning behind each tradition—from ceremony sequences and family customs to food preferences, religious considerations and guest experience.</p></div>
<div><span class="script">ii.</span><h3>Choice, Not a Template</h3><p>Access a diverse network of venue and vendor options. We help you compare styles, services and budgets so the celebration feels like yours.</p></div>
<div><span class="script">iii.</span><h3>Vendor Choice &amp; Negotiation</h3><p>Our established vendor relationships help us shortlist appropriate options, compare proposals and negotiate terms with your priorities in mind. We gladly coordinate vendors you have chosen, too.</p></div>
<div><span class="script">iv.</span><h3>Experience You Can Rely On</h3><p>Anvaya is a new brand, supported by event experience gained over eight years through JRN Events and work on hundreds of celebrations. We bring that practical knowledge to every planning decision.</p></div>
</div></div></section>

<section><div class="wrap">
<div class="head reveal"><p class="kicker">Celebrations &amp; Inspiration</p><h2 class="h-display">Celebrations That Inspire</h2><div class="rule"></div></div>
<div class="gallery">
{slot("gallery/1.jpg","Wedding Ceremony","tall")}{slot("gallery/2.jpg","Elegant Tablescapes","wide")}{slot("gallery/3.jpg","Sangeet Celebration")}{slot("gallery/4.jpg","Mehndi Details","tall")}{slot("gallery/5.jpg","Inspired Dining")}{slot("gallery/6.jpg","Waterfront Weddings","wide")}
</div></div></section>

''' + mapsection("Rooted in South Florida. Planning Beyond.",
  "We plan weddings, traditions, milestones and corporate events in Miami, Fort Lauderdale, Boca Raton and Palm Beach, with U.S. and international destinations available by arrangement.",
  ["From city hotels to waterfront venues, we plan occasions across Miami-Dade, Broward and Palm Beach counties.",
   "Destination wedding weekends, family celebrations and corporate programs planned with local venue and vendor coordination.",
   "Thoughtful planning for coastal celebrations, estate gatherings and intimate occasions on Florida’s Gulf Coast.",
   "Have a meaningful destination in mind? Tell us where; we can discuss the logistics and planning scope."]) + f'''
<section><div class="wrap">
<div class="head reveal"><p class="kicker">Kind Words</p><h2 class="h-display">Words from the Families We Serve</h2><div class="rule"></div></div>
<div class="words stagger">
<blockquote><p><span class="placeholder">[Genuine, permission-approved client review]</span></p><cite><span class="placeholder">[Client · Occasion · Location]</span></cite></blockquote>
<blockquote><p><span class="placeholder">[Genuine, permission-approved client review]</span></p><cite><span class="placeholder">[Client · Occasion · Location]</span></cite></blockquote>
<blockquote><p><span class="placeholder">[Genuine, permission-approved client review]</span></p><cite><span class="placeholder">[Client · Occasion · Location]</span></cite></blockquote>
</div></div></section>
''' + cta("Begin Here","Let’s Plan Something Meaningful Together.","Tell us what you are planning, which traditions matter and where you imagine bringing everyone together. We’ll explore how to make it beautifully yours.", label2="Contact Anvaya")

# ------------------------------------------------------------------ ABOUT
about = banner("Our Story","Eight Years of Experience. Hundreds of Celebrations.",
 ["Anvaya brings together eight years of event experience developed through JRN Events, including hundreds of weddings and celebrations across different cultures and traditions.",
  "We understand what makes each celebration meaningful, from honoring family traditions to coordinating every detail. With trusted vendor relationships, thoughtful planning, and a commitment to quality and value, we take care of everything so you can enjoy the moments that matter most."],
 [("about/kitchen.jpg","Wedding morning, garlands on the kitchen floor"),("studio/team.jpg","The Anvaya team"),("about/evening.jpg","Last guests leaving, lanterns still lit")]) + f'''
<section><div class="wrap">
<div class="head reveal"><p class="kicker">The Story of Anvaya</p><h2 class="h-display">The Experience and People Behind Anvaya</h2><div class="rule"></div></div>
{story([
 ("about/kitchen.jpg","Wedding morning at home"),
 ("about/evening.jpg","Hosts missing their own celebration"),
 ("studio/design-board.jpg","Our table in the studio"),
 ("studio/team.jpg","The team today"),
],[
 ("one","Every Celebration Begins with Your Story","No two celebrations should feel the same. We begin by understanding your people, customs, priorities and the experiences you want to share."),
 ("two","Experience That Makes a Difference","Anvaya draws on eight years of team experience developed through JRN Events and work across hundreds of weddings and events—bringing hands-on knowledge of vendors, production and family celebrations."),
 ("three","Trusted Relationships. More Choices for You.","We help you explore suitable venues and vendors, compare proposals, negotiate terms and bring your selected professionals into a coordinated plan—without limiting you to one décor partner."),
 ("four","Celebrations Across South Florida","Based in the South Florida market, we plan Indian, Pakistani, South Asian, multicultural and interfaith weddings, traditional ceremonies, milestone occasions and corporate events in Florida and beyond."),
])}
</div></section>

<section class="ivory"><div class="wrap">
<div class="head reveal"><p class="kicker">What Drives Us</p><h2 class="h-display">Our Mission and Vision</h2><div class="rule"></div></div>
<div class="mv">
<div class="panel">{slot("milestones/vow-renewal.jpg","Garlands exchanged at fifty years")}<div class="card"><p class="kicker">Mission</p><h3>Make Every Moment Matter</h3><p>To create deeply personal celebrations through cultural understanding, meaningful design, thoughtful vendor choices and seamless coordination—so hosts and guests can truly enjoy being together.</p></div></div>
<div class="panel">{slot("weddings/ceremony.jpg","Pheras under the mandap")}<div class="card"><p class="kicker">Vision</p><h3>Become a Trusted Celebration Partner</h3><p>To be known across Florida for celebrations that connect people, honor traditions and bring creativity together with clarity, care and dependable execution.</p></div></div>
</div></div></section>

<section><div class="wrap">
<div class="head reveal"><p class="kicker">What We Believe</p><h2 class="h-display">What Guides Every Decision We Make</h2><div class="rule"></div></div>
<div class="cols stagger">
<div><span class="script">one</span><h3>Traditions Deserve Understanding</h3><p>We ask, listen and plan with intention. Whether it's a Hindu muhurtham, Sikh Anand Karaj, Muslim nikah or a family-specific custom, the meaning guides the logistics.</p></div>
<div><span class="script">two</span><h3>Vendor Options With Guidance</h3><p>You deserve options, not a predetermined list. We use our network and negotiation experience to help you compare qualified vendors and choose what fits your style, requirements and budget.</p></div>
<div><span class="script">three</span><h3>Details Should Work Together</h3><p>Creative ideas are only as good as their execution. We connect teams, timelines and guest needs so every part of the experience feels considered.</p></div>
</div></div></section>

<section class="sage"><div class="wrap">
<div class="head reveal"><p class="kicker">Who We Work With</p><h2 class="h-display">Who We Plan For</h2></div>
<div class="cols four stagger">
<div><span class="script">a.</span><h3>Couples Planning Multicultural Weddings</h3><p>Indian, Pakistani, Bangladeshi, Sikh, South Indian and interfaith celebrations often involve distinct events, family priorities and guest logistics. We build the plan around your needs.</p></div>
<div><span class="script">b.</span><h3>Families Honoring Milestones</h3><p>From milestone anniversaries to family reunions, we help turn shared memories and new beginnings into gatherings with heart.</p></div>
<div><span class="script">c.</span><h3>Families Celebrating Traditions</h3><p>Dhoti, half-saree, naming ceremonies and housewarmings deserve a plan that respects ceremonial details and makes every guest feel welcome.</p></div>
<div><span class="script">d.</span><h3>Teams Planning Meaningful Events</h3><p>Corporate dinners, launches, retreats and celebrations supported by clear budgets, logistics and brand-minded execution.</p></div>
</div></div></section>

<!-- testimonial slot: hidden until a verified, permission-approved review is available -->
<section hidden><div class="wrap">
<p class="quote-block reveal"><span class="script">in their words</span><span class="q"><span class="placeholder">[Verified, permission-approved client review]</span></span><cite style="font-style:normal"><span class="placeholder">[Client · Occasion · Location]</span></cite></p>
</div></section>

''' + mapsection("Across South Florida and Beyond",
  "South Florida is our primary home for planning. We also support celebrations elsewhere in the United States and internationally when the scope and logistics allow.",
  ["South Florida celebrations, from modern city venues to intimate waterfront settings.",
   "Destination wedding weekends and corporate programs with coordinated venue, vendor and guest planning.",
   "Estate events, family milestones and elegant gatherings along the Gulf Coast.",
   "Tell us where the celebration belongs; we’ll explore the right planning approach together."]) + '''
''' + cta("Begin Here","Let’s Create Something Meaningful","Share your vision, your guest list and the moments that matter most. We would love to help bring them together.")

# ------------------------------------------------------------------ BLOG POSTS (listed on Weddings, so parsed first)
# blog.md: "## Blog N — Headline", "**Field:** value" lines, "### " subheadings, paragraphs with **bold**
RELATED = {"Weddings":"weddings.html", "Contact":"contact.html", "About":"about.html", "Traditions":"traditions.html"}
inline = lambda s: re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html.escape(s))
POSTS = []
for chunk in ("\n" + (ROOT / "blog.md").read_text(encoding="utf-8")).split("\n## ")[1:]:
    first, *rows = chunk.strip().split("\n")
    p = {"h": first.split(" — ", 1)[1], "body": ""}
    for r in map(str.strip, rows):
        m = re.match(r"\*\*(.+?):\*\* *(.*)", r)
        if m: p[m[1]] = m[2]
        elif r.startswith("### "): p["body"] += f"<h2>{inline(r[4:])}</h2>"
        elif r: p["body"] += f"<p>{inline(r)}</p>"
    p["path"] = p["Suggested slug"].strip("/")
    POSTS.append(p)
RESOURCES = [("blog/indian-wedding-planning-timeline", "Indian Wedding Planning Timeline: 14 Months, 9 Months or 6 Months", "What happens fourteen, nine or six months before an Indian or South Asian wedding weekend, from venues and vendors to the weekend itself.")]
POST_CARDS = '<div class="cols posts stagger">' + "".join(f'<div><h3><a href="{path}/index.html">{keep_whole(html.escape(h))}</a></h3><p>{html.escape(d)}</p></div>' for path,h,d in [(p["path"], p["h"], p["Meta description"]) for p in POSTS] + RESOURCES) + '</div>'

# ------------------------------------------------------------------ WEDDINGS
WED_FAQ = [  # rendered on the page and in the FAQPage schema
 ("When should we hire an Indian wedding planner in South Florida?","For a multi-event wedding, starting 12–18 months ahead often allows more venue and vendor choices, especially during popular dates. A shorter timeline can still work depending on availability, guest count and flexibility."),
 ("Does Anvaya plan Pakistani, Sikh and other South Asian weddings?","Yes. Our planning approach accommodates Indian, Pakistani, Bangladeshi, Sikh, Hindu, Muslim, Christian and multicultural celebrations. We learn your exact customs with your family and officiants rather than assuming every wedding follows the same traditions."),
 ("Can we use vendors we have already selected?","Absolutely. We can coordinate with your existing venue, caterer, décor team or other suppliers, review the remaining needs and bring everyone into a connected schedule."),
 ("What affects the cost of wedding planning?","The scope depends on the number of events, guest count, venues, travel requirements, design and production complexity, and how much planning support you need. We discuss the scope and fee before you commit."),
 ("Can you coordinate a wedding across multiple venues and days?","Yes. We can connect event schedules, vendor arrivals, ceremony timing, guest transportation and venue transitions across a multi-day wedding weekend. The result is one coordinated plan rather than separate events competing for attention."),
]
WED_CTA = cta("Begin Here","Your Wedding Should Feel Like Your Family","Tell us about the traditions you treasure, the celebrations you imagine and the people coming together. We’ll help connect every moment.", "Plan Your Wedding Weekend")  # also closes every blog post
weddings = banner("Weddings","Your wedding, celebrated the way your family remembers it","At Anvaya, we plan Indian, South Asian and multicultural weddings across South Florida, thoughtfully honoring each family’s traditions and celebrations.", W) + f'''
<section><div class="wrap"><div class="letter reveal">
<div class="photo">{slot("weddings/ceremony.jpg","Pheras, ghee on the fire")}<span class="plate">Weddings</span></div>
<div>
<p class="kicker">What We Plan</p><h2 class="h-serif" style="margin:.6rem 0 1.4rem">Every Tradition Honored. Every Detail Considered.</h2>
<div class="text">
<p>Every wedding is a beautiful combination of traditions, family, and unforgettable moments. From mehndi, haldi, and sangeet to the ceremony and reception, we ensure every celebration receives the attention it&nbsp;deserves.</p>
<p>Anvaya brings together venues, trusted vendors, budgets, and family needs through one thoughtful plan. Our strong vendor relationships help us secure competitive pricing without compromising on quality or service, while we coordinate every detail so you can enjoy your celebration.</p>
<p>We plan Indian, Pakistani, Bangladeshi, Sikh, South Indian, Muslim, Hindu, Christian, and interfaith weddings across South Florida, honoring the traditions that make your celebration uniquely yours.</p>
<p><a class="textlink" href="traditions.html">Explore Traditional Ceremonies</a></p>
</div></div></div></div></section>

<section class="ivory" id="process"><div class="wrap">
<div class="head reveal"><p class="kicker">How We Plan Your Wedding</p><h2 class="h-display">How We Plan Your Wedding, Step by Step</h2><div class="rule"></div><p class="lede">Understand the family. Find the setting. Choose the right team. Design the events. Connect the logistics. Celebrate with confidence.</p></div>
{timeline([
 ("Understand Your Family &amp; Vision","We learn the wedding events, religious and family traditions, guest expectations, planning priorities and budget. Your story becomes the planning brief.",["Event list","Budget priorities","Guest estimate"],("studio/listening.jpg","Over coffee, listening")),
 ("Find &amp; Secure Your Venues","We compare venues with more than aesthetics in mind: ceremony space, baraat possibilities, catering policies, guest rooms, weather backup and event transitions.",["Ceremony venue","Reception venue","Hotel rooms"],("studio/walkthrough.jpg","Walking the ballroom")),
 ("Build Your Vendor Team","From caterers and decorators to photographers, DJs and officiants, we present suitable options, coordinate comparisons and help you assemble your preferred team.",["Catering","Décor &amp; florals","Photo &amp; film","Entertainment","Beauty","Officiants"],("studio/tasting.jpg","Tasting with the family")),
 ("Design Each Celebration","We bring together décor, menus, ceremony needs, event styling and guest touchpoints—giving each function its own identity while keeping the wedding cohesive.",["Design concept","Tasting","Stationery","Ceremony schedule"],("studio/design-board.jpg","The design board")),
 ("Connect the Logistics","We build working timelines for events, vendors, transport, guest flow, rehearsals and contingency plans so no important detail stands alone.",["Event schedules","Seating","Transport","Weather plan"],("studio/timeline.jpg","The timeline, printed")),
 ("Manage the Wedding Weekend","Our on-site team coordinates setup, vendors, ceremony transitions and event cues while you celebrate with the people who matter.",["On-site team","Vendor coordination","Final send-off"],("weddings/ceremony.jpg","The ceremony, held")),
], "Whether you are planning well in advance or working with a shorter timeline, we adapt the pace to your celebration.")}
</div></section>

<section><div class="wrap">
<div class="head reveal"><p class="kicker">Your Wedding Vendor Team</p><h2 class="h-display">The Right Vendors for Every Part of Your Wedding</h2><div class="rule"></div><p class="lede">Explore a range of vendor styles and services. We help compare options, match them to your priorities and coordinate the professionals you choose.</p></div>
''' + ledger([
 ("Venues","Hotels, resorts, ballrooms and outdoor settings assessed for ceremonies, guest capacity, catering, room blocks and multi-event logistics.",("studio/walkthrough.jpg","Walking a Palm Beach ballroom")),
 ("Catering","Indian, Pakistani, South Asian and fusion menus, tastings, vegetarian and religious dietary needs, live stations and late-night food.",("gallery/5.jpg","Live dosa and chaat counter")),
 ("Décor &amp; Florals","Mandaps, stages, aisle design, centerpieces, draping, lighting and floral concepts shaped around every celebration.",("gallery/1.jpg","North Indian mandap, roses and orchids")),
 ("Photography &amp; Film","Photography and cinematography teams suited to your style, schedule and culturally significant wedding moments.",("gallery/4.jpg","Photographer framing mehndi")),
 ("Music &amp; Entertainment","DJs, dhol, live musicians, singers, hosts and sangeet entertainment matched to each event’s energy.",("gallery/3.jpg","DJ and dhol at the sangeet")),
 ("Hair, Makeup &amp; Outfits","Bridal beauty, family styling, outfit changes and getting-ready schedules across multiple events.",("weddings/ceremony.jpg","Bride, mid-ceremony")),
 ("Officiants &amp; Ceremony","Pandits, granthis, imams, ministers and other officiants, with ceremony timing guided by your faith and family preferences.",("weddings/mandap.jpg","Priest at the mandap")),
 ("Transportation &amp; Baraat","Guest shuttles, vehicle logistics, arrival coordination and practical planning for baraat processions where permitted.",("weddings/baraat.jpg","Baraat arriving")),
 ("Invitations &amp; Guest Experience","Save-the-dates, invitation suites, wedding websites, RSVPs, welcome gifts and information for visiting guests.",("studio/design-board.jpg","Invitation suite on the board")),
]) + '''
</div></section>
<section class="ivory"><div class="wrap">
<div class="head reveal"><p class="kicker">Ways to Work With Us</p><h2 class="h-display">Wedding Planning Services Tailored to You</h2><div class="rule"></div></div>
<div class="ways stagger">
<div><p class="kicker">Full Planning</p><h3>Full Wedding Planning, From Start to Finish</h3><p>For couples who want one experienced team to plan and coordinate the entire wedding journey.</p><ul><li>Budget, venues and vendor selection</li><li>Event design and guest experience</li><li>Accommodations and transportation</li><li>Detailed schedules and on-site management</li></ul></div>
<div class="mark"><p class="kicker">Partial Planning</p><h3>Expert Guidance for the Plans You’ve Begun</h3><p>For couples who have booked key elements and want experienced guidance to complete the plan.</p><ul><li>Review existing bookings and budgets</li><li>Source remaining vendor options</li><li>Refine designs and event logistics</li><li>Manage the wedding weekend</li></ul></div>
<div><p class="kicker">Wedding Weekend Management</p><h3>We Coordinate. You Celebrate.</h3><p>For couples who have made their selections and want professional coordination for the final stretch and celebration days.</p><ul><li>Vendor handover and final confirmations</li><li>Detailed schedules and cue sheets</li><li>Rehearsal and ceremony coordination</li><li>On-site event management</li></ul></div>
</div></div></section>

<section><div class="wrap">
<div class="head reveal"><p class="kicker">Questions Couples Ask</p><h2 class="h-display">Frequently Asked Wedding Planning Questions</h2><div class="rule"></div></div>
''' + faq(WED_FAQ) + '''</div></section>

<section class="ivory"><div class="wrap">
<div class="head reveal"><h2 class="h-display">Blog</h2><div class="rule"></div></div>
''' + POST_CARDS + '''
</div></section>
''' + WED_CTA.replace("Your Wedding Should Feel Like Your Family", "Let’s Bring Your Wedding Vision Together")  # this page only: blog posts and the calendar page keep the shared heading

# ------------------------------------------------------------------ MILESTONES
MS_CTA = cta("Begin Here","Let’s Celebrate What Matters Most","Tell us who you’re celebrating and what makes the occasion special. We’ll help shape the experience around them.", "Plan a Milestone")
milestones = banner("Milestone celebrations · Miami &amp; Florida","Life’s milestones, celebrated with meaning and care","At Anvaya, we plan birthdays, anniversaries and milestone celebrations across Florida, creating thoughtful experiences centered around the people who matter most.", M) + f'''
<section><div class="wrap">
<div class="head reveal"><p class="kicker">Occasions</p><h2 class="h-display">Life’s Milestones, Beautifully Celebrated</h2><div class="rule"></div><p class="lede">Some milestones deserve an intimate dinner. Others bring everyone together. We plan each around the people being celebrated, with thoughtful details and dependable coordination.</p></div>
<div class="occasions stagger">
<div tabindex="0"><div class="bg"><img src="img/milestones/first-birthday.jpg" alt="" loading="lazy"></div><p class="kicker">01</p><h3>Milestone Birthdays</h3><p>Celebrate 40, 50, 60, 70 or any meaningful birthday with a setting, food and entertainment that reflect the guest of honor.</p></div>
<div tabindex="0"><div class="bg"><img src="img/milestones/anniversary.jpg" alt="" loading="lazy"></div><p class="kicker">02</p><h3>Silver &amp; Golden Anniversaries</h3><p>Mark 25, 40 or 50 years with a personal gathering, meaningful speeches and shared memories.</p></div>
<div tabindex="0"><div class="bg"><img src="img/milestones/baby-shower.jpg" alt="" loading="lazy"></div><p class="kicker">03</p><h3>Baby Showers</h3><p>Welcome a new chapter with a beautiful, comfortable celebration for family and friends.</p></div>
<div tabindex="0"><div class="bg"><img src="img/gallery/3.jpg" alt="" loading="lazy"></div><p class="kicker">04</p><h3>Sweet Sixteens &amp; Quinceañeras</h3><p>Create a celebration that reflects their personality, from entrances and décor to music, dining and special family moments.</p></div>
<div tabindex="0"><div class="bg"><img src="img/gallery/2.jpg" alt="" loading="lazy"></div><p class="kicker">05</p><h3>Graduation Celebrations</h3><p>Honor achievements with a gathering that makes the graduate feel seen and celebrated.</p></div>
<div tabindex="0"><div class="bg"><img src="img/corporate/dinner.jpg" alt="" loading="lazy"></div><p class="kicker">06</p><h3>Retirement &amp; Personal Achievements</h3><p>Bring together colleagues, friends and family to recognize a meaningful life chapter.</p></div>
</div>
<p class="occ-more reveal">Planning a naming ceremony, housewarming or family ritual? <a class="textlink" href="traditions.html">Explore Traditions</a></p>
</div></section>

<section class="ivory" id="process"><div class="wrap">
<div class="head reveal"><p class="kicker">How We Plan a Milestone</p><h2 class="h-display">How We Plan Your Milestone Celebration</h2><div class="rule"></div><p class="lede">From the first idea to the last guest, we connect the creative and practical details.</p></div>
{timeline([
 ("Discover the Occasion","We understand who you are celebrating, your guest list, priorities, budget and the feeling you want to create.",["Occasion","Guest count","Budget"],("studio/listening.jpg","Listening first")),
 ("Choose the Setting","We source suitable spaces and compare their atmosphere, convenience and practical fit for your gathering.",["Venue options","Date"],("milestones/baby-shower.jpg","A garden terrace, held")),
 ("Select the Right Vendors","Catering, décor, photography, entertainment and specialty suppliers—chosen to suit the occasion and your preferences.",["Catering","Florals","Photography","Music","Cake"],("milestones/first-birthday.jpg","Cake, florals, grandparents")),
 ("Design the Experience","We shape invitations, room styling, menus and entertainment around the guest of honor and the celebration.",["Invitations","RSVPs","Design","Menu"],("studio/design-board.jpg","Design board")),
 ("Finalize the Details","Guest counts, vendor times, special moments and final schedules are aligned before the celebration begins.",["Guest count","Program","Vendor times"],("studio/timeline.jpg","Run-of-show in hand")),
 ("Celebrate with Confidence","We coordinate the setup and flow of the event so you can enjoy every moment with your guests.",["Setup","On-site coordination"],("milestones/vow-renewal.jpg","Fifty years, garlands exchanged")),
], "Whether it’s a small gathering or a major milestone, we plan around your occasion—not a fixed formula.")}
</div></section>

<section><div class="wrap">
<div class="head reveal"><p class="kicker">What We Coordinate</p><h2 class="h-display">Everything Your Celebration Needs</h2><div class="rule"></div><p class="lede">From the setting to the final toast, we help bring the right people and details together.</p></div>
''' + ledger([
 ("Venue","Private dining spaces, gardens, hotels, homes and ballrooms selected for guest comfort and occasion.",("milestones/baby-shower.jpg","A garden terrace")),
 ("Food &amp; Drink","Caterers, custom menus, cakes, dessert displays and dietary options that feel right for your guests.",("milestones/first-birthday.jpg","Cake and florals")),
 ("Décor &amp; Florals","Backdrops, table styling, floral design, lighting and personalized details.",("milestones/anniversary.jpg","Candlelit anniversary table")),
 ("Photography","Photography, videography and photo experiences that preserve the memories.",("gallery/4.jpg","Photographer at work")),
 ("Entertainment &amp; Program","Music, hosts, speeches, activities and timing for the event’s special moments.",("gallery/3.jpg","DJ and dance floor")),
 ("Guest Experience","Invitations, seating, welcome details, accessibility and the flow of meaningful speeches and family moments.",("studio/design-board.jpg","Invitations and welcome details")),
]) + '''
</div></section>
''' + plan_link("milestones", MS_PLAN, "Your Planning Calendar", "Planning Around Your Celebration Date", "Explore how your celebration can come together based on the time available.", "ivory") + '''
''' + MS_CTA

# ------------------------------------------------------------------ TRADITIONS (new in V4; mirrors the Milestones page)
T = [("about/kitchen.jpg","Marigold garlands strung at home before the ceremony"),("weddings/ceremony.jpg","A priest-led ritual by the sacred fire"),("milestones/first-birthday.jpg","Grandparents at a family celebration")]
TR_CTA = cta("Begin Here","Let\u2019s Honor Your Tradition, Your Way.","Tell us the ceremony, the date and the customs important to your family. We\u2019ll help bring the right people and details together.", "Plan a Traditional Celebration", "Contact Anvaya")
traditions = banner("Traditional ceremonies \u00b7 Miami &amp; Florida","Traditions Worth Honoring. Moments Worth Sharing.","From dhoti and half-saree ceremonies to naming celebrations and housewarmings, we plan the rituals, d\u00e9cor, hospitality and flow with care for what each occasion means to your family.", T) + f'''
<section><div class="wrap">
<div class="head reveal"><p class="kicker">Our Traditions</p><h2 class="h-display">Every Tradition Has a Meaning. Every Detail Deserves Care.</h2><div class="rule"></div><p class="lede">Your family\u2019s customs deserve more than a beautiful backdrop. We coordinate the ceremony, timing, hospitality and vendors so generations can share the occasion together.</p></div>
<div class="occasions stagger">
<div tabindex="0"><div class="bg"><img src="img/weddings/ceremony.jpg" alt="" loading="lazy"></div><p class="kicker">01</p><h3>Dhoti Ceremony</h3><p>A meaningful coming-of-age celebration with thoughtful staging, family seating, ritual arrangements and hospitality.</p></div>
<div tabindex="0"><div class="bg"><img src="img/gallery/4.jpg" alt="" loading="lazy"></div><p class="kicker">02</p><h3>Half-Saree Ceremony</h3><p>Mark an important cultural milestone with elegant d\u00e9cor, ceremony flow, outfits and guest coordination.</p></div>
<div tabindex="0"><div class="bg"><img src="img/milestones/first-birthday.jpg" alt="" loading="lazy"></div><p class="kicker">03</p><h3>Naming &amp; Cradle Ceremonies</h3><p>From naamkaran to cradle celebrations, we coordinate the family traditions and a welcoming gathering around them.</p></div>
<div tabindex="0"><div class="bg"><img src="img/about/kitchen.jpg" alt="" loading="lazy"></div><p class="kicker">04</p><h3>Housewarming &amp; Griha Pravesh</h3><p>Ceremony timing, priest coordination, seating and catering planned carefully for celebrations at home.</p></div>
<div tabindex="0"><div class="bg"><img src="img/gallery/5.jpg" alt="" loading="lazy"></div><p class="kicker">05</p><h3>Annaprashan &amp; <span style="white-space:nowrap">First-Rice</span> Ceremonies</h3><p>A warm, family-centered occasion with ceremonial details, d\u00e9cor and meal arrangements brought together.</p></div>
<div tabindex="0"><div class="bg"><img src="img/weddings/mandap.jpg" alt="" loading="lazy"></div><p class="kicker">06</p><h3>Pujas, Blessings &amp; Family Rituals</h3><p>We listen to your family and officiant, then build a practical event plan around your specific observance.</p></div>
</div></div></section>

<section class="ivory" id="process"><div class="wrap">
<div class="head reveal"><p class="kicker">How We Plan</p><h2 class="h-display">Planning Around Your Family’s Traditions</h2><div class="rule"></div><p class="lede">Each family follows its own customs. We begin by understanding yours, then coordinate the people and details that make the celebration feel right.</p></div>
{timeline([
 ("Understand the Tradition","We learn the occasion, family customs, officiant needs, guest count and budget.",["Customs","Guests","Budget"],("studio/listening.jpg","Listening to the family")),
 ("Choose the Setting","We assess the home or venue for ceremony space, seating, catering and comfortable guest flow.",["Venue","Layout","Timing"],("about/evening.jpg","An evening gathering at home")),
 ("Curate Your Partners","We offer suitable choices for décor, catering, photography and other event needs, including vendors you already prefer.",["Vendor options","Proposals","Coordination"],("studio/tasting.jpg","Tasting the menu")),
 ("Plan the Ceremony &amp; Design","We coordinate with the family and officiant on ritual order, supplies, décor, outfits and hospitality.",["Ritual sequence","Décor","Food"],("studio/design-board.jpg","Ceremony and décor details")),
 ("Confirm the Day","We finalize vendors, delivery times, family responsibilities, guest movement and the event schedule.",["Timeline","Vendor calls","Guest flow"],("studio/timeline.jpg","The run-of-show")),
 ("Coordinate While You Celebrate","Our team manages the setup, transitions and vendors, giving the family more time to be present.",["On-site team","Celebration"],("milestones/vow-renewal.jpg","Garlands, family gathered")),
], "Every family’s customs are different. We plan around yours.")}
</div></section>

<section><div class="wrap">
<div class="head reveal"><p class="kicker">What We Coordinate</p><h2 class="h-display">Everything Needed for Your Traditional Celebration</h2><div class="rule"></div><p class="lede">We bring together the vendors and practical requirements your family needs, with choice and thoughtful coordination.</p></div>
''' + ledger([
 ("Venue &amp; Layout","Homes, clubhouses and event spaces with practical arrangements for ceremony and guests.",("about/evening.jpg","An evening gathering at home")),
 ("Catering &amp; Hospitality","Vegetarian, regional and family-preferred menus, serving arrangements and guest comfort.",("gallery/5.jpg","A vegetarian live counter")),
 ("D\u00e9cor &amp; Florals","Ceremony backdrops, stages, seating, floral accents and personalized welcome details.",("gallery/1.jpg","Florals and a ceremony stage")),
 ("Photography &amp; Film","Artists who can follow key ceremonial moments without interrupting them.",("gallery/4.jpg","Photographer at a ceremony")),
 ("Priest / Officiant Coordination","Confirmed ritual order, timing, supplies and family participation with the officiant you choose.",("weddings/mandap.jpg","Priest at the ceremony")),
 ("Guest &amp; Day-of Logistics","Invitations, seating, vendor arrival, parking and a clear run-of-show.",("studio/timeline.jpg","Run-of-show in hand")),
]) + '''
</div></section>
''' + plan_link("traditions", TR_PLAN, "Your Planning Timeline", "Your Ceremony Planning Timeline", "Whether your occasion is months away or approaching soon, we help set clear priorities for the time available.", "ivory") + '''
''' + TR_CTA

# ------------------------------------------------------------------ CORPORATE
CORP_CTA = cta("Begin Here","Have an Event in Mind? Let’s Make It Happen.","Share your dates, goals, guest count and budget parameters. We’ll discuss an approach tailored to your event.", "Request a Proposal")
corporate = banner("Corporate event planners · Miami &amp; Florida","Corporate gatherings, planned to feel effortless","At Anvaya, we produce offsites, launches, award nights, holiday celebrations and client dinners across Florida, from our home in Miami, with one point of contact.", C) + f'''
<section><div class="wrap">
<div class="head reveal"><p class="kicker">Occasions</p><h2 class="h-display">Corporate Events That Reflect Your Brand</h2><div class="rule"></div><p class="lede">Whether you are celebrating a team, welcoming clients or introducing something new, we turn your business objective into a well-orchestrated experience.</p></div>
<div class="occasions stagger">
<div tabindex="0"><div class="bg"><img src="img/studio/walkthrough.jpg" alt="" loading="lazy"></div><p class="kicker">Internal</p><h3>Offsites &amp; Retreats</h3><p>Purposeful environments for collaboration, connection and fresh thinking, supported by thoughtful schedules and guest logistics.</p></div>
<div tabindex="0"><div class="bg"><img src="img/corporate/launch.jpg" alt="" loading="lazy"></div><p class="kicker">External</p><h3>Product Launches</h3><p>Brand-led environments, staging, AV and show moments that make your launch feel memorable and professional.</p></div>
<div tabindex="0"><div class="bg"><img src="img/corporate/gala.jpg" alt="" loading="lazy"></div><p class="kicker">Recognition</p><h3>Awards &amp; Galas</h3><p>Elegant production, smooth guest flow and well-timed programs that give recognition its moment.</p></div>
<div tabindex="0"><div class="bg"><img src="img/corporate/dinner.jpg" alt="" loading="lazy"></div><p class="kicker">Seasonal</p><h3>Holiday Celebrations</h3><p>Team gatherings with personalized design, great hospitality and entertainment that reflects your culture.</p></div>
<div tabindex="0"><div class="bg"><img src="img/corporate/rehearsal.jpg" alt="" loading="lazy"></div><p class="kicker">Relationships</p><h3>Client Dinners &amp; Hospitality</h3><p>Thoughtful dining, welcoming details and seamless execution that make important guests feel valued.</p></div>
<div tabindex="0"><div class="bg"><img src="img/weddings/sangeet.jpg" alt="" loading="lazy"></div><p class="kicker">Culture</p><h3>Diwali, Eid &amp; Festive Gatherings</h3><p>Inclusive cultural occasions planned with respect for traditions and the people celebrating them.</p></div>
</div></div></section>

<section class="ivory" id="process"><div class="wrap">
<div class="head reveal"><p class="kicker">How We Produce Your Event</p><h2 class="h-display">From Event Brief to Confident Execution</h2><div class="rule"></div><p class="lede">From the brief to the final cue, we bring creative ideas and production details into one coordinated plan.</p></div>
{timeline([
 ("Understand the Brief","We align on the objective, audience, guest count, location, budget and brand requirements.",["Objective","Guests","Budget","Brand"],("studio/listening.jpg","The brief")),
 ("Secure the Venue","We compare spaces based on function, atmosphere, technical needs, accessibility and total event costs.",["Venue","Contract","Requirements"],("studio/walkthrough.jpg","Walking the venue")),
 ("Build the Production Team","AV, staging, catering, décor, branding, entertainment and registration partners are coordinated to support the experience.",["AV","Catering","Branding","Registration"],("corporate/launch.jpg","The launch floor")),
 ("Map the Event Flow","We develop schedules, technical cues, speaker requirements and guest movement to keep the program on track.",["Run-of-show","Rehearsal","Seating"],("corporate/rehearsal.jpg","Tech rehearsal")),
 ("Confirm Every Detail","We finalize headcounts, vendor arrival times, materials, technical checks and team responsibilities.",["Final count","Print","Vendor call sheet"],("studio/timeline.jpg","Call sheet in hand")),
 ("Deliver with Confidence","Our on-site team oversees suppliers, program transitions and guest experience so your team can focus on hosting.",["On-site production","Wrap-up","Debrief"],("corporate/gala.jpg","Gala, mid-applause")),
], "One coordinated team behind the scenes. A seamless experience in the room.")}
</div></section>

''' + plan_link("corporate", CORP_PLAN, "Your Production Calendar", "Your Corporate Event Planning Timeline", "Explore planning priorities for the timeframe you have, from early venue decisions to final production details.", "white") + '''
<section class="ivory"><div class="wrap">
<div class="head reveal"><p class="kicker">Working With Your Team</p><h2 class="h-display"><span style="display:inline-block">One Coordinated Team.</span> <span style="display:inline-block">Every Detail Managed.</span></h2><div class="rule"></div></div>
<div class="cols four stagger">
<div><span class="script">i.</span><h3>One Planning Point of Contact</h3><p>A coordinated lead for schedules, updates and supplier questions, reducing unnecessary back-and-forth.</p></div>
<div><span class="script">ii.</span><h3>Logistics Considered Early</h3><p>Venue requirements, insurance coordination, permits where applicable and production needs are addressed before event week.</p></div>
<div><span class="script">iii.</span><h3>Designed Around Your Brand</h3><p>We align décor, printed materials, displays and guest touchpoints with your event goals and brand identity.</p></div>
<div><span class="script">iv.</span><h3>Prepared for the Live Moment</h3><p>Run-of-show planning, rehearsals, vendor cues and on-site management help the entire program run smoothly.</p></div>
</div></div></section>
''' + CORP_CTA.replace("Have an Event in Mind? Let’s Make It Happen.", "Let’s Plan Your Next Corporate Event")  # this page only: the calendar page keeps the shared heading

# ------------------------------------------------------------------ CONTACT
contact = f'''
<section style="padding-top:clamp(3rem,6vw,5rem)"><div class="wrap">
<div class="head reveal"><p class="kicker">Contact Anvaya</p><h1 class="h-display">Let’s Start Planning Your Celebration</h1><div class="rule"></div><p class="lede">Tell us what you are celebrating, where your family is gathering and what matters most. We’ll discuss the right planning approach, vendor options and next steps. Or <a href="#0" data-book class="textlink">book a call</a> directly.</p></div>
<div class="contact reveal">
<div>
<dl>
<div><dt>Telephone</dt><dd><span class="placeholder">[Phone number]</span></dd></div>
<div><dt>Email</dt><dd><span class="placeholder">[hello@anvaya…]</span></dd></div>
<div><dt>Studio</dt><dd>Miami, Florida · Meetings by appointment</dd></div>
<div><dt>Where We Work</dt><dd>Miami, Fort Lauderdale, Boca Raton, Palm Beach and destinations across Florida.</dd></div>
<div><dt>Hours</dt><dd><span class="placeholder">[Business hours]</span></dd></div>
<div><dt>Instagram</dt><dd><span class="placeholder">[@anvaya…]</span></dd></div>
</dl>
<div class="after">
<div><span class="script">i.</span><div><h3>Tell Us Your Story</h3><p>Share the occasion, potential date, location and a few details about your vision.</p></div></div>
<div><span class="script">ii.</span><div><h3>Let’s Talk It Through</h3><p>We discuss priorities, guest count, cultural needs, budget and the kind of support you need.</p></div></div>
<div><span class="script">iii.</span><div><h3>Explore the Next Steps</h3><p>We outline a suitable planning approach and the information needed to move forward.</p></div></div>
</div>
</div>
<div>
<form id="enquiry">
<div class="row2"><label for="f-name">Your Name<input id="f-name" name="name" type="text" autocomplete="name" required></label><label for="f-email">Email<input id="f-email" name="email" type="email" autocomplete="email" required></label></div>
<div class="row2"><label for="f-phone">Telephone<input id="f-phone" name="phone" type="tel" autocomplete="tel"></label><label for="f-date">A Date or Season in Mind<input id="f-date" name="date" type="text" placeholder="November 2027, or flexible"></label></div>
<fieldset><legend>What Are We Celebrating?</legend>
<div class="chooser">
<label><input type="radio" name="type" value="Wedding" id="t-w" checked><span>A Wedding or Wedding Weekend</span></label>
<label><input type="radio" name="type" value="Milestone" id="t-m"><span>A Milestone</span></label>
<label><input type="radio" name="type" value="Traditional Ceremony" id="t-t"><span>A Traditional Ceremony</span></label>
<label><input type="radio" name="type" value="Corporate" id="t-c"><span>A Corporate Occasion</span></label>
<label><input type="radio" name="type" value="Other" id="t-o"><span>Something Else</span></label>
</div></fieldset>
<div class="row2"><label for="f-guests">Roughly How Many Guests?<select id="f-guests" name="guests"><option>Under 50</option><option>50 to 150</option><option selected>150 to 300</option><option>300 to 500</option><option>Over 500</option></select></label>
<label for="f-events">How Many Events?<select id="f-events" name="events"><option>1</option><option>2</option><option selected>3</option><option>4</option><option>5 or more</option></select></label></div>
<label for="f-msg">Tell Us a Little<textarea id="f-msg" name="message" placeholder="Who it is for, where you are dreaming of, traditions we should know, anything already booked."></textarea></label>
<label for="f-how">How Did You Find Us?<input id="f-how" name="source" type="text"></label>
<button class="btn fill" type="submit">Send Your Inquiry {ARROW}</button>
<p class="note">Your inquiry is used only to respond to your celebration request.</p>
</form>
<div class="sent" role="status"><p class="kicker">Received</p><h3 class="h-serif" style="font-size:1.7rem">Thank You for Reaching Out<span class="who"></span></h3><p class="muted">Your message has been received. We look forward to learning more about your celebration.</p></div>
</div>
</div>
</div></section>
'''

# ------------------------------------------------------------------ BLOG
def post_main(p):
    rel = " · ".join(f'<a class="textlink" href="{RELATED[n]}">{n}</a>' for n in p["Related pages"].split(" · "))
    return f'''<section><div class="wrap article reveal">
<h1 class="h-display">{keep_whole(html.escape(p["h"]))}</h1><div class="rule left"></div>
{p["body"]}
<p class="related">Related pages: {rel}</p>
</div></section>''' + (TR_CTA if "Traditions" in p["Related pages"] else WED_CTA)  # close on the celebration the article is about

def post_ld(p):
    url = SITE + p["Suggested slug"]
    org = {"@type":"Organization","name":"Anvaya","url":SITE}
    return '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"BlogPosting","headline":p["h"],"description":p["Meta description"],"url":url,"mainEntityOfPage":url,"author":org,"publisher":org}) + '</script>'

blog_index = f'''<section><div class="wrap">
<div class="head reveal"><h1 class="h-display">Blog</h1><div class="rule"></div></div>
{POST_CARDS}
</div></section>'''

# ------------------------------------------------------------------ PLANNING CALENDARS
# one page per celebration, reached from the preview on its celebration page (plan_link)
CALS = {
 CAL_PAGE["weddings"]: dict(sid="weddings", parent="Blog", parent_href="blog/index.html", crumb="Wedding Planning Timeline", name="Indian &amp; South Asian Weddings", tile=W[0][0], data=WED_PLAN, cta=WED_CTA,
   h="Indian Wedding Planning Timeline: 14 Months, 9 Months or 6 Months", lede="Explore a planning approach for the time you have. The sequence stays thoughtful; the schedule adapts.",
   trio=[("studio/walkthrough.jpg","Walking the venue"),("weddings/baraat.jpg","Baraat route agreed"),("studio/tasting.jpg","Tasting with the family")],
   imgs=[("studio/listening.jpg","The first conversation"),("studio/walkthrough.jpg","Walking the venue"),("studio/tasting.jpg","Tasting with the family"),("studio/design-board.jpg","Design board"),("weddings/baraat.jpg","Baraat route agreed"),("studio/timeline.jpg","Timeline in hand"),("weddings/ceremony.jpg","The weekend")],
   title="Indian Wedding Planning Timeline: 14, 9 or 6 Months | Anvaya",
   desc="Plan an Indian or South Asian wedding in South Florida at the right pace: what happens fourteen, nine or six months out, from venues and vendors to the wedding weekend."),
 CAL_PAGE["milestones"]: dict(sid="milestones", parent="Milestones", name="Milestone Celebrations", tile=M[0][0], data=MS_PLAN, cta=MS_CTA,
   h="A Thoughtful Plan for Your Timeline", lede="Explore how your celebration can come together based on the time available.",
   trio=[("milestones/baby-shower.jpg","Baby shower brunch on the terrace"),("milestones/vow-renewal.jpg","Fifty years, garlands exchanged"),("milestones/first-birthday.jpg","First birthday with grandparents")],
   imgs=[("studio/listening.jpg","Listening first"),("milestones/baby-shower.jpg","The room, held"),("milestones/first-birthday.jpg","Cake and florals"),("studio/design-board.jpg","Invitations and design"),("studio/timeline.jpg","Run-of-show"),("milestones/vow-renewal.jpg","The day")],
   title="Milestone Celebration Planning Calendar | Anvaya",
   desc="How a milestone celebration comes together in South Florida with three months, six weeks or three weeks to go, from the first conversation to the day."),
 CAL_PAGE["traditions"]: dict(sid="traditions", parent="Traditions", name="Traditional Ceremonies", tile=T[0][0], data=TR_PLAN, cta=TR_CTA,
   h="A Simple Plan for Your Date", lede="Whether your occasion is months away or approaching soon, we help set clear priorities for the time available.",
   trio=[("about/evening.jpg","An evening gathering at home"),("weddings/ceremony.jpg","A priest-led ritual by the sacred fire"),("about/kitchen.jpg","Marigold garlands strung at home")],
   imgs=[("studio/listening.jpg","Listening to the family"),("about/evening.jpg","The home, prepared"),("studio/tasting.jpg","Tasting the menu"),("studio/design-board.jpg","Ceremony and d\u00e9cor details"),("studio/timeline.jpg","The run-of-show"),("milestones/vow-renewal.jpg","The day")],
   title="Traditional Ceremony Planning Calendar | Anvaya",
   desc="How a dhoti, half-saree, naming or housewarming ceremony comes together in South Florida with three months, six weeks or three weeks to go."),
 CAL_PAGE["corporate"]: dict(sid="corporate", parent="Corporate", name="Corporate Events", tile=C[0][0], data=CORP_PLAN, cta=CORP_CTA,
   h="The Right Timeline for Your Event", lede="Explore planning priorities for the timeframe you have, from early venue decisions to final production details.",
   trio=[("corporate/rehearsal.jpg","Tech rehearsal"),("corporate/gala.jpg","Awards gala, Miami ballroom"),("corporate/launch.jpg","Product launch, Wynwood")],
   imgs=[("studio/listening.jpg","The brief"),("studio/walkthrough.jpg","Venue held"),("corporate/launch.jpg","Production floor"),("studio/design-board.jpg","Brand proofs"),("corporate/rehearsal.jpg","Rehearsal"),("corporate/gala.jpg","Event day")],
   title="Corporate Event Planning Calendar | Anvaya",
   desc="Production calendars for corporate events in South Florida: what happens twelve, eight or four weeks out, from the brief and venue to event day."),
}
def paces_text(data):  # "Fourteen months, nine months or six months"
    ls = [d["label"].lower() for d in data]
    return (", ".join(ls[:-1]) + " or " + ls[-1]).capitalize()

def cal_page(slug):
    """breadcrumb banner, the calendar, the other two calendars, and the celebration's own closing CTA"""
    c = CALS[slug]
    crumb = f'<a href="{c.get("parent_href", c["sid"] + ".html")}">{c["parent"]}</a> <span aria-hidden="true">/</span> {c.get("crumb", "Planning Calendar")}'
    others = "".join(f'<a class="t-{o["sid"]}" href="{s}.html"><div class="bg"><img src="{IMG}/{o["tile"]}" alt="" loading="lazy"></div><h3>{o["name"]}</h3><p>{paces_text(o["data"])}</p><p class="go">View the calendar {ARROW}</p></a>' for s,o in CALS.items() if s != slug)
    return banner(crumb, c["h"], c["lede"], c["trio"]) + planner(c["data"], c["imgs"]) + f'''
<section class="ivory"><div class="wrap">
<div class="head reveal"><p class="kicker">Planning Something Else?</p><h2 class="h-display">More Planning Calendars</h2><div class="rule"></div></div>
<div class="occasions plan-tiles stagger">{others}</div>
</div></section>
''' + c["cta"]

BODIES = {"index":home,"about":about,"weddings":weddings,"milestones":milestones,"traditions":traditions,"corporate":corporate,"contact":contact}
THEME = {"index":"","about":"t-about","weddings":"t-weddings","milestones":"t-milestones","traditions":"t-traditions","corporate":"t-corporate","contact":""}
TITLES = {
 "index":"Indian &amp; South Asian Wedding Planner in Miami | Anvaya",
 "about":"About Anvaya | Experienced Wedding Planners South Florida",
 "weddings":"Indian &amp; South Asian Wedding Planner Miami, FL | Anvaya",
 "milestones":"Milestone Event Planner Miami &amp; South Florida | Anvaya",
 "traditions":"Indian Traditional Ceremony Planner Miami &amp; South Florida | Anvaya",
 "corporate":"Corporate Event Planner Miami &amp; South Florida | Anvaya",
 "contact":"Contact Anvaya | Wedding &amp; Event Planner South Florida",
}
DESC = {
 "index":"Anvaya plans Indian, South Asian and multicultural weddings across South Florida with eight years of team experience, vendor selection and full-service coordination.",
 "about":"Meet Anvaya, a South Florida wedding and event planner backed by eight years of team experience through JRN Events, cultural expertise and vendor negotiation.",
 "weddings":"Full-service Indian, Pakistani, Sikh, South Indian and multicultural wedding planning in Miami, Fort Lauderdale and Palm Beach, with experienced vendor coordination.",
 "milestones":"Plan milestone birthdays, anniversaries, baby showers, graduations and retirement celebrations in Miami, Fort Lauderdale and Palm Beach with Anvaya.",
 "traditions":"Plan dhoti, half-saree, naming and housewarming ceremonies in Miami, Fort Lauderdale and Palm Beach with culturally informed event planning from Anvaya.",
 "corporate":"Anvaya coordinates company celebrations, launches, galas, retreats and client events across Miami, Fort Lauderdale and Palm Beach with thoughtful design and reliable logistics.",
 "contact":"Connect with Anvaya to plan weddings, traditional ceremonies, milestone celebrations and corporate events in Miami, Fort Lauderdale and Palm Beach.",
}
ACTIVE = {}
for s, c in CALS.items():
    BODIES[s], THEME[s], TITLES[s], DESC[s], ACTIVE[s] = cal_page(s), "t-" + c["sid"], c["title"], c["desc"], "" if "parent_href" in c else c["sid"]

def page_url(slug):  # canonical URL; a page ending in /index is served as its folder
    return f'{SITE}/' if slug == "index" else f'{SITE}/{slug[:-5]}' if slug.endswith("/index") else f'{SITE}/{slug}.html'

def schema(slug):
    biz = {"@context":"https://schema.org","@type":["LocalBusiness","EventPlanner"],"name":"Anvaya","url":SITE,"image":f"{SITE}/img/weddings/mandap.jpg",
      "description":"Luxury Indian and South Asian wedding planner and event planning studio in Miami, serving South Florida and all of Florida.",
      "areaServed":[{"@type":"State","name":"Florida"}]+[{"@type":"City","name":c} for c in ["Miami","Coral Gables","Miami Beach","Fort Lauderdale","Hollywood","Boca Raton","Delray Beach","West Palm Beach","Palm Beach","Jupiter","Naples","Orlando","Tampa","Sarasota","Fort Myers","Jacksonville","Key West"]],
      "address":{"@type":"PostalAddress","addressLocality":"Miami","addressRegion":"FL","addressCountry":"US"},
      "knowsAbout":["Wedding planning in Florida","Destination weddings in Orlando, Tampa and Naples","Indian wedding planning","South Asian weddings","Hindu wedding ceremonies","Sikh weddings","Muslim weddings","Sangeet","Mehndi","Baraat","Anniversary celebrations","Corporate event production"],
      "hasOfferCatalog":{"@type":"OfferCatalog","name":"Celebrations","itemListElement":[
        {"@type":"Offer","itemOffered":{"@type":"Service","name":"Indian & South Asian wedding planning","url":f"{SITE}/weddings.html"}},
        {"@type":"Offer","itemOffered":{"@type":"Service","name":"Milestone celebration planning","url":f"{SITE}/milestones.html"}},
        {"@type":"Offer","itemOffered":{"@type":"Service","name":"Traditional ceremony planning","url":f"{SITE}/traditions.html"}},
        {"@type":"Offer","itemOffered":{"@type":"Service","name":"Corporate event production","url":f"{SITE}/corporate.html"}}]}}
    out = [biz]
    if slug == "weddings":
        out.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
          {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in WED_FAQ]})
    crumbs = [("Home", f"{SITE}/")]
    if slug in CALS:
        c = CALS[slug]
        crumbs += [(c["parent"], f'{SITE}/{c.get("parent_href", c["sid"] + ".html")}'), (c.get("crumb", "Planning Calendar"), page_url(slug))]
    elif slug != "index":
        crumbs.append((dict(PAGES)[slug], page_url(slug)))
    if len(crumbs) > 1:
        out.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
          {"@type":"ListItem","position":k+1,"name":n,"item":u} for k,(n,u) in enumerate(crumbs)]})
    return '<script type="application/ld+json">' + json.dumps(out) + '</script>'

def shell(title, desc, main, url, ld, active="", base=""):
    """head and body shared by every page; base re-roots relative links for pages in sub-folders"""
    body = f'{nav(active)}<main>{main}</main>{FOOTER}{FAB}<script>{JS}</script>'
    d = f'<meta name="description" content="{desc}">' if desc else ''
    head = ((f'<base href="{base}">' if base else '') + f'<title>{title}</title>{d}'
            f'<meta property="og:title" content="{title}">' + (f'<meta property="og:description" content="{desc}">' if desc else '') + f'<meta property="og:image" content="{SITE}/img/weddings/mandap.jpg"><meta property="og:type" content="website">'
            f'<link rel="canonical" href="{url}">'
            f'<meta name="claude:viewport-fit-sides" content="cover"><link rel="icon" href="{IMG}/favicon.png">{FONTS}<style>{CSS}</style>{ld}')
    return head, body

def document(head, body, theme=""):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">{head}</head><body class="{theme}">{body}</body></html>'

def page(slug, fragment):
    theme = THEME[slug]
    base = "../" * slug.count("/")  # pages in sub-folders (the blog resource) re-root their relative links
    head, body = shell(TITLES[slug], DESC[slug], BODIES[slug], page_url(slug), schema(slug), ACTIVE.get(slug, slug), base)
    if fragment:
        return head + f'<script>document.addEventListener("DOMContentLoaded",function(){{document.body.classList.add("{theme}")}})</script>' + body
    return document(head, body, theme)

def write(rel, text):
    (DIST / rel).parent.mkdir(parents=True, exist_ok=True)
    (DIST / rel).write_text(text, encoding="utf-8", newline="\n")

for slug,_ in PAGES:
    write(f"{slug}.html", page(slug, fragment=False))
for slug in CALS:
    write(f"{slug}.html", page(slug, fragment=False))
write("artifact-index.html", page("index", fragment=True))
write("blog/index.html", document(*shell("Blog | Anvaya", "", blog_index, f"{SITE}/blog/", "", base="../")))
for p in POSTS:
    write(f'{p["path"]}/index.html', document(*shell(html.escape(p["SEO title"]), html.escape(p["Meta description"]), post_main(p), SITE + p["Suggested slug"], post_ld(p), base="../../")))
print("built", sorted(str(p.relative_to(DIST)) for p in DIST.rglob("*.html")))
