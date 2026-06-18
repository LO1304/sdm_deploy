const CACHE_NAME = 'sdm-premium-v4';
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

// ── PUSH NOTIFICATIONS ──
self.addEventListener('push', (event) => {
  let data = {};
  if (event.data) {
    try {
      data = event.data.json();
    } catch (e) {
      data = { notification: { title: 'SDM Premium', body: event.data.text() } };
    }
  }

  const title = data.notification?.title || 'Nouvelle Notification SDM';
  const options = {
    body: data.notification?.body || '',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-72x72.png',
    data: data.data || { url: '/' },
    vibrate: [200, 100, 200]
  };

  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  const urlToOpen = new URL(event.notification.data.url || '/', self.location.origin).href;

  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((windowClients) => {
      // Cherche si l'URL est déjà ouverte
      for (let i = 0; i < windowClients.length; i++) {
        const client = windowClients[i];
        if (client.url === urlToOpen && 'focus' in client) {
          return client.focus();
        }
      }
      // Sinon on l'ouvre
      if (clients.openWindow) {
        return clients.openWindow(urlToOpen);
      }
    })
  );
});
