"""
Renderiza videos de YouTube Shorts usando MoviePy.
Versión: Gratis (MoviePy + FFmpeg)
"""
from moviepy import *
from moviepy.video.fx import FadeIn, FadeOut
import os
from typing import List, Dict, Optional


def create_text_clip(text: str, duration: float, position: str = "center",
                     fontsize: int = 70, color: str = "white",
                     start_time: float = 0):
    """Crea un clip de texto animado."""
    
    txt_clip = TextClip(
        text=text,
        font_size=fontsize,
        color=color,
        stroke_color="black",
        stroke_width=2,
        size=(900, None),
        text_align="center"
    ).with_duration(duration).with_start(start_time)
    
    # Posicionar
    if position == "center":
        txt_clip = txt_clip.with_position("center")
    elif position == "top":
        txt_clip = txt_clip.with_position(("center", 200))
    elif position == "bottom":
        txt_clip = txt_clip.with_position(("center", 1500))
    
    return txt_clip


def render_short_video(
    audio_path: str,
    script_sections: List[str],
    thumbnail_path: str,
    output_path: str = "output/video.mp4",
    add_subtitles: bool = True
) -> bool:
    """
    Renderiza un video de YouTube Short completo.
    
    Args:
        audio_path: Ruta al archivo de audio (MP3)
        script_sections: Lista de secciones del script con timestamps
        thumbnail_path: Ruta a la imagen de thumbnail (para fondo)
        output_path: Ruta de salida del video
        add_subtitles: Si es True, añade subtítulos animados
    
    Returns:
        True si exitoso
    """
    try:
        print("🎬 Renderizando video...")
        
        # 1. Cargar audio
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
        print(f"   Duración del audio: {duration:.1f}s")
        
        # 2. Crear fondo
        # Opción A: Color sólido degradado
        bg = ColorClip(size=(1080, 1920), color=(20, 20, 40))
        bg = bg.with_duration(duration)
        
        # Opción B: Usar thumbnail como fondo (blur)
        # if os.path.exists(thumbnail_path):
        #     from PIL import Image, ImageFilter
        #     img = Image.open(thumbnail_path)
        #     img = img.filter(ImageFilter.GaussianBlur(radius=10))
        #     img.save("output/bg_blur.jpg")
        #     bg = ImageClip("output/bg_blur.jpg").set_duration(duration)
        #     bg = bg.resize(height=1920)
        
        # 3. Preparar clips
        clips = [bg]
        
        # 4. Añadir subtítulos por sección
        if add_subtitles and script_sections:
            # Parsear timestamps y calcular duraciones
            current_time = 0
            
            for i, section in enumerate(script_sections):
                # Extraer texto (quitar timestamp)
                text = section.split(']', 1)[1].strip() if ']' in section else section
                
                # Calcular duración de esta sección
                if i < len(script_sections) - 1:
                    # Buscar siguiente timestamp
                    next_section = script_sections[i + 1]
                    # Simple: dividir duración total entre número de secciones
                    section_duration = duration / len(script_sections)
                else:
                    section_duration = duration - current_time
                
                # Crear clip de texto
                txt_clip = create_text_clip(
                    text=text,
                    duration=min(section_duration, duration - current_time),
                    position="center",
                    fontsize=80,
                    start_time=current_time
                )
                
                clips.append(txt_clip)
                current_time += section_duration
        
        # 5. Añadir watermark/logo
        watermark = TextClip(
            text="@ClaudeTipsES",
            font_size=40,
            color="white",
            stroke_color="black",
            stroke_width=1
        ).with_duration(duration).with_position((20, 20))
        clips.append(watermark)
        
        # 6. Combinar todos los clips
        video = CompositeVideoClip(clips, size=(1080, 1920))
        
        # 7. Añadir audio
        video = video.with_audio(audio)
        
        # 8. Exportar
        print("   Exportando... (esto puede tardar)")
        video.write_videofile(
            output_path,
            fps=30,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="output/temp-audio.m4a",
            remove_temp=True,
            threads=4,
            preset="ultrafast",  # Más rápido, ligeramente más grande
            logger=None  # Silenciar logs de moviepy
        )
        
        # 9. Limpiar
        video.close()
        audio.close()
        
        print(f"✅ Video renderizado: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error renderizando video: {e}")
        import traceback
        traceback.print_exc()
        return False


def get_video_info(video_path: str) -> Optional[Dict]:
    """Obtiene información del video generado."""
    try:
        from moviepy.editor import VideoFileClip
        
        clip = VideoFileClip(video_path)
        info = {
            'duration': clip.duration,
            'fps': clip.fps,
            'size': clip.size,
            'file_size_mb': os.path.getsize(video_path) / (1024 * 1024)
        }
        clip.close()
        return info
        
    except Exception as e:
        print(f"⚠️ Error obteniendo info: {e}")
        return None


if __name__ == "__main__":
    # Test (requiere audio de prueba)
    print("Para testear, primero genera un audio con generate_voice.py")
