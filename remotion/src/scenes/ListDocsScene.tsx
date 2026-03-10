import { useCurrentFrame, useSpring, useVideoConfig } from "remotion";
import React from "react";
import { ChatBubble } from "../components/ChatBubble";

const documents = [
  "ventas_enero.pdf",
  "ventas_febrero.pdf",
  "ventas_marzo.pdf",
  "reporte_clientes.pdf",
  "analisis_marketing.pdf",
];

export const ListDocsScene: React.FC = () => {
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
      {/* Chat Bubble del usuario */}
      <ChatBubble
        text="Tengo 5 informes de ventas que necesito analizar"
        isUser={true}
        delay={0}
      />

      {/* Lista de documentos */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 12,
          marginTop: 32,
          width: "100%",
          maxWidth: 600,
        }}
      >
        {documents.map((doc, index) => {
          const docScale = useSpring({
            frame: frame - 30 - index * 8,
            fps,
            from: 0.8,
            to: 1,
            config: {
              damping: 12,
              stiffness: 100,
            },
          });

          const docOpacity = useSpring({
            frame: frame - 30 - index * 8,
            fps,
            from: 0,
            to: 1,
            config: {
              damping: 20,
              stiffness: 100,
            },
          });

          return (
            <div
              key={doc}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 16,
                backgroundColor: "#2a2a2a",
                padding: "16px 24px",
                borderRadius: 12,
                transform: `scale(${docScale})`,
                opacity: docOpacity,
                border: "1px solid rgba(255,255,255,0.1)",
              }}
            >
              {/* Icono PDF */}
              <div
                style={{
                  width: 48,
                  height: 48,
                  backgroundColor: "#e53935",
                  borderRadius: 8,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: 14,
                  fontWeight: "bold",
                  color: "white",
                }}
              >
                PDF
              </div>
              <span
                style={{
                  fontSize: 24,
                  color: "#ffffff",
                  fontWeight: 500,
                }}
              >
                {doc}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};