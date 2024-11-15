document.addEventListener("DOMContentLoaded", function () {
    var video = document.getElementById('videoPlayer');
    var hls;

    // Function to load the stream
    function loadStream(url) {
        if (Hls.isSupported()) {
            hls = new Hls();
            hls.loadSource(url);
            hls.attachMedia(video);
            hls.on(Hls.Events.MANIFEST_PARSED, function () {
                video.play().catch(error => {
                    console.log("Error al reproducir el video:", error);
                });
            });

            hls.on(Hls.Events.ERROR, function (event, data) {
                console.error("Error de HLS:", data);
                if (data.fatal) {
                    switch (data.type) {
                        case Hls.ErrorTypes.NETWORK_ERROR:
                            console.error("Error de red, reintentando...");
                            hls.startLoad();
                            break;
                        case Hls.ErrorTypes.MEDIA_ERROR:
                            console.error("Error de medios, intentando recuperar...");
                            hls.recoverMediaError();
                            break;
                        default:
                            console.error("Error fatal, destruyendo HLS...");
                            hls.destroy();
                            break;
                    }
                }
            });
        } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
            video.src = url;
            video.addEventListener('loadedmetadata', function () {
                video.play().catch(error => {
                    console.log("Error al reproducir el video:", error);
                });
            });
        }
    }

    var primaryUrl = 'http://10.232.118.72:5001/static/hls/index.m3u8';
    var secondaryUrl = 'http://192.168.1.172:5001/static/hls/index.m3u8';

    fetch(primaryUrl, { method: 'HEAD' })
        .then(() => {
            console.log("Cargando la URL primaria:", primaryUrl);
            loadStream(primaryUrl);
        })
        .catch(() => {
            console.log("URL primaria falló, intentando con la URL secundaria:", secondaryUrl);
            loadStream(secondaryUrl);
        });

    video.addEventListener('pause', function () {
        video.play().catch(error => {
            console.log("Error al intentar reanudar la reproducción:", error);
        });
    });

    const counterValue = document.getElementById('counter-value');

    function updateIncidenceCounter() {
        fetch('/get_alarm_count')
            .then(response => response.json())
            .then(data => {
                counterValue.textContent = data.count;
            })
            .catch(error => {
                console.error("Error al actualizar el contador:", error);
            });
    }

    // Update counter on page load
    updateIncidenceCounter();

    // Update counter every 10 seconds
    setInterval(updateIncidenceCounter, 10000);

    // --- Nueva funcionalidad para la gráfica de incidencias diarias ---
    const weeklyChartCtx = document.getElementById('weeklyChart').getContext('2d');
    let weeklyChart;

    function fetchDailyIncidences() {
        fetch('/get_daily_incidences')
            .then(response => response.json())
            .then(data => {
                const labels = Object.keys(data); // Fechas de los últimos 7 días
                const incidences = Object.values(data); // Conteo de incidencias
    
                const neonColors = [
                    'rgba(0, 255, 255, 0.7)', // Cian
                    'rgba(0, 255, 128, 0.7)', // Verde Neón
                    'rgba(255, 255, 0, 0.7)', // Amarillo Neón
                    'rgba(255, 0, 128, 0.7)', // Rosa Neón
                    'rgba(128, 0, 255, 0.7)', // Púrpura Neón
                    'rgba(0, 128, 255, 0.7)', // Azul Neón
                    'rgba(255, 128, 0, 0.7)', // Naranja Neón
                ];
    
                const neonBorderColors = neonColors.map(color => color.replace('0.7', '1')); // Bordes opacos
    
                if (weeklyChart) {
                    // Actualizar gráfica existente
                    weeklyChart.data.labels = labels;
                    weeklyChart.data.datasets[0].data = incidences;
                    weeklyChart.update();
                } else {
                    // Crear gráfica si no existe
                    weeklyChart = new Chart(weeklyChartCtx, {
                        type: 'bar',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Incidencias Diarias',
                                data: incidences,
                                backgroundColor: neonColors,
                                borderColor: neonBorderColors,
                                borderWidth: 2,
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    display: true,
                                    labels: {
                                        color: '#FFFFFF', // Color del texto de la leyenda
                                        font: {
                                            size: 14,
                                        }
                                    }
                                }
                            },
                            scales: {
                                x: {
                                    ticks: {
                                        color: '#FFFFFF', // Color de los ticks en eje X
                                    },
                                    grid: {
                                        color: 'rgba(255, 255, 255, 0.2)', // Líneas de cuadrícula
                                    }
                                },
                                y: {
                                    ticks: {
                                        color: '#FFFFFF', // Color de los ticks en eje Y
                                        stepSize: 1, // Asegura que el incremento sea de 1 unidad
                                        precision: 0, // Evita decimales
                                    },
                                    grid: {
                                        color: 'rgba(255, 255, 255, 0.2)', // Líneas de cuadrícula
                                    },
                                    min: 0, // Valor mínimo del eje Y
                                    max: 10, // Valor máximo del eje Y
                                }
                            },
                            layout: {
                                padding: {
                                    top: 20,
                                    right: 20,
                                    bottom: 20,
                                    left: 20,
                                }
                            }
                        }
                    });
                }
            })
            .catch(error => {
                console.error("Error al obtener las incidencias diarias:", error);
            });
    }
    

    // Llamar a fetchDailyIncidences al cargar la página y actualizar cada 10 segundos
    fetchDailyIncidences();
    setInterval(fetchDailyIncidences, 10000);
});
