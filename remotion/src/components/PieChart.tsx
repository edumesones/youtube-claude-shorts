import { useCurrentFrame, useSpring, useVideoConfig } from "remotion";
import React from "react";

interface PieChartProps {
  data: { label: string; value: number; color: string }[];
  delay?: number;
}

export const PieChart: React.FC<PieChartProps> = ({ data, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const total = data.reduce((sum, item) => sum + item.value, 0);
  const radius = 120;
  const centerX = 140;
  const centerY = 140;

  let currentAngle = -Math.PI / 2;

  const scale = useSpring({
    frame: frame - delay,
    fps,
    from: 0,
    to: 1,
    config: {
      damping: 12,
      stiffness: 100,
    },
  });

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 32,
        padding: 24,
        backgroundColor: "#2a2a2a",
        borderRadius: 16,
      }}
    >
      <svg
        width={280}
        height={280}
        style={{
          transform: `scale(${scale})`,
        }}
      >
        {data.map((item, index) => {
          const angle = (item.value / total) * 2 * Math.PI;
          const startAngle = currentAngle;
          const endAngle = currentAngle + angle * scale;
          currentAngle += angle;

          const x1 = centerX + radius * Math.cos(startAngle);
          const y1 = centerY + radius * Math.sin(startAngle);
          const x2 = centerX + radius * Math.cos(endAngle);
          const y2 = centerY + radius * Math.sin(endAngle);

          const largeArc = angle > Math.PI ? 1 : 0;

          const path = [
            `M ${centerX} ${centerY}`,
            `L ${x1} ${y1}`,
            `A ${radius} ${radius} 0 ${largeArc} 1 ${x2} ${y2}`,
            "Z",
          ].join(" ");

          return (
            <path
              key={item.label}
              d={path}
              fill={item.color}
              stroke="#2a2a2a"
              strokeWidth={2}
            />
          );
        })}
        <circle cx={centerX} cy={centerY} r={60} fill="#2a2a2a" />
      </svg>

      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {data.map((item, index) => (
          <div
            key={item.label}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 12,
              opacity: useSpring({
                frame: frame - delay - index * 3,
                fps,
                from: 0,
                to: 1,
                config: { damping: 20, stiffness: 100 },
              }),
            }}
          >
            <div
              style={{
                width: 20,
                height: 20,
                backgroundColor: item.color,
                borderRadius: 4,
              }}
            />
            <div>
              <div style={{ fontSize: 18, color: "#aaaaaa" }}>{item.label}</div>
              <div style={{ fontSize: 24, fontWeight: "bold", color: "#ffffff" }}>
                {Math.round((item.value / total) * 100)}%
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};