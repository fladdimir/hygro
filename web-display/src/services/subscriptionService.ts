// tbd: check for feature-availability, existing subscriptions, unsubscribe, etc
export async function subscribe() {
  const permissionCheckResult = await Notification.requestPermission();
  if (permissionCheckResult !== "granted") {
    return;
  }

  const registration = await navigator.serviceWorker.register(
    "service-worker.js"
  );

  let subscription = await registration.pushManager.getSubscription();
  if (!subscription) {
    subscription = await newSubscription(registration);
  }

  await fetch("/push-notifications/register-subscription", {
    method: "post",
    headers: { "Content-type": "application/json" },
    body: JSON.stringify(subscription),
  });
}

async function newSubscription(registration: ServiceWorkerRegistration) {
  const serverPublicKey = await getServerPublicKey();
  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: serverPublicKey,
  });
  return subscription;
}

async function getServerPublicKey() {
  const response = await fetch("/push-notifications/vapid-public-key");
  const key = await response.text();
  return key;
}
