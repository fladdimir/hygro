import { subscribe } from "../../services/subscriptionService";

interface NotificationSubscribeProps {
  available: boolean;
}

function NotificationSubscription(props: NotificationSubscribeProps) {
  if (!props.available) {
    return <></>;
  }
  return (
    <>
      <button onClick={() => subscribe()}>subscribe</button>
    </>
  );
}

export default NotificationSubscription;
