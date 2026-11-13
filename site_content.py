"""Read-only, validated GitHub-managed content. No server-side edits."""
import base64, html, json
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parent
KEYS=("schedule","route","tshirt","medal","posters","photos","faq","run_registration")
TITLES=("Event schedule","Route map","Event T-shirt","Event medal","More event posters","Photo gallery","Frequently asked questions","Run registration")
def text(value):
    if not isinstance(value,str) or len(value)>12000:raise ValueError("Use text values under 12,000 characters.")
    return value
def url(value):
    value=text(value).strip()
    p=urlsplit(value)
    if value and (p.scheme!="https" or not p.netloc or p.username or p.password):raise ValueError("Links must be complete https:// URLs.")
    return value
def local_image(value):
    value=text(value)
    p=(ROOT/value).resolve()
    if not p.is_relative_to((ROOT/"images").resolve()) or p.suffix.lower() not in (".png",".jpg",".jpeg",".webp") or not p.is_file():
        raise ValueError("Image must exist inside images/: "+value)
    if p.stat().st_size>10*1024*1024:raise ValueError("Keep each image under 10 MB.")
    return p
def load_content(path=None):
    d=json.loads(Path(path or ROOT/"content.json").read_text(encoding="utf-8-sig"))
    for key in ("name","category","headline","intro","contact","registration_label","updated"):
        text(d[key])
    url(d["registration_url"])
    poster=d["poster"]
    if not isinstance(poster["visible"],bool):raise ValueError("poster.visible must be true or false.")
    text(poster["caption"]);text(poster["alt"])
    if poster["visible"]:local_image(poster["file"])
    if not isinstance(d["announcements"],list) or len(d["announcements"])>100:raise ValueError("Use up to 100 announcements.")
    for a in d["announcements"]:
        for k in ("date","title","body"):text(a[k])
    for key in KEYS:
        sec=d["sections"][key]
        if not isinstance(sec["published"],bool):raise ValueError(key+".published must be true or false.")
        text(sec["body"]);url(sec["link"])
        if not isinstance(sec["images"],list) or len(sec["images"])>24:raise ValueError("Use at most 24 images in each section.")
        if sec["published"]:
            if not(sec["body"].strip() or sec["images"] or sec["link"]):raise ValueError("Add content before publishing "+key)
            for im in sec["images"]:local_image(im)
    return d
def esc(s):return html.escape(s,quote=True)
def image_tag(path,alt):
    p=local_image(path)
    mime={".png":"image/png",".jpg":"image/jpeg",".jpeg":"image/jpeg",".webp":"image/webp"}[p.suffix.lower()]
    data=base64.b64encode(p.read_bytes()).decode("ascii")
    return '<img loading="lazy" src="data:'+mime+';base64,'+data+'" alt="'+esc(alt)+'">'
def button(link,label):
    if not link:return ""
    return '<a class="button" target="_blank" rel="noopener noreferrer" href="'+esc(url(link))+'">'+esc(label)+' ↗</a>'
def render(d):
    nav=''.join('<a href="#'+k+'">'+label+'</a>' for k,label in (("guide","Event guide"),("collection","T-shirt &amp; medal"),("gallery","Gallery"),("faq","FAQ"),("run_registration","Run registration")))
    if d["poster"]["visible"]:nav='<a href="#poster">Recruitment poster</a>'+nav
    parts=['<div class="spin-site"><header><a class="brand" href="#top">SPIN <span>USM BUBBLE RUN 2027</span></a><nav aria-label="Main navigation">'+nav+'</nav></header>']
    parts.append('<main id="top"><section class="intro-section"><p class="eyebrow">'+esc(d["name"])+'</p><div class="intro-grid"><div><p class="label">'+esc(d["category"])+'</p><h1>'+esc(d["headline"])+'</h1></div><div class="intro-side"><p>'+esc(d["intro"])+'</p>'+button(d["registration_url"],d["registration_label"])+'</div></div></section>')
    if d["poster"]["visible"]:
        p=d["poster"];parts.append('<section id="poster" class="poster-section"><div class="poster-frame">'+image_tag(p["file"],p["alt"])+'</div><p class="poster-caption">'+esc(p["caption"])+'</p></section>')
    if d["announcements"]:
        parts.append('<section class="future-section" id="updates"><p class="eyebrow">LATEST UPDATES</p><h2>From the team.</h2>')
        for a in d["announcements"]:parts.append('<article class="post"><time>'+esc(a["date"])+'</time><div><h3>'+esc(a["title"])+'</h3><p>'+esc(a["body"])+'</p></div></article>')
        parts.append('</section>')
    def card(key):
        sec=d["sections"][key];title=dict(zip(KEYS,TITLES))[key]
        if not sec["published"]:
            return '<article class="future-card" id="'+key+'"><h3>'+title+'</h3><p>Details will be announced here.</p><span class="soon">Coming soon</span></article>'
        images=''.join(image_tag(im,title+' — image '+str(i+1)) for i,im in enumerate(sec["images"]))
        label="Register for the run" if key=="run_registration" else "View details"
        return '<article class="future-card" id="'+key+'"><h3>'+title+'</h3><p>'+esc(sec["body"])+'</p><div class="published-gallery">'+images+'</div>'+button(sec["link"],label)+'</article>'
    for group,eyebrow,title,keys in [
        ("guide","01 / PLAN YOUR DAY","The event guide.",("schedule","route")),
        ("collection","02 / THE COLLECTION","A little SPIN to keep.",("tshirt","medal")),
        ("gallery","03 / THE NOTICEBOARD","Posters &amp; moments.",("posters","photos"))]:
        parts.append('<section class="future-section" id="'+group+'"><p class="eyebrow">'+eyebrow+'</p><h2>'+title+'</h2><div class="feature-grid">'+''.join(card(k) for k in keys)+'</div></section>')
    parts.append('<section class="future-section"><p class="eyebrow">04 / GOOD TO KNOW</p>'+card("faq")+'</section>')
    parts.append('<section class="future-section"><p class="eyebrow">05 / JOIN THE RUN</p>'+card("run_registration")+'</section>')
    parts.append('<section class="closing"><div><p class="eyebrow">GET IN TOUCH</p><h2>See you at SPIN.</h2><p>'+esc(d["contact"])+'</p></div>'+button(d["registration_url"],d["registration_label"])+'</section></main>')
    parts.append('<footer><strong>'+esc(d["name"])+'</strong><span>'+('Last updated: '+esc(d["updated"]) if d["updated"] else '')+'</span></footer></div>')
    return ''.join(parts)
if __name__=="__main__":
    load_content()
    print("Content is valid. Published image files and links checked.")
