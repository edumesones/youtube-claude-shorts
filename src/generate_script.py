"""
Genera scripts virales para YouTube Shorts usando Claude API.
Versión: Optimizada para bajo costo (Claude 3 Haiku es más barato)
"""
import os
from anthropic import Anthropic
from typing import Dict, Optional


def generate_script(tip: Dict) -> Optional[Dict]:
    """
    Genera un script viral de 30-45 segundos para YouTube Short.
    
    Args:
        tip: Dict con version, title, description
    
    Returns:
        Dict con: full_script, sections (con timestamps), title, description, hashtags
    """
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY no configurado")
        return None
    
    client = Anthropic(api_key=api_key)
    
    prompt = f"""
Eres un creador de contenido viral de tecnología. Tu especialidad es explicar tips de Claude Code en español de forma rápida y entretenida.

INFORMACIÓN DEL TIP:
- Versión: {tip['version']}
- Descripción: {tip['description']}

CREA UN GUION PARA YOUTUBE SHORT (30-45 segundos):

REGLAS:
1. Hook en los primeros 3 segundos ("¿Sabías que...?", "Atención...", "Esto cambia todo...")
2. Explica el problema/solución en lenguaje simple
3. Máximo emojis (🚀 ⚡ 💡 🤯)
4. Llamada a la acción final ("Sígueme", "Dale like", "Comenta")
5. Divide en secciones con timestamps

FORMATO DE RESPUESTA:
TITULO: [título atractivo con emoji]

GUIÓN:
[0:00-0:03] [texto del hook]
[0:03-0:15] [texto explicando]
[0:15-0:25] [texto solución/beneficio]
[0:25-0:35] [texto llamada a la acción]

DESCRIPCION: [descripción para YouTube, incluye hashtags]

HASHTAGS: #claude #claudecode #[otros 3 hashtags relevantes]
"""
    
    try:
        # Usar Claude 3 Haiku (más barato: $0.25/1K input, $1.25/1K output)
        # vs Opus ($15/1K input, $75/1K output) = 60x más barato
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            temperature=0.8,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        content = response.content[0].text
        
        # Parsear respuesta
        lines = content.strip().split('\n')
        
        # Extraer secciones
        script_sections = []
        full_script = []
        title = ""
        description = ""
        hashtags = ""
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith("TITULO:"):
                title = line.replace("TITULO:", "").strip()
            elif line.startswith("DESCRIPCION:"):
                description = line.replace("DESCRIPCION:", "").strip()
            elif line.startswith("HASHTAGS:"):
                hashtags = line.replace("HASHTAGS:", "").strip()
            elif line.startswith("[0:"):
                # Es una sección con timestamp
                script_sections.append(line)
                # Extraer solo el texto (sin timestamp)
                text_only = ']'.join(line.split(']')[1:]).strip()
                full_script.append(text_only)
        
        return {
            'title': title,
            'full_script': ' '.join(full_script),
            'sections': script_sections,
            'description': description,
            'hashtags': hashtags,
            'cost_usd': response.usage.input_tokens * 0.00025 / 1000 + response.usage.output_tokens * 0.00125 / 1000
        }
        
    except Exception as e:
        print(f"❌ Error generando script: {e}")
        return None


if __name__ == "__main__":
    # Test
    test_tip = {
        'version': '2.1.62',
        'description': 'Fixed prompt suggestion cache regression that reduced cache hit rates'
    }
    
    script = generate_script(test_tip)
    if script:
        print(f"✅ Script generado:")
        print(f"   Título: {script['title']}")
        print(f"   Costo: ${script['cost_usd']:.4f}")
        print(f"   Secciones:")
        for section in script['sections']:
            print(f"      {section}")
    else:
        print("❌ No se pudo generar script")
