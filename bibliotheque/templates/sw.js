const CACHE_NAME = 'sdm-premium-cache-v1';
const DYNAMIC_CACHE = 'sdm-premium-dynamic-v1';

// Fichiers à cacher initialement (App Shell)
const STATIC_ASSETS = [
    '/',
    '/offline/',
    '/static/manifest.json',
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Amiri:ital,wght@0,400;0,700;1,400&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
    'https://cdn.tailwindcss.com'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[Service Worker] Installation - Caching static assets');
            // 'addAll' is risky if one URL fails, the whole promise rejects. Let's do it safely.
            return Promise.all(
                STATIC_ASSETS.map(url => {
                    return fetch(url).then(response => {
                        if (response.ok) {
                            return cache.put(url, response);
                        }
                    }).catch(error => console.log('[Service Worker] Failed to cache: ', url));
                })
            );
        }).then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.filter(key => key !== CACHE_NAME && key !== DYNAMIC_CACHE)
                    .map(key => caches.delete(key))
            );
        }).then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', (event) => {
    // Ne pas intercepter les requêtes non-GET ou vers des API d'analytics externes
    if (event.request.method !== 'GET') return;

    // Gestion des requêtes HTML (Navigation) - Stratégie: Network First with Fallback to Cache
    if (event.request.headers.get('accept').includes('text/html')) {
        event.respondWith(
            fetch(event.request)
                .then(response => {
                    // Mettre en cache la page visitée pour un accès hors-ligne futur
                    const copy = response.clone();
                    caches.open(DYNAMIC_CACHE).then(cache => {
                        cache.put(event.request.url, copy);
                    });
                    return response;
                })
                .catch(() => {
                    // Si réseau indisponible, essayer de trouver la page dans le cache
                    return caches.match(event.request).then(cachedResponse => {
                        return cachedResponse || caches.match('/offline/');
                    });
                })
        );
        return;
    }

    // Gestion des médias (Audio, Images, PDF) - Stratégie: Cache First ou Network First (ici Cache First pour économiser)
    const isMedia = event.request.url.match(/\.(mp3|wav|jpg|jpeg|png|gif|svg|pdf)$/);
    if (isMedia) {
        event.respondWith(
            caches.match(event.request).then(cachedResponse => {
                return cachedResponse || fetch(event.request).then(response => {
                    // Si le média n'est pas encore en cache, on le met en cache après le fetch
                    const copy = response.clone();
                    caches.open(DYNAMIC_CACHE).then(cache => {
                        cache.put(event.request.url, copy);
                    });
                    return response;
                }).catch(() => {
                    // Fichier média indisponible hors ligne
                    return new Response('', { status: 404, statusText: 'Offline representation missing' });
                });
            })
        );
        return;
    }

    // Autres requêtes (CSS, JS) - Cache First
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            return cachedResponse || fetch(event.request).then(response => {
                return caches.open(DYNAMIC_CACHE).then(cache => {
                    cache.put(event.request.url, response.clone());
                    return response;
                });
            });
        }).catch(() => {})
    );
});
