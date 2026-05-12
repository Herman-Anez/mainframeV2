k6 scripts

k6 (Grafana k6) es una herramienta moderna de código abierto, escrita en Go, con scripting en JavaScript. Su filosofía se alinea perfectamente con los SDET que ya programan JS/TS. Ofrece rendimiento superior con menos recursos que JMeter y está diseñada para CI/CD.

Instalación: (Linux) sudo apt install k6, o usando Docker.
Script básico (script.js):
javascript

import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 }, // rampa a 50 usuarios
    { duration: '3m', target: 50 }, // mantener 50
    { duration: '1m', target: 0 },  // bajar
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% de las peticiones < 500ms
    'http_req_failed': ['rate<0.01'], // tasa de errores < 1%
  },
};

export default function () {
  const res = http.get('https://test-api.example.com/users/1');
  check(res, {
    'status es 200': (r) => r.status === 200,
    'respuesta rápida': (r) => r.timings.duration < 800,
  });
  sleep(1);
}

Conceptos fundamentales desde la óptica del SDET:

    options.stages: Define el perfil de carga fácilmente (ramp-up, sostenido, bajada). No necesita lógica de bucles; k6 maneja el control de concurrencia.

    thresholds: Son las aserciones de rendimiento. Si se superan, k6 termina con código de salida distinto de cero, lo que permite romper el pipeline CI.

    Checks: Validaciones por petición (funcionalidad/rendimiento). Se pueden usar para verificar el cuerpo de la respuesta y que no haya errores de negocio, aunque no son tan potentes como las aserciones de una herramienta de automatización funcional.

    Métricas: k6 recolecta automáticamente métricas como http_req_duration, data_received, vus (usuarios virtuales activos), etc. Además, se pueden definir métricas personalizadas con Trend, Counter, Gauge.

    Ejecución local vs. nube: k6 run script.js para local, o k6 cloud script.js para ejecución en k6 Cloud con más capacidad. También hay integraciones con Grafana Cloud.

Casos de uso SDET:

    Pruebas de regresión de rendimiento: En el pipeline de CI, tras cada merge a main, ejecutar un script k6 con carga baja (prueba de humo de rendimiento) que verifique que los tiempos no se disparan.

    Pruebas de estrés de un endpoint: se ejecuta manualmente o en horarios programados.

    Pruebas continuas en staging: se programa un workflow diario que corre k6 con 500 usuarios y almacena las métricas en InfluxDB para visualizar en Grafana.

Integración en GitHub Actions:
yaml

- name: Run k6 performance test
  uses: grafana/k6-action@v0.3.1
  with:
    filename: perf/load-test.js
    flags: --out json=results.json
- name: Upload results
  uses: actions/upload-artifact@v4
  with:
    name: k6-results
    path: results.json

O directamente con comando k6 run en un runner con k6 instalado.

Comparativa con JMeter: k6 tiene menor curva de aprendizaje para desarrolladores, es más ligero y orientado a infraestructura como código. JMeter sigue siendo más adecuado para protocolos no web (JDBC, FTP) o cuando se requiere un modelo de concurrencia por peticiones por segundo controladas manualmente, aunque k6 también permite constant-arrival-rate en el executor.