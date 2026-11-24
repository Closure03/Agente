# Fotos de modelos (opcional)

La app muestra, para cada modelo, en este orden: **foto local → URL registrada → ilustración SVG**.

## Poner una foto local
1. Guarde la imagen en esta carpeta con el **id del modelo** como nombre: `ktm_390_duke.jpg`, `yamaha_nmax_155.png`, `honda_pcx.webp`...
   (extensiones aceptadas: jpg, jpeg, png, webp). Los ids están en la pestaña **Catálogo** y en `src/catalogo_modelos.py`.
2. Reinicie la app (o pulse "Rerun"). No hay que tocar código.

## Registrar una URL con su crédito
En `src/catalogo_modelos.py`:
```python
IMAGENES_URL["ktm_390_duke"] = "https://.../390-duke.jpg"
FUENTES_IMAGEN["ktm_390_duke"] = "Foto: KTM (sala de prensa)"
```

## Derechos de las imágenes
Las fotos de revistas y portales de motos (por ejemplo Motor, MotoGP.com, etc.) tienen derechos de autor: no las copie sin permiso.
Opciones seguras: salas de prensa / *press kits* de cada fabricante (suelen permitir uso editorial), imágenes con licencia libre
(Wikimedia Commons, citando autor y licencia) o fotos propias. Cite siempre la fuente en `FUENTES_IMAGEN`.
