#!/usr/bin/env python3
"""
inject_meta_pixel.py
====================
Injeta o Meta Pixel (1357993553145702) em todas as paginas HTML do site
Triangle Flooring, e adiciona o evento 'Lead' na pagina /thanks/.

USO:
    python inject_meta_pixel.py

COMPORTAMENTO:
    - Insere o codigo base do Pixel (PageView) antes de </head> em todas as paginas
    - Na pagina /thanks/ tambem dispara fbq('track', 'Lead') = 1 conversao por form enviado
    - Idempotente: se o Pixel ja esta na pagina, pula
    - Backup automatico em .bak ao lado de cada arquivo modificado

REVERTER:
    find . -name "*.bak" -exec sh -c 'mv "$1" "${1%.bak}"' _ {} \\;
"""

import os
import re
import sys
from pathlib import Path

PIXEL_ID = '1357993553145702'

BASE_SNIPPET = f'''<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '{PIXEL_ID}');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id={PIXEL_ID}&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
'''

LEAD_SNIPPET = '''<!-- Meta Pixel Lead event (thanks page) -->
<script>fbq('track', 'Lead');</script>
'''


def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return ('error', str(e))

    # Idempotencia
    if PIXEL_ID in content:
        return ('skipped', 'already_injected')

    original = content
    is_thanks = '/thanks/' in filepath.replace(os.sep, '/')

    snippet = BASE_SNIPPET + (LEAD_SNIPPET if is_thanks else '')

    head_close = re.compile(r'</head>', re.IGNORECASE)
    if head_close.search(content):
        content = head_close.sub(snippet + '</head>', content, count=1)
        if content != original:
            backup = filepath + '.bak'
            if not os.path.exists(backup):
                with open(backup, 'w', encoding='utf-8') as f:
                    f.write(original)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return ('lead' if is_thanks else 'inserted', None)

    return ('no_head_tag', None)


def main():
    root = Path('.').resolve()
    print(f"Diretorio: {root}")
    print(f"Pixel ID:  {PIXEL_ID}\n")

    stats = {'inserted': 0, 'lead': 0, 'skipped': 0, 'no_head_tag': 0, 'error': 0}
    errors = []

    html_files = sorted(root.rglob('*.html'))
    print(f"Encontrados {len(html_files)} arquivos .html\n")

    for filepath in html_files:
        rel = filepath.relative_to(root)
        status, detail = process_file(str(filepath))
        stats[status] = stats.get(status, 0) + 1
        if status == 'lead':
            print(f"  [LEAD] {rel}  (Pixel + evento Lead)")
        elif status == 'no_head_tag':
            print(f"  [!] {rel}  (sem <head> - ignorado)")
        elif status == 'error':
            errors.append((rel, detail))
            print(f"  [X] {rel}  ({detail})")

    print("\n" + "=" * 56)
    print("RELATORIO FINAL")
    print("=" * 56)
    print(f"  Total HTML:            {len(html_files)}")
    print(f"  Pixel inserido:        {stats['inserted']}")
    print(f"  Pixel + Lead (thanks): {stats['lead']}")
    print(f"  Ja tinham (pulados):   {stats['skipped']}")
    print(f"  Sem <head>:            {stats['no_head_tag']}")
    print(f"  Erros:                 {stats['error']}")
    print(f"\n  MODIFICADOS: {stats['inserted'] + stats['lead']}")
    if errors:
        print("\n  Erros:")
        for path, err in errors:
            print(f"     {path}: {err}")
    print("=" * 56)
    return 0 if stats['error'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
