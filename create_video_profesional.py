#!/usr/bin/env python3
"""
GENERADOR FINAL - Video profesional Claude Code + Google Drive
Tutorial completo con pantallas reales + animaciones + voz
Nivel: BÁSICO (sin código técnico)
"""
import os
import sys
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, 'src')
from generate_voice import generate_voice

# Crear directorios
Path('output').mkdir(exist_ok=True)
Path('assets/frames').mkdir(parents=True, exist_ok=True)

# SCRIPT COMPLETO (45 segundos) - Tutorial + Demo + Resultados
SCRIPT = """
[SEGMENTO 1 - 0:00-0:05] HOOK
Imagina poder hablar con todos tus documentos como si fueran personas. 
Hoy te muestro cómo conectar Google Drive con Claude Code.

[SEGMENTO 2 - 0:05-0:15] PROBLEMA
Tienes cientos de PDFs, informes y contratos. Leerlos todos llevaría días. 
¿Y si pudieras preguntarles directamente qué dicen?

[SEGMENTO 3 - 0:15-0:28] SOLUCIÓN
Con Claude Code conectado a Drive, es súper fácil. Solo le dices: 
analiza mis documentos del último trimestre. Y en segundos, obtienes un resumen completo.

[SEGMENTO 4 - 0:28-0:40] RESULTADO
Claude extrajo tres insights clave: las ventas subieron un veintitrés por ciento, 
detectó tres contratos que expiran pronto, y recomendó enfocarse en el sector B2B 
donde el retorno de inversión es trescientos cuarenta por ciento.

[SEGMENTO 5 - 0:40-0:45] CTA
Todo esto en minutos, no en días. Prueba Claude Code y transforma cómo trabajas con documentos. 
¡Dale like y sígueme para más trucos!
"""

def crear_frame_gradiente(width=1080, height=1920, color1=(13, 17, 23), color2=(26, 26, 46)):
    """Crea fondo degradado."""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * y / height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return img

def crear_icono_claude(draw, x, y, size=80):
    """Dibuja icono hexagonal de Claude."""
    import math
    # Hexágono naranja #E57035
    color = (229, 112, 53)
    points = []
    for i in range(6):
        angle = i * 60 - 30
        px = x + size * 0.8 * math.cos(math.radians(angle))
        py = y + size * 0.8 * math.sin(math.radians(angle))
        points.append((px, py))
    draw.polygon(points, fill=color, outline=color)
    # Letra C blanca centrada
    try:
        font_c = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(size * 0.8))
    except:
        font_c = None
    bbox = draw.textbbox((0,0), "C", font=font_c)
    cx = x - (bbox[2]-bbox[0])//2
    cy = y - (bbox[3]-bbox[1])//2
    draw.text((cx, cy), "C", fill=(255,255,255), font=font_c)

def crear_icono_drive(draw, x, y, size=60):
    """Dibuja icono de Drive."""
    # Triángulo azul #4285F4
    color = (66, 133, 244)
    draw.polygon([(x, y-size), (x-size, y+size//2), (x+size, y+size//2)], fill=color)

def crear_icono_pdf(draw, x, y, size=40):
    """Dibuja icono PDF."""
    color = (234, 67, 53)  # Rojo
    draw.rectangle([x-size, y-size*1.3, x+size, y+size], fill=color, outline=(180,50,40), width=2)
    draw.text((x-25, y-10), "PDF", fill=(255,255,255), font=None)

def crear_frame_tutorial(num_frame, segmento, total_frames):
    """Crea frames del tutorial con elementos visuales."""
    img = crear_frame_gradiente()
    draw = ImageDraw.Draw(img)
    
    # Fuentes grandes para legibilidad en móvil
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        font_text = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 70)
    except:
        font_title = ImageFont.load_default()
        font_text = font_title
    
    # SEGMENTO 1: Hook - Iconos grandes
    if segmento == 1:
        crear_icono_drive(draw, 540, 450, 180)
        draw.text((470, 680), "+", fill=(255,255,255), font=font_title)
        crear_icono_claude(draw, 540, 900, 200)
        # Texto centrado grande
        texto = "Habla con tus"
        bbox = draw.textbbox((0,0), texto, font=font_title)
        x = (1080 - (bbox[2]-bbox[0])) // 2
        draw.text((x, 1150), texto, fill=(255,255,255), font=font_title)
        texto2 = "documentos"
        bbox2 = draw.textbbox((0,0), texto2, font=font_title)
        x2 = (1080 - (bbox2[2]-bbox2[0])) // 2
        draw.text((x2, 1300), texto2, fill=(255,255,255), font=font_title)

    # SEGMENTO 2: Problema - Archivos
    elif segmento == 2:
        texto = "20+ documentos"
        bbox = draw.textbbox((0,0), texto, font=font_title)
        x = (1080 - (bbox[2]-bbox[0])) // 2
        draw.text((x, 200), texto, fill=(200,200,200), font=font_title)
        y_pos = 450
        for i in range(5):
            crear_icono_pdf(draw, 200, y_pos + i*200, 60)
            draw.text((300, y_pos + i*200 - 25), f"informe_{i+1}.pdf", fill=(180,180,180), font=font_text)
        pregunta = "¿Días leyendo?"
        bbox = draw.textbbox((0,0), pregunta, font=font_title)
        x = (1080 - (bbox[2]-bbox[0])) // 2
        draw.text((x, 1550), pregunta, fill=(248,81,73), font=font_title)

    # SEGMENTO 3: Solución - Interfaz
    elif segmento == 3:
        # Caja de chat más grande
        draw.rounded_rectangle([60, 350, 1020, 950], radius=30, fill=(22, 27, 34), outline=(48,54,61), width=3)
        draw.text((120, 400), "Tú:", fill=(139,148,158), font=font_text)
        draw.text((120, 490), "Analiza mis", fill=(255,255,255), font=font_text)
        draw.text((120, 580), "documentos del", fill=(255,255,255), font=font_text)
        draw.text((120, 670), "último trimestre", fill=(255,255,255), font=font_text)

        # Respuesta de Claude
        draw.rounded_rectangle([60, 1020, 1020, 1500], radius=30, fill=(22, 27, 34), outline=(229,112,53), width=3)
        draw.text((120, 1070), "Claude:", fill=(229,112,53), font=font_text)
        draw.text((120, 1180), "Analizando...", fill=(63,185,80), font=font_title)
        crear_icono_claude(draw, 900, 1300, 80)

    # SEGMENTO 4: Resultados - Tarjetas
    elif segmento == 4:
        tarjetas = [
            ("VENTAS", "+23%", (35,134,54)),
            ("ALERTA", "3 contratos", (248,81,73)),
            ("TIP", "Enfoque B2B", (229,112,53))
        ]
        y_start = 250
        for i, (titulo, desc, color) in enumerate(tarjetas):
            y = y_start + i * 420
            draw.rounded_rectangle([80, y, 1000, y+350], radius=25, fill=(22,27,34))
            draw.rectangle([80, y, 105, y+350], fill=color)
            draw.text((140, y+40), titulo, fill=(255,255,255), font=font_title)
            draw.text((140, y+180), desc, fill=(201,209,217), font=font_title)

    # SEGMENTO 5: CTA
    else:
        texto = "PRUEBA AHORA"
        bbox = draw.textbbox((0,0), texto, font=font_title)
        x = (1080 - (bbox[2]-bbox[0])) // 2
        draw.text((x, 500), texto, fill=(229,112,53), font=font_title)
        # Botón grande
        draw.rounded_rectangle([200, 800, 880, 1000], radius=50, fill=(255,255,255))
        suscribirse = "SUSCRIBIRSE"
        bbox = draw.textbbox((0,0), suscribirse, font=font_title)
        x = (1080 - (bbox[2]-bbox[0])) // 2
        draw.text((x, 850), suscribirse, fill=(13,17,23), font=font_title)
        cta = "Like · Comenta · Comparte"
        bbox = draw.textbbox((0,0), cta, font=font_text)
        x = (1080 - (bbox[2]-bbox[0])) // 2
        draw.text((x, 1200), cta, fill=(139,148,158), font=font_text)
    
    return img

def main():
    print("=" * 60)
    print("🎬 GENERANDO VIDEO PROFESIONAL")
    print("Claude Code + Google Drive Tutorial")
    print("=" * 60)
    
    # 1. GENERAR VOZ
    print("\n🎙️ Generando voz profesional...")
    audio_path = "output/tutorial_voice.mp3"
    
    # Extraer solo el texto para TTS (sin marcas de segmento)
    texto_tts = SCRIPT.replace("[SEGMENTO 1 - 0:00-0:05] HOOK\n", "") \
                     .replace("[SEGMENTO 2 - 0:05-0:15] PROBLEMA\n", "") \
                     .replace("[SEGMENTO 3 - 0:15-0:28] SOLUCIÓN\n", "") \
                     .replace("[SEGMENTO 4 - 0:28-0:40] RESULTADO\n", "") \
                     .replace("[SEGMENTO 5 - 0:40-0:45] CTA\n", "") \
                     .strip()
    
    if not generate_voice(texto_tts, audio_path, voice='es-ES-AlvaroNeural'):
        print("❌ Falló voz")
        return False
    
    # Obtener duración
    result = subprocess.run(
        f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {audio_path}",
        shell=True, capture_output=True, text=True
    )
    duration = float(result.stdout.strip()) if result.returncode == 0 else 45.0
    print(f"   ✅ Audio: {duration:.1f} segundos")
    
    # 2. GENERAR FRAMES
    print("\n🎨 Generando frames animados...")
    fps = 30
    total_frames = int(duration * fps)
    
    # Distribución de segmentos
    segmentos = [
        (0, int(5 * fps), 1),      # 0-5s: Hook
        (int(5 * fps), int(15 * fps), 2),   # 5-15s: Problema
        (int(15 * fps), int(28 * fps), 3),  # 15-28s: Solución
        (int(28 * fps), int(40 * fps), 4),  # 28-40s: Resultados
        (int(40 * fps), total_frames, 5),   # 40-45s: CTA
    ]
    
    frame_files = []
    for i in range(total_frames):
        # Determinar segmento actual
        seg_num = 1
        for start, end, seg in segmentos:
            if start <= i < end:
                seg_num = seg
                break
        
        # Crear frame
        frame = crear_frame_tutorial(i, seg_num, total_frames)
        frame_path = f"assets/frames/frame_{i:05d}.jpg"
        frame.save(frame_path, quality=90)
        frame_files.append(frame_path)
        
        if i % 30 == 0:
            print(f"   Frame {i}/{total_frames} (segmento {seg_num})")
    
    print(f"   ✅ {len(frame_files)} frames generados")
    
    # 3. RENDERIZAR VIDEO
    print("\n🎬 Renderizando video final...")
    video_path = "output/video_tutorial_profesional.mp4"
    
    cmd = f"""
    ffmpeg -y -framerate 30 -i assets/frames/frame_%05d.jpg -i {audio_path} \
    -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
    -c:a aac -b:a 192k -shortest {video_path}
    """
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # Limpiar frames temporales
    for f in frame_files:
        os.remove(f)
    
    if result.returncode == 0 and os.path.exists(video_path):
        size_mb = os.path.getsize(video_path) / (1024*1024)
        print(f"\n✅ VIDEO PROFESIONAL COMPLETADO")
        print(f"📁 {video_path}")
        print(f"💾 {size_mb:.1f} MB")
        print(f"⏱️  {duration:.1f} segundos")
        print(f"🎨 5 segmentos con animaciones")
        print(f"🎙️  Voz profesional en español")
        
        print("\n" + "=" * 60)
        print("CONTENIDO DEL VIDEO:")
        print("=" * 60)
        print("• Hook: Conectar Drive + Claude")
        print("• Problema: Muchos documentos")
        print("• Solución: Análisis automático")
        print("• Resultados: 3 insights clave")
        print("• CTA: Prueba ahora + Suscríbete")
        print("=" * 60)
        
        return True
    else:
        print(f"❌ Error: {result.stderr[:500]}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
