import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);

export const COMPOSITION_CONFIG = {
  width: 1080,
  height: 1920,
  fps: 30,
  durationInFrames: 780, // 26 segundos (0-3s hook, 3-9s chat, 9-13s analyze, 13-16s results, 16-26s PDF)
};