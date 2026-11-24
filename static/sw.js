const CACHE_NAME = 'sdm-premium-v23';
const SHELL_ASSETS = [
  '/',
  '/offline/',
  '/apprentissage/',
  '/masaalik/',
  '/zikr-compteur/',
  '/telechargements/',
  '/static/css/sdm_theme.css',
  '/static/js/sdm_main.js',
  '/static/js/sdm_instant_nav.js',
  '/static/js/sdm_offline_vault.js',
  '/static/js/sdm_audio_engine.js',
  '/static/js/sdm_notifications.js',
  '/static/manifest.json',
  '/static/images/icons/icon-192x192.png',
  '/static/images/serigne_touba_splash.jpg',
  '/static/images/sdm_rappels/thumbs/sdm_touba_emerald.jpg',
  '/static/images/sdm_rappels/thumbs/sdm_parchemin_royal.jpg',
  '/static/images/sdm_rappels/thumbs/sdm_nuit_medine.jpg',
  '/static/images/sdm_rappels/thumbs/sdm_kaaba_or.jpg',
  '/static/images/sdm_rappels/thumbs/sdm_firdaws_jade.jpg',
  '/static/images/sdm_rappels/thumbs/sdm_sufi_dawn.jpg',
  'https://cdn.tailwindcss.com'
];

const INSTANT_SHELL_PATHS = new Set([
  '/',
  '/apprentissage/',
  '/masaalik/',
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
    const silent = Boolean(data.silent);
    const options = {
      body: data.body || '',
      icon: '/static/images/icons/icon-192x192.png',
      badge: '/static/images/icons/icon-192x192.png',
      tag: data.tag || 'sdm-reminder',
      renotify: true,
      silent: silent,
      vibrate: silent ? undefined : [180, 90, 180],
      data: { url: data.url || '/' }
    };
    event.waitUntil(self.registration.showNotification(title, options));
  }
});

// ── VÉRIFICATION EN ARRIÈRE-PLAN (Periodic Background Sync sur Android PWA même app fermée) ──
async function runSwBackgroundNotificationCheck() {
  try {
    const stateCache = await caches.open('sdm-notif-state-v1');
    const stateRes = await stateCache.match('/__sdm_notif_state__');
    const state = stateRes ? await stateRes.json() : {};
    const prefs = state.prefs || { enabled: true, prayerEnabled: true, wirdEnabled: true, sonEnabled: true, khassidaEnabled: true };
    if (!prefs.enabled) return;

    const firedRes = await stateCache.match('/__sdm_sw_fired__');
    const fired = firedRes ? await firedRes.json() : {};

    const feedRes = await fetch('/api/notifications/sync-feed/', { credentials: 'same-origin' });
    if (!feedRes.ok) return;
    const feed = await feedRes.json();

    const now = new Date();
    const nowMin = now.getHours() * 60 + now.getMinutes();
    const today = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
    const toMin = (hhmm) => {
      if (!hhmm || !String(hhmm).includes(':')) return -1;
      const [h, m] = String(hhmm).slice(0, 5).split(':').map(Number);
      return (isNaN(h) || isNaN(m)) ? -1 : h * 60 + m;
    };

    let changed = false;
    const silent = (prefs.soundMode === 'silent');

    // 1. Nouveau Son publié
    if (prefs.sonEnabled && feed.latest_son && feed.latest_son.id) {
      const sid = String(feed.latest_son.id);
      if (fired.last_son_id && fired.last_son_id !== sid) {
        fired.last_son_id = sid;
        changed = true;
        await self.registration.showNotification(`🎧 Nouveau Son : ${feed.latest_son.titre}`, {
          body: `${feed.latest_son.auteur || 'Kourel Mouride'} vient d'être ajouté sur SDM Mouride.`,
          icon: '/static/images/icons/icon-192x192.png',
          badge: '/static/images/icons/icon-192x192.png',
          tag: `sdm-son-${sid}`,
          silent: silent,
          vibrate: silent ? undefined : [160, 80, 160],
          data: { url: `/collection/son/?autoplay=${sid}` }
        });
      } else if (!fired.last_son_id) {
        fired.last_son_id = sid;
        changed = true;
      }
    }

    // 2. Prières du jour
    if (prefs.prayerEnabled) {
      const prayers = state.prayers || feed.prayers || [];
      const lead = parseInt(prefs.prayerLeadMin || 5, 10);
      const pSilent = (prefs.prayerSoundMode === 'silent');
      for (const p of prayers) {
        const pm = toMin(p.time);
        const k = `sw_prayer_${today}_${p.name}`;
        if (pm >= 0 && !fired[k] && nowMin >= (pm - lead) && nowMin <= (pm + 25)) {
          fired[k] = Date.now();
          changed = true;
          await self.registration.showNotification(`🕌 Heure de la Prière : ${p.name}`, {
            body: `La prière de ${p.name} est prévue à ${p.time}.`,
            icon: '/static/images/icons/icon-192x192.png',
            badge: '/static/images/icons/icon-192x192.png',
            tag: k,
            silent: pSilent,
            vibrate: pSilent ? undefined : [180, 90, 180],
            data: { url: '/' }
          });
          break;
        }
      }
    }

    // 3. Wird Mahuz (06h30 Suba / 17h00 Takussan)
    if (prefs.wirdEnabled) {
      const wm = toMin(prefs.wirdMorningTime || '06:30');
      const we = toMin(prefs.wirdEveningTime || '17:00');
      const wUrl = feed.wird_url || '/wird/mahuz-al-khafif/';
      const kM = `sw_wird_m_${today}`;
      if (wm >= 0 && !fired[kM] && nowMin >= wm && nowMin <= wm + 180) {
        fired[kM] = Date.now();
        changed = true;
        await self.registration.showNotification('📿 Rappel Wird Mahuz du Matin (06h30)', {
          body: 'Ouvrez le compteur sacré pour accomplir votre Wird du matin après Suba.',
          icon: '/static/images/icons/icon-192x192.png',
          badge: '/static/images/icons/icon-192x192.png',
          tag: kM,
          silent: silent,
          vibrate: silent ? undefined : [160, 80, 160],
          data: { url: wUrl }
        });
      }
      const kE = `sw_wird_e_${today}`;
      if (we >= 0 && !fired[kE] && nowMin >= we && nowMin <= we + 180) {
        fired[kE] = Date.now();
        changed = true;
        await self.registration.showNotification('📿 Rappel Wird Mahuz du Soir (17h00)', {
          body: 'N\'oubliez pas votre Wird Mahuz du soir après Takussan !',
          icon: '/static/images/icons/icon-192x192.png',
          badge: '/static/images/icons/icon-192x192.png',
          tag: kE,
          silent: silent,
          vibrate: silent ? undefined : [160, 80, 160],
          data: { url: wUrl }
        });
      }
    }

    if (changed) {
      await stateCache.put('/__sdm_sw_fired__', new Response(JSON.stringify(fired), {
        headers: { 'Content-Type': 'application/json' }
      }));
    }
  } catch (e) {}
}

self.addEventListener('periodicsync', (event) => {
  if (event.tag === 'sdm-smart-notifs') {
    event.waitUntil(runSwBackgroundNotificationCheck());
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
  const rawUrl = (event.notification.data && event.notification.data.url) || '/';
  const targetUrl = new URL(rawUrl, self.location.origin).href;
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((windowClients) => {
      for (let i = 0; i < windowClients.length; i++) {
        const client = windowClients[i];
        if (client.url.startsWith(self.location.origin)) {
          if ('navigate' in client) {
            return client.navigate(targetUrl).then((navClient) => (navClient && 'focus' in navClient ? navClient.focus() : null)).catch(() => client.focus());
          }
          if ('focus' in client) return client.focus();
        }
      }
      if (clients.openWindow) return clients.openWindow(targetUrl);
    })
  );
});
