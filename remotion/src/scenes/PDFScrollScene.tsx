import { useCurrentFrame, useSpring, useVideoConfig } from "remotion";
import React from "react";
import { PDFReport } from "../components/PDFReport";

export const PDFScrollScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = useSpring({
    frame: frame - 15,
    fps,
    from: 0.9,
    to: 1,
    config: {
      damping: 12,
      stiffness: 100,
    },
  });

  const opacity = useSpring({
    frame: frame - 15,
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
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "flex-start",
        backgroundColor: "#1a1a1a",
        padding: "40px 0",
        overflow: "hidden",
      }}
    >
      {/* Título */}
      <div
        style={{
          fontSize: 36,
          fontWeight: "bold",
          color: "#ffffff",
          marginBottom: 24,
          opacity: useSpring({
            frame: frame,
            fps,
            from: 0,
            to: 1,
            config: { damping: 20, stiffness: 100 },
          }),
        }}
      >
        Reporte Completo Generado
      </div>

      {/* PDF con scroll */}
      <div
        style={{
          transform: `scale(${scale})`,
          opacity,
          display: "flex",
          justifyContent: "center",
          alignItems: "flex-start",
        }}
      >
        <PDFReport />
      </div>

      {/* Branding Claude al final */}
      <div
        style={{
          position: "absolute",
          bottom: 40,
          display: "flex",
          alignItems: "center",
          gap: 16,
          opacity: useSpring({
            frame: frame - 250,
            fps,
            from: 0,
            to: 1,
            config: { damping: 20, stiffness: 100 },
          }),
        }}
      >
        <div
          style={{
            width: 48,
            height: 48,
            backgroundColor: "#E6643E",
            borderRadius: 12,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <svg
            width="28"
            height="28"
            viewBox="0 0 100 100"
            fill="none"
          >
            <path
              d="M20 30 L50 80 L80 30"
              stroke="white"
              strokeWidth="8"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>
        <span
          style={{
            fontSize: 24,
            color: "#888888",
            fontWeight: 500,
          }}
        >
          Generado con Claude Code
        </span>
      </div>
    </div>
  );
};