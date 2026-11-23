/**
 * SDM MOURIDE — MOTEUR AUDIO GLOBAL STABLE (ZÉRO CRASH, ZÉRO GRÉSILLEMENT, ZÉRO DOUBLE-LECTURE)
 * - Coordination inter-onglets via BroadcastChannel : 1 seul onglet lit l'audio à la fois
 * - Aucun spam localStorage / MediaSession (écriture espacée toutes les 5 secondes max)
 * - Aucune boucle pause/play agressive qui fait grésiller le décodeur audio mobile
 * - Micro-widget ultra-compact à côté du nom synchronisé sur toutes les pages et onglets
 */
(function () {
    'use strict';

    if (window.SDMAudioEngine) return;

    const STATE_KEY = 'sdm_now_playing_v2';
    const PLAYLIST_KEY = 'sdm_audio_playlist_v2';
    const LEGACY_KEY = 'sdm_last_audio';
    const TAB_PLAYING_KEY = 'sdm_this_tab_was_playing';
    const TAB_ID = 'tab_' + Math.random().toString(36).slice(2) + '_' + Date.now();

    // Canal inter-onglets pour empêcher 2 onglets de jouer du son en même temps (cause n°1 des crashs / échos)
    let bus = null;
    let anotherTabIsPlaying = false;
    try {
        if ('BroadcastChannel' in window) {
            bus = new BroadcastChannel('sdm_audio_single_owner_v2');
        }
    } catch (e) {}

    // Injecter les styles du micro-widget ultra-compact à côté du nom
    const styleEl = document.createElement('style');
    styleEl.setAttribute('data-sdm-global-style', '1');
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
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.45);
            vertical-align: middle;
            user-select: none;
            flex-shrink: 0;
        }
        .sdm-name-audio-widget.visible { display: inline-flex; }
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
            animation: sdmMiniEqBounce 0.65s ease-in-out infinite alternate;
        }
        .sdm-mini-eq span:nth-child(1) { height: 45%; animation-delay: 0s; }
        .sdm-mini-eq span:nth-child(2) { height: 100%; animation-delay: 0.18s; }
        .sdm-mini-eq span:nth-child(3) { height: 65%; animation-delay: 0.36s; }
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
        }
    `;
    document.head.appendChild(styleEl);

    function getOrCreateGlobalAudio() {
        let el = document.getElementById('sdm-global-audio') || document.getElementById('aud');
        if (!el) {
            el = document.createElement('audio');
            el.id = 'sdm-global-audio';
            el.preload = 'none';
            el.setAttribute('playsinline', '');
            el.setAttribute('webkit-playsinline', '');
            document.body.appendChild(el);
        } else {
            el.setAttribute('playsinline', '');
            el.setAttribute('webkit-playsinline', '');
        }
        return el;
    }

    let aud = null;
    let playlist = [];
    let currentTrack = null;
    let lastPersistMs = 0;
    let lastPosStateMs = 0;
    let activeBlobUrl = null;

    function loadSavedState() {
        try {
            const raw = localStorage.getItem(STATE_KEY);
            return raw ? JSON.parse(raw) : null;
        } catch (e) {
            return null;
        }
    }

    function saveState(override = {}, force = false) {
        if (!currentTrack && !override.id) return;
        const now = Date.now();
        if (!force && now - lastPersistMs < 4500) return;
        lastPersistMs = now;

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
            ownerTabId: TAB_ID,
            updatedAt: now
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
                if (Array.isArray(parsed) && parsed.length > 0) playlist = parsed;
            }
        } catch (e) {}

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
                try { localStorage.setItem(PLAYLIST_KEY, JSON.stringify(list.slice(0, 650))); } catch (e) {}
                return;
            }
        }

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
                        try { localStorage.setItem(PLAYLIST_KEY, JSON.stringify(playlist.slice(0, 650))); } catch (e) {}
                    }
                })
                .catch(() => {});
        }
    }

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
            navigator.mediaSession.setActionHandler('play', () => window.SDMAudioEngine.play());
            navigator.mediaSession.setActionHandler('pause', () => window.SDMAudioEngine.pause());
            navigator.mediaSession.setActionHandler('previoustrack', () => window.SDMAudioEngine.prev());
            navigator.mediaSession.setActionHandler('nexttrack', () => window.SDMAudioEngine.next());
            navigator.mediaSession.setActionHandler('seekto', (details) => {
                if (aud && details.seekTime !== undefined && isFinite(details.seekTime)) {
                    aud.currentTime = details.seekTime;
                    updatePositionState(true);
                }
            });
        } catch (e) {}
    }

    function updatePositionState(force = false) {
        if (!('mediaSession' in navigator) || !aud) return;
        const now = Date.now();
        if (!force && now - lastPosStateMs < 5000) return;
        lastPosStateMs = now;
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

    function renderMiniWidgets(remotePlaying = null) {
        const widgets = document.querySelectorAll('.sdm-name-audio-widget');
        if (!widgets.length) return;

        const hasTrack = currentTrack && currentTrack.titre && currentTrack.url;
        const isPlaying = remotePlaying !== null ? remotePlaying : Boolean(aud && !aud.paused);

        widgets.forEach(w => {
            if (!hasTrack) {
                w.classList.remove('visible');
                return;
            }
            if (!w.dataset.hydrated) {
                w.dataset.hydrated = '1';
                w.innerHTML = `
                    <span class="sdm-mini-eq" title="En cours d'écoute"><span></span><span></span><span></span></span>
                    <a href="/collection/son/" class="sdm-mini-track-link" title="Ouvrir l'Audiothèque"></a>
                    <button type="button" class="sdm-mini-btn sdm-mini-toggle" title="Lecture / Pause"><i class="fa-solid fa-play"></i></button>
                    <button type="button" class="sdm-mini-btn sdm-mini-next" title="Son suivant"><i class="fa-solid fa-forward-step"></i></button>
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
            if (iconEl) iconEl.className = isPlaying ? 'fa-solid fa-pause' : 'fa-solid fa-play';
        });
    }

    // Coordination propre entre onglets (empêche les doubles sons / crash audio quand un autre onglet est ouvert)
    if (bus) {
        bus.onmessage = (event) => {
            const msg = event.data || {};
            if (msg.tabId === TAB_ID) return;

            if (msg.type === 'CLAIM_PLAYBACK') {
                // Un autre onglet prend la main sur la lecture : on met en pause localement proprement (sans crash!)
                anotherTabIsPlaying = true;
                try { sessionStorage.removeItem(TAB_PLAYING_KEY); } catch (e) {}
                if (aud && !aud.paused) {
                    aud.pause();
                }
                if (msg.track) currentTrack = msg.track;
                renderMiniWidgets(true);
            } else if (msg.type === 'REMOTE_PAUSED') {
                anotherTabIsPlaying = false;
                if (msg.track) currentTrack = msg.track;
                renderMiniWidgets(false);
            } else if (msg.type === 'WHO_IS_PLAYING') {
                if (aud && !aud.paused && currentTrack) {
                    bus.postMessage({ type: 'I_AM_PLAYING', tabId: TAB_ID, track: currentTrack });
                }
            } else if (msg.type === 'I_AM_PLAYING') {
                anotherTabIsPlaying = true;
                if (msg.track) currentTrack = msg.track;
                renderMiniWidgets(true);
            } else if (msg.type === 'CMD_PAUSE') {
                if (aud && !aud.paused) aud.pause();
            } else if (msg.type === 'CMD_NEXT') {
                if (aud && !aud.paused) window.SDMAudioEngine.next();
            }
        };
    }

    async function resolveOfflineOrRemoteUrl(track) {
        if (!track || !track.url) return '';
        if (window.SDMOfflineVault && track.id) {
            try {
                const item = await window.SDMOfflineVault.getItem('son', track.id);
                if (item && item.blob) {
                    if (activeBlobUrl) {
                        try { URL.revokeObjectURL(activeBlobUrl); } catch (e) {}
                    }
                    activeBlobUrl = URL.createObjectURL(item.blob);
                    return activeBlobUrl;
                }
            } catch (e) {}
        }
        return track.url;
    }

    function bindAudioEvents() {
        if (!aud || aud.dataset.sdmEngineBound) return;
        aud.dataset.sdmEngineBound = '1';

        aud.addEventListener('play', () => {
            anotherTabIsPlaying = false;
            try { sessionStorage.setItem(TAB_PLAYING_KEY, '1'); } catch (e) {}
            saveState({ isPlaying: true }, true);
            updateMediaSession();
            updatePositionState(true);
            renderMiniWidgets(true);
            if (bus) bus.postMessage({ type: 'CLAIM_PLAYBACK', tabId: TAB_ID, track: currentTrack });
            window.dispatchEvent(new CustomEvent('sdm-audio-state', { detail: { isPlaying: true, track: currentTrack } }));
        });

        aud.addEventListener('pause', () => {
            try { sessionStorage.removeItem(TAB_PLAYING_KEY); } catch (e) {}
            saveState({ isPlaying: false }, true);
            updateMediaSession();
            renderMiniWidgets(false);
            if (bus) bus.postMessage({ type: 'REMOTE_PAUSED', tabId: TAB_ID, track: currentTrack });
            window.dispatchEvent(new CustomEvent('sdm-audio-state', { detail: { isPlaying: false, track: currentTrack } }));
        });

        aud.addEventListener('loadedmetadata', () => {
            saveState({ duration: aud.duration }, true);
            updatePositionState(true);
        });

        aud.addEventListener('timeupdate', () => {
            if (!aud.duration || document.hidden) return;
            saveState({ currentTime: aud.currentTime, duration: aud.duration, isPlaying: !aud.paused }, false);
            updatePositionState(false);
        });

        aud.addEventListener('ended', () => {
            if (!aud.loop) {
                window.SDMAudioEngine.next();
            }
        });
    }

    // Sauvegarder la position exacte uniquement au moment de quitter la page dans CET onglet
    window.addEventListener('pagehide', () => {
        if (aud && currentTrack) {
            const wasPlaying = !aud.paused;
            try {
                if (wasPlaying) sessionStorage.setItem(TAB_PLAYING_KEY, '1');
                else sessionStorage.removeItem(TAB_PLAYING_KEY);
            } catch (e) {}
            saveState({ currentTime: aud.currentTime, isPlaying: wasPlaying }, true);
        }
    });

    // API publique du moteur audio global
    window.SDMAudioEngine = {
        init() {
            aud = getOrCreateGlobalAudio();
            bindAudioEvents();
            loadPlaylist();

            // Vérifier d'abord si un autre onglet joue déjà (évite 100% des doubles sons / crashs entre onglets)
            if (bus) bus.postMessage({ type: 'WHO_IS_PLAYING', tabId: TAB_ID });

            const saved = loadSavedState();
            if (!saved || !saved.url) return;
            currentTrack = saved;
            renderMiniWidgets(false);

            // Reprendre automatiquement UNIQUEMENT si c'est CE MÊME ONGLET qui venait de changer de page
            let thisTabWasPlaying = false;
            try { thisTabWasPlaying = sessionStorage.getItem(TAB_PLAYING_KEY) === '1'; } catch (e) {}

            if (thisTabWasPlaying && saved.isPlaying && !anotherTabIsPlaying) {
                const elapsedSec = saved.updatedAt ? Math.max(0, Math.min(3, (Date.now() - saved.updatedAt) / 1000)) : 0;
                const resumeTime = Math.max(0, (saved.currentTime || 0) + elapsedSec);

                resolveOfflineOrRemoteUrl(saved).then(playUrl => {
                    if (anotherTabIsPlaying) return;
                    aud.src = playUrl;
                    aud.playbackRate = saved.playbackRate || 1;
                    aud.loop = !!saved.isLoop;
                    const seekAndPlay = () => {
                        if (resumeTime > 0 && isFinite(aud.duration) && resumeTime < aud.duration - 1) {
                            try { aud.currentTime = resumeTime; } catch (e) {}
                        }
                        aud.play().catch(() => {
                            renderMiniWidgets(false);
                        });
                    };
                    if (aud.readyState >= 1) {
                        seekAndPlay();
                    } else {
                        aud.addEventListener('loadedmetadata', seekAndPlay, { once: true });
                        aud.load();
                    }
                });
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
            anotherTabIsPlaying = false;

            currentTrack = {
                id: String(trackObj.id || ''),
                titre: trackObj.titre || 'Audio SDM',
                auteur: trackObj.auteur || 'Kourel',
                url: trackObj.url,
                currentTime: 0,
                duration: 0,
                isPlaying: true
            };
            saveState(currentTrack, true);
            renderMiniWidgets(true);

            const playUrl = await resolveOfflineOrRemoteUrl(currentTrack);
            aud.src = playUrl;
            return aud.play().then(() => {
                updateMediaSession();
                renderMiniWidgets(true);
            });
        },

        play() {
            if (!aud) aud = getOrCreateGlobalAudio();
            anotherTabIsPlaying = false;
            if (!aud.src && currentTrack && currentTrack.url) {
                return this.loadAndPlay(currentTrack);
            }
            return aud.play().catch(() => {});
        },

        pause() {
            if (anotherTabIsPlaying && bus) {
                bus.postMessage({ type: 'CMD_PAUSE', tabId: TAB_ID });
                anotherTabIsPlaying = false;
                renderMiniWidgets(false);
                return;
            }
            if (aud) aud.pause();
        },

        toggle() {
            if (anotherTabIsPlaying) {
                this.pause();
                return;
            }
            if (!aud || aud.paused) this.play();
            else this.pause();
        },

        next() {
            if (anotherTabIsPlaying && bus) {
                bus.postMessage({ type: 'CMD_NEXT', tabId: TAB_ID });
                return;
            }
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
            if (aud && aud.currentTime > 4) {
                aud.currentTime = 0;
                return;
            }
            if (typeof window._sdmPagePlayPrev === 'function') {
                window._sdmPagePlayPrev();
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
            anotherTabIsPlaying = false;
            saveState({
                id: String(trackObj.id || ''),
                titre: trackObj.titre || 'Audio SDM',
                auteur: trackObj.auteur || 'Kourel',
                url: trackObj.url,
                currentTime: aud ? aud.currentTime : 0,
                isPlaying: isPlaying
            }, true);
            updateMediaSession();
            renderMiniWidgets(isPlaying);
        },

        refreshWidgets() {
            renderMiniWidgets(anotherTabIsPlaying ? true : null);
        }
    };

    // Arrêt propre si l'utilisateur ferme / balaie l'application des apps récentes (sans affecter l'écoute en arrière-plan)
    window.addEventListener('pagehide', () => {
        if (aud) {
            saveState({ isPlaying: false }, true);
            try { aud.pause(); } catch (e) {}
            try { aud.removeAttribute('src'); aud.load(); } catch (e) {}
        }
        try {
            if ('mediaSession' in navigator) {
                navigator.mediaSession.playbackState = 'none';
            }
        } catch (e) {}
    });

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => window.SDMAudioEngine.init());
    } else {
        window.SDMAudioEngine.init();
    }
})();
