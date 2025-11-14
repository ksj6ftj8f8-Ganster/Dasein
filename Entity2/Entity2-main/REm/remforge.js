/**
 * REMForge JavaScript - Funcionalidades adicionales para la interfaz web
 * ====================================================================
 * 
 * Este script proporciona funcionalidades avanzadas para:
 * - Manejo de archivos y procesamiento
 * - Visualizaciones interactivas
 * - Exportación de datos
 * - Análisis en tiempo real
 */

class REMForgeInterface {
    constructor() {
        this.currentREMData = null;
        this.charts = {};
        this.colorPalette = {
            primary: '#2C5530',
            secondary: '#D4C5A9',
            accent: '#8B7355',
            visual: '#4A90E2',
            auditory: '#F5A623',
            haptic: '#BD10E0',
            affective: '#E24A8B',
            background: '#F8F6F0'
        };
        
        this.modalityColors = {
            visual: '#4A90E2',
            auditory: '#F5A623',
            haptic: '#BD10E0',
            proprioceptive: '#9013FE',
            affective: '#E24A8B',
            olfactory: '#50E3C2',
            gustatory: '#B8E986',
            digital: '#7ED321'
        };
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.initializeCharts();
        this.loadSampleData();
    }
    
    setupEventListeners() {
        // Manejo de archivos
        document.addEventListener('change', (e) => {
            if (e.target.type === 'file') {
                this.handleFileSelect(e);
            }
        });
        
        // Botones de exportación
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('export-btn')) {
                this.handleExport(e.target.dataset.format);
            }
        });
        
        // Controles de visualización
        document.addEventListener('change', (e) => {
            if (e.target.name === 'chartType') {
                this.updateChartType(e.target.value);
            }
        });
    }
    
    handleFileSelect(event) {
        const files = Array.from(event.target.files);
        this.processFiles(files);
    }
    
    async processFiles(files) {
        if (files.length === 0) return;
        
        this.showLoading(true);
        
        try {
            // Simular procesamiento de archivos
            await this.simulateFileProcessing(files);
            
            // Generar datos REM
            const remData = await this.generateREMData(files);
            
            // Actualizar visualizaciones
            this.updateVisualizations(remData);
            
            // Guardar datos actuales
            this.currentREMData = remData;
            
            this.showNotification('Archivos procesados exitosamente', 'success');
            
        } catch (error) {
            console.error('Error procesando archivos:', error);
            this.showNotification('Error procesando archivos', 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    async simulateFileProcessing(files) {
        // Simular tiempo de procesamiento basado en el tamaño y tipo de archivo
        const totalSize = files.reduce((sum, file) => sum + file.size, 0);
        const baseTime = 2000; // 2 segundos base
        const sizeFactor = Math.min(totalSize / (10 * 1024 * 1024), 3); // Máximo 3 segundos adicionales
        const processingTime = baseTime + (sizeFactor * 1000);
        
        await new Promise(resolve => setTimeout(resolve, processingTime));
    }
    
    async generateREMData(files) {
        const remSequence = [];
        
        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            const fileType = this.getFileType(file);
            
            const rem = await this.generateREMForFile(file, fileType, i);
            remSequence.push(rem);
        }
        
        return {
            sequence: remSequence,
            metadata: {
                totalFiles: files.length,
                processedAt: new Date().toISOString(),
                totalSize: files.reduce((sum, file) => sum + file.size, 0)
            }
        };
    }
    
    getFileType(file) {
        const extension = file.name.split('.').pop().toLowerCase();
        const typeMap = {
            'txt': 'text', 'md': 'text',
            'png': 'image', 'jpg': 'image', 'jpeg': 'image', 'bmp': 'image',
            'wav': 'audio', 'mp3': 'audio',
            'mp4': 'video', 'avi': 'video', 'mov': 'video'
        };
        return typeMap[extension] || 'unknown';
    }
    
    async generateREMForFile(file, fileType, index) {
        // Generar datos REM simulados basados en el tipo de archivo
        const baseREM = {
            rem_id: `rem_${Date.now()}_${index}`,
            timestamp: new Date().toISOString(),
            file_info: {
                name: file.name,
                type: fileType,
                size: file.size
            }
        };
        
        switch (fileType) {
            case 'text':
                return this.generateTextREM(baseREM, file);
            case 'image':
                return this.generateImageREM(baseREM, file);
            case 'audio':
                return this.generateAudioREM(baseREM, file);
            case 'video':
                return this.generateVideoREM(baseREM, file);
            default:
                return this.generateGenericREM(baseREM);
        }
    }
    
    generateTextREM(baseREM, file) {
        const textNarratives = [
            "El texto revela una experiencia introspectiva llena de matices emocionales",
            "Las palabras crean un paisaje mental de profunda contemplación",
            "La narrativa transporta a un estado de conciencia alterado",
            "Cada frase resuena con significados ocultos y qualia lingüísticos"
        ];
        
        return {
            ...baseREM,
            narrative_stream: textNarratives[Math.floor(Math.random() * textNarratives.length)],
            intentional_act: {
                mode: 'reflection',
                directedness: 'linguistic_analysis'
            },
            sensorium: {
                modality_confidence: {
                    visual: 0.2,
                    auditory: 0.1,
                    haptic: 0.05,
                    affective: 0.7,
                    proprioceptive: 0.3,
                    digital: 0.9
                },
                affective_valence: (Math.random() - 0.5) * 1.5,
                spatial_horizon: 'imaginal_space'
            },
            semantic_contamination: {
                lexical_anchors: ['palabra', 'significado', 'introspección', 'conciencia'],
                contamination_strength: 0.8,
                qualia_tokens: [
                    {token: 'profundo', is_sensorial: false, is_affective: true},
                    {token: 'claro', is_sensorial: true, is_affective: false}
                ]
            }
        };
    }
    
    generateImageREM(baseREM, file) {
        const imageDescriptions = [
            "La imagen revela una composición visual de extraordinaria belleza",
            "Los colores y formas crean una experiencia visual inmersiva",
            "La luz capturada evoca emociones profundas y qualia visuales",
            "Cada píxel contribuye a una sinfonía de percepción visual"
        ];
        
        return {
            ...baseREM,
            narrative_stream: imageDescriptions[Math.floor(Math.random() * imageDescriptions.length)],
            intentional_act: {
                mode: 'perception',
                directedness: 'visual_contemplation'
            },
            sensorium: {
                modality_confidence: {
                    visual: 0.95,
                    auditory: 0.1,
                    haptic: 0.2,
                    affective: 0.6,
                    proprioceptive: 0.3,
                    digital: 0.8
                },
                affective_valence: (Math.random() - 0.3) * 1.2,
                spatial_horizon: 'peripersonal_space'
            },
            semantic_contamination: {
                lexical_anchors: ['color', 'forma', 'luz', 'composición'],
                contamination_strength: 0.6,
                qualia_tokens: [
                    {token: 'brillante', is_sensorial: true, is_affective: false},
                    {token: 'armonioso', is_sensorial: false, is_affective: true}
                ]
            }
        };
    }
    
    generateAudioREM(baseREM, file) {
        const audioDescriptions = [
            "El sonido crea una atmósfera auditiva de extraordinaria riqueza",
            "Las ondas sonoras transportan a estados de conciencia profundos",
            "La melodía evoca qualia auditivos puros e inmediatos",
            "Cada nota resuena con significados emocionales y sensoriales"
        ];
        
        return {
            ...baseREM,
            narrative_stream: audioDescriptions[Math.floor(Math.random() * audioDescriptions.length)],
            intentional_act: {
                mode: 'contemplation',
                directedness: 'auditory_presence'
            },
            sensorium: {
                modality_confidence: {
                    visual: 0.1,
                    auditory: 0.95,
                    haptic: 0.3,
                    affective: 0.7,
                    proprioceptive: 0.4,
                    digital: 0.6
                },
                affective_valence: (Math.random() - 0.4) * 1.8,
                spatial_horizon: 'ambiental_space'
            },
            semantic_contamination: {
                lexical_anchors: ['sonido', 'melodía', 'ritmo', 'armonía'],
                contamination_strength: 0.5,
                qualia_tokens: [
                    {token: 'suave', is_sensorial: true, is_affective: false},
                    {token: 'emocionante', is_sensorial: false, is_affective: true}
                ]
            }
        };
    }
    
    generateVideoREM(baseREM, file) {
        const videoDescriptions = [
            "La secuencia visual crea una narrativa temporal inmersiva",
            "El movimiento capturado evoca qualia cinéticos y temporales",
            "La sinfonía de imágenes y sonidos crea una experiencia multimodal",
            "Cada frame contribuye a una percepción temporal fluida"
        ];
        
        return {
            ...baseREM,
            narrative_stream: videoDescriptions[Math.floor(Math.random() * videoDescriptions.length)],
            intentional_act: {
                mode: 'perception',
                directedness: 'temporal_flow'
            },
            sensorium: {
                modality_confidence: {
                    visual: 0.8,
                    auditory: 0.7,
                    haptic: 0.2,
                    affective: 0.6,
                    proprioceptive: 0.5,
                    digital: 0.9
                },
                affective_valence: (Math.random() - 0.5) * 1.6,
                spatial_horizon: 'extrapersonal_space'
            },
            semantic_contamination: {
                lexical_anchors: ['movimiento', 'secuencia', 'tiempo', 'flujo'],
                contamination_strength: 0.7,
                qualia_tokens: [
                    {token: 'dinámico', is_sensorial: true, is_affective: false},
                    {token: 'evocador', is_sensorial: false, is_affective: true}
                ]
            }
        };
    }
    
    generateGenericREM(baseREM) {
        return {
            ...baseREM,
            narrative_stream: "Experiencia digital de qualia inmediatos y puros",
            intentional_act: {
                mode: 'perception',
                directedness: 'digital_presence'
            },
            sensorium: {
                modality_confidence: {
                    visual: 0.4,
                    auditory: 0.3,
                    haptic: 0.2,
                    affective: 0.5,
                    proprioceptive: 0.3,
                    digital: 0.9
                },
                affective_valence: (Math.random() - 0.5) * 2,
                spatial_horizon: 'digital_space'
            },
            semantic_contamination: {
                lexical_anchors: ['digital', 'experiencia', 'qualia', 'presencia'],
                contamination_strength: 0.4,
                qualia_tokens: [
                    {token: 'inmediato', is_sensorial: true, is_affective: false}
                ]
            }
        };
    }
    
    initializeCharts() {
        // Inicializar contenedores de gráficos
        this.chartContainers = {
            modality: document.getElementById('modalityChart'),
            temporal: document.getElementById('temporalChart'),
            affective: document.getElementById('affectiveChart'),
            spatial: document.getElementById('spatialChart')
        };
    }
    
    updateVisualizations(remData) {
        if (!remData || !remData.sequence) return;
        
        this.createModalityChart(remData.sequence);
        this.createTemporalChart(remData.sequence);
        this.createAffectiveChart(remData.sequence);
        this.createSpatialChart(remData.sequence);
        this.updateStatistics(remData);
    }
    
    createModalityChart(sequence) {
        const modalities = ['visual', 'auditory', 'haptic', 'affective', 'proprioceptive', 'olfactory', 'gustatory', 'digital'];
        
        // Calcular promedio de confianzas por modalidad
        const avgConfidences = modalities.map(modality => {
            const confidences = sequence.map(rem => 
                rem.sensorium?.modality_confidence?.[modality] || 0
            );
            return confidences.reduce((sum, val) => sum + val, 0) / confidences.length;
        }).filter(confidence => confidence > 0);
        
        const activeModalities = modalities.filter((_, i) => avgConfidences[i] > 0);
        
        const data = [{
            x: activeModalities,
            y: avgConfidences,
            type: 'bar',
            marker: {
                color: activeModalities.map(mod => this.modalityColors[mod] || this.colorPalette.primary),
                line: { color: 'white', width: 2 }
            },
            text: avgConfidences.map(val => val.toFixed(3)),
            textposition: 'auto'
        }];
        
        const layout = {
            title: 'Distribución de Confianza por Modalidad',
            xaxis: { title: 'Modalidad Sensorial' },
            yaxis: { title: 'Confianza Promedio', range: [0, 1] },
            plot_bgcolor: 'rgba(0,0,0,0)',
            paper_bgcolor: 'rgba(0,0,0,0)',
            font: { color: this.colorPalette.primary },
            margin: { t: 50, b: 80, l: 60, r: 30 }
        };
        
        if (this.chartContainers.modality) {
            Plotly.newPlot(this.chartContainers.modality, data, layout, { responsive: true });
        }
    }
    
    createTemporalChart(sequence) {
        const timestamps = sequence.map((_, i) => i);
        const valences = sequence.map(rem => rem.sensorium?.affective_valence || 0);
        
        const data = [{
            x: timestamps,
            y: valences,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Valencia Afectiva',
            line: { color: this.colorPalette.affective, width: 3 },
            marker: { size: 8, color: this.colorPalette.affective }
        }];
        
        // Añadir línea de cero
        data.push({
            x: [Math.min(...timestamps), Math.max(...timestamps)],
            y: [0, 0],
            type: 'scatter',
            mode: 'lines',
            name: 'Neutral',
            line: { color: this.colorPalette.accent, width: 1, dash: 'dash' },
            showlegend: false
        });
        
        const layout = {
            title: 'Evolución Temporal de la Valencia Afectiva',
            xaxis: { title: 'Secuencia Temporal' },
            yaxis: { title: 'Valencia Afectiva', range: [-1, 1] },
            plot_bgcolor: 'rgba(0,0,0,0)',
            paper_bgcolor: 'rgba(0,0,0,0)',
            font: { color: this.colorPalette.primary },
            margin: { t: 50, b: 60, l: 60, r: 30 }
        };
        
        if (this.chartContainers.temporal) {
            Plotly.newPlot(this.chartContainers.temporal, data, layout, { responsive: true });
        }
    }
    
    createAffectiveChart(sequence) {
        const valences = sequence.map(rem => rem.sensorium?.affective_valence || 0);
        
        const data = [{
            x: valences,
            type: 'histogram',
            nbinsx: 15,
            marker: {
                color: this.colorPalette.affective,
                opacity: 0.7,
                line: { color: 'white', width: 2 }
            },
            name: 'Distribución de Valencia'
        }];
        
        const layout = {
            title: 'Distribución de Valencia Afectiva',
            xaxis: { title: 'Valencia Afectiva', range: [-1, 1] },
            yaxis: { title: 'Frecuencia' },
            plot_bgcolor: 'rgba(0,0,0,0)',
            paper_bgcolor: 'rgba(0,0,0,0)',
            font: { color: this.colorPalette.primary },
            margin: { t: 50, b: 60, l: 60, r: 30 }
        };
        
        if (this.chartContainers.affective) {
            Plotly.newPlot(this.chartContainers.affective, data, layout, { responsive: true });
        }
    }
    
    createSpatialChart(sequence) {
        const spatialHorizons = {};
        
        sequence.forEach(rem => {
            const horizon = rem.sensorium?.spatial_horizon || 'unknown';
            spatialHorizons[horizon] = (spatialHorizons[horizon] || 0) + 1;
        });
        
        const data = [{
            labels: Object.keys(spatialHorizons),
            values: Object.values(spatialHorizons),
            type: 'pie',
            marker: {
                colors: [this.colorPalette.primary, this.colorPalette.accent, 
                        this.colorPalette.secondary, '#E24A8B', '#4A90E2'],
                line: { color: 'white', width: 2 }
            },
            textinfo: 'label+percent',
            textposition: 'auto'
        }];
        
        const layout = {
            title: 'Distribución de Horizontes Espaciales',
            plot_bgcolor: 'rgba(0,0,0,0)',
            paper_bgcolor: 'rgba(0,0,0,0)',
            font: { color: this.colorPalette.primary },
            margin: { t: 50, b: 30, l: 30, r: 30 }
        };
        
        if (this.chartContainers.spatial) {
            Plotly.newPlot(this.chartContainers.spatial, data, layout, { responsive: true });
        }
    }
    
    updateStatistics(remData) {
        // Actualizar estadísticas en la interfaz
        const stats = this.calculateStatistics(remData);
        this.displayStatistics(stats);
    }
    
    calculateStatistics(remData) {
        if (!remData || !remData.sequence) return {};
        
        const sequence = remData.sequence;
        
        return {
            totalExperiences: sequence.length,
            totalQualia: sequence.reduce((sum, rem) => 
                sum + (rem.semantic_contamination?.qualia_tokens?.length || 0), 0),
            totalAnchors: sequence.reduce((sum, rem) => 
                sum + (rem.semantic_contamination?.lexical_anchors?.length || 0), 0),
            avgValence: sequence.reduce((sum, rem) => 
                sum + (rem.sensorium?.affective_valence || 0), 0) / sequence.length,
            duration: remData.metadata?.processedAt ? 
                new Date(remData.metadata.processedAt).getTime() : 0
        };
    }
    
    displayStatistics(stats) {
        // Actualizar elementos de estadísticas en el DOM
        const elements = {
            totalExperiences: document.getElementById('totalExperiences'),
            totalQualia: document.getElementById('totalQualia'),
            totalAnchors: document.getElementById('totalAnchors'),
            avgValence: document.getElementById('avgValence')
        };
        
        if (elements.totalExperiences) {
            elements.totalExperiences.textContent = stats.totalExperiences || 0;
        }
        if (elements.totalQualia) {
            elements.totalQualia.textContent = stats.totalQualia || 0;
        }
        if (elements.totalAnchors) {
            elements.totalAnchors.textContent = stats.totalAnchors || 0;
        }
        if (elements.avgValence) {
            elements.avgValence.textContent = stats.avgValence ? 
                stats.avgValence.toFixed(3) : '0.000';
        }
    }
    
    handleExport(format) {
        if (!this.currentREMData) {
            this.showNotification('No hay datos para exportar', 'warning');
            return;
        }
        
        switch (format) {
            case 'json':
                this.exportToJSON();
                break;
            case 'csv':
                this.exportToCSV();
                break;
            case 'report':
                this.generateReport();
                break;
            default:
                this.showNotification('Formato de exportación no válido', 'error');
        }
    }
    
    exportToJSON() {
        const dataStr = JSON.stringify(this.currentREMData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `remforge_data_${new Date().toISOString().slice(0, 10)}.json`;
        link.click();
        
        this.showNotification('Datos exportados como JSON', 'success');
    }
    
    exportToCSV() {
        const sequence = this.currentREMData.sequence;
        if (!sequence || sequence.length === 0) return;
        
        // Crear encabezados
        const headers = ['rem_id', 'timestamp', 'narrative', 'affective_valence', 
                        'spatial_horizon', 'intentional_mode', 'dominant_modality'];
        
        // Crear filas de datos
        const rows = sequence.map(rem => {
            const modalities = rem.sensorium?.modality_confidence || {};
            const dominantModality = Object.keys(modalities).length > 0 ? 
                Object.keys(modalities).reduce((a, b) => modalities[a] > modalities[b] ? a : b) : 'unknown';
            
            return [
                rem.rem_id || '',
                rem.timestamp || '',
                `"${(rem.narrative_stream || '').substring(0, 100)}"`,
                rem.sensorium?.affective_valence || 0,
                rem.sensorium?.spatial_horizon || '',
                rem.intentional_act?.mode || '',
                dominantModality
            ];
        });
        
        // Combinar encabezados y filas
        const csvContent = [headers, ...rows]
            .map(row => row.join(','))
            .join('\n');
        
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `remforge_data_${new Date().toISOString().slice(0, 10)}.csv`;
        link.click();
        
        this.showNotification('Datos exportados como CSV', 'success');
    }
    
    generateReport() {
        // Generar reporte HTML detallado
        const report = this.createHTMLReport();
        const blob = new Blob([report], { type: 'text/html' });
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `remforge_report_${new Date().toISOString().slice(0, 10)}.html`;
        link.click();
        
        this.showNotification('Reporte generado exitosamente', 'success');
    }
    
    createHTMLReport() {
        const sequence = this.currentREMData.sequence;
        const stats = this.calculateStatistics(this.currentREMData);
        
        return `
        <!DOCTYPE html>
        <html>
        <head>
            <title>REMForge Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .header { background: linear-gradient(135deg, #2C5530, #8B7355); color: white; padding: 30px; border-radius: 10px; }
                .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }
                .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
                .rem-item { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #2C5530; }
                .qualia-badge { display: inline-block; background: #E24A8B; color: white; padding: 2px 6px; border-radius: 10px; font-size: 0.8em; margin: 2px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>REMForge Analysis Report</h1>
                <p>Generated on ${new Date().toLocaleString()}</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>${stats.totalExperiences}</h3>
                    <p>Total Experiences</p>
                </div>
                <div class="stat-card">
                    <h3>${stats.totalQualia}</h3>
                    <p>Qualia Detected</p>
                </div>
                <div class="stat-card">
                    <h3>${stats.totalAnchors}</h3>
                    <p>Semantic Anchors</p>
                </div>
                <div class="stat-card">
                    <h3>${stats.avgValence?.toFixed(3) || 0}</h3>
                    <p>Average Valence</p>
                </div>
            </div>
            
            <h2>Experiences</h2>
            ${sequence.map(rem => `
                <div class="rem-item">
                    <h4>${rem.rem_id}</h4>
                    <p><strong>Narrative:</strong> ${rem.narrative_stream}</p>
                    <p><strong>Intentional Mode:</strong> ${rem.intentional_act?.mode}</p>
                    <p><strong>Affective Valence:</strong> ${rem.sensorium?.affective_valence?.toFixed(3)}</p>
                    <p><strong>Qualia:</strong> 
                        ${rem.semantic_contamination?.qualia_tokens?.map(q => 
                            `<span class="qualia-badge">${q.token}</span>`
                        ).join('') || 'None'}
                    </p>
                </div>
            `).join('')}
        </body>
        </html>
        `;
    }
    
    showLoading(show) {
        const loadingElement = document.getElementById('loadingIndicator');
        if (loadingElement) {
            loadingElement.style.display = show ? 'block' : 'none';
        }
    }
    
    showNotification(message, type = 'info') {
        // Crear notificación temporal
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Estilos para la notificación
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            transition: all 0.3s ease;
            transform: translateX(100%);
        `;
        
        // Colores según el tipo
        const colors = {
            success: '#7ED321',
            error: '#D0021B',
            warning: '#F5A623',
            info: '#4A90E2'
        };
        
        notification.style.backgroundColor = colors[type] || colors.info;
        
        document.body.appendChild(notification);
        
        // Animar entrada
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Remover después de 5 segundos
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 5000);
    }
    
    loadSampleData() {
        // Cargar datos de muestra para demostración
        const sampleData = {
            sequence: [
                {
                    rem_id: "sample_001",
                    timestamp: new Date().toISOString(),
                    narrative_stream: "Experiencia de qualia visual con colores vibrantes",
                    intentional_act: {
                        mode: "perception",
                        directedness: "qualia_visual"
                    },
                    sensorium: {
                        modality_confidence: {
                            visual: 0.9,
                            auditory: 0.2,
                            haptic: 0.1,
                            affective: 0.6,
                            proprioceptive: 0.3,
                            digital: 0.7
                        },
                        affective_valence: 0.7,
                        spatial_horizon: "peripersonal_space"
                    },
                    semantic_contamination: {
                        lexical_anchors: ["color", "vibrante", "visual", "qualia"],
                        contamination_strength: 0.6,
                        qualia_tokens: [
                            {token: "brillante", is_sensorial: true, is_affective: false},
                            {token: "hermoso", is_sensorial: false, is_affective: true}
                        ]
                    }
                }
            ],
            metadata: {
                totalFiles: 1,
                processedAt: new Date().toISOString(),
                totalSize: 1024
            }
        };
        
        // Actualizar visualizaciones con datos de muestra
        setTimeout(() => {
            this.updateVisualizations(sampleData);
        }, 1000);
    }
}

// Inicializar la interfaz cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.remForgeInterface = new REMForgeInterface();
});

// Funciones de utilidad adicionales
const REMForgeUtils = {
    // Formatear tamaño de archivo
    formatFileSize: (bytes) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    // Formatear timestamp
    formatTimestamp: (isoString) => {
        return new Date(isoString).toLocaleString();
    },
    
    // Generar color basado en valencia afectiva
    getValenceColor: (valence) => {
        if (valence > 0.5) return '#7ED321'; // Verde para alta positividad
        if (valence > 0.1) return '#F5A623'; // Naranja para positividad leve
        if (valence > -0.1) return '#8B7355'; // Marrón para neutral
        if (valence > -0.5) return '#BD10E0'; // Púrpura para negatividad leve
        return '#D0021B'; // Rojo para alta negatividad
    },
    
    // Validar datos REM
    validateREMData: (data) => {
        if (!data || typeof data !== 'object') return false;
        if (!Array.isArray(data.sequence)) return false;
        if (data.sequence.length === 0) return false;
        
        // Validar que cada REM tenga los campos mínimos
        return data.sequence.every(rem => 
            rem.rem_id && 
            rem.timestamp && 
            rem.narrative_stream &&
            rem.sensorium &&
            rem.intentional_act
        );
    },
    
    // Calcular estadísticas avanzadas
    calculateAdvancedStats: (sequence) => {
        if (!sequence || sequence.length === 0) return {};
        
        const valences = sequence.map(rem => rem.sensorium?.affective_valence || 0);
        const modalities = {};
        
        // Recopilar datos de modalidades
        sequence.forEach(rem => {
            const confidences = rem.sensorium?.modality_confidence || {};
            Object.entries(confidences).forEach(([modality, confidence]) => {
                if (!modalities[modality]) modalities[modality] = [];
                modalities[modality].push(confidence);
            });
        });
        
        // Calcular estadísticas por modalidad
        const modalityStats = {};
        Object.entries(modalities).forEach(([modality, confidences]) => {
            modalityStats[modality] = {
                mean: confidences.reduce((sum, val) => sum + val, 0) / confidences.length,
                std: Math.sqrt(confidences.reduce((sum, val) => sum + Math.pow(val - modalityStats[modality]?.mean, 2), 0) / confidences.length),
                min: Math.min(...confidences),
                max: Math.max(...confidences)
            };
        });
        
        return {
            valence: {
                mean: valences.reduce((sum, val) => sum + val, 0) / valences.length,
                std: Math.sqrt(valences.reduce((sum, val) => sum + Math.pow(val - valences.reduce((s, v) => s + v, 0) / valences.length, 2), 0) / valences.length),
                min: Math.min(...valences),
                max: Math.max(...valences),
                positive: valences.filter(v => v > 0.1).length,
                negative: valences.filter(v => v < -0.1).length,
                neutral: valences.filter(v => v >= -0.1 && v <= 0.1).length
            },
            modalities: modalityStats
        };
    }
};

// Exportar para uso global
window.REMForgeUtils = REMForgeUtils;