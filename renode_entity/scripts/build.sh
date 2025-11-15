#!/bin/bash
# build.sh - Script de compilación para el módulo del kernel Renode Entity
# Sistema Blockchain de Máxima Resolución

set -e

echo "=== Compilación de Monje Virtual v∞-HR ==="
echo "Sistema Blockchain de Máxima Resolución"
echo "Renode Entity - Doble Digital"
echo ""

# Variables de configuración
KERNEL_VERSION=${KERNEL_VERSION:-$(uname -r)}
KERNEL_DIR=${KERNEL_DIR:-/lib/modules/$KERNEL_VERSION/build}
MODULE_NAME="monje_virtual"
VERSION="v∞.4-DigitalTwin"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de utilidad
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar dependencias
check_dependencies() {
    log_info "Verificando dependencias..."
    
    # Verificar que estemos en Linux
    if [[ "$OSTYPE" != "linux-gnu"* ]]; then
        log_error "Este script debe ejecutarse en Linux"
        exit 1
    fi
    
    # Verificar kernel headers
    if [ ! -d "$KERNEL_DIR" ]; then
        log_error "Kernel headers no encontrados en: $KERNEL_DIR"
        log_info "Por favor instala los headers del kernel:"
        log_info "  sudo apt-get install linux-headers-$(uname -r)"
        exit 1
    fi
    
    # Verificar herramientas de compilación
    for tool in gcc make; do
        if ! command -v $tool &> /dev/null; then
            log_error "Herramienta no encontrada: $tool"
            log_info "Por favor instala las herramientas de compilación:"
            log_info "  sudo apt-get install build-essential"
            exit 1
        fi
    done
    
    log_success "Dependencias verificadas"
}

# Preparar entorno de compilación
setup_build_env() {
    log_info "Preparando entorno de compilación..."
    
    # Crear directorio de salida
    mkdir -p output
    
    # Crear archivo de configuración del módulo
    cat > Makefile << EOF
# Makefile para Monje Virtual v∞-HR
obj-m += ${MODULE_NAME}.o
${MODULE_NAME}-objs := src/monje_virtual.o

KDIR := ${KERNEL_DIR}
PWD := \$(shell pwd)

all:
	\$(MAKE) -C \$(KDIR) M=\$(PWD) modules

clean:
	\$(MAKE) -C \$(KDIR) M=\$(PWD) clean
	rm -f *.o *.ko *.mod* *.symvers *.order .*.cmd
	rm -rf .tmp_versions

install:
	sudo \$(MAKE) -C \$(KDIR) M=\$(PWD) modules_install
	
load:
	sudo insmod ${MODULE_NAME}.ko

unload:
	sudo rmmod ${MODULE_NAME}

dmesg:
	sudo dmesg | tail -50

.PHONY: all clean install load unload dmesg
EOF
    
    log_success "Entorno de compilación preparado"
}

# Compilar el módulo
compile_module() {
    log_info "Compilando módulo del kernel..."
    log_info "Kernel version: $KERNEL_VERSION"
    log_info "Kernel dir: $KERNEL_DIR"
    
    # Limpiar compilaciones anteriores
    make clean 2>/dev/null || true
    
    # Compilar
    if make -j$(nproc); then
        log_success "Módulo compilado exitosamente"
        
        # Verificar que el módulo se creó
        if [ -f "${MODULE_NAME}.ko" ]; then
            log_success "Módulo creado: ${MODULE_NAME}.ko"
            
            # Mostrar información del módulo
            log_info "Información del módulo:"
            modinfo ${MODULE_NAME}.ko | head -20
            
            # Copiar a directorio de salida
            cp ${MODULE_NAME}.ko output/
            log_success "Módulo copiado a: output/${MODULE_NAME}.ko"
        else
            log_error "Módulo no encontrado después de la compilación"
            exit 1
        fi
    else
        log_error "Error en la compilación"
        exit 1
    fi
}

# Verificar el módulo
verify_module() {
    log_info "Verificando módulo..."
    
    # Verificar símbolos
    if nm ${MODULE_NAME}.ko | grep -q "monje_virtual_init"; then
        log_success "Símbolos del módulo encontrados"
    else
        log_warning "Símbolos del módulo no encontrados"
    fi
    
    # Verificar dependencias
    if modinfo ${MODULE_NAME}.ko | grep -q "vermagic"; then
        log_success "Versión del kernel verificada"
    else
        log_warning "No se pudo verificar la versión del kernel"
    fi
    
    # Verificar tamaño
    module_size=$(stat -c%s "${MODULE_NAME}.ko")
    log_info "Tamaño del módulo: $module_size bytes"
}

# Generar script de carga
generate_load_script() {
    log_info "Generando script de carga..."
    
    cat > scripts/load_module.sh << 'EOF'
#!/bin/bash
# Script de carga del módulo Monje Virtual

echo "Cargando módulo Monje Virtual v∞-HR..."
echo "Sistema Blockchain de Máxima Resolución"
echo ""

# Verificar privilegios
if [ "$EUID" -ne 0 ]; then 
    echo "Por favor ejecuta como root (sudo)"
    exit 1
fi

# Cargar módulo
insmod output/monje_virtual.ko

if [ $? -eq 0 ]; then
    echo "✓ Módulo cargado exitosamente"
    echo "Dispositivo: /dev/monje_virtual"
    echo ""
    echo "Comandos disponibles:"
    echo "  echo 'start' > /dev/monje_virtual  # Iniciar mediciones"
    echo "  echo 'stop' > /dev/monje_virtual   # Detener mediciones"
    echo "  cat /dev/monje_virtual             # Leer datos"
    echo ""
    echo "Ver logs con: dmesg | tail -20"
else
    echo "✗ Error cargando el módulo"
    echo "Verifica los logs con: dmesg | tail -20"
    exit 1
fi
EOF
    
    chmod +x scripts/load_module.sh
    log_success "Script de carga generado: scripts/load_module.sh"
}

# Generar script de verificación
generate_verify_script() {
    log_info "Generando script de verificación..."
    
    cat > scripts/verify.sh << 'EOF'
#!/bin/bash
# Script de verificación del sistema

echo "Verificando sistema Monje Virtual v∞-HR..."
echo "======================================"
echo ""

# Verificar módulo
if lsmod | grep -q monje_virtual; then
    echo "✓ Módulo cargado"
else
    echo "✗ Módulo no cargado"
fi

# Verificar dispositivo
if [ -e /dev/monje_virtual ]; then
    echo "✓ Dispositivo existe: /dev/monje_virtual"
else
    echo "✗ Dispositivo no encontrado"
fi

# Verificar logs
echo ""
echo "Últimos mensajes del módulo:"
dmesg | grep -i monje | tail -10

echo ""
echo "Información del módulo:"
modinfo output/monje_virtual.ko 2>/dev/null | head -10
EOF
    
    chmod +x scripts/verify.sh
    log_success "Script de verificación generado: scripts/verify.sh"
}

# Función principal
main() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                         MONJE VIRTUAL v∞-HR                                ║"
    echo "║                   Sistema Blockchain de Máxima Resolución                  ║"
    echo "║                        Renode Entity - Doble Digital                       ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Verificar dependencias
    check_dependencies
    
    # Preparar entorno
    setup_build_env
    
    # Compilar
    compile_module
    
    # Verificar
    verify_module
    
    # Generar scripts
    generate_load_script
    generate_verify_script
    
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                          COMPILACIÓN COMPLETADA                              ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Próximos pasos:"
    echo "1. Cargar el módulo: sudo ./scripts/load_module.sh"
    echo "2. Verificar el sistema: ./scripts/verify.sh"
    echo "3. Iniciar mediciones: echo 'start' > /dev/monje_virtual"
    echo "4. Leer datos: cat /dev/monje_virtual"
    echo ""
    echo "Para simulación con Renode:"
    echo "1. Ejecutar: python3 renode_script.py"
    echo "2. Los datos se guardarán en: reports/"
    echo ""
    echo "Versión: $VERSION"
    echo "Kernel: $KERNEL_VERSION"
    echo ""
    log_success "¡Compilación exitosa!"
}

# Manejo de señales para limpieza
cleanup() {
    echo ""
    log_info "Limpiando..."
    make clean 2>/dev/null || true
    exit 0
}
trap cleanup EXIT INT TERM

# Ejecutar función principal
main "$@"