"""
Transcriptor de audio a texto usando Faster-Whisper.
Soporta español y múltiples formatos de audio.
"""
import os
import sys
from faster_whisper import WhisperModel
from pathlib import Path


def transcribir_audio(ruta_audio: str, modelo: str = "small") -> str:
    """
    Transcribe un archivo de audio a texto en español.
    
    Args:
        ruta_audio: Ruta al archivo (mp3, wav, m4a, etc.)
        modelo: Tamaño del modelo (tiny, base, small, medium, large)
                tiny = más rápido, menos preciso
                large = más lento, más preciso
    
    Returns:
        Texto transcrito completo
    """
    if not os.path.exists(ruta_audio):
        return f"❌ Error: No existe el archivo {ruta_audio}"
    
    print(f"🎙️ Cargando modelo Whisper ({modelo})...")
    print(f"📁 Archivo: {ruta_audio}")
    
    try:
        # Cargar modelo (primera vez descarga ~150MB para 'small')
        model = WhisperModel(
            modelo,
            device="cpu",           # Usar CPU (funciona en cualquier servidor)
            compute_type="int8"     # Optimizado para velocidad
        )
        
        print("📝 Transcribiendo... (puede tardar unos segundos)")
        
        # Transcribir
        segments, info = model.transcribe(
            ruta_audio,
            language="es",          # Forzar español
            task="transcribe",
            beam_size=5,
            best_of=5,
            condition_on_previous_text=True
        )
        
        print(f"   Detectado idioma: {info.language} (prob: {info.language_probability:.2f})")
        
        # Unir todos los segmentos
        texto_completo = []
        for segment in segments:
            texto_completo.append(segment.text.strip())
            print(f"   [{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        
        resultado = " ".join(texto_completo)
        
        print(f"\n✅ Transcripción completa!")
        print(f"   Duración total: {info.duration:.1f} segundos")
        print(f"   Palabras: {len(resultado.split())}")
        
        return resultado
        
    except Exception as e:
        return f"❌ Error en transcripción: {str(e)}"


def guardar_transcripcion(texto: str, ruta_salida: str = None):
    """Guarda la transcripción en un archivo."""
    if ruta_salida is None:
        ruta_salida = "output/transcripcion.txt"
    
    Path(ruta_salida).parent.mkdir(parents=True, exist_ok=True)
    
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(texto)
    
    print(f"💾 Guardado en: {ruta_salida}")


# === USO DIRECTO ===
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("=" * 60)
        print("🎙️ TRANSCRIPTOR DE AUDIO - Faster Whisper")
        print("=" * 60)
        print("\nUso:")
        print("  python transcribir.py <ruta_al_audio> [modelo]")
        print("\nEjemplos:")
        print("  python transcribir.py mi_audio.mp3")
        print("  python transcribir.py audio.wav large")
        print("\nModelos disponibles:")
        print("  tiny   - Rápido, básico")
        print("  base   - Balanceado")
        print("  small  - Buena precisión (recomendado)")
        print("  medium - Alta precisión")
        print("  large  - Máxima precisión, más lento")
        print("=" * 60)
        sys.exit(1)
    
    audio_file = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "small"
    
    resultado = transcribir_audio(audio_file, model_size)
    
    if not resultado.startswith("❌"):
        # Guardar automáticamente
        output_file = audio_file.rsplit('.', 1)[0] + "_transcripcion.txt"
        guardar_transcripcion(resultado, output_file)
        
        print("\n" + "=" * 60)
        print("TEXTO COMPLETO:")
        print("=" * 60)
        print(resultado)
        print("=" * 60)
