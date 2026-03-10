import { useCurrentFrame, useVideoConfig } from "remotion";
import { Series } from "remotion";
import React from "react";

import { IntroScene } from "./scenes/IntroScene";
import { ListDocsScene } from "./scenes/ListDocsScene";
import { AnalyzeScene } from "./scenes/AnalyzeScene";
import { ResultsScene } from "./scenes/ResultsScene";
import { PDFScrollScene } from "./scenes/PDFScrollScene";

// Duraciones en frames (30 fps)
const SCENES = {
  intro: 90,        // 3 segundos (1s silencio + 2s animación)
  listDocs: 90,     // 3 segundos
  analyze: 90,      // 3 segundos
  results: 90,      // 3 segundos
  pdfScroll: 300,   // 10 segundos
};

// Transición entre escenas
const Transition: React.FC<{ frame: number; duration: number }> = ({
  frame,
  duration,
}) => {
  const opacity = frame < duration ? frame / 10 : 1;

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "#1a1a1a",
        opacity: 1 - opacity,
        pointerEvents: "none",
      }}
    />
  );
};

export const Video: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor: "#1a1a1a",
      }}
    >
      <Series>
        {/* Escena 1: Intro (3s) */}
        <Series.Sequence durationInFrames={SCENES.intro}>
          <IntroScene />
        </Series.Sequence>

        {/* Escena 2: Listar documentos (3s) */}
        <Series.Sequence durationInFrames={SCENES.listDocs}>
          <ListDocsScene />
        </Series.Sequence>

        {/* Escena 3: Analizando (3s) */}
        <Series.Sequence durationInFrames={SCENES.analyze}>
          <AnalyzeScene />
        </Series.Sequence>

        {/* Escena 4: Resultados (3s) */}
        <Series.Sequence durationInFrames={SCENES.results}>
          <ResultsScene />
        </Series.Sequence>

        {/* Escena 5: PDF Scroll (10s) */}
        <Series.Sequence durationInFrames={SCENES.pdfScroll}>
          <PDFScrollScene />
        </Series.Sequence>
      </Series>
    </div>
  );
};