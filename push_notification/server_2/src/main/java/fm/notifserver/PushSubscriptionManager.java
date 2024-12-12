package fm.notifserver;

import static java.util.stream.Collectors.toSet;

import java.util.Set;
import java.util.concurrent.ExecutionException;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.function.ThrowingFunction;

import fm.notifserver.PushNotifications.PushSubscription;
import fm.notifserver.PushNotifications.PushSubscriptionSerializer;
import glide.api.GlideClient;
import glide.api.models.configuration.GlideClientConfiguration;
import glide.api.models.configuration.NodeAddress;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class PushSubscriptionManager {

    private final ValkeyClient vkc;

    public void register(PushSubscription subscription) {
        vkc.addSubscription(PushSubscriptionSerializer.toString(subscription));
    }

    public Set<PushSubscription> getSubscriptions() {
        return vkc.getSubscriptions().stream().map(PushSubscriptionSerializer::fromString).collect(toSet());
    }

    @Service
    static class ValkeyClient {

        private static final String SUBSCRIPTIONS_KEY = "SUBSCRIPTIONS";

        private static final boolean USE_SSL = false;

        private final GlideClientConfiguration config;

        ValkeyClient(@Value("#{environment.VALKEY_HOST ?: 'localhost'}") String host,
                @Value("#{environment.VALKEY_PORT ?: '6379'}") int port) {
            config = GlideClientConfiguration.builder()
                    .address(NodeAddress.builder().host(host).port(port).build())
                    .useTLS(USE_SSL)
                    .build();
        }

        void addSubscription(String value) {
            run(gc -> gc.sadd(SUBSCRIPTIONS_KEY, new String[] { value }));
        }

        Set<String> getSubscriptions() {
            return run(gc -> gc.smembers(SUBSCRIPTIONS_KEY).get());
        }

        private <T> T run(ThrowingFunction<GlideClient, T> task) {
            try (GlideClient client = GlideClient.createClient(config).get()) {
                return task.apply(client);
            } catch (ExecutionException | InterruptedException e) {
                throw new IllegalStateException(e);
            }
        }

    }

}