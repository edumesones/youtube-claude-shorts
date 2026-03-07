"""
Script para obtener el refresh token de YouTube (setup inicial).
EJECUTAR LOCALMENTE UNA SOLA VEZ.
"""
import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


def get_refresh_token():
    """
    Obtiene refresh token para YouTube API.
    Este script abre un navegador para autorización.
    """
    print("=" * 60)
    print("🔐 SETUP INICIAL: YouTube OAuth")
    print("=" * 60)
    print()
    print("Este script te ayudará a obtener el refresh token necesario")
    print("para que el bot suba videos automáticamente.")
    print()
    print("⚠️  IMPORTANTE: Necesitas haber creado:")
    print("   1. Canal de YouTube")
    print("   2. Proyecto en Google Cloud Console")
    print("   3. OAuth credentials (Desktop app)")
    print()
    
    # Verificar que existe client_secrets.json
    if not os.path.exists('client_secret.json'):
        print("❌ No se encontró 'client_secret.json'")
        print()
        print("Para obtenerlo:")
        print("1. Ve a https://console.cloud.google.com")
        print("2. Selecciona tu proyecto")
        print("3. APIs & Services → Credentials")
        print("4. Download OAuth client (formato JSON)")
        print("5. Renómbralo a 'client_secret.json' y ponlo aquí")
        return None
    
    print("✅ client_secret.json encontrado")
    print()
    
    try:
        # Crear flujo OAuth
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json',
            SCOPES,
            redirect_uri='urn:ietf:wg:oauth:2.0:oob'  # Para desktop app
        )
        
        # Obtener URL de autorización
        auth_url, _ = flow.authorization_url(prompt='consent')
        
        print("📋 PASOS A SEGUIR:")
        print("1. Se abrirá tu navegador (o copia la URL de abajo)")
        print("2. Inicia sesión con la cuenta de YouTube del canal")
        print("3. Acepta los permisos")
        print("4. Copia el código de verificación")
        print()
        print(f"🔗 URL: {auth_url}")
        print()
        
        # Abrir navegador automáticamente
        import webbrowser
        webbrowser.open(auth_url)
        
        # Pedir código al usuario
        code = input("🔑 Pega el código de autorización aquí: ").strip()
        
        # Intercambiar código por tokens
        flow.fetch_token(code=code)
        
        # Obtener credenciales
        credentials = flow.credentials
        
        print()
        print("=" * 60)
        print("✅ AUTENTICACIÓN EXITOSA")
        print("=" * 60)
        print()
        print("📝 GUARDA ESTOS VALORES EN GITHUB SECRETS:")
        print()
        print(f"YOUTUBE_REFRESH_TOKEN={credentials.refresh_token}")
        print(f"YOUTUBE_CLIENT_ID={credentials.client_id}")
        print(f"YOUTUBE_CLIENT_SECRET={credentials.client_secret}")
        print()
        print("=" * 60)
        print()
        
        # Guardar en archivo para referencia
        with open('youtube_credentials.txt', 'w') as f:
            f.write(f"YOUTUBE_REFRESH_TOKEN={credentials.refresh_token}\n")
            f.write(f"YOUTUBE_CLIENT_ID={credentials.client_id}\n")
            f.write(f"YOUTUBE_CLIENT_SECRET={credentials.client_secret}\n")
        
        print("💾 Credenciales guardadas en 'youtube_credentials.txt'")
        print("   (NO subas este archivo a GitHub)")
        print()
        
        # Test: obtener info del canal
        from googleapiclient.discovery import build
        youtube = build('youtube', 'v3', credentials=credentials)
        
        response = youtube.channels().list(part='snippet', mine=True).execute()
        if response['items']:
            channel = response['items'][0]
            print(f"📺 Canal conectado: {channel['snippet']['title']}")
        
        return {
            'refresh_token': credentials.refresh_token,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret
        }
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


if __name__ == "__main__":
    result = get_refresh_token()
    
    if result:
        print("\n🎉 Setup completado. Ahora configura los secrets en GitHub.")
    else:
        print("\n❌ Setup fallido. Revisa los errores arriba.")
