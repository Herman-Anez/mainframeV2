Integración con Slack

El feedback inmediato a todo el equipo cuando una suite falla es crítico. La integración se hace en la sección post del pipeline o mediante una shared library.

Paso a paso con el plugin de Slack:

    Instalar el plugin "Slack Notification" en Jenkins.

    Configurar en "Manage Jenkins > Configure System" el espacio de trabajo de Slack y el token (usando un secret text credential).

    En el Jenkinsfile, se usa slackSend:
    groovy

    post {
        success {
            slackSend (
                channel: '#qa-alerts',
                color: 'good',
                message: "Suite de tests pasó: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Ver>)"
            )
        }
        failure {
            slackSend (
                channel: '#qa-alerts',
                color: 'danger',
                message: "Suite de tests FALLÓ: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Ver>)"
            )
        }
    }

    Se puede personalizar para adjuntar un resumen de los test results (total, fallidos, saltados) extrayendo la información de los archivos junit o mediante slackUploadFile.

Mensajes condicionales avanzados:

    Notificar solo si falla en la rama main o en una rama de release.

    Incluir menciones a responsables (@canal) en casos críticos.

    Usar slackSend con attachments para dar formato estructurado (campos title, pretext, fields).

Alternativas: Microsoft Teams con el plugin Office 365 Connector, o webhooks genéricos.