import { useCurrentFrame, useSpring, useVideoConfig } from "remotion";
import React from "react";

interface KPICardProps {
  label: string;
  value: string;
  trend?: "up" | "down" | "neutral";
  delay?: number;
}

export const KPICard: React.FC<KPICardProps> = ({
  label,
  value,
  trend = "neutral",
  delay = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = useSpring({
    frame: frame - delay,
    fps,
    from: 0.8,
    to: 1,
    config: {
      damping: 12,
      stiffness: 100,
    },
  });

  const opacity = useSpring({
    frame: frame - delay,
    fps,
    from: 0,
    to: 1,
    config: {
      damping: 15,
      stiffness: 100,
    },
  });

  const getTrendColor = () => {
    switch (trend) {
      case "up":
        return "#32a852";
      case "down":
        return "#e53935";
      default:
        return "#888888";
    }
  };

  return (
    <div
      style={{
        backgroundColor: "#2a2a2a",
        borderRadius: 16,
        padding: "24px 32px",
        minWidth: 200,
        boxShadow: "0 4px 20px rgba(0,0,0,0.4)",
        transform: `scale(${scale})`,
        opacity,
        border: "1px solid rgba(255,255,255,0.1)",
      }}
    >
      <div
        style={{
          fontSize: 18,
          color: "#888888",
          marginBottom: 8,
          textTransform: "uppercase",
          letterSpacing: 1,
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontSize: 48,
          fontWeight: "bold",
          color: getTrendColor(),
        }}
      >
        {value}
      </div>
    </div>
  );
};