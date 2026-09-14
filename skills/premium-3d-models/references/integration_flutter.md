# Embedding a generated model in Flutter

The simplest, most reliable path is the `model_viewer_plus` package — it
wraps Google's `<model-viewer>` web component in a native widget, so you
get camera controls, auto-rotate, AR launch, and correct PBR material
rendering for free, on iOS, Android, and web, from the same `.glb`.

## 1. Add the package and the asset

```yaml
# pubspec.yaml
dependencies:
  model_viewer_plus: ^1.7.0   # check pub.dev for the current version

flutter:
  assets:
    - assets/models/bracket.glb
```

Copy the `.glb` this skill generated into `assets/models/`.

## 2. Show it

```dart
import 'package:model_viewer_plus/model_viewer_plus.dart';

class ModelScreen extends StatelessWidget {
  const ModelScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('3D preview')),
      body: const ModelViewer(
        src: 'assets/models/bracket.glb',
        alt: 'A 4-hole mounting bracket',
        ar: true,                 // tap-to-view-in-your-space on supported devices
        autoRotate: true,
        cameraControls: true,
        backgroundColor: Color(0xFF12141C),
      ),
    );
  }
}
```

That's the whole integration — no manual OpenGL/three.js setup needed.

## Loading from a URL instead of a bundled asset

If the model is hosted (not bundled into the app), use `src:
'https://.../bracket.glb'` instead of the `assets/` path — same widget,
no other changes. Useful when models are generated/updated server-side
rather than shipped with each app release.

## AR on iOS vs. Android

- **Android** (Scene Viewer): works directly from the `.glb` — nothing
  else needed.
- **iOS** (Quick Look AR): Apple's Quick Look wants a `.usdz` file, not
  `.glb`. `model_viewer_plus` exposes an `iosSrc:` parameter for this.
  This pipeline does not generate `.usdz` (no reliable pure-Python
  exporter) — if iOS AR launch specifically is needed, convert the `.glb`
  with Apple's free Reality Converter (Mac app) or the `usdzconvert` CLI
  from Apple's USDZ tools, then pass that file as `iosSrc:`. Without it,
  the model viewer itself (rotate/zoom/pan) still works fine on iOS —
  only the "view in your room" AR launch needs the usdz.

## Performance note

`model_viewer_plus` renders through a WebView, which is fine for a
single model on a detail screen but not for many models in a scroll list
at once — each instance spins up its own WebView. For a list/grid of many
models, render static preview images instead (this skill's
`render_preview.py --mode hero` output) and only load the live 3D viewer
when the user opens one.
