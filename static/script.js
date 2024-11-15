document.addEventListener("DOMContentLoaded", function () {
    var video = document.getElementById('videoPlayer');
    var hls;

    // Función para cargar el stream HLS
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

    // URLs para el stream HLS
    var primaryUrl = 'http://10.232.118.72:5001/static/hls/index.m3u8';
    var secondaryUrl = 'http://192.168.1.172:5001/static/hls/index.m3u8';

    // Carga el stream desde la URL primaria o secundaria
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

    // --- Contador de incidencias ---
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

    // Actualiza el contador al cargar la página
    updateIncidenceCounter();

    // Actualiza el contador cada 10 segundos
    setInterval(updateIncidenceCounter, 10000);

    // --- Configuración dinámica de Chart.js ---
    const isLocalNetwork = location.hostname.startsWith("10.232.118");
    const chartJsUrl = isLocalNetwork
        ? "http://10.232.118.72:5001/static/libs/chart.js"
        : "http://192.168.1.172:5001/static/libs/chart.js";

    // Agregar dinámicamente el script de Chart.js
    const chartJsScript = document.createElement("script");
    chartJsScript.src = chartJsUrl;
    chartJsScript.defer = true;
    document.head.appendChild(chartJsScript);

    chartJsScript.onload = function () {
        console.log("Chart.js cargado correctamente.");
        initializeChart();
    };

    chartJsScript.onerror = function () {
        console.error("Error al cargar Chart.js desde " + chartJsUrl);
    };

    // --- Función para inicializar la gráfica ---
    const weeklyChartCtx = document.getElementById('weeklyChart').getContext('2d');
    let weeklyChart;

    function initializeChart() {
        fetchDailyIncidences();
        setInterval(fetchDailyIncidences, 10000);
    }

    function fetchDailyIncidences() {
        if (typeof Chart === 'undefined') {
            console.error("Chart.js no está definido. Verifica que el archivo se cargó correctamente.");
            return;
        }

        fetch('/get_daily_incidences')
            .then(response => response.json())
            .then(data => {
                const labels = Object.keys(data); // Fechas de los últimos 7 días
                const incidences = Object.values(data); // Conteo de incidencias

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
                                backgroundColor: 'rgba(99, 99, 99, 0.8)', // Barras en gris oscuro
                                borderColor: 'rgba(150, 150, 150, 1)', // Bordes en gris claro
                                borderWidth: 1,
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    display: true,
                                    labels: {
                                        color: '#FFFFFF', // Color de la leyenda
                                    }
                                }
                            },
                            scales: {
                                x: {
                                    ticks: {
                                        color: '#FFFFFF',
                                    },
                                    grid: {
                                        color: 'rgba(255, 255, 255, 0.1)',
                                    }
                                },
                                y: {
                                    ticks: {
                                        color: '#FFFFFF',
                                        stepSize: 1,
                                    },
                                    grid: {
                                        color: 'rgba(255, 255, 255, 0.1)',
                                    },
                                    min: 0,
                                    max: 10,
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
});
