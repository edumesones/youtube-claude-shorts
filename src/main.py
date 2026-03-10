"""
Pipeline principal: Une todo el flujo de generación de video.
Ejecutar: python src/main.py
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Importar módulos
from fetch_tip import fetch_latest_tip
from generate_script import generate_script
from generate_voice import generate_voice
from generate_thumbnail import generate_thumbnail
from render_video import render_short_video, get_video_info
from upload_youtube import upload_video


def setup_directories():
    """Crea directorios necesarios."""
    dirs = ['output', 'logs', 'assets/fonts', 'assets/music']
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)


def log_result(data: dict):
    """Guarda log del video generado."""
    date_str = datetime.now().strftime('%Y-%m-%d')
    log_file = f'logs/{date_str}.json'
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"📝 Log guardado: {log_file}")


def main():
    """Pipeline completo de generación de video."""
    print("=" * 60)
    print("🎬 YOUTUBE CLAUDE SHORTS - PIPELINE")
    print("=" * 60)
    
    setup_directories()
    
    # Timestamp para archivos
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    try:
        # 1. FETCH TIP
        print("\n📥 Paso 1: Obteniendo tip del CHANGELOG...")
        tip = fetch_latest_tip()
        if not tip:
            print("❌ No se pudo obtener tip. Abortando.")
            return False
        
        print(f"   ✅ Tip: {tip['title']}")
        print(f"   📝 {tip['description'][:60]}...")
        
        # 2. GENERATE SCRIPT
        print("\n✍️ Paso 2: Generando script con Claude...")
        script_data = generate_script(tip)
        if not script_data:
            print("❌ No se pudo generar script. Abortando.")
            return False
        
        print(f"   ✅ Título: {script_data['title']}")
        print(f"   💰 Costo: ${script_data['cost_usd']:.4f}")
        print(f"   🎬 Secciones: {len(script_data['sections'])}")
        
        # 3. GENERATE VOICE
        print("\n🎙️ Paso 3: Generando voz (edge-tts)...")
        audio_path = f"output/voice_{timestamp}.mp3"
        
        if not generate_voice(script_data['full_script'], audio_path):
            print("❌ Falló generación de voz. Abortando.")
            return False
        
        print(f"   ✅ Audio: {audio_path}")
        
        # 4. GENERATE THUMBNAIL
        print("\n🎨 Paso 4: Generando thumbnail...")
        thumbnail_path = f"output/thumbnail_{timestamp}.jpg"
        
        if not generate_thumbnail(
            title=script_data['title'].replace('🚀', '').replace('⚡', '').strip(),
            subtitle=f"v{tip['version']}",
            output_path=thumbnail_path
        ):
            print("⚠️ Falló thumbnail, continuando sin él...")
            thumbnail_path = None
        else:
            print(f"   ✅ Thumbnail: {thumbnail_path}")
        
        # 5. RENDER VIDEO
        print("\n🎬 Paso 5: Renderizando video...")
        video_path = f"output/video_{timestamp}.mp4"
        
        if not render_short_video(
            audio_path=audio_path,
            script_sections=script_data['sections'],
            thumbnail_path=thumbnail_path,
            output_path=video_path
        ):
            print("❌ Falló renderizado. Abortando.")
            return False
        
        # Info del video
        video_info = get_video_info(video_path)
        if video_info:
            print(f"   ✅ Video: {video_info['duration']:.1f}s, {video_info['file_size_mb']:.1f}MB")
        
        # 6. UPLOAD TO YOUTUBE (opcional - solo si hay credenciales)
        print("\n📤 Paso 6: Subiendo a YouTube...")
        
        if not os.environ.get('YOUTUBE_REFRESH_TOKEN'):
            print("   ⚠️ No hay credenciales de YouTube. Video generado pero no subido.")
            print(f"   📁 Video local: {video_path}")
            result = {
                'success': True,
                'uploaded': False,
                'video_path': video_path,
                'reason': 'No YouTube credentials'
            }
        else:
            # Preparar tags
            tags = ['claude', 'claude code', 'inteligencia artificial', 'programación', 
                   'tutorial', 'coding', 'ai', 'tips'] + tip.get('all_changes', [])[:3]
            
            # Limitar tags
            tags = [t[:50] for t in tags[:15]]  # Max 15 tags, 50 chars cada uno
            
            upload_result = upload_video(
                video_path=video_path,
                title=script_data['title'],
                description=f"{script_data['description']}\n\n{script_data['hashtags']}",
                tags=tags,
                thumbnail_path=thumbnail_path,
                privacy_status="public"
            )
            
            if upload_result:
                print(f"   ✅ Subido: {upload_result['url']}")
                result = {
                    'success': True,
                    'uploaded': True,
                    'video_id': upload_result['video_id'],
                    'url': upload_result['url'],
                    'video_path': video_path
                }
            else:
                print("   ❌ Falló upload. Video guardado localmente.")
                result = {
                    'success': True,
                    'uploaded': False,
                    'video_path': video_path,
                    'reason': 'Upload failed'
                }
        
        # 7. LOG RESULT
        log_data = {
            'date': datetime.now().isoformat(),
            'tip': tip,
            'script': {
                'title': script_data['title'],
                'sections': script_data['sections'],
                'cost_usd': script_data['cost_usd']
            },
            'result': result,
            'video_info': video_info
        }
        
        log_result(log_data)
        
        print("\n" + "=" * 60)
        print("✅ PIPELINE COMPLETADO")
        print("=" * 60)
        
        if result.get('url'):
            print(f"🎉 Video publicado: {result['url']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN PIPELINE: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
