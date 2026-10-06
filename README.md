# santiagovalenzuelalopez-gif.github.io

Portafolio de Santiago Valenzuela López: siete proyectos con su caso de estudio (problema, arquitectura, decisiones, qué se verificó y qué no). Sitio estático en español, tema oscuro, sin dependencias de build.

**Sitio:** https://santiagovalenzuelalopez-gif.github.io

## Cómo está hecho

HTML estático generado con un script de la biblioteca estándar de Python a partir de un único archivo de contenido:

```
tools/content.py   perfil, experiencia, stack y los siete casos de estudio (texto)
tools/build.py     genera index.html, proyectos/*.html, 404.html, sitemap.xml y robots.txt
tools/check.py     comprueba enlaces internos, anclas, metadatos, un único h1 y contenido que no debe publicarse
assets/style.css   tema oscuro (un solo acento), responsive, sin framework
```

```bash
python tools/build.py && python tools/check.py     # regenerar y comprobar
python -m http.server 8000                         # ver en http://localhost:8000
```

Los diagramas son Mermaid (cargado desde jsDelivr) con un tema oscuro propio; si el CDN no responde, se ve el código del diagrama en un bloque legible.

## Decisiones

- **Estático y sin build**: GitHub Pages lo sirve tal cual; nada que mantener ni que se rompa con una actualización.
- **El contenido es dato**: cambiar un texto es editar `content.py` y regenerar; el CI falla si el HTML commiteado no coincide con lo generado.
- **Accesibilidad y SEO básicos**: `lang="es"`, enlace para saltar al contenido, foco visible, `prefers-reduced-motion`, un `h1` por página, metadatos Open Graph, `sitemap.xml` y JSON-LD de persona.
- **Honestidad como criterio de diseño**: cada caso incluye una sección «Límites: lo que no se verificó».

## Licencia

MIT
