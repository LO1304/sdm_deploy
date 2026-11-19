/**
 * SDM MOURIDE — MOTEUR AUDIO GLOBAL PERSISTANT & MICRO-WIDGET À CÔTÉ DU NOM
 * - Continue la musique même lorsqu'on change de page ou qu'on sort de l'application (arrière-plan / écran verrouillé)
 * - Pilote le micro-widget ultra-compact placé à côté du nom de l'utilisateur
 * - Synchronise l'Audiothèque (liste_sons.html) avec toutes les pages de l'application
 */
(function () {
    'use strict';

    if (window.SDMAudioEngine) return;

    const STATE_KEY = 'sdm_now_playing_v2';
    const PLAYLIST_KEY = 'sdm_audio_playlist_v2';
    const LEGACY_KEY = 'sdm_last_audio';

    // Injecter les styles du micro-widget ultra-compact ("très, très, très petit à côté de mon nom")
    const styleEl = document.createElement('style');
    styleEl.textContent = `
        .sdm-name-audio-widget {
            display: none;
            align-items: center;
            gap: 5px;
            height: 22px;
            max-width: 195px;
            padding: 0 7px 0 6px;
            border-radius: 999px;
            background: linear-gradient(135deg, rgba(12, 34, 25, 0.94), rgba(4, 11, 8, 0.96));
            border: 1px solid rgba(212, 175, 55, 0.48);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.45), 0 0 8px rgba(212, 175, 55, 0.15);
            vertical-align: middle;
            user-select: none;
            flex-shrink: 0;
        }
        .sdm-name-audio-widget.visible {
            display: inline-flex;
        }
        .sdm-mini-eq {
            display: inline-flex;
            align-items: flex-end;
            gap: 1.5px;
            width: 10px;
            height: 9px;
            flex-shrink: 0;
        }
        .sdm-mini-eq span {
            width: 2px;
            background: #FDE047;
            border-radius: 1px;
            animation: sdmMiniEqBounce 0.55s ease-in-out infinite alternate;
        }
        .sdm-mini-eq span:nth-child(1) { height: 45%; animation-delay: 0s; }
        .sdm-mini-eq span:nth-child(2) { height: 100%; animation-delay: 0.16s; }
        .sdm-mini-eq span:nth-child(3) { height: 65%; animation-delay: 0.32s; }
        .sdm-name-audio-widget.is-paused .sdm-mini-eq span {
            animation-play-state: paused;
            height: 35% !important;
            opacity: 0.55;
        }
        @keyframes sdmMiniEqBounce {
            from { transform: scaleY(0.35); }
            to   { transform: scaleY(1); }
        }
        .sdm-mini-track-link {
            font-size: 9.5px;
            font-weight: 800;
            color: #FDE047;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 108px;
            text-decoration: none;
            line-height: 1;
            cursor: pointer;
            letter-spacing: 0.01em;
        }
        .sdm-mini-track-link:hover {
            text-decoration: underline;
        }
        .sdm-mini-btn {
            width: 15px;
            height: 15px;
            border-radius: 50%;
            border: none;
            background: rgba(212, 175, 55, 0.22);
            color: #FFFFFF;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 7.5px;
            cursor: pointer;
            padding: 0;
            flex-shrink: 0;
            transition: transform 0.15s ease, background 0.15s ease;
        }
        .sdm-mini-btn:active {
            transform: scale(0.86);
        }
        .sdm-mini-btn:hover {
            background: rgba(212, 175, 55, 0.45);
            color: #040B08;
        }
    `;
    document.head.appendChild(styleEl);

    // Créer ou récupérer l'élément <audio> global unique
    function getOrCreateGlobalAudio() {
        let aud = document.getElementById('sdm-global-audio') || document.getElementById('aud');
        if (!aud) {
            aud = document.createElement('audio');
            aud.id = 'sdm-global-audio';
            aud.preload = 'auto';
            aud.setAttribute('playsinline', '');
            aud.setAttribute('webkit-playsinline', '');
            document.body.appendChild(aud);
        } else {
            aud.preload = 'auto';
            aud.setAttribute('playsinline', '');
            aud.setAttribute('webkit-playsinline', '');
        }
        return aud;
    }

    let aud = null;
    let userExplicitlyPaused = true;
    let lastBackgroundTimestamp = 0;
    let lockResolver = null;
    let playlist = [];
    let currentTrack = null;

    function loadSavedState() {
        try {
            const raw = localStorage.getItem(STATE_KEY);
            if (raw) return JSON.parse(raw);
        } catch (e) {}
        return null;
    }

    function saveState(override = {}) {
        if (!currentTrack && !override.id) return;
        const base = currentTrack || {};
        const state = {
            id: override.id !== undefined ? override.id : base.id,
            titre: override.titre !== undefined ? override.titre : base.titre,
            auteur: override.auteur !== undefined ? override.auteur : base.auteur,
            url: override.url !== undefined ? override.url : base.url,
            currentTime: override.currentTime !== undefined ? override.currentTime : (aud ? aud.currentTime || 0 : 0),
            duration: override.duration !== undefined ? override.duration : (aud && isFinite(aud.duration) ? aud.duration : (base.duration || 0)),
            isPlaying: override.isPlaying !== undefined ? override.isPlaying : (aud ? !aud.paused : false),
            isLoop: override.isLoop !== undefined ? override.isLoop : (aud ? !!aud.loop : false),
            playbackRate: override.playbackRate !== undefined ? override.playbackRate : (aud ? aud.playbackRate || 1 : 1),
            updatedAt: Date.now()
        };
        currentTrack = state;
        try {
            localStorage.setItem(STATE_KEY, JSON.stringify(state));
            localStorage.setItem(LEGACY_KEY, JSON.stringify({
                id: String(state.id),
                time: state.currentTime,
                duration: state.duration
            }));
        } catch (e) {}
    }

    function loadPlaylist() {
        try {
            const raw = localStorage.getItem(PLAYLIST_KEY);
            if (raw) {
                const parsed = JSON.parse(raw);
                if (Array.isArray(parsed) && parsed.length > 0) {
                    playlist = parsed;
                }
            }
        } catch (e) {}

        // Si on est sur liste_sons.html, synchroniser immédiatement à partir du DOM
        const domItems = document.querySelectorAll('.track-item[data-url]');
        if (domItems.length > 0) {
            const list = [];
            domItems.forEach(el => {
                list.push({
                    id: String(el.dataset.id),
                    titre: el.dataset.titre || 'Audio SDM',
                    auteur: el.dataset.auteur || 'Kourel',
                    url: el.dataset.url
                });
            });
            if (list.length > 0) {
                playlist = list;
                try { localStorage.setItem(PLAYLIST_KEY, JSON.stringify(list)); } catch (e) {}
                return;
            }
        }

        // Sinon charger la playlist en arrière-plan si vide
        if (playlist.length === 0) {
            fetch('/sons-api/liste/')
                .then(r => r.json())
                .then(data => {
                    if (data && Array.isArray(data.playlist) && data.playlist.length > 0) {
                        playlist = data.playlist.map(item => ({
                            id: String(item.id),
                            titre: item.titre,
                            auteur: item.auteur,
                            url: item.url
                        }));
                        try { localStorage.setItem(PLAYLIST_KEY, JSON.stringify(playlist)); } catch (e) {}
                    }
                })
                .catch(() => {});
        }
    }

    // Maintenir un verrou Web Lock pendant la lecture pour empêcher l'OS mobile de geler l'onglet en arrière-plan
    function acquireBackgroundLock() {
        if ('locks' in navigator && !lockResolver) {
            navigator.locks.request('sdm_persistent_audio_lock', () => {
                return new Promise(resolve => {
                    lockResolver = resolve;
                });
            }).catch(() => {});
        }
    }

    function releaseBackgroundLock() {
        if (lockResolver) {
            lockResolver();
            lockResolver = null;
        }
    }

    // Mettre à jour MediaSession (Écran de verrouillage Android / iOS & Centre de contrôle)
    function updateMediaSession() {
        if (!('mediaSession' in navigator) || !currentTrack) return;
        try {
            navigator.mediaSession.metadata = new MediaMetadata({
                title: currentTrack.titre || 'SDM Mouride Audio',
                artist: currentTrack.auteur || 'SDM Mouride',
                album: 'Audiothèque SDM Mouride',
                artwork: [
                    { src: '/static/images/icons/icon-192x192.png', sizes: '192x192', type: 'image/png' },
                    { src: '/static/images/icons/icon-512x512.png', sizes: '512x512', type: 'image/png' }
                ]
            });
            navigator.mediaSession.playbackState = (aud && !aud.paused) ? 'playing' : 'paused';

            navigator.mediaSession.setActionHandler('play', () => {
                window.SDMAudioEngine.play();
            });
            navigator.mediaSession.setActionHandler('pause', () => {
                window.SDMAudioEngine.pause();
            });
            navigator.mediaSession.setActionHandler('previoustrack', () => {
                window.SDMAudioEngine.prev();
            });
            navigator.mediaSession.setActionHandler('nexttrack', () => {
                window.SDMAudioEngine.next();
            });
            navigator.mediaSession.setActionHandler('seekto', (details) => {
                if (aud && details.seekTime !== undefined) {
                    aud.currentTime = details.seekTime;
                    updatePositionState();
                }
            });
        } catch (e) {}
    }

    function updatePositionState() {
        if (!('mediaSession' in navigator) || !aud) return;
        if ('setPositionState' in navigator.mediaSession && isFinite(aud.duration) && aud.duration > 0) {
            try {
                navigator.mediaSession.setPositionState({
                    duration: aud.duration,
                    playbackRate: aud.playbackRate || 1,
                    position: Math.min(aud.currentTime, aud.duration)
                });
            } catch (e) {}
        }
    }

    // Rendu et mise à jour de tous les micro-widgets à côté du nom (.sdm-name-audio-widget)
    function renderMiniWidgets() {
        const widgets = document.querySelectorAll('.sdm-name-audio-widget');
        if (!widgets.length) return;

        const hasTrack = currentTrack && currentTrack.titre && currentTrack.url;
        const isPlaying = aud && !aud.paused;

        widgets.forEach(w => {
            if (!hasTrack) {
                w.classList.remove('visible');
                return;
            }

            if (!w.dataset.hydrated) {
                w.dataset.hydrated = '1';
                w.innerHTML = `
                    <span class="sdm-mini-eq" title="En cours d'écoute">
                        <span></span><span></span><span></span>
                    </span>
                    <a href="/collection/son/" class="sdm-mini-track-link" title="Ouvrir l'Audiothèque"></a>
                    <button type="button" class="sdm-mini-btn sdm-mini-toggle" title="Lecture / Pause">
                        <i class="fa-solid fa-play"></i>
                    </button>
                    <button type="button" class="sdm-mini-btn sdm-mini-next" title="Son suivant">
                        <i class="fa-solid fa-forward-step"></i>
                    </button>
                `;
                w.querySelector('.sdm-mini-toggle').addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    window.SDMAudioEngine.toggle();
                });
                w.querySelector('.sdm-mini-next').addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    window.SDMAudioEngine.next();
                });
            }

            w.classList.add('visible');
            w.classList.toggle('is-paused', !isPlaying);

            const titleEl = w.querySelector('.sdm-mini-track-link');
            if (titleEl) {
                titleEl.textContent = currentTrack.titre;
                titleEl.title = `${currentTrack.titre} (${currentTrack.auteur || 'SDM'})`;
            }

            const iconEl = w.querySelector('.sdm-mini-toggle i');
            if (iconEl) {
                iconEl.className = isPlaying ? 'fa-solid fa-pause' : 'fa-solid fa-play';
            }
        });
    }

    async function resolveOfflineOrRemoteUrl(track) {
        if (!track || !track.url) return '';
        if (window.SDMOfflineVault && track.id) {
            try {
                const item = await window.SDMOfflineVault.getItem('son', track.id);
                if (item && item.blob) {
                    return URL.createObjectURL(item.blob);
                }
            } catch (e) {}
        }
        return track.url;
    }

    function bindAudioEvents() {
        if (!aud || aud.dataset.sdmEngineBound) return;
        aud.dataset.sdmEngineBound = '1';

        aud.addEventListener('play', () => {
            acquireBackgroundLock();
            saveState({ isPlaying: true });
            updateMediaSession();
            renderMiniWidgets();
            window.dispatchEvent(new CustomEvent('sdm-audio-state', { detail: { isPlaying: true, track: currentTrack } }));
        });

        aud.addEventListener('pause', () => {
            // Si la mise en pause survient exactement au moment où l'utilisateur quitte l'application
            // ou verrouille l'écran (sans avoir appuyé sur Pause), on relance immédiatement la lecture !
            const now = Date.now();
            const isBackgroundTransition = document.visibilityState === 'hidden' || (now - lastBackgroundTimestamp < 1500);
            if (!userExplicitlyPaused && !aud.ended && isBackgroundTransition) {
                setTimeout(() => {
                    if (!userExplicitlyPaused && aud.paused) {
                        aud.play().catch(() => {});
                    }
                }, 30);
                return;
            }
            saveState({ isPlaying: false });
            updateMediaSession();
            renderMiniWidgets();
            window.dispatchEvent(new CustomEvent('sdm-audio-state', { detail: { isPlaying: false, track: currentTrack } }));
        });

        aud.addEventListener('loadedmetadata', () => {
            saveState({ duration: aud.duration });
            updatePositionState();
        });

        aud.addEventListener('timeupdate', () => {
            if (!aud.duration) return;
            if (Math.floor(aud.currentTime) % 2 === 0) {
                saveState({
                    currentTime: aud.currentTime,
                    duration: aud.duration,
                    isPlaying: !aud.paused
                });
                updatePositionState();
            }
        });

        aud.addEventListener('ended', () => {
            if (!aud.loop) {
                window.SDMAudioEngine.next();
            }
        });
    }

    // Protection quand l'utilisateur sort de l'application ou change de page
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'hidden') {
            lastBackgroundTimestamp = Date.now();
            if (aud && !aud.paused) {
                userExplicitlyPaused = false;
                saveState({ isPlaying: true, currentTime: aud.currentTime });
            }
        }
    });

    window.addEventListener('pagehide', () => {
        if (aud && currentTrack) {
            saveState({
                currentTime: aud.currentTime,
                isPlaying: !aud.paused && !userExplicitlyPaused
            });
        }
    });

    window.addEventListener('beforeunload', () => {
        if (aud && currentTrack) {
            saveState({
                currentTime: aud.currentTime,
                isPlaying: !aud.paused && !userExplicitlyPaused
            });
        }
    });

    // API publique du moteur audio global
    window.SDMAudioEngine = {
        init() {
            aud = getOrCreateGlobalAudio();
            bindAudioEvents();
            loadPlaylist();

            const saved = loadSavedState();
            if (saved && saved.url) {
                currentTrack = saved;
                renderMiniWidgets();

                // Si la page n'a pas encore chargé la source dans <audio>
                if (!aud.src || aud.src === window.location.href) {
                    const elapsedSec = saved.isPlaying && saved.updatedAt
                        ? Math.max(0, Math.min(4, (Date.now() - saved.updatedAt) / 1000))
                        : 0;
                    const resumeTime = Math.max(0, (saved.currentTime || 0) + elapsedSec);

                    resolveOfflineOrRemoteUrl(saved).then(playUrl => {
                        aud.src = playUrl;
                        aud.playbackRate = saved.playbackRate || 1;
                        aud.loop = !!saved.isLoop;
                        aud.addEventListener('loadedmetadata', function onMeta() {
                            aud.removeEventListener('loadedmetadata', onMeta);
                            if (resumeTime > 0 && (!aud.duration || resumeTime < aud.duration - 1)) {
                                try { aud.currentTime = resumeTime; } catch (e) {}
                            }
                        });

                        if (saved.isPlaying) {
                            userExplicitlyPaused = false;
                            aud.play().then(() => {
                                renderMiniWidgets();
                                updateMediaSession();
                            }).catch(() => {
                                // Si le navigateur attend un geste tactile, reprendre dès le premier toucher sur l'écran
                                const resumeOnTap = () => {
                                    document.removeEventListener('pointerdown', resumeOnTap);
                                    if (!userExplicitlyPaused && aud.paused) {
                                        aud.play().catch(() => {});
                                    }
                                };
                                document.addEventListener('pointerdown', resumeOnTap, { once: true });
                            });
                        }
                    });
                }
            }
        },

        getAudioElement() {
            if (!aud) aud = getOrCreateGlobalAudio();
            bindAudioEvents();
            return aud;
        },

        getCurrentTrack() {
            return currentTrack;
        },

        async loadAndPlay(trackObj) {
            if (!aud) aud = getOrCreateGlobalAudio();
            bindAudioEvents();
            userExplicitlyPaused = false;

            currentTrack = {
                id: String(trackObj.id || ''),
                titre: trackObj.titre || 'Audio SDM',
                auteur: trackObj.auteur || 'Kourel',
                url: trackObj.url,
                currentTime: 0,
                duration: 0,
                isPlaying: true
            };
            saveState(currentTrack);
            renderMiniWidgets();

            const playUrl = await resolveOfflineOrRemoteUrl(currentTrack);
            aud.src = playUrl;
            return aud.play().then(() => {
                updateMediaSession();
                renderMiniWidgets();
            });
        },

        play() {
            if (!aud) aud = getOrCreateGlobalAudio();
            userExplicitlyPaused = false;
            if (!aud.src && currentTrack && currentTrack.url) {
                return this.loadAndPlay(currentTrack);
            }
            return aud.play().then(() => {
                saveState({ isPlaying: true });
                renderMiniWidgets();
            }).catch(() => {});
        },

        pause() {
            userExplicitlyPaused = true;
            releaseBackgroundLock();
            if (aud) {
                aud.pause();
                saveState({ isPlaying: false });
            }
            renderMiniWidgets();
        },

        toggle() {
            if (!aud || aud.paused) {
                this.play();
            } else {
                this.pause();
            }
        },

        next() {
            // Si la page liste_sons.html possède sa propre fonction playNext avec la liste filtrée, l'utiliser
            if (typeof window._sdmPagePlayNext === 'function') {
                window._sdmPagePlayNext();
                return;
            }
            if (!playlist.length) loadPlaylist();
            if (!playlist.length) return;
            const curId = currentTrack ? String(currentTrack.id) : '';
            const idx = playlist.findIndex(t => String(t.id) === curId);
            const nextTrack = playlist[(idx + 1) % playlist.length];
            if (nextTrack) this.loadAndPlay(nextTrack);
        },

        prev() {
            if (typeof window._sdmPagePlayPrev === 'function') {
                window._sdmPagePlayPrev();
                return;
            }
            if (aud && aud.currentTime > 4) {
                aud.currentTime = 0;
                return;
            }
            if (!playlist.length) loadPlaylist();
            if (!playlist.length) return;
            const curId = currentTrack ? String(currentTrack.id) : '';
            const idx = playlist.findIndex(t => String(t.id) === curId);
            const prevTrack = playlist[(idx - 1 + playlist.length) % playlist.length];
            if (prevTrack) this.loadAndPlay(prevTrack);
        },

        syncFromPageTrack(trackObj, isPlaying = true) {
            userExplicitlyPaused = !isPlaying;
            saveState({
                id: String(trackObj.id || ''),
                titre: trackObj.titre || 'Audio SDM',
                auteur: trackObj.auteur || 'Kourel',
                url: trackObj.url,
                currentTime: aud ? aud.currentTime : 0,
                isPlaying: isPlaying
            });
            updateMediaSession();
            renderMiniWidgets();
        },

        refreshWidgets() {
            renderMiniWidgets();
        }
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => window.SDMAudioEngine.init());
    } else {
        window.SDMAudioEngine.init();
    }
})();
