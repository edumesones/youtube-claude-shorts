import { useSpring, useCurrentFrame, useVideoConfig } from "remotion";
import React from "react";

interface ChatBubbleProps {
  text: string;
  isUser?: boolean;
  delay?: number;
}

const COLORS = {
  user: {
    bg: "#3268c9",
    text: "#ffffff",
  },
  ai: {
    bg: "#32a852",
    text: "#ffffff",
  },
};

export const ChatBubble: React.FC<ChatBubbleProps> = ({
  text,
  isUser = false,
  delay = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const colors = isUser ? COLORS.user : COLORS.ai;

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

  const opacity = useSpring({
    frame: frame - delay,
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
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        padding: "10px 20px",
        opacity,
      }}
    >
      <div
        style={{
          backgroundColor: colors.bg,
          color: colors.text,
          padding: "16px 20px",
          borderRadius: isUser ? "20px 20px 4px 20px" : "20px 20px 20px 4px",
          maxWidth: "80%",
          fontSize: "32px",
          fontWeight: 500,
          lineHeight: 1.4,
          boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
          transform: `scale(${scale})`,
          transformOrigin: isUser ? "bottom right" : "bottom left",
        }}
      >
        {text}
      </div>
    </div>
  );
};