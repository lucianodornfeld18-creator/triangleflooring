#!/usr/bin/env python3
"""
fix_blog_images.py
Atualiza o CSS .article-feature-img em todos os blog posts pra reduzir
o tamanho/altura das imagens e focar melhor no piso.
"""

import os
import re
from pathlib import Path

# CSS antigo (single-line)
OLD_CSS = '.article-feature-img{max-width:1100px;margin:-2rem auto 0;padding:0 20px}\n.article-feature-img img{width:100%;border-radius:14px;box-shadow:var(--shadow-lg);aspect-ratio:8/5;object-fit:cover}'

# CSS novo - mais compacto, foco no piso, responsivo
NEW_CSS = '.article-feature-img{max-width:850px;margin:-1.5rem auto 0;padding:0 20px}\n.article-feature-img img{width:100%;border-radius:14px;box-shadow:var(--shadow-lg);aspect-ratio:16/9;object-fit:cover;object-position:center 60%;max-height:430px}\n@media(max-width:768px){.article-feature-img img{aspect-ratio:16/10;max-height:240px}}'

# Também precisa substituir versão de _build_pricing_posts.py (duplo {{ }})
OLD_CSS_PRICING = '.article-feature-img{{max-width:1100px;margin:-2rem auto 0;padding:0 20px}}\n.article-feature-img img{{width:100%;border-radius:14px;box-shadow:var(--shadow-lg);aspect-ratio:8/5;object-fit:cover}}'

NEW_CSS_PRICING = '.article-feature-img{{max-width:850px;margin:-1.5rem auto 0;padding:0 20px}}\n.article-feature-img img{{width:100%;border-radius:14px;box-shadow:var(--shadow-lg);aspect-ratio:16/9;object-fit:cover;object-position:center 60%;max-height:430px}}\n@media(max-width:768px){{.article-feature-img img{{aspect-ratio:16/10;max-height:240px}}}}'


def process_file(filepath):
    """Substitui o CSS no arquivo. Retorna True se modificou."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return False
    
    original = content
    
    # Tenta substituir versão padrão
    if OLD_CSS in content:
        content = content.replace(OLD_CSS, NEW_CSS)
    
    # Tenta substituir versão com {{ }} (template do _build_pricing_posts.py)
    if OLD_CSS_PRICING in content:
        content = content.replace(OLD_CSS_PRICING, NEW_CSS_PRICING)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    root = Path('.').resolve()
    print(f"📂 Diretório: {root}\n")
    
    modified = 0
    total = 0
    
    # Processa HTMLs do blog
    for filepath in sorted(root.glob('blog/**/*.html')):
        total += 1
        rel = filepath.relative_to(root)
        if process_file(str(filepath)):
            modified += 1
            print(f"  ✅ {rel}")
    
    # Processa scripts de build pra futuros rebuilds não desfazerem
    for script in ['_build_blog.py', '_build_pricing_posts.py']:
        if (root / script).exists():
            total += 1
            if process_file(str(root / script)):
                modified += 1
                print(f"  ✅ {script}")
    
    print(f"\n📊 Modificados: {modified} de {total} arquivos")
    return 0


if __name__ == '__main__':
    main()
