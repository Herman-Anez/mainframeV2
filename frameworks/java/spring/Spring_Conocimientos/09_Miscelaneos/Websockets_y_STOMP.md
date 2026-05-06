# Miscelaneos/Websockets_y_STOMP.md
WebSockets: comunicación full-duplex

El protocolo WebSocket permite un canal de comunicación persistente y bidireccional entre el cliente (navegador) y el servidor, superando las limitaciones de HTTP (petición-respuesta). Es ideal para notificaciones en tiempo real, chats, dashboards en vivo.

Spring proporciona soporte tanto para WebSockets crudos como para la capa de subprotocolo STOMP (Simple Text Oriented Messaging Protocol), que añade encaminamiento de mensajes mediante destinos (similar a tópicos y colas de mensajería).
Habilitar WebSocket en Spring

Dependencia: spring-boot-starter-websocket.

Configuración básica con STOMP:
java

@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        registry.enableSimpleBroker("/topic", "/queue"); // prefijos para destinos del broker
        registry.setApplicationDestinationPrefixes("/app"); // prefijo para mensajes del cliente al servidor
    }

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws")
                .setAllowedOriginPatterns("*")
                .withSockJS(); // habilita fallback SockJS
    }
}

    Broker simple (/topic, /queue): es un broker en memoria que reenvía mensajes a los clientes suscritos.

    /app: prefijo para los destinos de los métodos @MessageMapping (mensajes que llegan del cliente).

    SockJS: emula WebSocket en navegadores antiguos usando long polling.

Controlador de mensajes STOMP

Similar a @Controller MVC pero con anotaciones propias:
java

@Controller
public class ChatController {

    @MessageMapping("/chat.enviar")
    @SendTo("/topic/mensajes")
    public Mensaje enviar(Mensaje mensaje) {
        // se puede persistir aquí
        return mensaje; // se reenvía a todos los suscritos a /topic/mensajes
    }

    @MessageMapping("/chat.privado")
    public void privado(Mensaje msg, Principal principal) {
        // Enviar a un usuario específico (destino /queue/privado-{username})
        simpMessagingTemplate.convertAndSendToUser(msg.getDestinatario(), "/queue/privado", msg);
    }
}

    @MessageMapping("/ruta"): escucha mensajes enviados por clientes a /app/ruta.

    @SendTo: define a qué destino broker se envía el valor de retorno del método (broadcast).

    Principal: disponible si la sesión está autenticada.

Envío de mensajes desde el servidor

Inyectamos SimpMessagingTemplate:
java

@Autowired
private SimpMessagingTemplate messagingTemplate;

public void notificarCambio(Evento evento) {
    messagingTemplate.convertAndSend("/topic/eventos", evento);
}

public void notificarUsuario(String username, Notificacion notif) {
    messagingTemplate.convertAndSendToUser(username, "/queue/notificaciones", notif);
}

convertAndSendToUser envía a un destino único por usuario: internamente se resuelve a /user/{username}/queue/notificaciones. El cliente debe suscribirse a /user/queue/notificaciones.
Autenticación y autorización en STOMP

Spring Security se integra con WebSocket. Se puede interceptar el handshake HTTP para extraer credenciales y luego aplicar seguridad a los destinos:
java

@Configuration
public class WebSocketSecurityConfig implements WebSocketMessageBrokerConfigurer {
    @Override
    public void configureClientInboundChannel(ChannelRegistration registration) {
        registration.interceptors(new ChannelInterceptor() {
            @Override
            public Message<?> preSend(Message<?> message, MessageChannel channel) {
                StompHeaderAccessor accessor = MessageHeaderAccessor.getAccessor(message, StompHeaderAccessor.class);
                if (StompCommand.CONNECT.equals(accessor.getCommand())) {
                    // autenticar vía token en headers
                }
                return message;
            }
        });
    }
}

Y autorización con @PreAuthorize en métodos @MessageMapping.
Broker externo: RabbitMQ o ActiveMQ

Para aplicaciones en cluster, el broker simple no es suficiente porque no replica mensajes entre instancias. Spring permite conectar un broker STOMP externo (RabbitMQ, ActiveMQ) que haga de relay:
java

@Override
public void configureMessageBroker(MessageBrokerRegistry registry) {
    registry.enableStompBrokerRelay("/topic", "/queue")
            .setRelayHost("localhost")
            .setRelayPort(61613)
            .setClientLogin("guest")
            .setClientPasscode("guest");
}

Ahora el broker externo maneja las suscripciones y la distribución, mientras los controladores siguen funcionando igual.
Cliente JavaScript (STOMP.js)
javascript

const socket = new SockJS('/ws');
const stompClient = Stomp.over(socket);
stompClient.connect({}, function(frame) {
    stompClient.subscribe('/topic/mensajes', function(mensaje) {
        // JSON.parse(mensaje.body)
    });
    stompClient.send("/app/chat.enviar", {}, JSON.stringify({texto: "Hola"}));
});

Serialización y mensajes

Spring usa un MessageConverter para convertir entre objetos Java y el cuerpo del mensaje STOMP. Por defecto, MappingJackson2MessageConverter con JSON, configurable.
Consideraciones de escalabilidad y estado

    Los clientes mantienen una sesión con el servidor. En un cluster, el broker externo permite compartir suscripciones.

    El fallback SockJS puede crear múltiples peticiones HTTP; hay que dimensionar el pool de hilos.

    Cuida el envío masivo: para miles de usuarios, el broker externo es obligatorio.

    Las sesiones WebSocket no comparten el HttpSession automáticamente; se puede configurar un HandshakeInterceptor para transferir el usuario autenticado.
