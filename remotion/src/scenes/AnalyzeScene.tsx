import { useCurrentFrame, useSpring, useVideoConfig, interpolate } from "remotion";
import React from "react";
import { ChatBubble } from "../components/ChatBubble";

export const AnalyzeScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Progreso de 0 a 100
  const progress = interpolate(
    frame,
    [30, 90],
    [0, 100],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  const scale = useSpring({
    frame: frame - 30,
    fps,
    from: 0.9,
    to: 1,
    config: {
      damping: 12,
      stiffness: 100,
    },
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "#1a1a1a",
        padding: 40,
      }}
    >
      {/* Respuesta de Claude */}
      <ChatBubble
        text="Perfecto, déjame analizar todos los documentos..."
        isUser={false}
        delay={0}
      />

      {/* Contenedor del progreso */}
      <div
        style={{
          marginTop: 60,
          width: "100%",
          maxWidth: 700,
          transform: `scale(${scale})`,
        }}
      >
        {/* Barra de progreso */}
        <div
          style={{
            height: 24,
            backgroundColor: "#2a2a2a",
            borderRadius: 12,
            overflow: "hidden",
            boxShadow: "inset 0 2px 4px rgba(0,0,0,0.3)",
          }}
        >
          <div
            style={{
              height: "100%",
              width: `${progress}%`,
              background: "linear-gradient(90deg, #E6643E 0%, #ff8a65 100%)",
              borderRadius: 12,
              transition: "none",
              boxShadow: "0 0 20px rgba(230, 100, 62, 0.5)",
            }}
          />
        </div>

        {/* Texto del progreso */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginTop: 16,
            fontSize: 24,
            color: "#888888",
          }}
        >
          <span>Analizando documentos...</span>
          <span style={{ color: "#E6643E", fontWeight: "bold" }}>
            {Math.round(progress)}%
          </span>
        </div>

        {/* Animación de puntos */}
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            gap: 12,
            marginTop: 40,
          }}
        >
          {[0, 1, 2].map((i) => {
            const dotY = useSpring({
              frame: frame - i * 10,
              fps,
              from: 0,
              to: -20,
              config: {
                damping: 5,
                stiffness: 200,
              },
            });

            return (
              <div
                key={i}
                style={{
                  width: 16,
                  height: 16,
                  backgroundColor: "#E6643E",
                  borderRadius: "50%",
                  transform: `translateY(${dotY}px)`,
                  opacity: interpolate(
                    dotY,
                    [-20, -10, 0],
                    [1, 0.5, 1]
                  ),
                }}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
};