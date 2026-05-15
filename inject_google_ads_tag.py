#!/usr/bin/env python3
"""
inject_google_ads_tag.py
========================
Injeta o Google Ads tag (AW-16536846393) e o Call Conversion snippet em
todos os arquivos HTML do site Triangle Flooring.

USO:
    1. Copia este arquivo pra raiz do repo do site (mesma pasta do index.html)
    2. Roda: python3 inject_google_ads_tag.py
    3. Confere o relatório no terminal
    4. Commit + push pro GitHub

COMPORTAMENTO:
    - Se o HTML já tem GA4 (G-7VP0F63NPC): adiciona só as 2 linhas do AW logo após
    - Se NÃO tem GA4: insere o bloco completo (GA4 + AW + phone tracking) no <head>
    - Se já tem AW: pula (idempotente, pode rodar quantas vezes quiser)
    - Backup automático em .bak ao lado de cada arquivo modificado

REVERTER (caso precise):
    find . -name "*.bak" -exec sh -c 'mv "$1" "${1%.bak}"' _ {} \\;
"""

import os
import re
import sys
from pathlib import Path

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

AW_ID = 'AW-16536846393'
CALL_CONVERSION_LABEL = 'AW-16536846393/ZMrfCKLcq60cELmAsc09'
GA4_ID = 'G-7VP0F63NPC'
PHONE = '(941) 402-6861'

# ============================================================================
# SNIPPETS
# ============================================================================

# Bloco completo - inserido quando o arquivo NÃO tem GA4 ainda
FULL_SNIPPET = f'''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA4_ID}');
  gtag('config', '{AW_ID}');
  gtag('config', '{CALL_CONVERSION_LABEL}', {{
    'phone_conversion_number': '{PHONE}'
  }});
</script>
'''

# Linhas adicionais - inseridas após o gtag('config', 'G-...') existente
APPEND_LINES = f'''
  gtag('config', '{AW_ID}');
  gtag('config', '{CALL_CONVERSION_LABEL}', {{
    'phone_conversion_number': '{PHONE}'
  }});'''


def process_file(filepath):
    """Processa um arquivo HTML. Retorna status do processamento."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return ('error', str(e))

    # Já injetado? (idempotência)
    if AW_ID in content:
        return ('skipped', 'already_injected')

    original = content

    # Caso 1: GA4 já está presente — adicionar linhas AW logo após
    ga4_config_pattern = re.compile(
        r"(gtag\(\s*['\"]config['\"]\s*,\s*['\"]"
        + re.escape(GA4_ID)
        + r"['\"]\s*\)\s*;?)",
        re.IGNORECASE
    )
    if ga4_config_pattern.search(content):
        content = ga4_config_pattern.sub(
            lambda m: m.group(1) + APPEND_LINES,
            content,
            count=1
        )
        if content != original:
            write_file(filepath, content, original)
            return ('appended', None)

    # Caso 2: GA4 ausente — inserir bloco completo antes de </head>
    head_close_pattern = re.compile(r'</head>', re.IGNORECASE)
    if head_close_pattern.search(content):
        content = head_close_pattern.sub(
            FULL_SNIPPET + '</head>',
            content,
            count=1
        )
        if content != original:
            write_file(filepath, content, original)
            return ('inserted', None)

    return ('no_head_tag', None)


def write_file(filepath, new_content, original_content):
    """Salva o arquivo, fazendo backup do original."""
    backup = filepath + '.bak'
    if not os.path.exists(backup):
        with open(backup, 'w', encoding='utf-8') as f:
            f.write(original_content)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)


def main():
    root = Path('.').resolve()
    print(f"📂 Diretório: {root}")
    print(f"🎯 AW ID:     {AW_ID}")
    print(f"📞 Phone:     {PHONE}")
    print()

    stats = {
        'appended': 0,
        'inserted': 0,
        'skipped': 0,
        'no_head_tag': 0,
        'error': 0,
    }
    errors = []

    # Encontra TODOS os .html (não só index.html)
    html_files = sorted(root.rglob('*.html'))
    print(f"🔍 Encontrados {len(html_files)} arquivos .html\n")

    for filepath in html_files:
        rel = filepath.relative_to(root)
        status, detail = process_file(str(filepath))

        if status == 'skipped':
            stats['skipped'] += 1
        elif status == 'appended':
            stats['appended'] += 1
            print(f"  ✅ {rel}  (GA4 já presente → linhas AW adicionadas)")
        elif status == 'inserted':
            stats['inserted'] += 1
            print(f"  ✅ {rel}  (bloco completo inserido)")
        elif status == 'no_head_tag':
            stats['no_head_tag'] += 1
            print(f"  ⚠️  {rel}  (sem <head> — ignorado)")
        else:
            stats['error'] += 1
            errors.append((rel, detail))
            print(f"  ❌ {rel}  ({detail})")

    # Relatório final
    print()
    print("=" * 60)
    print("📊 RELATÓRIO FINAL")
    print("=" * 60)
    print(f"  Total de arquivos HTML:        {len(html_files)}")
    print(f"  AW adicionado após GA4:        {stats['appended']}")
    print(f"  Bloco completo inserido:       {stats['inserted']}")
    print(f"  Já tinham AW (pulados):        {stats['skipped']}")
    print(f"  Sem <head> (ignorados):        {stats['no_head_tag']}")
    print(f"  Erros:                         {stats['error']}")
    print()
    print(f"  🎯 ARQUIVOS MODIFICADOS:       {stats['appended'] + stats['inserted']}")
    print()
    print("  💾 Backups salvos em *.bak ao lado de cada arquivo modificado.")
    print("     Pra reverter:")
    print('     find . -name "*.bak" -exec sh -c \'mv "$1" "${1%.bak}"\' _ {} \\;')
    print()

    if errors:
        print("  ❌ Erros encontrados:")
        for path, err in errors:
            print(f"     {path}: {err}")

    print("=" * 60)
    print("✅ PRÓXIMO PASSO:")
    print("   1. Confere visualmente um dos arquivos modificados (ex: index.html)")
    print("   2. Deleta os .bak: find . -name '*.bak' -delete")
    print("   3. git add . && git commit -m 'Add Google Ads tag' && git push")
    print("=" * 60)

    return 0 if stats['error'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
