import { Composition } from "remotion";
import { Video } from "./Video";
import { COMPOSITION_CONFIG } from "../remotion.config";

export const Root: React.FC = () => {
  return (
    <Composition
      id="Video"
      component={Video}
      durationInFrames={COMPOSITION_CONFIG.durationInFrames}
      fps={COMPOSITION_CONFIG.fps}
      width={COMPOSITION_CONFIG.width}
      height={COMPOSITION_CONFIG.height}
    />
  );
};