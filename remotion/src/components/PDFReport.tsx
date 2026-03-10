import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import React from "react";
import { BarChart } from "./BarChart";
import { PieChart } from "./PieChart";
import { KPICard } from "./KPICard";

export const PDFReport: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Scroll animado durante 10 segundos (300 frames)
  const scrollY = interpolate(
    frame,
    [0, 300],
    [0, -800],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  const barData = [
    { label: "Ene", value: 45, color: "#E6643E" },
    { label: "Feb", value: 62, color: "#E6643E" },
    { label: "Mar", value: 78, color: "#E6643E" },
    { label: "Abr", value: 95, color: "#E6643E" },
  ];

  const pieData = [
    { label: "Online", value: 45, color: "#3268c9" },
    { label: "Tienda", value: 30, color: "#32a852" },
    { label: "Distribuidores", value: 25, color: "#E6643E" },
  ];

  return (
    <div
      style={{
        width: 800,
        height: 1400,
        backgroundColor: "#f5f5f5",
        borderRadius: 16,
        overflow: "hidden",
        boxShadow: "0 8px 32px rgba(0,0,0,0.5)",
      }}
    >
      <div
        style={{
          transform: `translateY(${scrollY}px)`,
          padding: 48,
        }}
      >
        {/* Header */}
        <div
          style={{
            backgroundColor: "#E6643E",
            padding: "32px 48px",
            borderRadius: 16,
            marginBottom: 32,
          }}
        >
          <h1
            style={{
              fontSize: 48,
              color: "#ffffff",
              margin: 0,
              fontWeight: "bold",
            }}
          >
            Reporte de Ventas Q1 2024
          </h1>
          <p
            style={{
              fontSize: 24,
              color: "rgba(255,255,255,0.9)",
              margin: "12px 0 0 0",
            }}
          >
            Generado por Claude Code
          </p>
        </div>

        {/* KPI Cards */}
        <div
          style={{
            display: "flex",
            gap: 24,
            marginBottom: 32,
            flexWrap: "wrap",
          }}
        >
          <div style={{ flex: 1, minWidth: 200 }}>
            <div
              style={{
                backgroundColor: "#ffffff",
                padding: 24,
                borderRadius: 12,
                boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
              }}
            >
              <div style={{ fontSize: 16, color: "#666", marginBottom: 8 }}>
                VENTAS TOTALES
              </div>
              <div
                style={{ fontSize: 36, fontWeight: "bold", color: "#32a852" }}
              >
                +23%
              </div>
            </div>
          </div>
          <div style={{ flex: 1, minWidth: 200 }}>
            <div
              style={{
                backgroundColor: "#ffffff",
                padding: 24,
                borderRadius: 12,
                boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
              }}
            >
              <div style={{ fontSize: 16, color: "#666", marginBottom: 8 }}>
                NUEVOS CLIENTES
              </div>
              <div
                style={{ fontSize: 36, fontWeight: "bold", color: "#3268c9" }}
              >
                +156
              </div>
            </div>
          </div>
          <div style={{ flex: 1, minWidth: 200 }}>
            <div
              style={{
                backgroundColor: "#ffffff",
                padding: 24,
                borderRadius: 12,
                boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
              }}
            >
              <div style={{ fontSize: 16, color: "#666", marginBottom: 8 }}>
                TICKET PROMEDIO
              </div>
              <div
                style={{ fontSize: 36, fontWeight: "bold", color: "#E6643E" }}
              >
                $245
              </div>
            </div>
          </div>
        </div>

        {/* Bar Chart Section */}
        <div
          style={{
            backgroundColor: "#ffffff",
            padding: 32,
            borderRadius: 16,
            marginBottom: 32,
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
          }}
        >
          <h2
            style={{
              fontSize: 28,
              color: "#333",
              marginBottom: 24,
              fontWeight: "bold",
            }}
          >
            Evolución Mensual
          </h2>
          <div style={{ transform: "scale(0.85)", transformOrigin: "left" }}>
            <BarChart data={barData} delay={0} />
          </div>
        </div>

        {/* Pie Chart Section */}
        <div
          style={{
            backgroundColor: "#ffffff",
            padding: 32,
            borderRadius: 16,
            marginBottom: 32,
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
          }}
        >
          <h2
            style={{
              fontSize: 28,
              color: "#333",
              marginBottom: 24,
              fontWeight: "bold",
            }}
          >
            Distribución por Canal
          </h2>
          <div style={{ transform: "scale(0.85)", transformOrigin: "left" }}>
            <PieChart data={pieData} delay={60} />
          </div>
        </div>

        {/* Conclusion Section */}
        <div
          style={{
            backgroundColor: "#32a852",
            padding: 32,
            borderRadius: 16,
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
          }}
        >
          <h2
            style={{
              fontSize: 28,
              color: "#ffffff",
              marginBottom: 16,
              fontWeight: "bold",
            }}
          >
            Conclusión
          </h2>
          <p
            style={{
              fontSize: 20,
              color: "rgba(255,255,255,0.95)",
              lineHeight: 1.6,
            }}
          >
            El análisis de los 5 informes muestra un crecimiento consistente.
            Las ventas online lideran con un 45% del total. Se recomienda
            aumentar inversión en marketing digital para mantener el impulso.
          </p>
        </div>
      </div>
    </div>
  );
};