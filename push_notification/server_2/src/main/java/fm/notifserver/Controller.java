package fm.notifserver;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import fm.notifserver.PushNotifications.PushSubscription;
import fm.notifserver.PushNotifications.VapidKeyProvider;
import lombok.RequiredArgsConstructor;

@RestController
@CrossOrigin(origins = "*") // tbd: test only
@RequiredArgsConstructor
public class Controller {

    private final VapidKeyProvider vapidKeyProvider;
    private final PushSubscriptionManager subscriptionManager;

    @GetMapping("/vapid-public-key")
    String getVapidPublicKey() {
        return vapidKeyProvider.getVapidPublicKey();
    }

    @PostMapping("/register-subscription")
    void registerSubscription(@RequestBody PushSubscription subscription) {
        System.out.println("received subscription: " + subscription.getEndpoint());
        subscriptionManager.register(subscription);
    }

}
