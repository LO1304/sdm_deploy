const CACHE_NAME = 'sdm-premium-v11';
const ASSETS_TO_CACHE = [
  '/',
  '/collection/son/',
  '/collection/khassida/',
  '/coran/',
  '/zikr-compteur/',
  '/offline/',
  '/telechargements/',
  '/static/css/sdm_theme.css',
  '/static/js/sdm_main.js',
  '/static/js/sdm_instant_nav.js',
  '/static/js/sdm_offline_vault.js',
  '/static/js/sdm_audio_engine.js',
  '/static/manifest.json',
  'https://cdn.tailwindcss.com',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Amiri:wght@400;700&display=swap'
];

// Écrans principaux de l'app mobile : servis INSTANTANÉMENT depuis le cache puis mis à jour en arrière-plan (Stale-While-Revalidate)
const INSTANT_SHELL_PATHS = new Set([
  '/',
  '/collection/son/',
  '/collection/khassida/',
  '/coran/',
  '/zikr-compteur/',
  '/telechargements/'
]);

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => Promise.allSettled(ASSETS_TO_CACHE.map((url) => cache.add(url))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) =>
      Promise.all(cacheNames.map((cache) => (cache !== CACHE_NAME ? caches.delete(cache) : null)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  const url = event.request.url;

  // 1. Ressources statiques, CDN (Tailwind, FontAwesome, Fonts) & Miniatures PDF : Cache-First ultra-rapide (<5ms)
  if (
    url.includes('/thumb-pdf/') ||
    url.includes('/static/') ||
    url.includes('cdnjs.cloudflare.com') ||
    url.includes('cdn.tailwindcss.com') ||
    url.includes('fonts.googleapis.com') ||
    url.includes('fonts.gstatic.com')
  ) {
    event.respondWith(
      caches.match(event.request).then((cached) => {
        if (cached) return cached;
        return fetch(event.request).then((res) => {
          if (res && (res.status === 200 || res.type === 'opaque')) {
            const clone = res.clone();
            caches.open(CACHE_NAME).then((c) => c.put(event.request, clone));
          }
          return res;
        }).catch(() => cached);
      })
    );
    return;
  }

  // 2. Ne jamais intercepter les flux audio/PDF lourds, proxies ou APIs dynamiques
  if (
    url.includes('/media/') ||
    url.includes('/proxy-pdf/') ||
    url.includes('/proxy-audio/') ||
    url.includes('cloudinary.com') ||
    url.includes('archive.org') ||
    url.includes('mp3quran.net') ||
    url.includes('lepodcast.fr') ||
    url.includes('podcloud.fr') ||
    url.includes('mediamouride.org') ||
    url.includes('alquran.cloud') ||
    url.includes('islamic.network') ||
    url.includes('/api/') ||
    url.includes('/sons-api/') ||
    url.includes('/admin/') ||
    url.includes('/login') ||
    url.includes('/logout') ||
    url.includes('/register') ||
    url.includes('/profile')
  ) {
    return;
  }

  // 3. Écrans principaux de l'app mobile : Stale-While-Revalidate (ouverture instantanée <15ms + rafraîchissement silencieux)
  let parsedUrl = null;
  try { parsedUrl = new URL(url); } catch (e) {}

  if (parsedUrl && parsedUrl.origin === self.location.origin && (INSTANT_SHELL_PATHS.has(parsedUrl.pathname) || parsedUrl.pathname === '/collection/son/')) {
    event.respondWith(
      caches.open(CACHE_NAME).then((cache) =>
        cache.match(event.request).then((cached) => {
          const networkPromise = fetch(event.request).then((networkRes) => {
            if (networkRes && networkRes.status === 200 && networkRes.type === 'basic') {
              cache.put(event.request, networkRes.clone());
            }
            return networkRes;
          }).catch(() => cached || caches.match('/offline/'));

          return cached || networkPromise;
        })
      )
    );
    return;
  }

  // 4. Autres pages HTML : Network-First avec repli Cache Hors-Ligne
  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, responseClone));
        }
        return networkResponse;
      })
      .catch(() =>
        caches.match(event.request).then((cachedResponse) => {
          if (cachedResponse) return cachedResponse;
          if (event.request.mode === 'navigate') {
            return caches.match('/telechargements/').then((dlPage) => dlPage || caches.match('/offline/'));
          }
        })
      )
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
      for (let i = 0; i < windowClients.length; i++) {
        const client = windowClients[i];
        if (client.url === urlToOpen && 'focus' in client) {
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow(urlToOpen);
      }
    })
  );
});
