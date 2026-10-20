# Adds the Meta Pixel (dataset 1969956100367800) to every public page. Runs last in rebuild.sh.
# Events: PageView everywhere; ViewContent on machine pages (/p/mN, ids match catalog.csv); Lead when someone
# opens WhatsApp (links or Buy now buttons); Contact when someone taps the call button.
import json, os, re, glob
T = os.path.dirname(os.path.abspath(__file__)); PUB = os.path.join(T, '..', 'public')
PID = '1969956100367800'
P = {p['k']: p for p in json.load(open(os.path.join(T, 'products.json')))}
SKIP = ('media/', 'new/', 'google', 'gumtree/')
BASE = ("<!-- Meta Pixel Code --><script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?"
        "n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';"
        "n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}"
        "(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');"
        f"fbq('init','{PID}');fbq('track','PageView');%s"
        "(function(){var last=0;function lead(u){var n=Date.now();if(n-last<1500)return;last=n;"
        "fbq('track',/^tel:/.test(u)?'Contact':'Lead',window.TA_VC||{})}"
        "document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href]');if(!a)return;var h=a.getAttribute('href')||'';"
        "if(/wa\\.me\\/\\d|phone=\\d|^tel:/.test(h))lead(h)},true);"
        "var o=window.open;window.open=function(u){try{if(/wa\\.me\\/\\d|phone=\\d/.test(String(u)))lead(String(u))}catch(x){}return o.apply(this,arguments)}})();"
        "</script><noscript><img height=\"1\" width=\"1\" style=\"display:none\" "
        f"src=\"https://www.facebook.com/tr?id={PID}&ev=PageView&noscript=1\"/></noscript><!-- End Meta Pixel Code -->")
n = 0
for f in glob.glob(os.path.join(PUB, '**', '*.html'), recursive=True):
    rel = os.path.relpath(f, PUB)
    if rel.startswith(SKIP): continue
    s = open(f, encoding='utf-8').read()
    if "fbq('init'" in s or '</head>' not in s: continue
    extra = ''
    m = re.fullmatch(r'p/m(\d+)\.html', rel)
    if m and int(m.group(1)) in P:
        p = P[int(m.group(1))]
        vc = dict(content_ids=[p['model']], content_type='product', content_name=p['name'],
                  value=int(re.sub(r'\D', '', p['price']) or 0), currency='ZAR')
        extra = f"window.TA_VC={json.dumps(vc, ensure_ascii=False)};fbq('track','ViewContent',window.TA_VC);"
    s = s.replace('</head>', BASE % extra + '</head>', 1)
    open(f, 'w', encoding='utf-8').write(s); n += 1
print('meta pixel added to', n, 'pages')
