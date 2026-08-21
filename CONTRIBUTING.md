# Cómo cargar papers

## Regla que sostiene todo

Los datos viven **solo** en `src/content/papers/*.yml` y `src/data/taxonomy.yml`.

## Los tres estados

Un paper nunca se bloquea esperando clasificación completa.

| status | Qué exige | Para qué sirve |
|---|---|---|
| `captured` | nada, solo metadata automática | no perder el link |
| `triaged` | `area`, `level`, `type` | ya aparece en el índice |
| `read` | además `tldr`, `topics`, `capability` | ya sirve como recap |

Podés dejar un paper en `triaged` durante meses. Lo que no puede tener fricción es el momento de agregarlo.

## Flujo Automatizado (Recomendado)

La forma más fácil de agregar un paper es a través de un Issue en GitHub. 

1. Ve a la pestaña de **Issues** y selecciona "Add a Paper".
2. Pega el enlace al paper y el **BibTeX**.
3. Selecciona el área a la que pertenece.
4. Al enviar el Issue, un GitHub Action (bot) leerá el BibTeX, extraerá toda la información y creará un **Pull Request** de forma automática con tu paper.

## Flujo Local

Si prefieres hacerlo de forma local, el repositorio ahora es un sitio web en Astro.

```bash
# 1. Instalar dependencias
npm install

# 2. Correr el entorno de desarrollo
npm run dev

# 3. Crear el paper a mano (copia un .yml existente a src/content/papers)
# o usa el viejo script add.py si quieres bajarlo de arXiv:
python scripts/add.py 2210.03629
```

Todos los datos se validan automáticamente con **Zod** durante el `npm run dev` y `npm run build`. Si escribes un área que no existe, el compilador fallará asegurando la integridad de la taxonomía.

## Cuándo tocar la taxonomía

Agregar un topic nuevo a `taxonomy.yml` es barato y esperable. Agregar un **area** nueva es una decisión estructural.

## Qué NO va acá

`ecosystem/` (frameworks, repos de GitHub) y `benchmarks/` son colecciones aparte, con su propio schema.

