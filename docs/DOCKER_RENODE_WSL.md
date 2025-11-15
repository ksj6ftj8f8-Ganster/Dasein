# 🐳 Implementación de Renode Entity con Docker en WSL2

Este documento detalla los pasos para configurar y ejecutar el sistema de simulación Renode Entity dentro de un contenedor Docker, utilizando WSL2 (Windows Subsystem for Linux 2) y Docker Desktop en Windows. Esto permite un entorno de desarrollo consistente y aislado.

---

## 📋 Tabla de Contenidos
1. [Prerrequisitos](#prerrequisitos)
2. [Configuración del Entorno WSL2](#configuración-del-entorno-wsl2)
3. [Archivos Clave Añadidos/Modificados](#archivos-clave-añadidosmodificados)
4. [Construcción y Ejecución del Contenedor Renode](#construcción-y-ejecución-del-contenedor-renode)
5. [Verificación de la Simulación](#verificación-de-la-simulación)
6. [Recolección de Resultados](#recolección-de-resultados)
7. [Troubleshooting](#troubleshooting)

---

## 🚀 1. Prerrequisitos

Para seguir esta guía, necesitarás tener instalado lo siguiente en tu máquina Windows:

*   **Windows 10/11 (versión 2004 o superior):** Con WSL2 habilitado.
    *   [Instalar WSL](https://docs.microsoft.com/es-es/windows/wsl/install)
*   **Una distribución de Linux en WSL2:** Preferiblemente Ubuntu 22.04 LTS (o superior).
    *   Puedes instalarla desde la Microsoft Store.
*   **Docker Desktop para Windows:** Configurado para usar el backend de WSL2.
    *   [Instalar Docker Desktop](https://docs.docker.com/desktop/install/windows-install/)
    *   Asegúrate de que el WSL2 backend esté habilitado en la configuración de Docker Desktop (`Settings` > `WSL Integration`).
*   **Git:** Para clonar el repositorio.

---

## ⚙️ 2. Configuración del Entorno WSL2

1.  **Abre tu terminal WSL2:**
    Abre `Ubuntu` desde el menú de inicio de Windows o ejecuta `wsl` en PowerShell/CMD.

2.  **Clona el repositorio Dasein:**
    ```bash
    git clone https://github.com/ksj6ftj8f8-Ganster/Dasein.git
    cd Dasein
    ```

3.  **Actualiza permisos del script de ejecución:**
    ```bash
    chmod +x renode_entity/scripts/run_simulation_in_container.sh
    ```

---

## 📂 3. Archivos Clave Añadidos/Modificados

Los siguientes archivos han sido creados o modificados en el repositorio para permitir la contenerización de Renode:

*   **`Dockerfile.renode`**: Un nuevo `Dockerfile` para construir la imagen de Docker que incluye Renode, Python, herramientas de compilación y las cabeceras del kernel. Este `Dockerfile` también pre-compila el módulo `monje_virtual.ko`.
*   **`renode_entity/scripts/run_simulation_in_container.sh`**: Un nuevo script que se ejecuta dentro del contenedor de Renode. Este script se encarga de copiar el módulo del kernel compilado al lugar correcto dentro del contenedor y luego ejecutar `renode_script.py` para iniciar la simulación.
*   **`docker-compose.yml`**: Se ha modificado para incluir el servicio `renode-simulator`, que utiliza el `Dockerfile.renode` y monta los volúmenes necesarios para la persistencia de datos.

---

## 🐳 4. Construcción y Ejecución del Contenedor Renode

Dentro de tu terminal WSL2 y en el directorio raíz del proyecto `Dasein`:

1.  **Construye la imagen de Docker para Renode:**
    ```bash
    docker build -f Dockerfile.renode -t dasein-renode-simulator .
    ```
    *   Este paso puede tardar varios minutos, ya que descarga la imagen base, instala Renode y compila el módulo del kernel.

2.  **Ejecuta el stack de Docker Compose:**
    ```bash
    docker-compose up --build -d renode-simulator # Solo el servicio de Renode
    # O para ejecutar todo el ecosistema (LightRAG, Neo4j, etc. si están configurados):
    # docker-compose up --build -d
    ```
    *   El servicio `renode-simulator` se iniciará en segundo plano (`-d`).
    *   El script `run_simulation_in_container.sh` se ejecutará automáticamente dentro del contenedor, copiando el módulo del kernel y lanzando la simulación `renode_script.py`.

---

## ✅ 5. Verificación de la Simulación

Para ver los logs de la simulación de Renode en tiempo real:

```bash
docker logs -f renode_simulation_container
```

Deberías ver una salida similar a esta (los timestamps variarán):

```
renode_simulation_container | 🚀 Iniciando el contenedor de simulación Renode...
renode_simulation_container | ✅ Módulo del kernel monje_virtual.ko copiado a /lib/modules/5.15.0-89-generic/extra
renode_simulation_container | 📊 Ejecutando renode_script.py con duración de 60 segundos...
renode_simulation_container | 2025-11-15 08:00:05,123 - INFO - Renode encontrado: (versión de Renode)
renode_simulation_container | 2025-11-15 08:00:05,500 - INFO - Iniciando simulación Renode...
renode_simulation_container | ... (logs detallados de Renode y el kernel simulado) ...
renode_simulation_container | 2025-11-15 08:01:05,000 - INFO - Datos recopilados en: /app/renode_entity/reports/measurements_XXXXX.bin
renode_simulation_container | 🎉 Simulación Renode completada en el contenedor.
```

---

## 📁 6. Recolección de Resultados

Los archivos de salida de la simulación se guardarán en el directorio `renode_entity/reports/` en tu sistema de archivos local (gracias al volumen montado en `docker-compose.yml`).

Para listarlos:

```bash
ls -lh renode_entity/reports/
```

Deberías ver archivos como `measurements_XXXXX.bin`, `analysis_results_XXXXX.json`, `report_XXXXX.json`, etc. Puedes inspeccionar su contenido directamente en tu sistema de archivos.

---

## ⚠️ 7. Troubleshooting

*   **`docker: command not found` en WSL2:** Asegúrate de que Docker Desktop esté corriendo y que la integración con tu distribución de WSL2 esté habilitada en `Settings` > `WSL Integration`.
*   **Errores de compilación del módulo del kernel:** Verifica que `linux-headers-$(uname -r)` se haya instalado correctamente en el `Dockerfile.renode`. El `uname -r` debe coincidir con la versión del kernel de Ubuntu que está corriendo *dentro del contenedor Docker durante la construcción*.
*   **Simulación de Renode no se inicia:**
    *   Revisa los logs de Docker (`docker logs renode_simulation_container`) para ver si hay errores específicos de Renode o del `renode_script.py`.
    *   Asegúrate de que el script `run_simulation_in_container.sh` tenga permisos de ejecución (`chmod +x`).
    *   Si Renode o el módulo del kernel requieren acceso privilegiado al hardware, descomenta las líneas `privileged: true` y `devices:` en `docker-compose.yml` (esto es a menudo necesario para KVM o acceso directo a dispositivos, aunque no siempre es estrictamente requerido para una simulación básica).
*   **Archivos de salida no aparecen:** Asegúrate de que el volumen `- ./renode_entity/reports:/app/renode_entity/reports` esté configurado correctamente en `docker-compose.yml` y que los archivos se estén escribiendo en la ruta correcta dentro del contenedor (`/app/renode_entity/reports`).

---

¡Con estos pasos, deberías poder ejecutar el sistema Renode Entity en tu entorno Docker/WSL2 sin problemas! ¡Buena suerte! 🚀
