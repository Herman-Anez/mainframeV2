# Integración con Slack

El feedback inmediato es crítico en una cultura DevOps. Notificar automáticamente al equipo cuando una suite de pruebas falla permite reducir drásticamente el tiempo de resolución.

## Configuración paso a paso

1.  **Instalación**: Instalar el plugin "Slack Notification" desde la administración de Jenkins.
2.  **Conexión**: Configurar en `Manage Jenkins > Configure System` el espacio de trabajo de Slack y el token de autenticación (almacenado como un *Secret Text credential*).
3.  **Uso en Pipeline**: Se utiliza el comando `slackSend` dentro de los bloques `post`.

### Ejemplo de implementación

```groovy
post {
    success {
        slackSend (
            channel: '#qa-alerts',
            color: 'good',
            message: "✅ Suite de tests pasó: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Ver reporte>)"
        )
    }
    failure {
        slackSend (
            channel: '#qa-alerts',
            color: 'danger',
            message: "❌ Suite de tests FALLÓ: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Ver error>)"
        )
    }
}
```

## Notificaciones avanzadas

*   **Resumen de Resultados**: Es posible extraer el total de pruebas pasadas/fallidas de los archivos JUnit y adjuntarlo al mensaje.
*   **Archivos Adjuntos**: Usar `slackUploadFile` para enviar capturas de pantalla de fallos UI directamente al canal.
*   **Mensajes Condicionales**:
    *   Notificar solo en ramas críticas (`main`, `release`).
    *   Mencionar a responsables (`@canal` o `@usuario`) solo en fallos de regresión completa.
    *   Usar *attachments* para dar un formato más visual y estructurado.

> [!NOTE]
> Si tu equipo utiliza otras herramientas, existen plugins similares para **Microsoft Teams** (Office 365 Connector) o soporte nativo para **Webhooks** genéricos.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Pipelines declarativos](./Pipelines-declarativos.md) | [Home](../../../index.md) | [GitHub Actions](../GitHub-Actions/index.md) |