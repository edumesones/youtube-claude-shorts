# 🎬 Remotion - YouTube Shorts con Claude Code

Generación profesional de videos usando **Remotion** (React + TypeScript).

## 📁 Estructura

```
remotion/
├── src/
│   ├── index.tsx          # Entry point
│   ├── Root.tsx           # Router de composiciones
│   ├── Video.tsx          # Video principal con 5 escenas
│   └── components/
│       ├── ChatBubble.tsx # Burbujas animadas con spring
│       └── KPICard.tsx    # Tarjetas de métricas
├── remotion.config.ts     # Configuración 1080x1920
└── out/                   # Videos renderizados
```

## 🚀 Cómo usar

### Local (Preview)
```bash
cd remotion
npm install
npm run dev
```
Abre http://localhost:3000 para ver el preview en tiempo real.

### Renderizar video
```bash
npm run build
```
El video se guarda en `out/video.mp4`

### GitHub Actions (Automático)
Cada push a `main` que modifique la carpeta `remotion/` renderiza automáticamente el video.

**Descargar resultado:**
1. Ve a Actions → "Render Remotion Video"
2. Descarga el artifact "remotion-video"

## 🎨 Escenas

| Tiempo | Escena | Descripción |
|--------|--------|-------------|
| 0-3s | Hook | "¿40 HORAS?" con glow effect |
| 3-9s | Chat | Conversación usuario-Claude |
| 9-13s | Análisis | Barra de progreso animada |
| 13-16s | Resultados | KPI cards (+23%, 156, 92%) |
| 16-26s | PDF | Informe scrolleable con gráficos |

## 🛠️ Tecnologías

- **Remotion**: Renderizado de React a video
- **Spring animations**: Movimientos naturales
- **CSS-in-JS**: Estilos dinámicos
- **1080x1920**: Formato vertical YouTube Shorts

## 📝 Personalizar

Edita `src/Video.tsx` para cambiar:
- Textos de las burbujas de chat
- Colores (variable `CLAUDE_ORANGE`)
- Duración de escenas
- Contenido del PDF

## 🐛 Troubleshooting

### Error "Failed to launch browser"
Faltan dependencias de Chrome. En Ubuntu:
```bash
sudo apt-get install libnss3 libatk-bridge2.0-0 libxss1 libgtk-3-0 libgbm-dev
```

### Video muy lento en preview
El preview usa mucha CPU. Es normal, el render final es eficiente.

---

*Generado para Edu Mesones - Marzo 2024*
