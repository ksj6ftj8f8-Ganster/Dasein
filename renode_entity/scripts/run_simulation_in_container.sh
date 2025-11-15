#!/bin/bash
set -e

echo "🚀 Iniciando el contenedor de simulación Renode..."

# Establece el directorio de trabajo donde está el renode_script.py
cd /app/renode_entity

# Asegúrate de que el módulo del kernel esté en el lugar correcto
# El Dockerfile ya lo compiló, ahora lo copiamos para que renode_script.py lo encuentre
MODULE_NAME="monje_virtual.ko"
MODULE_PATH="/app/renode_entity/src/${MODULE_NAME}"
DEST_PATH="/lib/modules/$(uname -r)/extra"

# Crea el directorio de destino dentro del contenedor si no existe
sudo mkdir -p ${DEST_PATH}
sudo cp ${MODULE_PATH} ${DEST_PATH}/

echo "✅ Módulo del kernel ${MODULE_NAME} copiado a ${DEST_PATH}"

# Iniciar Renode y la simulación
# Pasamos el path completo al módulo para que renode_script.py lo use
echo "📊 Ejecutando renode_script.py con duración de 60 segundos..."
python3 renode_script.py --duration 60 --output reports --module ${DEST_PATH}/${MODULE_NAME}

echo "🎉 Simulación Renode completada en el contenedor."
