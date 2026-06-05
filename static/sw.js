const CACHE_NAME = 'sdm-premium-v3';
const ASSETS_TO_CACHE = [
  '/',
  '/offline/',
  '/static/css/sdm_theme.css',
  '/static/js/sdm_main.js',
  '/static/manifest.json',
  'https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700;900&family=Inter:wght@300;400;500;600;700&family=Amiri:wght@400;700&display=swap',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

// Installation du Service Worker et mise en cache des assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        return cache.addAll(ASSETS_TO_CACHE).catch(err => {
          console.warn('SW: Some assets failed to cache:', err);
        });
      })
      .then(() => self.skipWaiting())
  );
});

// Activation et nettoyage des anciens caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            return caches.delete(cache);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Interception des requêtes avec stratégie Network-First
self.addEventListener('fetch', (event) => {
  // Ne pas intercepter les fichiers média (PDF, Sons, Cloudinary) pour éviter les blocages
  const url = event.request.url;
  if (
    url.includes('/media/') ||
    url.includes('/proxy-pdf/') ||
    url.includes('cloudinary.com') ||
    url.includes('res.cloudinary.com') ||
    url.includes('/api/') ||
    url.includes('/admin/') ||
    event.request.method !== 'GET'
  ) {
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        // Clone et mise en cache dynamique pour les pages visitées
        if (networkResponse && networkResponse.status === 200) {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        // En cas d'échec réseau, chercher dans le cache
        return caches.match(event.request).then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }
          // Si page de navigation, renvoyer la page offline
          if (event.request.mode === 'navigate') {
            return caches.match('/offline/');
          }
        });
      })
  );
});
