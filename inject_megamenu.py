#!/usr/bin/env python3
"""
Injects the mega-menu header (from thank-you.html) into every HTML file
in the same directory, replacing whatever <header>…</header> block exists
and prepending the required CSS classes / JS if they are absent.
Also links up all pages correctly.
"""

import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

# ──────────────────────────────────────────────────────────────────────────────
# 1.  SHARED CSS  (mega-panel + mobile-drawer)
# ──────────────────────────────────────────────────────────────────────────────
SHARED_CSS = """
    /* ── Mega Menu ── */
    .nav-link{position:relative}
    .nav-link::after{content:"";position:absolute;left:0;right:100%;height:2px;bottom:-7px;background:var(--gold);transition:.25s}
    .nav-link:hover::after{right:0}
    .mega-panel{opacity:0;visibility:hidden;pointer-events:none;transform:translateY(14px) scale(.98);transition:.22s ease}
    .mega-open .mega-panel{opacity:1;visibility:visible;pointer-events:auto;transform:translateY(0) scale(1)}
    .mega-link{transition:.22s ease}
    .mega-link:hover{background:#F7F3EA;transform:translateX(-2px)}
    .mega-feature{background:radial-gradient(circle at 72% 12%,rgba(255,255,255,.18),transparent 28%),linear-gradient(135deg,#043755,#1493C5 55%,#021A28)}
    /* ── Mobile Drawer ── */
    .mobile-drawer{transform:translateX(100%);transition:.28s ease}
    .mobile-drawer.active{transform:translateX(0)}
    .mobile-overlay{opacity:0;pointer-events:none;transition:.25s ease}
    .mobile-overlay.active{opacity:1;pointer-events:auto}
    /* ── Shared helpers (safe to repeat) ── */
    .premium-card{background:rgba(255,255,255,.88);border:1px solid rgba(4,55,85,.08);box-shadow:0 18px 50px rgba(9,40,58,.10);backdrop-filter:blur(12px)}
    .section-eyebrow{letter-spacing:.18em;text-transform:uppercase;font-family:'Inter',sans-serif;font-size:12px;font-weight:800;color:var(--sky)}
    .btn-primary{background:linear-gradient(135deg,var(--sky),#0878A8);box-shadow:0 16px 34px rgba(20,147,197,.32);transition:.25s ease}
    .btn-primary:hover{transform:translateY(-2px);box-shadow:0 22px 46px rgba(20,147,197,.38)}
    .btn-gold{background:linear-gradient(135deg,#E8C76A,var(--gold));box-shadow:0 16px 34px rgba(215,168,63,.28);transition:.25s ease}
    .btn-gold:hover{transform:translateY(-2px)}
    .islamic-grid{position:absolute;inset:0;opacity:.13;background-image:url("data:image/svg+xml,%3Csvg width='120' height='120' viewBox='0 0 120 120' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' stroke='%23D7A83F' stroke-width='1.2'%3E%3Cpath d='M60 4 80 40l36 20-36 20-20 36-20-36L4 60l36-20Z'/%3E%3Cpath d='M60 22 72 48l26 12-26 12-12 26-12-26-26-12 26-12Z'/%3E%3Ccircle cx='60' cy='60' r='18'/%3E%3C/g%3E%3C/svg%3E");background-size:150px 150px}
"""

# ──────────────────────────────────────────────────────────────────────────────
# 2.  MEGA MENU HEADER HTML  (static template)
# ──────────────────────────────────────────────────────────────────────────────
HEADER_HTML = """  <!-- =========================================================
       HEADER / MEGA MENU NAVIGATION
  ========================================================== -->
  <header id="siteHeader" class="sticky top-0 z-50 bg-white/86 backdrop-blur-xl border-b border-ocean/10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="h-20 flex items-center justify-between gap-5">
        <!-- Logo -->
        <a href="index.html" class="flex items-center gap-3" aria-label="Khutbah TV Home">
          <img
            src="https://www.khutbahtv.com/wp-content/uploads/2026/05/Group-1000000925-1.png"
            alt="Khutbah TV"
            class="h-12 w-auto"
            onerror="this.src='https://www.khutbahtv.com/wp-content/uploads/2026/05/Group-1000000924.png'"
          />
        </a>

        <!-- Desktop Nav -->
        <nav class="hidden lg:flex items-center gap-7 font-semibold text-[15px] text-ocean">
          <a class="nav-link" href="index.html">হোম</a>
          <a class="nav-link" href="about.html">আমাদের সম্পর্কে</a>
          <a class="nav-link" href="video-archive.html">ভিডিও</a>
          <a class="nav-link" href="ebook-archive.html">ই-বুক</a>
          <a class="nav-link" href="question.html">প্রশ্নোত্তর</a>

          <!-- Mega Menu Trigger -->
          <div id="megaMenuWrap" class="relative">
            <button id="megaMenuBtn" class="inline-flex items-center gap-2 rounded-full bg-cream px-5 py-3 font-black text-ocean hover:bg-ocean hover:text-white transition">
              সব পেজ
              <span class="text-xs">⌄</span>
            </button>
          </div>
        </nav>

        <!-- Search / CTA -->
        <div class="hidden md:flex items-center gap-3">
          <div class="relative">
            <input id="headerSearch" class="w-56 rounded-full border border-ocean/15 bg-white px-5 py-3 text-sm outline-none focus:border-skybrand" placeholder="খুঁজুন..." />
            <span class="absolute right-4 top-3.5 text-ocean/50">⌕</span>
          </div>
          <a href="donation.html" class="btn-primary text-white px-5 py-3 rounded-full font-bold text-sm">
            দান করুন
          </a>
        </div>

        <!-- Mobile Menu Button -->
        <button id="mobileMenuBtn" class="lg:hidden w-11 h-11 rounded-full border border-ocean/15 flex items-center justify-center text-ocean" aria-label="Open menu">
          ☰
        </button>
      </div>
    </div>

    <!-- =====================================================
         DESKTOP MEGA MENU PANEL
    ====================================================== -->
    <div id="megaPanel" class="mega-panel absolute left-0 right-0 top-full px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto pt-4">
        <div class="premium-card rounded-[34px] p-5 lg:p-6 shadow-premium border border-ocean/10">
          <div class="grid lg:grid-cols-[1.1fr_1fr_1fr_.95fr] gap-5">
            <!-- Featured Mega Card -->
            <div class="mega-feature relative overflow-hidden rounded-[28px] p-6 text-white min-h-[330px] flex flex-col justify-between">
              <div class="islamic-grid"></div>
              <div class="relative">
                <img src="https://www.khutbahtv.com/wp-content/uploads/2026/05/Group-1000000924.png" class="w-16 h-16 rounded-full bg-white p-2 mb-5" alt="Khutbah TV">
                <p class="section-eyebrow text-gold">Khutbah TV</p>
                <h3 class="mt-2 text-3xl font-black leading-tight">সব গুরুত্বপূর্ণ পেজ এক জায়গায়</h3>
                <p class="mt-4 text-white/70 leading-7">ভিডিও, ই-বুক, প্রশ্নোত্তর, লেখক, ক্যাটাগরি, নীতিমালা ও ফর্ম পেজ দ্রুত ব্রাউজ করুন।</p>
              </div>
              <a href="all-categories.html" class="relative mt-6 btn-gold text-ocean px-5 py-3 rounded-full font-black text-center">সব ক্যাটাগরি</a>
            </div>

            <!-- Main Pages -->
            <div>
              <p class="section-eyebrow mb-4">Main Pages</p>
              <div class="space-y-2">
                <a class="mega-link flex items-start gap-3 rounded-2xl p-3" href="index.html"><span class="w-10 h-10 rounded-2xl bg-skybrand/10 text-skybrand flex items-center justify-center font-black">H</span><span><b class="text-ocean">হোম</b><small class="block text-ocean/55">Homepage overview</small></span></a>
                <a class="mega-link flex items-start gap-3 rounded-2xl p-3" href="about.html"><span class="w-10 h-10 rounded-2xl bg-gold/15 text-ocean flex items-center justify-center font-black">A</span><span><b class="text-ocean">আমাদের সম্পর্কে</b><small class="block text-ocean/55">About Khutbah TV</small></span></a>
                <a class="mega-link flex items-start gap-3 rounded-2xl p-3" href="contact-us.html"><span class="w-10 h-10 rounded-2xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-black">C</span><span><b class="text-ocean">যোগাযোগ</b><small class="block text-ocean/55">Contact form</small></span></a>
                <a class="mega-link flex items-start gap-3 rounded-2xl p-3" href="live.html"><span class="w-10 h-10 rounded-2xl bg-ocean/10 text-ocean flex items-center justify-center font-black">L</span><span><b class="text-ocean">লাইভ</b><small class="block text-ocean/55">YouTube/Facebook live</small></span></a>
                <a class="mega-link flex items-start gap-3 rounded-2xl p-3" href="404.html"><span class="w-10 h-10 rounded-2xl bg-red-100 text-red-600 flex items-center justify-center font-black">!</span><span><b class="text-ocean">404 পেজ</b><small class="block text-ocean/55">Error page</small></span></a>
              </div>
            </div>

            <!-- Content Pages -->
            <div>
              <p class="section-eyebrow mb-4">Content Archive</p>
              <div class="space-y-2">
                <a class="mega-link flex items-start gap-3 rounded-2xl p-3" href="video-archive.html"><span class="w-10 h-10 rounded-2xl bg-skybrand/10 text-skybrand flex items-center justify-center font-black">▶</span><span><b class="text-ocean">ভিডিও আর্কাইভ</b><small class="block text-ocean/55">All video list</small></span></a>
                <a class="mega-link flex items-start gap-3 rounded-2xl p-3" href="blog.html"><span class="w-10 h-10 rounded-2xl bg-gold/15 text-ocean flex items-center justify-center font-black">B</span><span><b class="text-ocean">ব্লগ</b><small class="block text-ocean/55">Articles and posts</small></span></a>
                <a class="mega-link flex items-start gap-3 rounded-2xl p-3" href="single.html"><span class="w-10 h-10 rounded-2xl bg-cream text-ocean flex items-center justify-center font-black">P</span><span><b class="text-ocean">ব্লগ সিঙ্গেল</b><small class="block text-ocean/55">Post details page</small></span></a>
                <a class="mega-link flex items-start gap-3 rounded-2xl p-3" href="archive.html"><span class="w-10 h-10 rounded-2xl bg-ocean/10 text-ocean flex items-center justify-center font-black">#</span><span><b class="text-ocean">আর্কাইভ</b><small class="block text-ocean/55">Category/Date archive</small></span></a>
                <a class="mega-link flex items-start gap-3 rounded-2xl p-3" href="all-categories.html"><span class="w-10 h-10 rounded-2xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-black">✓</span><span><b class="text-ocean">সব ক্যাটাগরি</b><small class="block text-ocean/55">Topics directory</small></span></a>
              </div>
            </div>

            <!-- Forms & Utility -->
            <div>
              <p class="section-eyebrow mb-4">Forms &amp; Utility</p>
              <div class="space-y-2">
                <a class="mega-link flex items-start gap-3 rounded-2xl p-3" href="question.html"><span class="w-10 h-10 rounded-2xl bg-skybrand/10 text-skybrand flex items-center justify-center font-black">?</span><span><b class="text-ocean">প্রশ্ন তালিকা</b><small class="block text-ocean/55">Question archive</small></span></a>
                <a class="mega-link flex items-start gap-3 rounded-2xl p-3" href="question-details.html"><span class="w-10 h-10 rounded-2xl bg-gold/15 text-ocean flex items-center justify-center font-black">Q</span><span><b class="text-ocean">প্রশ্ন বিস্তারিত</b><small class="block text-ocean/55">Answer details</small></span></a>
                <a class="mega-link flex items-start gap-3 rounded-2xl p-3" href="submit-question.html"><span class="w-10 h-10 rounded-2xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-black">+</span><span><b class="text-ocean">প্রশ্ন পাঠান</b><small class="block text-ocean/55">Ask question form</small></span></a>
                <a class="mega-link flex items-start gap-3 rounded-2xl p-3" href="donation.html"><span class="w-10 h-10 rounded-2xl bg-ocean/10 text-ocean flex items-center justify-center font-black">৳</span><span><b class="text-ocean">দান করুন</b><small class="block text-ocean/55">Support page</small></span></a>
                <a class="mega-link flex items-start gap-3 rounded-2xl p-3" href="privacy-policy.html"><span class="w-10 h-10 rounded-2xl bg-cream text-ocean flex items-center justify-center font-black">P</span><span><b class="text-ocean">Privacy Policy</b><small class="block text-ocean/55">Privacy page</small></span></a>
              </div>
            </div>
          </div>

          <!-- Mega Footer Links -->
          <div class="mt-5 pt-5 border-t border-ocean/10 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div class="flex flex-wrap gap-2">
              <a href="ebook-archive.html" class="rounded-full bg-cream px-4 py-2 font-bold text-ocean/70 hover:bg-ocean hover:text-white transition">ই-বুক আর্কাইভ</a>
              <a href="e-book-single.html" class="rounded-full bg-cream px-4 py-2 font-bold text-ocean/70 hover:bg-ocean hover:text-white transition">সিঙ্গেল ই-বুক</a>
              <a href="all-author.html" class="rounded-full bg-cream px-4 py-2 font-bold text-ocean/70 hover:bg-ocean hover:text-white transition">সব লেখক</a>
              <a href="author.html" class="rounded-full bg-cream px-4 py-2 font-bold text-ocean/70 hover:bg-ocean hover:text-white transition">Author Profile</a>
              <a href="faq.html" class="rounded-full bg-cream px-4 py-2 font-bold text-ocean/70 hover:bg-ocean hover:text-white transition">FAQ</a>
              <a href="sitemap.html" class="rounded-full bg-cream px-4 py-2 font-bold text-ocean/70 hover:bg-ocean hover:text-white transition">Sitemap</a>
              <a href="thank-you.html" class="rounded-full bg-cream px-4 py-2 font-bold text-ocean/70 hover:bg-ocean hover:text-white transition">Thank You</a>
              <a href="terms-conditions.html" class="rounded-full bg-cream px-4 py-2 font-bold text-ocean/70 hover:bg-ocean hover:text-white transition">Terms</a>
            </div>
            <a href="search.html" class="btn-primary text-white rounded-full px-5 py-3 font-black text-center">সার্চ রেজাল্ট</a>
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- =========================================================
       MOBILE DRAWER MENU
  ========================================================== -->
  <div id="mobileOverlay" class="mobile-overlay fixed inset-0 bg-ocean/70 backdrop-blur-sm z-[90]"></div>
  <aside id="mobileDrawer" class="mobile-drawer fixed right-0 top-0 bottom-0 w-[88%] max-w-md bg-white z-[100] shadow-premium overflow-y-auto">
    <div class="p-5 border-b border-ocean/10 flex items-center justify-between">
      <img src="https://www.khutbahtv.com/wp-content/uploads/2026/05/Group-1000000925-1.png" class="h-11 w-auto" alt="Khutbah TV">
      <button id="mobileCloseBtn" class="w-11 h-11 rounded-full bg-cream text-ocean font-black">×</button>
    </div>
    <div class="p-5">
      <p class="section-eyebrow">All Pages</p>
      <div class="mt-4 grid gap-2 font-bold text-ocean">
        <a class="rounded-2xl bg-cream px-4 py-3" href="index.html">হোম</a>
        <a class="rounded-2xl bg-cream px-4 py-3" href="about.html">আমাদের সম্পর্কে</a>
        <a class="rounded-2xl bg-cream px-4 py-3" href="video-archive.html">ভিডিও আর্কাইভ</a>
        <a class="rounded-2xl bg-cream px-4 py-3" href="videos-items.html">সব ভিডিও</a>
        <a class="rounded-2xl bg-cream px-4 py-3" href="ebook-archive.html">ই-বুক আর্কাইভ</a>
        <a class="rounded-2xl bg-cream px-4 py-3" href="e-book-single.html">সিঙ্গেল ই-বুক</a>
        <a class="rounded-2xl bg-cream px-4 py-3" href="question.html">প্রশ্ন তালিকা</a>
        <a class="rounded-2xl bg-cream px-4 py-3" href="submit-question.html">প্রশ্ন পাঠান</a>
        <a class="rounded-2xl bg-cream px-4 py-3" href="blog.html">ব্লগ</a>
        <a class="rounded-2xl bg-cream px-4 py-3" href="all-author.html">সব লেখক</a>
        <a class="rounded-2xl bg-cream px-4 py-3" href="all-categories.html">সব ক্যাটাগরি</a>
        <a class="rounded-2xl bg-cream px-4 py-3" href="donation.html">দান করুন</a>
        <a class="rounded-2xl bg-cream px-4 py-3" href="live.html">লাইভ</a>
        <a class="rounded-2xl bg-cream px-4 py-3" href="faq.html">FAQ</a>
        <a class="rounded-2xl bg-cream px-4 py-3" href="contact-us.html">যোগাযোগ</a>
        <a class="rounded-2xl bg-cream px-4 py-3" href="privacy-policy.html">Privacy Policy</a>
        <a class="rounded-2xl bg-cream px-4 py-3" href="terms-conditions.html">Terms &amp; Conditions</a>
        <a class="rounded-2xl bg-cream px-4 py-3" href="sitemap.html">Sitemap</a>
        <a class="rounded-2xl bg-cream px-4 py-3" href="search.html">সার্চ</a>
      </div>
    </div>
  </aside>
"""

# ──────────────────────────────────────────────────────────────────────────────
# 3.  MEGA MENU JS
# ──────────────────────────────────────────────────────────────────────────────
MEGA_JS = """
    // ── Mega Menu ──
    (function(){
      const btn = document.getElementById('megaMenuBtn');
      const panel = document.getElementById('megaPanel');
      const hdr = document.getElementById('siteHeader');
      if(!btn||!panel||!hdr) return;
      let timer;
      const open = ()=>{ clearTimeout(timer); hdr.classList.add('mega-open'); };
      const close = ()=>{ timer = setTimeout(()=>hdr.classList.remove('mega-open'), 140); };
      btn.addEventListener('mouseenter', open);
      btn.addEventListener('click', ()=>hdr.classList.toggle('mega-open'));
      panel.addEventListener('mouseenter', open);
      btn.addEventListener('mouseleave', close);
      panel.addEventListener('mouseleave', close);
      document.addEventListener('keydown', e=>{ if(e.key==='Escape') hdr.classList.remove('mega-open'); });
      document.addEventListener('click', e=>{ if(!e.target.closest('#siteHeader')) hdr.classList.remove('mega-open'); });
    })();
    // ── Mobile Drawer ──
    (function(){
      const openBtn = document.getElementById('mobileMenuBtn');
      const closeBtn = document.getElementById('mobileCloseBtn');
      const drawer = document.getElementById('mobileDrawer');
      const overlay = document.getElementById('mobileOverlay');
      if(!openBtn||!drawer) return;
      const open = ()=>{ drawer.classList.add('active'); overlay.classList.add('active'); document.body.style.overflow='hidden'; };
      const close = ()=>{ drawer.classList.remove('active'); overlay.classList.remove('active'); document.body.style.overflow=''; };
      openBtn.addEventListener('click', open);
      closeBtn?.addEventListener('click', close);
      overlay?.addEventListener('click', close);
    })();
    // ── Header search ──
    (function(){
      const s = document.getElementById('headerSearch');
      if(!s) return;
      s.addEventListener('keydown', e=>{
        if(e.key==='Enter'){
          e.preventDefault();
          const q = s.value.trim();
          if(q) window.location.href = 'search.html?s=' + encodeURIComponent(q);
        }
      });
    })();
"""

# ──────────────────────────────────────────────────────────────────────────────
# 4.  Helper: ensure CSS block exists in <style> inside <head>
# ──────────────────────────────────────────────────────────────────────────────
MARKER = "/* ── Mega Menu ── */"

def inject_css(html: str) -> str:
    if MARKER in html:
        return html  # already there
    # Insert before closing </style> (first one inside <head>)
    head_end = html.find('</head>')
    style_close = html.rfind('</style>', 0, head_end)
    if style_close == -1:
        # No style block – create one before </head>
        html = html[:head_end] + f"\n  <style>{SHARED_CSS}\n  </style>\n" + html[head_end:]
    else:
        html = html[:style_close] + SHARED_CSS + "\n  " + html[style_close:]
    return html

# ──────────────────────────────────────────────────────────────────────────────
# 5.  Helper: replace <header>…</header> block + any old mobile drawer/overlay
# ──────────────────────────────────────────────────────────────────────────────
def replace_header(html: str) -> str:
    # Remove old mobile overlay/drawer if present (before or after header)
    html = re.sub(
        r'\s*<div[^>]+id=["\']mobileOverlay["\'][^>]*>.*?</div>\s*',
        '', html, flags=re.DOTALL
    )
    html = re.sub(
        r'\s*<aside[^>]+id=["\']mobileDrawer["\'][^>]*>.*?</aside>\s*',
        '', html, flags=re.DOTALL
    )
    # Replace the <header>…</header> block
    html = re.sub(
        r'\s*<header\b[^>]*>.*?</header>\s*',
        '\n' + HEADER_HTML + '\n',
        html, count=1, flags=re.DOTALL
    )
    return html

# ──────────────────────────────────────────────────────────────────────────────
# 6.  Helper: inject JS before </body>
# ──────────────────────────────────────────────────────────────────────────────
JS_MARKER = "// ── Mega Menu ──"

def inject_js(html: str) -> str:
    if JS_MARKER in html:
        return html  # already there
    body_close = html.rfind('</body>')
    if body_close == -1:
        html += f"\n<script>{MEGA_JS}\n</script>\n"
    else:
        snippet = f"\n  <script>{MEGA_JS}\n  </script>\n"
        html = html[:body_close] + snippet + html[body_close:]
    return html

# ──────────────────────────────────────────────────────────────────────────────
# 7.  Process all HTML files
# ──────────────────────────────────────────────────────────────────────────────
html_files = [f for f in os.listdir(BASE) if f.endswith('.html')]
skip = {'inject_megamenu.py'}

results = []
for fname in sorted(html_files):
    if fname in skip:
        continue
    path = os.path.join(BASE, fname)
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            original = fh.read()

        updated = inject_css(original)
        updated = replace_header(updated)
        updated = inject_js(updated)

        if updated != original:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(updated)
            results.append(f"  ✅  {fname}")
        else:
            results.append(f"  ⚠️  {fname} — no change (check manually)")
    except Exception as exc:
        results.append(f"  ❌  {fname} — ERROR: {exc}")

print("\nMega Menu Injection Results")
print("=" * 48)
for r in results:
    print(r)
print(f"\nDone. {len(html_files)} files processed.")
