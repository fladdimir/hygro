package fm.notifserver;

import java.util.Set;

import org.springframework.stereotype.Service;

import fm.notifserver.Data.MeasurementData;
import fm.notifserver.PushNotifications.PushNotifcationService;
import fm.notifserver.PushNotifications.PushSubscription;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class NotificationDataHandler {

    private final PushSubscriptionManager subscriptionManager;
    private final PushNotifcationService pushService;

    public void handleNotificationData(MeasurementData data) {

        String payload = data.tsp() + " - " + data.measurement_type().name() + " : " + data.value();

        Set<PushSubscription> subscriptions = subscriptionManager.getSubscriptions();

        System.out.println("publishing '" + payload + "' to " + subscriptions.size() + " subscribers");

        subscriptions.forEach(s -> pushService.pushNotification(s, payload));
    }

}
