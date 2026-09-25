<!-- generated from template.md and entries/ on every merge to main. edit those, not this file. -->

# Mach Ecosystem

Every project written in or for the [Mach](https://github.com/briar-systems/mach) programming language.

Browse it with search, sorting, and project details at [machlang.org/ecosystem](https://machlang.org/ecosystem/). For a hand-picked selection, see [Awesome Mach](https://github.com/briar-systems/awesome-mach).

> This list is created via user submission. If your project is missing, please take a look at [CONTRIBUTING.md](CONTRIBUTING.md)!

## Contents

- [Language](#language)
- [Tooling](#tooling)
- [Editor support](#editor-support)
- [Web](#web)
- [Networking](#networking)
- [Cryptography](#cryptography)
- [Graphics](#graphics)
- [Media and assets](#media-and-assets)
- [GUI](#gui)
- [Games and simulation](#games-and-simulation)
- [Examples](#examples)

## Language

_The compiler, toolchain, and standard library._

- [mach](https://github.com/briar-systems/mach) - The Mach compiler and toolchain: a systems programming language with no hidden behavior.
- [mach-std](https://github.com/briar-systems/mach-std) - The Mach standard library.

## Tooling

_Language servers, grammars, templates, and benchmarks._

- [mach-bench](https://github.com/briar-systems/mach-bench) - Paired Mach and C benchmarks with identical kernels and data, checksum-verified, used to measure Mach codegen.
- [mach-lsp](https://github.com/briar-systems/mach-lsp) - Language server built on the Mach compiler's own frontend.
- [mach-template](https://github.com/briar-systems/mach-template) - Starting point for Mach projects with library layout, tiered CI, tag-driven releases, and branch rules as data.
- [mach-tree-sitter](https://github.com/briar-systems/mach-tree-sitter) - Tree-sitter grammar for Mach.

## Editor support

_Plugins and extensions for editors._

- [mach-vscode](https://github.com/briar-systems/mach-vscode) - Mach support for Visual Studio Code.
- [mach-zed](https://github.com/briar-systems/mach-zed) - Mach support for Zed with syntax highlighting, indentation, and code outline.

## Web

_Servers and frameworks for building on the web._

- [hedge](https://github.com/briar-systems/hedge) - Lightweight production web server written in Mach.
- [laurel](https://github.com/briar-systems/laurel) - Lightweight production web application framework for Mach.

## Networking

_Protocols and transports._

- [mach-acme](https://github.com/briar-systems/mach-acme) - Lightweight ACME client.
- [mach-http](https://github.com/briar-systems/mach-http) - Lightweight HTTP protocol engines.
- [mach-mdns](https://github.com/briar-systems/mach-mdns) - mDNS and DNS-SD (RFC 6762 and 6763) library.
- [mach-mqtt](https://github.com/briar-systems/mach-mqtt) - MQTT 3.1.1 protocol library and broker.
- [mach-quic](https://github.com/briar-systems/mach-quic) - Lightweight QUIC transport.
- [mach-tls](https://github.com/briar-systems/mach-tls) - Lightweight TLS.

## Cryptography

_Cryptographic primitives and protocols._

- [mach-crypto](https://github.com/briar-systems/mach-crypto) - Lightweight cryptographic primitives.

## Graphics

_GPU APIs, windowing, and shaders._

- [mach-gl](https://github.com/briar-systems/mach-gl) - OpenGL 4.6 core bindings generated from the Khronos registry.
- [mach-glfw](https://github.com/briar-systems/mach-glfw) - GLFW 3.4 bindings.
- [mach-shader](https://github.com/briar-systems/mach-shader) - Shader-side math that lowers to GLSL.std.450 on SPIR-V targets.
- [mach-vk](https://github.com/briar-systems/mach-vk) - Vulkan API declarations.

## Media and assets

_Images, fonts, models, and audio._

- [mach-audio](https://github.com/briar-systems/mach-audio) - Audio with a minimal device-layer binding and pure Mach mixing and DSP.
- [mach-font](https://github.com/briar-systems/mach-font) - Pure Mach TrueType parsing and rasterization.
- [mach-gltf](https://github.com/briar-systems/mach-gltf) - Pure Mach glTF 2.0 loader.
- [mach-image](https://github.com/briar-systems/mach-image) - Pure Mach image decoding and encoding.

## GUI

_User interface libraries._

- [blit](https://github.com/briar-systems/blit) - Immediate-mode GUI library.

## Games and simulation

_Engines, physics, and game tooling._

- [boom](https://github.com/briar-systems/boom) - 2D-first, 3D-capable game engine.
- [mach-phys](https://github.com/briar-systems/mach-phys) - Pure Mach 2D and 3D physics.
- [mach-raylib](https://github.com/Angluca/mach-raylib) - Mach bindings for Raylib.

## Examples

_Small projects that show how Mach is written._

- [mach-sieve](https://github.com/briar-systems/mach-sieve) - Sieve of Eratosthenes showing the intended layout of a Mach project and its dependencies.

## Contributing

Adding a project takes one json file. See [CONTRIBUTING.md](CONTRIBUTING.md).
