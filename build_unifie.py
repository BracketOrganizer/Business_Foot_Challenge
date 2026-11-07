#!/usr/bin/env python3
"""Génère index.html « Business Foot Challenge » (menu 20/24/32) à partir des 3 fichiers sources.
Usage : python3 build_unifie.py   (les 3 fichiers Foot_inter_entreprises_Challenge_XX.html dans le même dossier)"""
import re, sys, json, os
SRC = {20:'Foot_inter_entreprises_Challenge_20.html', 24:'Foot_inter_entreprises_Challenge_24.html', 32:'Foot_inter_entreprises_Challenge_32.html'}
LABEL = {20:'20 équipes', 24:'24 équipes', 32:'32 équipes'}
OUT = 'index.html'   # page d'accueil du dépôt (GitHub Pages)

import unicodedata
BASE = os.path.dirname(os.path.abspath(__file__))
def find_src(name):
    """Cherche le fichier dans Sources/, sources/ ou à côté du script (insensible aux accents NFC/NFD)."""
    want = unicodedata.normalize('NFC', name)
    for d in ('Sources', 'sources', '.'):
        folder = os.path.join(BASE, d)
        if not os.path.isdir(folder): continue
        for f in os.listdir(folder):
            if unicodedata.normalize('NFC', f) == want:
                return os.path.join(folder, f)
    sys.exit('Fichier manquant : ' + name + ' (à placer dans le dossier Sources/)')

def esc(s):  # protège le contenu dans <script type="text/plain">
    return s.replace('<!--','<\\!--').replace('</script','<\\/script').replace('<script','<\\script')

blocks=[]
for n,fn in SRC.items():
    s=open(find_src(fn),encoding='utf-8',newline='').read().replace('\r\n','\n')
    blocks.append(f'<script type="text/plain" id="app{n}">\n{esc(s)}\n</script>')

# Logos (déjà intégrés dans les apps sous forme de data-URI) -> réutilisés pour le menu
_first = blocks and open(find_src(SRC[20]),encoding='utf-8').read()
_m1 = re.search(r'--logo-fec:url\((data:[^)]+)\)', _first)
_m2 = re.search(r'--logo-ffse:url\((data:[^)]+)\)', _first)
if not (_m1 and _m2): sys.exit('Logos introuvables dans ' + SRC[20] + ' (utiliser les apps « Business Foot Challenge »)')
LOGO_FEC, LOGO_FFSE = _m1.group(1), _m2.group(1)

TEMPLATE = r'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#0f4a1f">
<link rel="icon" type="image/jpeg" href="@@FEC@@">
<title>⚽ Business Foot Challenge</title>
<style>
*{box-sizing:border-box}
body{margin:0;min-height:100vh;display:none;align-items:center;justify-content:center;padding:24px;font-family:'Segoe UI',system-ui,sans-serif;color:#fff;background:radial-gradient(ellipse at top,#145a28 0%,#0a2e15 60%,#04140a 100%)}
.box{width:100%;max-width:460px;text-align:center}
body{background:radial-gradient(ellipse at 50% 0%,#1f7a3a 0%,#0f4a1f 55%,#08301a 100%)}
.logo{display:block;width:190px;height:190px;object-fit:contain;background:#fff;padding:8px;margin:0 auto 14px;border-radius:24px;border:3px solid rgba(255,255,255,.9);box-shadow:0 8px 28px rgba(0,0,0,.5)}
h1{font-family:Oswald,'Segoe UI',system-ui,sans-serif;font-size:32px;line-height:1.1;margin:0 0 8px;text-transform:uppercase;letter-spacing:1.5px;text-shadow:0 2px 6px rgba(0,0,0,.4)}
.sub{margin:0 0 4px;color:#ffd36b;font-size:13px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase}
p{margin:0 0 22px;color:#c9f5d6;font-size:14px}
.fed{margin:26px auto 0;padding:10px;background:#fff;border-radius:18px;display:inline-block;box-shadow:0 6px 20px rgba(0,0,0,.35)}
.fed img{display:block;width:150px;max-width:45vw;height:auto;border-radius:10px}
@media(max-width:600px){.logo{width:150px}h1{font-size:25px}}
a.card{display:flex;align-items:center;gap:16px;margin:12px 0;padding:18px 20px;border-radius:16px;text-decoration:none;color:#fff;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);transition:.15s}
a.card:hover,a.card:active{background:rgba(255,255,255,.16);transform:translateY(-1px)}
a.card.last{border-color:#6ee790;box-shadow:0 0 0 2px rgba(110,231,144,.25)}
.num{font-size:34px;font-weight:800;min-width:56px;color:#6ee790}
.lbl{text-align:left;font-size:18px;font-weight:700}
.lbl small{display:block;font-weight:400;font-size:12px;color:#b9d8c1;margin-top:2px}
</style>
</head>
<body>
<div class="box">
  <img class="logo" src="@@FEC@@" alt="Logo Business Foot Challenge">
  <h1>Business Foot Challenge</h1>
  <div class="sub">Tournoi inter-entreprises</div>
  <p>Choisissez le format du tournoi</p>
  <a class="card" data-f="20" href="?f=20"><span class="num">20</span><span class="lbl">20 équipes<small>4 poules de 5 · 6 matchs par équipe</small></span></a>
  <a class="card" data-f="24" href="?f=24"><span class="num">24</span><span class="lbl">24 équipes<small>4 poules de 6 · 8 matchs par équipe</small></span></a>
  <a class="card" data-f="32" href="?f=32"><span class="num">32</span><span class="lbl">32 équipes<small>8 poules de 4 · 7 matchs par équipe</small></span></a>
  <div class="fed"><img src="@@FFSE@@" alt="FFSE - Ligue Pays de la Loire"></div>
</div>
@@BLOCKS@@
<script>
(function(){
  var f = new URLSearchParams(location.search).get('f');
  var el = f && document.getElementById('app'+f);
  function unesc(s){ return s.replace(/<\\\/script/g,'</script').replace(/<\\script/g,'<script').replace(/<\\!--/g,'<!--'); }
  function start(){
    if(!el){
      try{ var last=localStorage.getItem('footFormat'); var c=document.querySelector('a.card[data-f="'+last+'"]'); if(c) c.classList.add('last'); }catch(e){}
      document.querySelectorAll('a.card').forEach(function(a){ a.addEventListener('click',function(){ try{localStorage.setItem('footFormat',a.dataset.f);}catch(e){} }); });
      document.body.style.display='flex';
      return;
    }
    var html = unesc(el.textContent);
    // petit bouton « changer de format » (retour au menu), injecté avant la dernière balise </body>
    var btn = '<a href="'+location.pathname+'" title="Changer de format (20 / 24 / 32 équipes)" style="position:fixed;left:8px;bottom:8px;z-index:150;width:30px;height:30px;border-radius:50%;background:rgba(0,0,0,.55);color:#fff;font:16px/30px sans-serif;text-align:center;text-decoration:none;opacity:.5">⚽</a>';
    var i = html.lastIndexOf('</body>');
    if(i>-1) html = html.slice(0,i)+btn+html.slice(i);
    document.open(); document.write(html); document.close();
  }
  // document.open() n'est effectif qu'une fois le parsing terminé
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',function(){ setTimeout(start,0); });
  else setTimeout(start,0);
})();
</script>
</body>
</html>
'''
html = TEMPLATE.replace('@@FEC@@', LOGO_FEC).replace('@@FFSE@@', LOGO_FFSE).replace('@@BLOCKS@@', chr(10).join(blocks))
with open(os.path.join(BASE, OUT), 'w', encoding='utf-8', newline=chr(10)) as fh:
    fh.write(html)
print('OK ->', OUT, round(os.path.getsize(os.path.join(BASE, OUT)) / 1024), 'Ko')
