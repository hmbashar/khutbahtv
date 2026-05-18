import os

BASE = os.path.dirname(os.path.abspath(__file__))

OLD_JS = """    // ── Header search ──
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
    })();"""

NEW_JS = """    // ── Header search ──
    (function(){
      const s = document.getElementById('headerSearch');
      if(!s) return;
      s.addEventListener('keydown', e=>{
        if(e.key==='Enter'){
          if(document.getElementById('searchInput') || document.getElementById('blogSearch') || document.getElementById('qaSearch') || window.location.pathname.includes('search.html')) return;
          e.preventDefault();
          const q = s.value.trim();
          if(q) window.location.href = 'search.html?s=' + encodeURIComponent(q);
        }
      });
    })();"""

for fname in os.listdir(BASE):
    if fname.endswith('.html'):
        path = os.path.join(BASE, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Replace the injected header search logic with the smarter one
        if OLD_JS in content:
            content = content.replace(OLD_JS, NEW_JS)
            
        # 2. Replace all instances of 'globalSearch' with 'headerSearch'
        # This fixes the null reference errors in all pages.
        content = content.replace("'globalSearch'", "'headerSearch'")
        content = content.replace('"globalSearch"', '"headerSearch"')
        content = content.replace("getElementById('globalSearch')", "getElementById('headerSearch')")
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

print("Fixed search bug in all files.")
