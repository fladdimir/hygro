self.addEventListener("push", (e) => {
  const payload = e.data ? e.data.text() : " - ";
  e.waitUntil(
    self.registration.showNotification("Hygro alert", {
      body: payload,
    })
  );
});
