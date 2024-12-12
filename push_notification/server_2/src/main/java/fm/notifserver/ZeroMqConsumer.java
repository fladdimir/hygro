package fm.notifserver;

import java.nio.charset.StandardCharsets;
import java.time.Duration;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.integration.annotation.ServiceActivator;
import org.springframework.integration.channel.DirectChannel;
import org.springframework.integration.zeromq.inbound.ZeroMqMessageProducer;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageChannel;
import org.springframework.stereotype.Service;
import org.zeromq.SocketType;
import org.zeromq.ZContext;

import fm.notifserver.Data.MeasurementData;
import lombok.RequiredArgsConstructor;

@Configuration
public class ZeroMqConsumer {

    @Bean
    ZContext context() {
        return new ZContext();
    }

    @Bean
    MessageChannel notificationRelevantMeasurements() {
        return new DirectChannel();
    }

    @Bean
    ZeroMqMessageProducer zeroMqMessageProducer(ZContext context, MessageChannel notificationRelevantMeasurements,
            @Value("#{environment.ZMQ_SOCKET_CONNECTION ?: 'tcp://0.0.0.0:5556'}") String socketConnection) {
        ZeroMqMessageProducer messageProducer = new ZeroMqMessageProducer(context, SocketType.SUB);
        messageProducer.setOutputChannel(notificationRelevantMeasurements);
        messageProducer.setTopics("");
        messageProducer.setReceiveRaw(false);
        messageProducer.setConnectUrl(socketConnection);
        messageProducer.setConsumeDelay(Duration.ofMillis(1000));
        return messageProducer;
    }

    @Service
    @RequiredArgsConstructor
    static class ChannelMessageHandler {

        private final NotificationDataHandler handler;

        @ServiceActivator(inputChannel = "notificationRelevantMeasurements")
        void messageHandler(Message<byte[]> message) {

            byte[] bytes = message.getPayload();
            String text = new String(bytes, StandardCharsets.UTF_8);

            MeasurementData data = MeasurementData.fromString(text);

            handler.handleNotificationData(data);
        }

    }

}
