"""
Obtiene tips de Claude Code desde el CHANGELOG de GitHub.
Versión: Gratis (GitHub API pública)
"""
import requests
import re
from typing import Dict, Optional


def fetch_latest_tip() -> Optional[Dict]:
    """
    Obtiene el tip más reciente del CHANGELOG de claude-code.
    
    Returns:
        Dict con: version, title, description, url
    """
    try:
        # 1. Obtener CHANGELOG raw
        url = "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        changelog = response.text
        
        # 2. Parsear primera versión (la más reciente)
        # Formato: ## 2.1.62\n\n- cambio 1\n- cambio 2
        version_match = re.search(r'##\s+(\d+\.\d+\.\d+)\s*\n\n((?:-[^\n]+\n)+)', changelog)
        
        if not version_match:
            return None
        
        version = version_match.group(1)
        changes_text = version_match.group(2)
        
        # Extraer cambios individuales
        changes = [c.strip('- ') for c in changes_text.strip().split('\n') if c.strip()]
        
        if not changes:
            return None
        
        # Tomar el primer cambio (más importante)
        main_change = changes[0]
        
        return {
            'version': version,
            'title': f"Claude Code v{version}",
            'description': main_change,
            'all_changes': changes,
            'url': f"https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md",
            'date': None  # Podemos obtenerlo de los commits si es necesario
        }
        
    except Exception as e:
        print(f"❌ Error fetching tip: {e}")
        return None


def fetch_tip_from_commits() -> Optional[Dict]:
    """
    Alternativa: Obtener desde commits recientes (más detallado).
    """
    try:
        # Obtener commits del CHANGELOG
        commits_url = "https://api.github.com/repos/anthropics/claude-code/commits?path=CHANGELOG.md&per_page=5"
        response = requests.get(commits_url, timeout=30)
        commits = response.json()
        
        if not commits:
            return None
        
        # Tomar el commit más reciente
        latest = commits[0]
        commit_message = latest['commit']['message'].split('\n')[0]
        
        # Intentar extraer versión del mensaje
        version_match = re.search(r'(\d+\.\d+\.\d+)', commit_message)
        version = version_match.group(1) if version_match else "latest"
        
        return {
            'version': version,
            'title': f"Nueva actualización de Claude Code",
            'description': commit_message,
            'url': latest['html_url'],
            'date': latest['commit']['committer']['date'],
            'author': latest['commit']['author']['name']
        }
        
    except Exception as e:
        print(f"❌ Error fetching from commits: {e}")
        return None


if __name__ == "__main__":
    # Test
    tip = fetch_latest_tip()
    if tip:
        print(f"✅ Tip encontrado:")
        print(f"   Versión: {tip['version']}")
        print(f"   Título: {tip['title']}")
        print(f"   Descripción: {tip['description'][:80]}...")
    else:
        print("❌ No se encontró tip")
