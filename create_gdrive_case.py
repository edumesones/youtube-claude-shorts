"""
Genera video: Claude Code + Google Drive + Análisis de PDFs
Caso de uso real y práctico.
"""
import os
import sys
sys.path.insert(0, 'src')

from generate_voice import generate_voice
from generate_thumbnail import generate_thumbnail
import subprocess
from pathlib import Path


def main():
    print("=" * 60)
    print("🎬 CASO DE USO: Claude Code + Google Drive + PDFs")
    print("=" * 60)
    
    Path('output').mkdir(exist_ok=True)
    
    # SCRIPT DEL VIDEO (45 segundos)
    # Caso real: Conectar Google Drive y analizar PDFs
    
    script_por_secciones = [
        {
            'time': '[0:00-0:05]',
            'text': '¿Y si Claude pudiera leer todos tus documentos automáticamente?',
            'visual': 'Hook: Iconos Google Drive + Claude + flecha de conexión'
        },
        {
            'time': '[0:05-0:15]',
            'text': 'Así lo hice: conecté mi Google Drive a Claude Code con un comando.',
            'visual': 'Terminal mostrando: /mcp add google-drive'
        },
        {
            'time': '[0:15-0:28]',
            'text': 'Tenía cientos de PDFs de informes. Le pedí a Claude que analizara el último trimestre.',
            'visual': 'Lista de PDFs + cursor seleccionando uno'
        },
        {
            'time': '[0:28-0:40]',
            'text': 'En segundos, extrajo métricas clave, tendencias y me resumió los insights principales.',
            'visual': 'Pantalla dividida: PDF original vs resumen generado'
        },
        {
            'time': '[0:40-0:45]',
            'text': 'Horas de trabajo en minutos. Sígueme para más automatizaciones.',
            'visual': 'Reloj girando rápido + emoji cohete'
        }
    ]
    
    # Unir texto para TTS
    full_script = " ".join([s['text'] for s in script_por_secciones])
    
    print("\n📝 Script del video:")
    for i, sec in enumerate(script_por_secciones, 1):
        print(f"\n{i}. {sec['time']}")
        print(f"   🗣️  {sec['text']}")
        print(f"   👁️  {sec['visual']}")
    
    # 1. GENERAR VOZ
    print("\n🎙️ Generando voz...")
    audio_path = "output/caso_gdrive_voice.mp3"
    
    if not generate_voice(full_script, audio_path, voice='es-ES-AlvaroNeural'):
        print("❌ Falló voz")
        return False
    
    # Obtener duración real del audio
    result = subprocess.run(
        f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {audio_path}",
        shell=True, capture_output=True, text=True
    )
    duration = float(result.stdout.strip()) if result.returncode == 0 else 45.0
    
    print(f"   ✅ Audio: {duration:.1f}s")
    
    # 2. GENERAR THUMBNAIL
    print("\n🎨 Generando thumbnail...")
    thumbnail_path = "output/caso_gdrive_thumb.jpg"
    
    generate_thumbnail(
        title="CLAUDE + GOOGLE DRIVE",
        subtitle="Análisis de PDFs automático",
        output_path=thumbnail_path,
        style="dark"
    )
    
    # 3. INFO PARA EDICIÓN MANUAL
    print("\n" + "=" * 60)
    print("📋 INSTRUCCIONES PARA EDICIÓN PROFESIONAL")
    print("=" * 60)
    print(f"""
Para crear el video de alta calidad, necesitas editar manualmente:

🎬 SECUENCIA VISUAL SUGERIDA:

1. [0:00-0:05] HOOK
   - Fondo: Gradient azul-morado
   - Centro: Logo Claude + Logo Google Drive
   - Animación: Ambos logos aparecen con fade
   - Texto: "¿Y si Claude pudiera...?"

2. [0:05-0:15] DEMOSTRACIÓN
   - Fondo: Terminal oscuro
   - Mostrar: "/mcp add google-drive"
   - Cursor parpadeando
   - Texto: "Así lo hice..."

3. [0:15-0:28] CONTEXTO
   - Fondo: Interfaz de Google Drive (screenshot)
   - Múltiples íconos de PDF
   - Resaltado en uno de ellos
   - Texto: "Tenía cientos de PDFs..."

4. [0:28-0:40] RESULTADO
   - Split screen: PDF | Resumen
   - Gráficos simples subiendo
   - Texto destacado: "Métricas clave"

5. [0:40-0:45] CTA
   - Fondo: Mismo que inicio
   - Reloj animado girando rápido
   - Cohete 🚀
   - Texto: "Horas en minutos"

🎙️ AUDIO: {audio_path}
   Duración: {duration:.1f} segundos

🖼️ THUMBNAIL: {thumbnail_path}

💡 SUGERENCIA:
   Usa CapCut, Premiere o DaVinci Resolve
   Sincroniza cortes con las pausas naturales del audio.
""")
    
    # 4. GENERAR VIDEO SIMPLE (placeholder)
    print("\n🎬 Generando video base...")
    video_path = "output/caso_gdrive_video.mp4"
    
    cmd = f"""
    ffmpeg -y -f lavfi -i color=c=1a1a2e:s=1080x1920:d={duration} \
    -i {audio_path} -c:v libx264 -preset ultrafast \
    -c:a aac -shortest {video_path}
    """
    
    subprocess.run(cmd, shell=True, capture_output=True)
    
    if os.path.exists(video_path) and os.path.getsize(video_path) > 10000:
        size_mb = os.path.getsize(video_path) / (1024*1024)
        print(f"✅ Video base generado: {size_mb:.1f} MB")
        print(f"📁 {video_path}")
        
        print("\n" + "=" * 60)
        print("⚠️  NOTA IMPORTANTE")
        print("=" * 60)
        print("Este es un video BASE con fondo sólido.")
        print("Para alta calidad profesional, edita manualmente usando")
        print("las instrucciones de secuencia visual de arriba.")
        print("=" * 60)
        
        return True
    else:
        print("❌ Falló video")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
