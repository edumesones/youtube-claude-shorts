import { useCurrentFrame, useSpring, useVideoConfig } from "remotion";
import React from "react";
import { ChatBubble } from "../components/ChatBubble";
import { KPICard } from "../components/KPICard";

export const ResultsScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

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
        text="¡Listo! Aquí están los resultados clave:"
        isUser={false}
        delay={0}
      />

      {/* KPI Cards */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 20,
          marginTop: 48,
          width: "100%",
          maxWidth: 600,
        }}
      >
        <div
          style={{
            transform: `scale(${useSpring({
              frame: frame - 30,
              fps,
              from: 0.9,
              to: 1,
              config: { damping: 12, stiffness: 100 },
            })})`,
          }}
        >
          <KPICard label="Ventas" value="+23%" trend="up" delay={30} />
        </div>
        <div
          style={{
            transform: `scale(${useSpring({
              frame: frame - 45,
              fps,
              from: 0.9,
              to: 1,
              config: { damping: 12, stiffness: 100 },
            })})`,
          }}
        >
          <KPICard label="Clientes" value="+156" trend="up" delay={45} />
        </div>
        <div
          style={{
            transform: `scale(${useSpring({
              frame: frame - 60,
              fps,
              from: 0.9,
              to: 1,
              config: { damping: 12, stiffness: 100 },
            })})`,
          }}
        >
          <KPICard label="Ticket Promedio" value="$245" trend="up" delay={60} />
        </div>
      </div>

      {/* Checkmark grande */}
      <div
        style={{
          marginTop: 48,
          width: 100,
          height: 100,
          backgroundColor: "#32a852",
          borderRadius: "50%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          transform: `scale(${useSpring({
            frame: frame - 75,
            fps,
            from: 0,
            to: 1,
            config: { damping: 10, stiffness: 150 },
          })})`,
          boxShadow: "0 8px 32px rgba(50, 168, 82, 0.4)",
        }}
      >
        <svg
          width="60"
          height="60"
          viewBox="0 0 60 60"
          fill="none"
        >
          <path
            d="M10 30 L25 45 L50 15"
            stroke="white"
            strokeWidth="6"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
    </div>
  );
};