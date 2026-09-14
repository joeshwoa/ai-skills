# Embedding a generated model on the web / in React

Two levels, pick based on how much control is actually needed.

## Level 1 — `<model-viewer>` (zero JS framework needed, works in plain
HTML or inside React/Vue/whatever)

Google's `<model-viewer>` web component. This is the right default —
camera controls, auto-rotate, AR launch, correct PBR rendering, lazy
loading, all built in, and it's a genuine web component so it drops
straight into React JSX without a wrapper library.

```html
<script type="module"
  src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js">
</script>

<model-viewer
  src="bracket.glb"
  alt="A 4-hole mounting bracket"
  camera-controls
  auto-rotate
  ar
  shadow-intensity="1"
  style="width: 100%; height: 480px; background: #12141C;">
</model-viewer>
```

In React (the element just works as JSX — no package needed for basic
use, though `@google/model-viewer` on npm gives you TypeScript types if
the project wants them):

```jsx
import '@google/model-viewer';

function ModelPreview() {
  return (
    <model-viewer
      src="/models/bracket.glb"
      alt="A 4-hole mounting bracket"
      camera-controls
      auto-rotate
      style={{ width: '100%', height: 480, background: '#12141C' }}
    />
  );
}
```

## Level 2 — react-three-fiber (when the app needs real control: custom
lighting/postprocessing, interaction with the model's geometry, mixing
it into a larger three.js scene)

```bash
npm install three @react-three/fiber @react-three/drei
```

```jsx
import { Canvas } from '@react-three/fiber';
import { useGLTF, OrbitControls, Environment } from '@react-three/drei';

function Model() {
  const { scene } = useGLTF('/models/bracket.glb');
  return <primitive object={scene} />;
}

export default function Viewer() {
  return (
    <Canvas camera={{ position: [3, 2, 3], fov: 45 }}>
      <Environment preset="studio" />
      <Model />
      <OrbitControls />
    </Canvas>
  );
}
```

`useGLTF` reads the same PBR materials this skill assigned, so
metallic/roughness/color all come through without extra setup. Use this
level only when the app genuinely needs custom lighting or scene
composition — `<model-viewer>` covers "show this model nicely" with far
less code and no bundler/build-step dependency.

## Performance

- A `.glb` under a few MB loads instantly on a normal connection; if
  `validate_model.py --platform web_realtime` flagged a poly-count
  warning, consider `mesh.simplify_quadric_decimation()` (trimesh) before
  the final export, or ask this skill to lower primitive segment counts
  (fewer `sections` on cylinders/cones/torus/revolves) — that's usually
  where excess triangles come from.
- Both approaches above lazy-load the model file itself; nothing renders
  until the `.glb` is fetched, so a loading placeholder (a static
  `render_preview.py --mode hero` PNG as the poster/background) reads
  better than a blank box while it loads.
