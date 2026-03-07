"""
Genera thumbnails para YouTube Shorts usando Pillow (GRATIS).
Versión: Sin APIs de pago, solo código Python.
"""
from PIL import Image, ImageDraw, ImageFont
import os
from typing import Tuple, Optional


def create_gradient_background(width: int, height: int, color1: Tuple[int, int, int], 
                                color2: Tuple[int, int, int]) -> Image.Image:
    """Crea un fondo degradado."""
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * y / height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return image


def add_text_with_outline(draw: ImageDraw.Draw, text: str, position: Tuple[int, int],
                          font: ImageFont.FreeTypeFont, fill: str = "white",
                          outline: str = "black", outline_width: int = 3):
    """Añade texto con contorno para mejor legibilidad."""
    x, y = position
    
    # Dibujar contorno
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline)
    
    # Dibujar texto principal
    draw.text((x, y), text, font=font, fill=fill)


def generate_thumbnail(title: str, subtitle: str = None, output_path: str = "output/thumbnail.jpg",
                       style: str = "dark") -> bool:
    """
    Genera una thumbnail para YouTube Short.
    
    Args:
        title: Título principal (ej: "CLAUDE MÁS RÁPIDO 🚀")
        subtitle: Subtítulo opcional (ej: "Actualización 2.1.62")
        output_path: Ruta de salida
        style: "dark" o "light"
    
    Returns:
        True si exitoso
    """
    try:
        # Dimensiones para Shorts (vertical)
        width, height = 1080, 1920
        
        # Colores según estilo
        if style == "dark":
            bg_color1 = (15, 15, 35)      # Azul muy oscuro
            bg_color2 = (40, 20, 60)      # Púrpura oscuro
            text_color = "white"
            accent_color = (100, 200, 255)  # Azul claro
        else:
            bg_color1 = (240, 240, 250)
            bg_color2 = (200, 220, 255)
            text_color = "black"
            accent_color = (50, 100, 200)
        
        # Crear fondo degradado
        image = create_gradient_background(width, height, bg_color1, bg_color2)
        draw = ImageDraw.Draw(image)
        
        # Intentar cargar fuentes
        try:
            # Intentar fuentes del sistema
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
            font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60)
            font_emoji = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 150)
        except:
            # Fallback a fuente por defecto
            font_title = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()
            font_emoji = font_title
        
        # Dibujar decoración (círculos/rectángulos)
        draw.ellipse([(-100, -100), (300, 300)], fill=(*accent_color, 50))
        draw.ellipse([(width-200, height-400), (width+100, height-100)], fill=(*accent_color, 30))
        
        # Separar título en palabras para wrap
        words = title.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > 12:  # Máximo ~12 chars por línea
                lines.append(' '.join(current_line[:-1]))
                current_line = [current_line[-1]]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Dibujar líneas de título
        y_start = 650
        line_height = 140
        
        for i, line in enumerate(lines[:3]):  # Máximo 3 líneas
            y = y_start + i * line_height
            
            # Centrar texto
            bbox = draw.textbbox((0, 0), line, font=font_title)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            
            add_text_with_outline(draw, line, (x, y), font_title, 
                                  fill=text_color, outline=(0, 0, 0) if style == "dark" else (255, 255, 255))
        
        # Dibujar subtítulo
        if subtitle:
            bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = y_start + len(lines) * line_height + 50
            
            add_text_with_outline(draw, subtitle, (x, y), font_subtitle,
                                  fill=text_color, outline=(0, 0, 0) if style == "dark" else (255, 255, 255))
        
        # Guardar
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path, "JPEG", quality=95)
        
        print(f"✅ Thumbnail generada: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error generando thumbnail: {e}")
        return False


def generate_thumbnail_variants(title: str, subtitle: str = None, output_dir: str = "output") -> list:
    """
    Genera múltiples variantes de thumbnail para A/B testing.
    
    Returns:
        Lista de rutas de archivos generados
    """
    variants = []
    
    # Variante A: Estilo oscuro
    path_a = os.path.join(output_dir, "thumbnail_a.jpg")
    if generate_thumbnail(title, subtitle, path_a, style="dark"):
        variants.append(path_a)
    
    # Variante B: Estilo claro
    path_b = os.path.join(output_dir, "thumbnail_b.jpg")
    if generate_thumbnail(title, subtitle, path_b, style="light"):
        variants.append(path_b)
    
    return variants


if __name__ == "__main__":
    # Test
    success = generate_thumbnail(
        title="CLAUDE MÁS RÁPIDO 🚀",
        subtitle="Actualización 2.1.62",
        output_path="output/thumbnail_test.jpg"
    )
    
    if success:
        print("✅ Thumbnail de prueba generada")
        print("💰 Costo: $0.00 (Pillow es gratis)")
    else:
        print("❌ Falló la generación")
