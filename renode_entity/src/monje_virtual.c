// monje_virtual.c - Kernel virtual para análisis de side-channel en Renode
// Sistema de medición de 72 dimensiones con puente de simulación

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/device.h>
#include <linux/uaccess.h>
#include <linux/i2c.h>
#include <linux/time.h>
#include <linux/ktime.h>
#include <linux/hrtimer.h>
#include <linux/gpio.h>
#include <linux/interrupt.h>
#include <linux/cdev.h>
#include <linux/slab.h>
#include <linux/mutex.h>
#include <linux/workqueue.h>
#include <linux/perf_event.h>

#define DEVICE_NAME "monje_virtual"
#define CLASS_NAME "monje"
#define I2C_ADDR_INA219 0x40
#define GPIO_PPS 18
#define SAMPLE_PERIOD_NS 50000  // 50µs
#define MAX_DIMENSIONS 72
#define MAX_SAMPLES 1000

typedef struct {
    u64 timestamp;
    double temperature;
    double energy;
    double latency;
    double dimensions[MAX_DIMENSIONS];
} measurement_t;

typedef struct {
    measurement_t samples[MAX_SAMPLES];
    int sample_count;
    int is_running;
    struct mutex lock;
} measurement_buffer_t;

static measurement_buffer_t *measurement_buffer;
static dev_t dev_num;
static struct cdev c_dev;
static struct class *cl;
static struct device *dev;

// I2C client para INA219
static struct i2c_client *ina219_client;

// GPIO para PPS
static int pps_gpio = GPIO_PPS;
static int pps_irq;

// Timer para muestreo
static struct hrtimer sample_timer;
static ktime_t sample_period;

// Workqueue para procesamiento asíncrono
static struct workqueue_struct *measurement_wq;
static struct work_struct measurement_work;

// Estructura para almacenar el estado de mediciones
static struct {
    u64 last_tsc;
    u64 last_energy;
    u64 instruction_count;
    u64 cache_misses;
    u64 branch_misses;
    u64 cycle_count;
} measurement_state;

// Función para leer TSC (Time Stamp Counter)
static inline u64 rdtsc_virtual(void) {
    u64 tsc;
    /*
     * En Renode, el TSC es virtual y determinista.
     * Usamos la función del kernel para obtener el tiempo de CPU.
     */
    tsc = get_cpu_time();
    return tsc;
}

// Función para leer INA219 (a través de I2C)
static int ina219_read_virtual(u8 reg, u16 *value) {
    int ret;
    u8 data[2];
    
    if (!ina219_client) {
        pr_err("INA219 client not initialized\n");
        return -ENODEV;
    }
    
    ret = i2c_smbus_read_i2c_block_data(ina219_client, reg, 2, data);
    if (ret < 0) {
        pr_err("Failed to read INA219 register 0x%02x: %d\n", reg, ret);
        return ret;
    }
    
    *value = (data[0] << 8) | data[1];
    return 0;
}

// Función para leer temperatura del sensor virtual
static double read_temperature_virtual(void) {
    /*
     * En Renode, la temperatura es simulada basada en la energía.
     * Usamos un modelo simplificado que relaciona energía con temperatura.
     */
    u16 shunt_voltage;
    double energy_joules;
    double temperature_c;
    
    if (ina219_read_virtual(0x01, &shunt_voltage) < 0) {
        return 25.0; // Temperatura por defecto
    }
    
    // Convertir voltaje de shunt a energía (modelo simplificado)
    // 1 LSB = 10µV, asumimos una relación con energía
    energy_joules = (shunt_voltage * 10e-6) * 0.1; // Factor de conversión
    
    // Modelo de temperatura: T = T_ambiente + (Energía * factor térmico)
    temperature_c = 23.0 + (energy_joules * 1000.0);
    
    // Agregar ruido Johnson-Nyquist para realismo
    temperature_c += (get_random_u32() % 1000 - 500) * 0.000001;
    
    return temperature_c;
}

// Función para leer energía del INA219
static double read_energy_virtual(void) {
    u16 shunt_voltage;
    u16 bus_voltage;
    double current_ma;
    double voltage_v;
    double power_mw;
    double energy_uj;
    
    if (ina219_read_virtual(0x01, &shunt_voltage) < 0 ||
        ina219_read_virtual(0x02, &bus_voltage) < 0) {
        return 0.0021; // Energía por defecto (50µs)
    }
    
    // Convertir voltajes
    voltage_v = (bus_voltage >> 3) * 0.004; // LSB = 4mV
    current_ma = shunt_voltage * 0.01; // LSB = 10µV / Rshunt (0.1Ω)
    
    // Calcular potencia
    power_mw = voltage_v * current_ma;
    
    // Convertir a energía en el período de muestreo
    energy_uj = (power_mw * SAMPLE_PERIOD_NS) / 1000000.0;
    
    return energy_uj / 1000000.0; // Convertir a Joules
}

// Función para leer dimensiones adicionales (simuladas)
static void read_dimensions_virtual(double *dimensions) {
    u64 tsc = rdtsc_virtual();
    u64 cycles = tsc - measurement_state.last_tsc;
    
    // Simular 72 dimensiones basadas en contadores de rendimiento
    dimensions[0] = (double)cycles; // Ciclos de CPU
    dimensions[1] = (double)(cycles / 1000); // Instrucciones (estimado)
    dimensions[2] = read_energy_virtual() * 1000000; // Energía en µJ
    dimensions[3] = read_temperature_virtual(); // Temperatura
    
    // Simular métricas de caché y predicción
    dimensions[4] = (double)(cycles % 1000); // L1 Cache Misses (simulado)
    dimensions[5] = (double)((cycles / 10) % 100); // Branch Misses (simulado)
    dimensions[6] = (double)(tsc % 1000); // Latencia (simulado)
    dimensions[7] = (double)(get_random_u32() % 1000); // Ruido térmico
    
    // Llenar el resto con datos correlacionados
    for (int i = 8; i < MAX_DIMENSIONS; i++) {
        dimensions[i] = dimensions[i-8] * (0.9 + (get_random_u32() % 200) * 0.001);
    }
    
    measurement_state.last_tsc = tsc;
}

// Función principal de medición
static void perform_measurement(struct work_struct *work) {
    measurement_t *sample;
    u64 tsc_start, tsc_end;
    double latency_us;
    
    if (!measurement_buffer) {
        return;
    }
    
    mutex_lock(&measurement_buffer->lock);
    
    if (measurement_buffer->sample_count >= MAX_SAMPLES) {
        mutex_unlock(&measurement_buffer->lock);
        return;
    }
    
    sample = &measurement_buffer->samples[measurement_buffer->sample_count];
    
    // Medir latencia
    tsc_start = rdtsc_virtual();
    
    // Leer valores
    sample->timestamp = ktime_get_real_ns();
    sample->temperature = read_temperature_virtual();
    sample->energy = read_energy_virtual();
    read_dimensions_virtual(sample->dimensions);
    
    tsc_end = rdtsc_virtual();
    latency_us = (tsc_end - tsc_start) * 0.001; // Convertir a microsegundos
    sample->latency = latency_us;
    
    measurement_buffer->sample_count++;
    
    mutex_unlock(&measurement_buffer->lock);
    
    pr_info("Measurement %d: T=%.6f°C, E=%.6fJ, L=%.3fµs\n",
            measurement_buffer->sample_count - 1,
            sample->temperature, sample->energy, sample->latency);
}

// Timer callback para muestreo periódico
static enum hrtimer_restart sample_timer_callback(struct hrtimer *timer) {
    if (measurement_buffer && measurement_buffer->is_running) {
        queue_work(measurement_wq, &measurement_work);
    }
    
    hrtimer_forward_now(timer, sample_period);
    return HRTIMER_RESTART;
}

// Handler de interrupción PPS
static irqreturn_t pps_interrupt_handler(int irq, void *dev_id) {
    // Sincronizar con señal de tiempo preciso
    measurement_state.cycle_count = rdtsc_virtual();
    return IRQ_HANDLED;
}

// Funciones del dispositivo
static int monje_open(struct inode *inode, struct file *file) {
    return 0;
}

static int monje_release(struct inode *inode, struct file *file) {
    return 0;
}

static ssize_t monje_read(struct file *file, char __user *buf, size_t count, loff_t *ppos) {
    int ret;
    
    if (!measurement_buffer) {
        return -ENODEV;
    }
    
    mutex_lock(&measurement_buffer->lock);
    
    if (measurement_buffer->sample_count == 0) {
        mutex_unlock(&measurement_buffer->lock);
        return 0;
    }
    
    // Copiar datos al usuario
    ret = copy_to_user(buf, measurement_buffer->samples, 
                       measurement_buffer->sample_count * sizeof(measurement_t));
    
    if (ret) {
        mutex_unlock(&measurement_buffer->lock);
        return -EFAULT;
    }
    
    // Resetear buffer después de leer
    measurement_buffer->sample_count = 0;
    
    mutex_unlock(&measurement_buffer->lock);
    
    return measurement_buffer->sample_count * sizeof(measurement_t);
}

static ssize_t monje_write(struct file *file, const char __user *buf, size_t count, loff_t *ppos) {
    char command[32];
    
    if (count >= sizeof(command)) {
        return -EINVAL;
    }
    
    if (copy_from_user(command, buf, count)) {
        return -EFAULT;
    }
    
    command[count] = '\0';
    
    if (strncmp(command, "start", 5) == 0) {
        if (measurement_buffer) {
            measurement_buffer->is_running = 1;
            hrtimer_start(&sample_timer, sample_period, HRTIMER_MODE_REL);
            pr_info("Monje virtual measurement started\n");
        }
    } else if (strncmp(command, "stop", 4) == 0) {
        if (measurement_buffer) {
            measurement_buffer->is_running = 0;
            hrtimer_cancel(&sample_timer);
            pr_info("Monje virtual measurement stopped\n");
        }
    }
    
    return count;
}

static const struct file_operations monje_fops = {
    .owner = THIS_MODULE,
    .open = monje_open,
    .release = monje_release,
    .read = monje_read,
    .write = monje_write,
};

// Función de inicialización de I2C
static int ina219_probe(struct i2c_client *client, const struct i2c_device_id *id) {
    u16 config;
    int ret;
    
    ina219_client = client;
    
    // Configurar INA219
    config = (0x2000 | 0x0800 | 0x0080 | 0x0018); // Configuración estándar
    ret = i2c_smbus_write_word_data(client, 0x00, config);
    if (ret < 0) {
        pr_err("Failed to configure INA219\n");
        return ret;
    }
    
    // Calibrar (para modo de alta precisión)
    ret = i2c_smbus_write_word_data(client, 0x05, 0x1000);
    if (ret < 0) {
        pr_err("Failed to calibrate INA219\n");
        return ret;
    }
    
    pr_info("INA219 virtual sensor initialized\n");
    return 0;
}

static const struct i2c_device_id ina219_id[] = {
    { "ina219", 0 },
    { }
};
MODULE_DEVICE_TABLE(i2c, ina219_id);

static struct i2c_driver ina219_driver = {
    .driver = {
        .name = "ina219",
    },
    .probe = ina219_probe,
    .id_table = ina219_id,
};

// Función de inicialización del módulo
static int __init monje_virtual_init(void) {
    int ret;
    
    pr_info("Monje Virtual v∞-HR - Sistema de medición de 72 dimensiones\n");
    
    // Asignar número de dispositivo
    ret = alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME);
    if (ret < 0) {
        pr_err("Failed to allocate device number\n");
        return ret;
    }
    
    // Inicializar cdev
    cdev_init(&c_dev, &monje_fops);
    c_dev.owner = THIS_MODULE;
    
    ret = cdev_add(&c_dev, dev_num, 1);
    if (ret < 0) {
        pr_err("Failed to add cdev\n");
        unregister_chrdev_region(dev_num, 1);
        return ret;
    }
    
    // Crear clase de dispositivo
    cl = class_create(THIS_MODULE, CLASS_NAME);
    if (IS_ERR(cl)) {
        pr_err("Failed to create class\n");
        cdev_del(&c_dev);
        unregister_chrdev_region(dev_num, 1);
        return PTR_ERR(cl);
    }
    
    // Crear dispositivo
    dev = device_create(cl, NULL, dev_num, NULL, DEVICE_NAME);
    if (IS_ERR(dev)) {
        pr_err("Failed to create device\n");
        class_destroy(cl);
        cdev_del(&c_dev);
        unregister_chrdev_region(dev_num, 1);
        return PTR_ERR(dev);
    }
    
    // Inicializar buffer de mediciones
    measurement_buffer = kzalloc(sizeof(measurement_buffer_t), GFP_KERNEL);
    if (!measurement_buffer) {
        pr_err("Failed to allocate measurement buffer\n");
        device_destroy(cl, dev_num);
        class_destroy(cl);
        cdev_del(&c_dev);
        unregister_chrdev_region(dev_num, 1);
        return -ENOMEM;
    }
    
    mutex_init(&measurement_buffer->lock);
    
    // Inicializar timer
    hrtimer_init(&sample_timer, CLOCK_MONOTONIC, HRTIMER_MODE_REL);
    sample_timer.function = sample_timer_callback;
    sample_period = ktime_set(0, SAMPLE_PERIOD_NS);
    
    // Inicializar workqueue
    measurement_wq = alloc_workqueue("measurement_wq", WQ_UNBOUND, 1);
    if (!measurement_wq) {
        pr_err("Failed to create workqueue\n");
        kfree(measurement_buffer);
        device_destroy(cl, dev_num);
        class_destroy(cl);
        cdev_del(&c_dev);
        unregister_chrdev_region(dev_num, 1);
        return -ENOMEM;
    }
    
    INIT_WORK(&measurement_work, perform_measurement);
    
    // Solicitar GPIO para PPS
    ret = gpio_request(pps_gpio, "pps_gpio");
    if (ret) {
        pr_err("Failed to request GPIO %d\n", pps_gpio);
        destroy_workqueue(measurement_wq);
        kfree(measurement_buffer);
        device_destroy(cl, dev_num);
        class_destroy(cl);
        cdev_del(&c_dev);
        unregister_chrdev_region(dev_num, 1);
        return ret;
    }
    
    ret = gpio_direction_input(pps_gpio);
    if (ret) {
        pr_err("Failed to set GPIO direction\n");
        gpio_free(pps_gpio);
        destroy_workqueue(measurement_wq);
        kfree(measurement_buffer);
        device_destroy(cl, dev_num);
        class_destroy(cl);
        cdev_del(&c_dev);
        unregister_chrdev_region(dev_num, 1);
        return ret;
    }
    
    // Configurar interrupción PPS
    pps_irq = gpio_to_irq(pps_gpio);
    ret = request_irq(pps_irq, pps_interrupt_handler, IRQF_TRIGGER_RISING, "pps_irq", NULL);
    if (ret) {
        pr_err("Failed to request IRQ\n");
        gpio_free(pps_gpio);
        destroy_workqueue(measurement_wq);
        kfree(measurement_buffer);
        device_destroy(cl, dev_num);
        class_destroy(cl);
        cdev_del(&c_dev);
        unregister_chrdev_region(dev_num, 1);
        return ret;
    }
    
    // Registrar driver I2C
    ret = i2c_add_driver(&ina219_driver);
    if (ret) {
        pr_err("Failed to register I2C driver\n");
        free_irq(pps_irq, NULL);
        gpio_free(pps_gpio);
        destroy_workqueue(measurement_wq);
        kfree(measurement_buffer);
        device_destroy(cl, dev_num);
        class_destroy(cl);
        cdev_del(&c_dev);
        unregister_chrdev_region(dev_num, 1);
        return ret;
    }
    
    // Inicializar estado de mediciones
    memset(&measurement_state, 0, sizeof(measurement_state));
    measurement_state.last_tsc = rdtsc_virtual();
    
    pr_info("Monje Virtual module loaded successfully\n");
    pr_info("Device: /dev/%s (major=%d, minor=%d)\n", DEVICE_NAME, MAJOR(dev_num), MINOR(dev_num));
    pr_info("Sampling period: %d ns\n", SAMPLE_PERIOD_NS);
    pr_info("Max samples: %d\n", MAX_SAMPLES);
    pr_info("Dimensions: %d\n", MAX_DIMENSIONS);
    
    return 0;
}

// Función de limpieza del módulo
static void __exit monje_virtual_exit(void) {
    pr_info("Removing Monje Virtual module\n");
    
    // Detener mediciones
    if (measurement_buffer) {
        measurement_buffer->is_running = 0;
        hrtimer_cancel(&sample_timer);
    }
    
    // Limpiar workqueue
    if (measurement_wq) {
        destroy_workqueue(measurement_wq);
    }
    
    // Liberar recursos
    i2c_del_driver(&ina219_driver);
    
    if (pps_irq >= 0) {
        free_irq(pps_irq, NULL);
    }
    
    if (pps_gpio >= 0) {
        gpio_free(pps_gpio);
    }
    
    // Destruir dispositivo
    device_destroy(cl, dev_num);
    class_destroy(cl);
    cdev_del(&c_dev);
    unregister_chrdev_region(dev_num, 1);
    
    // Liberar buffer
    if (measurement_buffer) {
        kfree(measurement_buffer);
    }
    
    pr_info("Monje Virtual module unloaded\n");
}

module_init(monje_virtual_init);
module_exit(monje_virtual_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("LÍMITE ABSOLUTO - Sistema Blockchain de Máxima Resolución");
MODULE_DESCRIPTION("Monje Virtual v∞-HR - Sistema de medición de 72 dimensiones para Renode");
MODULE_VERSION("v∞.4-DigitalTwin");