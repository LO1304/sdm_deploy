const CACHE_NAME = 'sdm-premium-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/static/css/base.css',
  '/static/manifest.json',
  '/static/images/mosquee.jpg',
  'https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

// Installation du Service Worker et mise en cache des assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        return cache.addAll(ASSETS_TO_CACHE);
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

// Interception des requêtes
  // Ne pas intercepter les fichiers média (PDF, Sons) pour éviter les blocages
  if (event.request.url.includes('/media/') || event.request.url.includes('/proxy-pdf/')) {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Retourne la version en cache si elle existe
        if (response) {
          return response;
        }

        // Sinon, fait la requête réseau
        return fetch(event.request).then((networkResponse) => {
          // On peut mettre en cache dynamiquement ici si nécessaire
          return networkResponse;
        }).catch(() => {
          // En cas d'échec (ex: hors ligne), retourner une page par défaut si applicable
          // if (event.request.mode === 'navigate') { return caches.match('/'); }
        });
      })
  );
});
