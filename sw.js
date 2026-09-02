// SSKRU Campus Map Service Worker - Safari WebKit Safe Passthrough
self.addEventListener('install', (e) => {
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(keys.map((k) => caches.delete(k)));
    })
  );
  self.clients.claim();
});

// Do not intercept requests with e.respondWith to prevent Safari "WebKitInternal redirection" errors
self.addEventListener('fetch', (e) => {
  return;
});
