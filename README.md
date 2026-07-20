## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
##
## PARA ENTRAR AL DEPLOY ES CON LA SIGUIENTE IP: http://139.177.102.134:8000/
##
## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# M.A.R.V.I.N. // Fan Intel

**M.A.R.V.I.N.** significa **Módulo de Asistencia y Respuesta Virtual para
Información de Negocios**. Es un agente de consulta para una comunidad de fans de
Apex Legends y Titanfall, inspirado en los robots MRVN de ese universo.

El proyecto usa un flujo RAG real con **LangChain + Cohere**: divide varios PDFs
en fragmentos, crea embeddings multilingües, recupera la información más relevante
y genera una respuesta indicando el archivo y la página utilizados.

> Proyecto creado por fans. No está afiliado con Electronic Arts ni Respawn
> Entertainment.

## Capacidades

- Consulta simultánea de varios archivos PDF.
- Recuperación semántica con `CohereEmbeddings`.
- Respuestas con `ChatCohere` y Command A.
- Fuentes por nombre de archivo y número de página.
- Memoria breve de conversación.
- Detección de cambios en la biblioteca durante la ejecución.
- Interfaz responsive estilo terminal sci-fi.

## Arquitectura

```text
Navegador
   │
   ▼
FastAPI ──► LangChain
               │
               ├──► PDFs ──► fragmentos ──► Cohere Embeddings
               │                              │
               │                              ▼
               │                       búsqueda semántica
               │                              │
               └──► ChatCohere ◄── contexto recuperado
```

## Biblioteca de documentos

Los documentos deben guardarse dentro de:

```text
pdfs/
├── Apex Legends.pdf
├── Armas.pdf
├── Respawn Entertainment.pdf
├── Titanfall.pdf
└── Titanfall 2.pdf
```

M.A.R.V.I.N. carga automáticamente todos los archivos `*.pdf` de esa carpeta. Si
se agrega, elimina o modifica un archivo, el índice se reconstruye en la siguiente
consulta. Durante la migración, también puede detectar PDFs ubicados en la raíz
cuando `pdfs/` todavía no existe o está vacía.

## Configuración

1. Copia el archivo de ejemplo:

   ```bash
   cp .env.example .env
   ```

2. Agrega tu API key de Cohere:

   ```dotenv
   COHERE_API_KEY=tu-api-key-aqui
   MODEL_NAME=command-a-03-2025
   EMBEDDING_MODEL=embed-multilingual-v3.0
   PDF_DIR=pdfs
   ```

## Ejecución local

Requiere Python 3.11 o superior.

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
python -m app.main
```

Abre `http://localhost:8000`.

## Ejecución con Docker

```bash
docker compose up --build
```

El directorio local `pdfs/` se monta en modo lectura dentro del contenedor.

## API

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/ask` | Responde una consulta con fuentes |
| `GET` | `/api/documents` | Lista la biblioteca disponible |
| `POST` | `/api/reset` | Limpia la memoria de conversación |
| `GET` | `/api/health` | Informa estado, modelo y cantidad de PDFs |

Ejemplo:

```bash
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"¿Cómo se relacionan Titanfall y Apex Legends?"}'
```

## Pruebas

```bash
python -m unittest -v test_cohere_integration.py
```

Las pruebas usan dobles locales y no envían los PDFs a Cohere.

## Estructura principal

```text
app/
├── api/routes.py
├── core/config.py
├── services/agent.py
├── services/pdf_processor.py
└── main.py
pdfs/
static/
templates/
```


## Ejemplos de Preguntas que puede responder

¿Cuál es la historia general de Apex Legends?
¿Qué información hay sobre las armas del juego?
¿Cómo se relacionan Titanfall y Apex Legends?
¿Qué sabes de Respawn Entertainment?

## Ejemplos de respuestas generadas por el agente.

> 1. RESPUESTA

Apex Legends es un videojuego de los géneros *Battle Royale* y *Hero Shooter* en primera persona, desarrollado por Respawn Entertainment y publicado por Electronic Arts. Es un *spin-off* de la saga Titanfall y se sitúa al final de la cronología de la misma.
La historia general de Apex Legends se desarrolla en un universo de ciencia ficción donde los jugadores asumen el papel de "Leyendas", cada una con habilidades únicas y trasfondos personales. Estas Leyendas compiten en los "Apex Games", un evento de batalla donde equipos de tres se enfrentan para ser los últimos en pie. El juego se lanzó el 4 de febrero de 2019 para Microsoft Windows, PlayStation 4 y Xbox One, y posteriormente llegó a otras plataformas como Nintendo Switch y Steam.
El juego está inspirado en títulos como Halo, Destiny, Tom Clancy's Rainbow Six Siege y Overwatch, y utiliza el motor Source, el mismo que se usó para los juegos de Titanfall. Apex Legends se caracteriza por su enfoque en el trabajo en equipo, las habilidades únicas de las Leyendas y una narrativa en evolución que se expande a través de cinemáticas llamadas *Stories from the Outlands*, las cuales revelan las historias de origen de las Leyendas y otros personajes importantes del universo.
En resumen, Apex Legends combina elementos de combate intenso, estrategia y narrativa para crear una experiencia inmersiva en un mundo futurista y competitivo.

> 2. RESPUESTA

Según el contexto recuperado de la biblioteca, aquí está la información disponible sobre las armas en Apex Legends:

1. Tipos de armas: Se dividen en siete categorías principales:
- AR (Armas de Asalto)
- SMG (Subfusiles)
- LM (Ametralladoras Ligeras)
- Tiradores
- Francotiradores
- Escopetas
- Pistolas

2. Características comunes: Las armas dentro de un mismo tipo comparten características similares, como la velocidad de movimiento al apuntar, los tiempos de manejo y las limitaciones de los accesorios que pueden equipar.

3. Ejemplos de armas:
- Pistolas:
- Wingman: Revólver de alta potencia.
- P2020: Pistola semiautomática (se pueden usar dos a la vez).
- RE-45: Pistola automática.
- Escopetas:
- Peacekeeper: Escopeta con acción de palanca (originalmente podía equipar la mejora Estrangulador, ahora integrada).

4. Armas especiales:
- Armas de caída de suministro: Armas completamente equipadas.
- Armas de paintball modificadas: Personalizadas por Rampart.
- Armas exclusivas para modos de juego: Como el Cuchillo de lanzamiento (Gun Run) o el Heart Stealer (cita nocturna).
- Armas del Día de los Inocentes y Armas de habilidad: Categorías mencionadas, pero sin detalles específicos.

5. Cosméticos y variantes:
- Pieles de armas cuerpo a cuerpo.
- Auras: Hologramas flotantes sobre las leyendas, visibles en situaciones como saltos del transporte o gestos en tercera persona.

6. Estadísticas: Se mencionan comparaciones generales y TTK (tiempo para matar), pero no se proporcionan datos específicos en el contexto disponible.

Si necesitas información más detallada sobre estadísticas, daños o accesorios de armas específicas, sería útil consultar documentos más técnicos o guías de armas dentro de la biblioteca.

> 3. RESPUESTA

Según el contexto recuperado de la biblioteca, la relación entre Titanfall y Apex Legends se establece de la siguiente manera:

1. Universo compartido: Apex Legends es un *spin-off* de la saga Titanfall y se sitúa al final de la cronología de la misma. Esto indica que ambos juegos comparten el mismo universo narrativo.

2. Motor de juego: Apex Legends utiliza el motor Source, el mismo que se empleó en los juegos de Titanfall. Esto sugiere una continuidad técnica y de desarrollo entre ambas franquicias.

3. Inspiración y evolución: Apex Legends se inspira en varios juegos de disparos, incluyendo Titanfall, para refinar su concepto de leyendas y combate. Aunque no se mencionan elementos específicos de Titanfall en Apex Legends, la influencia es evidente en el diseño del juego.

4. Cronología: En la sección de "Cronología de videojuegos", se menciona que Apex Legends sigue a Titanfall: Assault, lo que refuerza la idea de que Apex Legends es una continuación o expansión del universo establecido en Titanfall.

En resumen, Apex Legends y Titanfall están conectados por su universo compartido, el motor de juego y la inspiración narrativa y técnica. Apex Legends se presenta como una evolución o expansión del mundo de Titanfall, aunque con su propia identidad y enfoque en el género *Battle Royale*.


> 4. RESPUESTA

Según el contexto recuperado de la biblioteca, aquí está la información disponible sobre Respawn Entertainment:

1. Fundación y fundadores: Respawn Entertainment fue fundada el 12 de abril de 2010 por Jason West y Vince Zampella, quienes anteriormente trabajaron en Infinity Ward.

2. Sede y forma legal: Es una empresa privada con sede en Sherman Oaks, California, Estados Unidos. Opera como una filial de Electronic Arts.

3. Adquisición por Electronic Arts: En noviembre de 2017, Respawn fue adquirida por Electronic Arts por 151 millones de dólares en efectivo y 164 millones de dólares en capital. La adquisición se completó el 1 de diciembre de 2017.

4. Productos destacados:
- Saga Titanfall: Su primer proyecto, lanzado en 2014, seguido por *Titanfall 2* en 2016.
- Apex Legends: Lanzado en febrero de 2019, es un *spin-off* de Titanfall en el género *Battle Royale*.
- Star Wars Jedi: Fallen Order: Anunciado en el E3 2018.
- Medal of Honor: Above and Beyond.

5. Presidente actual: Vince Zampella continúa como presidente de la compañía.

6. Filiales y empleados: Cuenta con una filial en Vancouver y tiene aproximadamente 140 empleados.

7. Motor de juego: Utiliza el motor Source (el mismo de Titanfall) para juegos como Apex Legends.

8. Decisiones recientes:
- En octubre de 2020, el director de Apex Legends confirmó que no hay desarrollo activo de Titanfall 3.
- Apex Legends surgió como una apuesta por el modelo Free to Play, inspirado en el éxito de Fortnite, aunque EA inicialmente lo consideró arriesgado.

9. Filosofía de desarrollo: Respawn mantuvo el desarrollo de Apex Legends en secreto hasta su lanzamiento, priorizando que los jugadores formaran opiniones basadas en la experiencia directa.

Si necesitas más detalles sobre algún aspecto específico, avísame.


## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
##
## PARA ENTRAR AL DEPLOY ES CON LA SIGUIENTE IP: http://139.177.102.134:8000/
##
## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!