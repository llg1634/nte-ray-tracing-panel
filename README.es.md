# NTE Ray Tracing Panel — Panel de activación de ray tracing para Neverness To Everness con un solo clic

Palabras clave de búsqueda: NTE cómo activar ray tracing, cómo activar ray tracing en NTE, Neverness To Everness cómo activar ray tracing, Neverness To Everness no aparece opción ray tracing, NTE no hay opción ray tracing, opción ray tracing NTE no se muestra, NTE arreglo ray tracing, NTE herramienta ray tracing, NTE desbloqueo ray tracing un clic, NTE instalación OptiScaler un clic, NTE configuración OptiScaler, NTE instalador winmm.dll, Ananta cómo activar ray tracing, Ananta no aparece opción ray tracing.

`NTE Ray Tracing Panel / 异环光追一键部署面板` es una herramienta WebUI local diseñada para jugadores que buscan cómo activar el ray tracing en Neverness To Everness o por qué no aparece la opción de ray tracing. Prepara automáticamente OptiScaler, instala el proxy local `winmm.dll` y `OptiScaler.ini`, convierte el proceso verificado de GPU spoof en un flujo automatizado con selección de GPU objetivo, respaldo y restauración.

English README: [README.en.md](README.en.md)
中文 README: [README.md](README.md)

URL local:

```text
http://127.0.0.1:22642
```

No es un servicio en línea. La página web solo muestra la interfaz y envía operaciones; el backend Python / exe escucha en `127.0.0.1:22642`, descarga OptiScaler, escribe archivos, respalda y restaura. Cerrar la pestaña del navegador no detiene el backend. Usa el botón "Salir" en el panel o termina `NTERayTracingPanel.exe` desde el Administrador de tareas.

## Palabras clave de búsqueda / Search Keywords

异环怎么开光追，异环光追怎么开，异环全景光追怎么开，异环光线追踪怎么开，异环没有光追选项，异环光追选项不显示，异环光追打不开，异环光追开不了，异环光追灰色，异环 RTX 5060 怎么开光追，异环 RTX 4060 怎么开光追，异环 5060 没有光追，异环 4060 没有光追，异环光追一键开启，异环光追一键安装，异环光追一键部署，异环开光追工具，异环光追工具，异环光追补丁，异环 OptiScaler 一键安装，异环 winmm.dll 一键安装，异环不改注册表光追。

NTE how to enable ray tracing, how to enable ray tracing in NTE, Neverness To Everness how to enable ray tracing, Neverness To Everness no ray tracing option, NTE no ray tracing option, NTE ray tracing option missing, NTE ray tracing not showing, NTE ray tracing fix, NTE ray tracing tool, NTE one-click ray tracing unlock, NTE one-click OptiScaler install, NTE OptiScaler setup, NTE winmm.dll installer, Ananta how to enable ray tracing, Ananta no ray tracing option, Ananta ray tracing unlock.

## Enfoque del proyecto

Este proyecto no es un "gestor de mods genérico", sino un flujo reutilizable para el caso concreto de desbloquear el ray tracing en Neverness To Everness:

- La versión de prueba actual de NTE oculta las opciones de ray tracing mediante una lista blanca de modelos de GPU.
- Se ha verificado en la máquina actual: al hacer GPU spoof a un modelo de la lista blanca mediante OptiScaler DXGI/Streamline, la opción de ray tracing aparece en el juego.
- Modificar directamente el registro de la tarjeta gráfica del sistema afecta a toda la máquina y no es adecuado para equipos de desarrollo principales.
- Esta herramienta escribe por defecto solo archivos proxy locales dentro del directorio `Win64` del juego y proporciona respaldo y restauración con manifest.

## Qué soluciona

Algunas GPUs RTX serie 50/40/30 soportan ray tracing físicamente, pero la versión de prueba de NTE oculta las opciones de "Ray Tracing / Iluminación global" según una lista blanca de modelos. Cambiar manualmente el registro de la GPU en Windows afecta a todo el sistema, lo cual no es adecuado para equipos de desarrollo o uso diario.

Esta herramienta usa por defecto el GPU spoof DXGI/Streamline de OptiScaler para hacer que `HTGame.exe` vea el nombre de GPU del perfil objetivo seleccionado, desbloqueando así las opciones de ray tracing en el juego. La WebUI ofrece tres perfiles: configuración original, `NVIDIA GeForce RTX 4090` y `NVIDIA GeForce RTX 5080 Laptop GPU`. Este método ha sido verificado en la máquina actual: tras la instalación, la opción de ray tracing aparece en el juego.

## Navegación de documentación

Lectura recomendada para nuevos usuarios:

1. [Guía rápida](docs/01-快速使用.md)
2. [Principio y ruta de prueba y error](docs/02-原理与试错路径.md)
3. [Respaldo, restauración y alcance de modificaciones](docs/03-备份恢复与修改范围.md)
4. [Guía de publicación](docs/04-发布指南.md)
5. [Preguntas frecuentes](docs/05-常见问题.md)

## Límites de seguridad

- No se usa ProcMon, Sysmon, monitoreo de drivers ni herramientas de captura a nivel kernel.
- Por defecto no se modifica el registro de GPU en `HKLM\SYSTEM\CurrentControlSet\Enum\PCI`.
- Por defecto solo se gestionan estos archivos dentro del directorio del juego:
  - `winmm.dll`
  - `OptiScaler.ini`
  - `OptiScaler.log`
  - `OptiScaler\`
  - Respaldo de compatibilidad con esquemas antiguos: `dlsstweaks.ini`, `dlsstweaks.log`
- Cada instalación crea `_nte_rt_backups\<timestamp>\manifest.json`.
- La restauración sigue estrictamente el manifest para evitar eliminar archivos no creados por esta herramienta.

## Uso

1. Ejecuta `run.bat`, o haz doble clic en el ejecutable `NTERayTracingPanel.exe`.
2. Cuando se abra la página, selecciona el directorio raíz de instalación de NTE, o directamente `Client\WindowsNoEditor\HT\Binaries\Win64`.
3. Haz clic en "Descargar/Preparar OptiScaler".
4. Selecciona el perfil de GPU objetivo: configuración original, RTX 4090 o RTX 5080M.
5. Confirma que el juego y el launcher están cerrados.
6. Haz clic en "Respaldar e instalar desbloqueo de ray tracing".
7. Inicia el juego y verifica las opciones de ray tracing en los ajustes gráficos.

## Ejecución y salida

Esta herramienta tiene dos capas:

- Frontend WebUI: la página en el navegador, solo muestra el estado y envía operaciones.
- Backend: `NTERayTracingPanel.exe` o `python app.py`, escucha en el puerto, selecciona carpetas, escribe archivos, respalda y restaura.

Por lo tanto, cerrar la pestaña del navegador no detiene el backend y el puerto `22642` seguirá ocupado. Para salir, haz clic en "Salir" en la parte inferior de la WebUI. Si ya cerraste la página, puedes volver a abrir:

```text
http://127.0.0.1:22642
```

Y luego haz clic en "Salir"; o termina `NTERayTracingPanel.exe` desde el Administrador de tareas.

## Restauración

En la tarjeta "Respaldo y restauración" de la página, selecciona una copia de seguridad reciente y haz clic en restaurar.

También puedes restaurar desde línea de comandos:

```powershell
python app.py --no-browser
```

Luego restaura la copia de seguridad deseada desde la WebUI.

## Principio

El GPU spoof de OptiScaler puede modificar la descripción de GPU, VendorId, DeviceId e información de VRAM que el proceso del juego lee a través de DXGI/Streamline. Esta herramienta genera la configuración según la selección en la WebUI. Tres perfiles de GPU objetivo:

- Configuración original: lee el nombre y DeviceId de la GPU NVIDIA actual, ideal para volver a la identificación nativa.
- RTX 4090: `SpoofedGPUName=NVIDIA GeForce RTX 4090`, `SpoofedDeviceId=0x2684`.
- RTX 5080M: `SpoofedGPUName=NVIDIA GeForce RTX 5080 Laptop GPU`, `SpoofedDeviceId=0x2C59`.

Todos los perfiles mantienen estos límites por defecto:

- `TargetProcessName=HTGame.exe`
- `SpoofedVendorId=0x10de`
- `Dxgi=true`
- `StreamlineSpoofing=true`
- `Registry=false`
- `User32=false`

Esto difiere del cambio de nombre global en el registro: modificar el registro afecta a toda la máquina, mientras que el DXGI spoof solo surte efecto cuando la DLL proxy local es cargada por `HTGame.exe`.

## Historial de versiones

Consulta `CHANGELOG.md`.

## Proyectos principales y agradecimientos

- [OptiScaler](https://github.com/optiscaler/OptiScaler): núcleo del GPU spoof usado por este proyecto. El panel prepara `OptiScaler.dll` desde el Release oficial de GitHub de OptiScaler y lo instala como proxy local `winmm.dll` dentro del directorio `Win64` de NTE.
- [DLSSTweaks](https://github.com/emoose/DLSSTweaks): proyecto relacionado de inyección/envoltura gráfica. Este proyecto no implementa el flujo de escala de renderizado DLSS de DLSSTweaks; solo reconoce posibles archivos heredados `dlsstweaks.ini` y `dlsstweaks.log` durante el respaldo y restauración para no sobrescribir experimentos anteriores.

Este proyecto no es OptiScaler, no es un fork de DLSSTweaks y no es una herramienta oficial de NVIDIA; es únicamente un panel de instalación, respaldo, restauración y explicación específico para NTE construido alrededor del flujo verificado de OptiScaler.
