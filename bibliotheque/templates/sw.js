const CACHE_NAME = 'sdm-premium-v4';

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          return caches.delete(cache);
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Bypass fetch entirely to let the browser handle requests natively, preventing blank screen issues
self.addEventListener('fetch', (event) => {
  // No-op
});

