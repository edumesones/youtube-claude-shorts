"""
Sube videos a YouTube usando la Data API v3.
Versión: Gratis (10,000 unidades/día)
"""
import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from typing import Optional, Dict


SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


def get_youtube_service():
    """
    Obtiene servicio autenticado de YouTube usando refresh token.
    """
    # Cargar credenciales desde environment variables
    client_id = os.environ.get('YOUTUBE_CLIENT_ID')
    client_secret = os.environ.get('YOUTUBE_CLIENT_SECRET')
    refresh_token = os.environ.get('YOUTUBE_REFRESH_TOKEN')
    
    if not all([client_id, client_secret, refresh_token]):
        raise ValueError("Faltan credenciales de YouTube en environment variables")
    
    # Crear credentials desde refresh token
    credentials = Credentials(
        None,  # No access token, se refresca automáticamente
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES
    )
    
    # Refrescar token
    credentials.refresh(Request())
    
    # Crear servicio
    youtube = build('youtube', 'v3', credentials=credentials, cache_discovery=False)
    
    return youtube


def upload_video(
    video_path: str,
    title: str,
    description: str,
    tags: list,
    thumbnail_path: str = None,
    privacy_status: str = "public"
) -> Optional[Dict]:
    """
    Sube un video a YouTube.
    
    Args:
        video_path: Ruta al archivo MP4
        title: Título del video (max 100 chars)
        description: Descripción (max 5000 chars)
        tags: Lista de tags
        thumbnail_path: Ruta a imagen JPG (opcional)
        privacy_status: "public", "private", o "unlisted"
    
    Returns:
        Dict con video_id, url, etc. o None si falla
    """
    try:
        youtube = get_youtube_service()
        
        print("📤 Subiendo video a YouTube...")
        
        # Preparar body del video
        body = {
            'snippet': {
                'title': title[:100],  # Límite de YouTube
                'description': description[:5000],
                'tags': tags[:15],  # Máximo 15 tags
                'categoryId': '28',  # Science & Technology
                'defaultLanguage': 'es',
                'defaultAudioLanguage': 'es'
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False,
                'publishAt': None  # Publicar inmediatamente
            },
            'contentDetails': {
                'license': 'youtube'  # Standard YouTube License
            }
        }
        
        # Subir video
        media = MediaFileUpload(
            video_path,
            mimetype='video/mp4',
            resumable=True
        )
        
        request = youtube.videos().insert(
            part='snippet,status,contentDetails',
            body=body,
            media_body=media
        )
        
        # Ejecutar upload con progreso
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"   Progreso: {int(status.progress() * 100)}%")
        
        video_id = response['id']
        print(f"✅ Video subido: https://youtube.com/shorts/{video_id}")
        
        # Subir thumbnail si existe
        if thumbnail_path and os.path.exists(thumbnail_path):
            print("🖼️ Subiendo thumbnail...")
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path, mimetype='image/jpeg')
            ).execute()
            print("✅ Thumbnail subido")
        
        return {
            'video_id': video_id,
            'url': f"https://youtube.com/shorts/{video_id}",
            'title': title,
            'privacy': privacy_status
        }
        
    except Exception as e:
        print(f"❌ Error subiendo video: {e}")
        return None


def get_channel_stats():
    """Obtiene estadísticas del canal."""
    try:
        youtube = get_youtube_service()
        
        # Obtener canal del usuario autenticado
        response = youtube.channels().list(
            part='statistics,snippet',
            mine=True
        ).execute()
        
        if response['items']:
            channel = response['items'][0]
            return {
                'title': channel['snippet']['title'],
                'subscribers': channel['statistics']['subscriberCount'],
                'views': channel['statistics']['viewCount'],
                'videos': channel['statistics']['videoCount']
            }
        
        return None
        
    except Exception as e:
        print(f"❌ Error obteniendo stats: {e}")
        return None


if __name__ == "__main__":
    # Test - requiere credenciales configuradas
    print("Para testear, configura las variables de entorno:")
    print("  YOUTUBE_CLIENT_ID")
    print("  YOUTUBE_CLIENT_SECRET")
    print("  YOUTUBE_REFRESH_TOKEN")
    
    # Si están configuradas, probar:
    if os.environ.get('YOUTUBE_REFRESH_TOKEN'):
        try:
            stats = get_channel_stats()
            if stats:
                print(f"✅ Conectado a canal: {stats['title']}")
                print(f"   Subs: {stats['subscribers']}, Views: {stats['views']}")
        except Exception as e:
            print(f"❌ Error: {e}")
