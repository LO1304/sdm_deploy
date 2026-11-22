const CACHE_NAME = 'sdm-premium-v14';
const SHELL_ASSETS = [
  '/',
  '/collection/son/',
  '/collection/khassida/',
  '/coran/',
  '/zikr-compteur/',
  '/telechargements/',
  '/offline/',
  '/notifications/',
  '/static/css/sdm_theme.css',
  '/static/js/sdm_main.js',
  '/static/js/sdm_instant_nav.js',
  '/static/js/sdm_offline_vault.js',
  '/static/js/sdm_audio_engine.js',
  '/static/js/sdm_notifications.js',
  '/static/manifest.json',
  '/static/images/icons/icon-192x192.png',
  '/static/images/sdm_rappels/sdm_touba_emerald.jpg',
  '/static/images/sdm_rappels/sdm_parchemin_royal.jpg',
  '/static/images/sdm_rappels/sdm_nuit_medine.jpg',
  '/static/images/sdm_rappels/sdm_kaaba_or.jpg',
  '/static/images/sdm_rappels/sdm_firdaws_jade.jpg',
  '/static/images/sdm_rappels/sdm_sufi_dawn.jpg',
  'https://cdn.tailwindcss.com',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
  'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Amiri:wght@400;700&display=swap'
];

const INSTANT_SHELL_PATHS = new Set([
  '/',
  '/collection/son/',
  '/collection/khassida/',
  '/coran/',
  '/zikr-compteur/',
  '/telechargements/',
  '/offline/'
]);

function fetchWithTimeout(req, ms = 3800) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('network-timeout')), ms);
    fetch(req).then((res) => {
      clearTimeout(timer);
      resolve(res);
    }).catch((err) => {
      clearTimeout(timer);
      reject(err);
    });
  });
}

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) =>
      Promise.allSettled(
        SHELL_ASSETS.map((url) =>
          fetch(url, { credentials: 'same-origin' })
            .then((res) => {
              if (res && (res.status === 200 || res.type === 'opaque')) {
                return cache.put(url, res);
              }
            })
            .catch(() => {})
        )
      )
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((names) => Promise.all(names.map((n) => (n !== CACHE_NAME ? caches.delete(n) : null))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  const url = event.request.url;

  // 1. Statiques, CDN (Tailwind, FontAwesome, Fonts) & Miniatures PDF : Cache-First (<5ms, 100% hors-ligne)
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
        }).catch(() => cached || new Response('', { status: 504 }));
      })
    );
    return;
  }

  // 2. Ne jamais intercepter les flux audio/PDF distants lourds, proxies ou APIs dynamiques
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
    url.includes('/register')
  ) {
    return;
  }

  let parsedUrl = null;
  try { parsedUrl = new URL(url); } catch (e) {}

  // 3. Écrans principaux de l'app mobile : Stale-While-Revalidate (ouverture instantanée même SANS connexion !)
  if (parsedUrl && parsedUrl.origin === self.location.origin && INSTANT_SHELL_PATHS.has(parsedUrl.pathname)) {
    event.respondWith(
      caches.open(CACHE_NAME).then((cache) =>
        cache.match(event.request).then((exactCached) => {
          const fallbackMatch = exactCached
            ? Promise.resolve(exactCached)
            : cache.match(event.request, { ignoreSearch: true });

          const networkPromise = fetchWithTimeout(event.request, 4000).then((networkRes) => {
            if (networkRes && networkRes.status === 200 && networkRes.type === 'basic') {
              cache.put(event.request, networkRes.clone());
            }
            return networkRes;
          }).catch(() => null);

          return fallbackMatch.then((cached) => {
            if (cached) {
              // Rafraîchissement silencieux en arrière-plan
              event.waitUntil(networkPromise);
              return cached;
            }
            return networkPromise.then((res) => {
              if (res) return res;
              return cache.match('/').then((homeRes) => homeRes || cache.match('/telechargements/') || cache.match('/offline/'));
            });
          });
        })
      )
    );
    return;
  }

  // 4. Autres pages HTML (/tazawwud/, /quiz/, /lire/, /profile/, etc.) : Network (timeout 4s) puis Cache Hors-Ligne
  if (event.request.mode === 'navigate' || (event.request.headers.get('accept') || '').includes('text/html')) {
    event.respondWith(
      fetchWithTimeout(event.request, 4200)
        .then((networkRes) => {
          if (networkRes && networkRes.status === 200 && networkRes.type === 'basic') {
            const clone = networkRes.clone();
            caches.open(CACHE_NAME).then((c) => c.put(event.request, clone));
          }
          return networkRes;
        })
        .catch(() =>
          caches.match(event.request)
            .then((r) => r || caches.match(event.request, { ignoreSearch: true }))
            .then((r) => r || caches.match('/'))
            .then((r) => r || caches.match('/telechargements/'))
            .then((r) => r || caches.match('/offline/'))
        )
    );
    return;
  }
});

// ── MESSAGES DE L'APPLICATION (Notifications locales programmées via Service Worker) ──
self.addEventListener('message', (event) => {
  const data = event.data || {};
  if (data.type === 'SHOW_NOTIFICATION') {
    const title = data.title || 'SDM Mouride';
    const options = {
      body: data.body || '',
      icon: '/static/images/icons/icon-192x192.png',
      badge: '/static/images/icons/icon-192x192.png',
      tag: data.tag || 'sdm-reminder',
      renotify: true,
      vibrate: [180, 90, 180],
      data: { url: data.url || '/' }
    };
    event.waitUntil(self.registration.showNotification(title, options));
  }
});

// ── PUSH NOTIFICATIONS SERVEUR ──
self.addEventListener('push', (event) => {
  let data = {};
  if (event.data) {
    try { data = event.data.json(); }
    catch (e) { data = { notification: { title: 'SDM Mouride', body: event.data.text() } }; }
  }
  const title = data.notification?.title || data.title || 'Rappel SDM Mouride';
  const options = {
    body: data.notification?.body || data.body || '',
    icon: '/static/images/icons/icon-192x192.png',
    badge: '/static/images/icons/icon-192x192.png',
    data: data.data || { url: data.url || '/' },
    vibrate: [200, 100, 200]
  };
  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  const targetUrl = new URL((event.notification.data && event.notification.data.url) || '/', self.location.origin).href;
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((windowClients) => {
      for (let i = 0; i < windowClients.length; i++) {
        const client = windowClients[i];
        if (client.url === targetUrl && 'focus' in client) return client.focus();
      }
      if (clients.openWindow) return clients.openWindow(targetUrl);
    })
  );
});
