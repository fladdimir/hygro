package fm.notifserver;

import java.io.IOException;
import java.security.GeneralSecurityException;
import java.security.Security;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.ExecutionException;
import java.util.stream.Stream;

import org.apache.http.HttpResponse;
import org.apache.http.util.EntityUtils;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.jose4j.lang.JoseException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import lombok.Data;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import nl.martijndwars.webpush.Notification;
import nl.martijndwars.webpush.PushService;

@Configuration
public class PushNotifications {

    @Service
    @Getter
    public static class VapidKeyProvider {

        @Value("#{environment.VAPID_PUBLIC_KEY}")
        String vapidPublicKey;
        @Value("#{environment.VAPID_PRIVATE_KEY}")
        private String vapidPrivateKey;
        @Value("#{environment.VAPID_SUBJECT}")
        private String vapidSubject;
    }

    @Data
    public static class PushSubscription {

        private String endpoint;
        private Keys keys;

        @Data
        public static class Keys {
            private String p256dh;
            private String auth;
        }
    }

    public static class PushSubscriptionSerializer {

        private static final ObjectMapper mapper = new ObjectMapper();

        public static String toString(PushSubscription ps) {
            try {
                return mapper.writeValueAsString(ps);
            } catch (JsonProcessingException e) {
                throw new IllegalStateException(e);
            }
        }

        public static PushSubscription fromString(String s) {
            try {
                return mapper.readValue(s, PushSubscription.class);
            } catch (JsonProcessingException e) {
                throw new IllegalStateException(e);
            }
        }
    }

    @Service
    @RequiredArgsConstructor
    public static class PushNotifcationService {

        private final PushService pushService;

        public void pushNotification(PushSubscription subscription, String payload) {
            System.out.println("publishing to subscription: " + subscription.getEndpoint());
            try {
                Notification notification = new Notification(subscription.getEndpoint(),
                        subscription.getKeys().getP256dh(), subscription.getKeys().getAuth(), payload);
                HttpResponse response = pushService.send(notification);
                if (!List.of(200, 201, 204).contains(response.getStatusLine().getStatusCode())) {
                    String responseString = EntityUtils.toString(response.getEntity());
                    throw new IllegalStateException("invalid response: " + response + "\n" + responseString);
                }
            } catch (GeneralSecurityException | JoseException
                    | IOException | ExecutionException | InterruptedException e) {
                throw new IllegalStateException(e);
            }

        }
    }

    @Bean
    PushService pushService(VapidKeyProvider vapidKeyProvider) {
        System.out.println("creating vapid key provider with public key: " + vapidKeyProvider.getVapidPublicKey()
                + " and subject: " + vapidKeyProvider.getVapidSubject());
        if (Stream
                .of(vapidKeyProvider.getVapidPublicKey(), vapidKeyProvider.getVapidPublicKey(),
                        vapidKeyProvider.getVapidSubject())
                .anyMatch(s -> Objects.isNull(s) || s.isBlank())) {
            throw new IllegalArgumentException("vapid keys/subject not set (forgot to set environment variables?)");
        }
        try {
            Security.addProvider(new BouncyCastleProvider());
            return new PushService(vapidKeyProvider.getVapidPublicKey(), vapidKeyProvider.getVapidPrivateKey(),
                    vapidKeyProvider.getVapidSubject());
        } catch (GeneralSecurityException e) {
            throw new IllegalStateException(e);
        }
    }
}
