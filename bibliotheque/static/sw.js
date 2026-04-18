// ══════════════════════════════════════════════
//  SDM Premium — Service Worker
//  Cache-first pour les assets, network-first
//  pour les pages Django
// ══════════════════════════════════════════════

const CACHE_NAME   = 'sdm-v3';
const STATIC_CACHE = 'sdm-static-v3';

// Assets à mettre en cache immédiatement
const PRECACHE_URLS = [
  '/',
  '/offline/',
  '/static/manifest.json',
  '/static/images/icons/icon-192x192.png',
  '/static/images/icons/icon-512x512.png',
  'https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&family=Inter:wght@300;400;500;600;700;800&display=swap',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
];

// ── INSTALL : précache les assets essentiels ──
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => {
      return cache.addAll(PRECACHE_URLS.map(url => {
        return new Request(url, { mode: 'no-cors' });
      })).catch(() => {
        // Silently fail for external resources
      });
    }).then(() => self.skipWaiting())
  );
});

// ── ACTIVATE : nettoie les anciens caches ──
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter(name => name !== CACHE_NAME && name !== STATIC_CACHE)
          .map(name => caches.delete(name))
      );
    }).then(() => self.clients.claim())
  );
});

// ── FETCH : stratégie hybride ──
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Ignorer les requêtes non-GET et les API externes
  if (event.request.method !== 'GET') return;
  if (url.pathname.startsWith('/admin/')) return;
  if (url.pathname.startsWith('/api/')) return;

  // Fichiers media (PDF, audio) : network-first, puis cache
  if (url.pathname.includes('/media/') ||
      url.pathname.endsWith('.pdf') ||
      url.pathname.endsWith('.mp3')) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(c => c.put(event.request, clone));
          }
          return response;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  // Fichiers statiques : cache-first
  if (url.pathname.startsWith('/static/') ||
      url.origin.includes('googleapis.com') ||
      url.origin.includes('cloudflare.com') ||
      url.origin.includes('unpkg.com')) {
    event.respondWith(
      caches.match(event.request).then(cached => {
        return cached || fetch(event.request).then(response => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(STATIC_CACHE).then(c => c.put(event.request, clone));
          }
          return response;
        });
      })
    );
    return;
  }

  // Pages Django : network-first, fallback offline
  event.respondWith(
    fetch(event.request)
      .then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(c => c.put(event.request, clone));
        }
        return response;
      })
      .catch(() => {
        return caches.match(event.request)
          || caches.match('/offline/');
      })
  );
});

// ── PUSH NOTIFICATIONS (optionnel) ──
self.addEventListener('push', (event) => {
  const data = event.data?.json() || { title: 'SDM Premium', body: 'Nouveau contenu disponible !' };
  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: '/static/images/icons/icon-192x192.png',
      badge: '/static/images/icons/icon-192x192.png',
    })
  );
});
