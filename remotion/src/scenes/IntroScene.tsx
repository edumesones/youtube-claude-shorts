import { useCurrentFrame, useSpring, useVideoConfig } from "remotion";
import React from "react";

export const IntroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = useSpring({
    frame: frame - 30, // Empieza después de 1 segundo (30 frames)
    fps,
    from: 0.5,
    to: 1,
    config: {
      damping: 12,
      stiffness: 100,
    },
  });

  const opacity = useSpring({
    frame: frame - 30,
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
        justifyContent: "center",
        backgroundColor: "#1a1a1a",
      }}
    >
      {/* Logo Claude */}
      <div
        style={{
          width: 180,
          height: 180,
          backgroundColor: "#E6643E",
          borderRadius: 40,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          marginBottom: 40,
          transform: `scale(${scale})`,
          boxShadow: "0 8px 32px rgba(230, 100, 62, 0.4)",
        }}
      >
        <svg
          width="100"
          height="100"
          viewBox="0 0 100 100"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M20 30 L50 80 L80 30"
            stroke="white"
            strokeWidth="8"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <circle cx="20" cy="30" r="10" fill="white" />
          <circle cx="80" cy="30" r="10" fill="white" />
        </svg>
      </div>

      {/* Texto Hola */}
      <div
        style={{
          fontSize: 72,
          fontWeight: "bold",
          color: "#ffffff",
          opacity,
          textAlign: "center",
        }}
      >
        ¡Hola, Claude!
      </div>

      <div
        style={{
          fontSize: 32,
          color: "#888888",
          marginTop: 16,
          opacity: useSpring({
            frame: frame - 45,
            fps,
            from: 0,
            to: 1,
            config: { damping: 20, stiffness: 100 },
          }),
        }}
      >
        Tu asistente de análisis
      </div>
    </div>
  );
};