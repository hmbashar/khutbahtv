import os

BASE = os.path.dirname(os.path.abspath(__file__))

ACTIVE_JS = """
    // ── Active Link Highlighting ──
    (function(){
      let currentUrl = window.location.pathname.split('/').pop() || 'index.html';
      document.querySelectorAll('.nav-link, .mega-link, #mobileDrawer a').forEach(link => {
        let href = link.getAttribute('href');
        if (href && href !== '#' && currentUrl === href) {
          link.classList.add('active');
          if (link.closest('#mobileDrawer')) {
            link.classList.add('bg-white', 'text-skybrand');
            link.classList.remove('bg-cream');
          } else if (link.classList.contains('mega-link')) {
            link.style.background = '#F7F3EA';
          }
        }
      });
    })();
"""

for fname in os.listdir(BASE):
    if fname.endswith('.html'):
        path = os.path.join(BASE, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add CSS rule for nav-link.active
        content = content.replace(".nav-link:hover::after{right:0}", ".nav-link:hover::after, .nav-link.active::after {right:0}")
        
        # Add JS before </script> of the mega menu
        if "Active Link Highlighting" not in content and "// ── Mega Menu ──" in content:
            content = content.replace("// ── Header search ──", ACTIVE_JS + "\n    // ── Header search ──")
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

print("Active states injected successfully.")
