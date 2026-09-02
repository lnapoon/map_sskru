// SSKRU Campus Map Service Worker
const CACHE_NAME = 'sskru-map-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/assets/css/styles.css',
  '/assets/js/app.js',
  '/assets/manifest.json'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE).catch(() => {});
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((k) => {
          if (k !== CACHE_NAME) return caches.delete(k);
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  // Let network handle API and auth requests directly
  if (e.request.url.includes('/api/') || e.request.url.includes('/admin/')) {
    return;
  }
  e.respondWith(
    caches.match(e.request).then((res) => {
      return res || fetch(e.request);
    }).catch(() => fetch(e.request))
  );
});
