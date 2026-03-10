import { useCurrentFrame, useSpring, useVideoConfig } from "remotion";
import React from "react";

interface BarChartProps {
  data: { label: string; value: number; color: string }[];
  delay?: number;
}

export const BarChart: React.FC<BarChartProps> = ({ data, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const maxValue = Math.max(...data.map((d) => d.value));

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 16,
        padding: 24,
        backgroundColor: "#2a2a2a",
        borderRadius: 16,
        width: "100%",
      }}
    >
      {data.map((item, index) => {
        const barDelay = delay + index * 5;
        const progress = useSpring({
          frame: frame - barDelay,
          fps,
          from: 0,
          to: item.value / maxValue,
          config: {
            damping: 15,
            stiffness: 80,
          },
        });

        const opacity = useSpring({
          frame: frame - barDelay,
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
            key={item.label}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 16,
              opacity,
            }}
          >
            <div
              style={{
                width: 100,
                fontSize: 18,
                color: "#aaaaaa",
                textAlign: "right",
              }}
            >
              {item.label}
            </div>
            <div
              style={{
                flex: 1,
                height: 36,
                backgroundColor: "#1a1a1a",
                borderRadius: 8,
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  height: "100%",
                  width: `${progress * 100}%`,
                  backgroundColor: item.color,
                  borderRadius: 8,
                  transition: "none",
                }}
              />
            </div>
            <div
              style={{
                width: 60,
                fontSize: 20,
                fontWeight: "bold",
                color: "#ffffff",
              }}
            >
              {Math.round(item.value * progress)}
            </div>
          </div>
        );
      })}
    </div>
  );
};