/**
 * SDM MOURIDE — COFFRE-FORT HORS-LIGNE ORGANISÉ PAR CATÉGORIE & DOSSIER (INDEXEDDB + CACHE API)
 * & PERSISTANCE DE CONNEXION MOBILE 365 JOURS
 */
(function () {
    'use strict';

    const DB_NAME = 'sdm_offline_vault_db';
    const DB_VERSION = 1;
    const STORE_NAME = 'offline_items';
    const CACHE_NAME = 'sdm-premium-v6';
    const FOLDERS_LS_KEY = 'sdm_offline_custom_folders_v1';

    const CATEGORY_LABELS = {
        'KHASSIDA': 'Khassidas Audio',
        'CORAN': 'Coran Audio',
        'XAM_XAM': 'Xam Xam Audio',
        'WAKHTANE': 'Wakhtane',
        'ZIKR': 'Zikr Audio',
        'RAJASS': 'Rajass',
        'ADHAN': 'Adhan',
        'khassida': 'Khassidas PDF',
        'coran': 'Coran PDF',
        'son': 'Audios'
    };

    // ═══════════════════════════════════════════════════════════════════
    // 1. PERSISTANCE AUTOMATIQUE DE CONNEXION (ANTI-DÉCONNEXION MOBILE)
    // ═══════════════════════════════════════════════════════════════════
    function getCookie(name) {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? decodeURIComponent(match[2]) : null;
    }

    function syncPersistentAuth() {
        try {
            const cookieToken = getCookie('sdm_remember_token');
            if (cookieToken) {
                localStorage.setItem('sdm_auth_token', cookieToken);
            }

            document.addEventListener('click', function (e) {
                const link = e.target.closest('a[href*="/logout"], button[formaction*="/logout"]');
                const form = e.target.closest('form[action*="/logout"]');
                if (link || form) {
                    localStorage.removeItem('sdm_auth_token');
                    document.cookie = 'sdm_remember_token=; Max-Age=0; path=/';
                }
            }, true);

            const storedToken = localStorage.getItem('sdm_auth_token');
            if (!cookieToken && storedToken && navigator.onLine) {
                fetch('/api/auth/restore-session/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-SDM-Auth-Token': storedToken
                    },
                    body: JSON.stringify({ token: storedToken }),
                    credentials: 'same-origin'
                })
                .then(r => r.json())
                .then(data => {
                    if (data && data.token) {
                        localStorage.setItem('sdm_auth_token', data.token);
                        if (data.status === 'restored') {
                            if (window.location.pathname.indexOf('/login') === 0) {
                                window.location.replace('/');
                            } else {
                                window.location.reload();
                            }
                        }
                    } else if (data && data.status === 'anonymous') {
                        localStorage.removeItem('sdm_auth_token');
                    }
                })
                .catch(() => {});
            }
        } catch (err) {}
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', syncPersistentAuth);
    } else {
        syncPersistentAuth();
    }

    // ═══════════════════════════════════════════════════════════════════
    // 2. GESTION DES DOSSIERS PERSONNALISÉS (ORGANISATION HORS-LIGNE)
    // ═══════════════════════════════════════════════════════════════════
    function readCustomFolders() {
        try {
            const raw = localStorage.getItem(FOLDERS_LS_KEY);
            const parsed = raw ? JSON.parse(raw) : [];
            return Array.isArray(parsed) ? parsed : [];
        } catch (e) {
            return [];
        }
    }

    function writeCustomFolders(list) {
        try {
            localStorage.setItem(FOLDERS_LS_KEY, JSON.stringify(list));
        } catch (e) {}
    }

    function computeDefaultFolder(meta) {
        if (meta.dossier && String(meta.dossier).trim()) {
            return String(meta.dossier).trim();
        }
        const cat = String(meta.categorie || '').toLowerCase();
        const sub = String(meta.sousCategorie || '').toUpperCase();
        if (cat === 'son') {
            if (sub && CATEGORY_LABELS[sub]) return CATEGORY_LABELS[sub];
            return 'Audios Divers';
        }
        if (cat === 'khassida') return 'Khassidas PDF';
        if (cat === 'coran') return 'Coran PDF';
        return 'Mes Téléchargements';
    }

    // ═══════════════════════════════════════════════════════════════════
    // 3. MOTEUR INDEXEDDB POUR LE STOCKAGE HORS-LIGNE DANS L'APPLICATION
    // ═══════════════════════════════════════════════════════════════════
    function openVaultDB() {
        return new Promise((resolve, reject) => {
            if (!('indexedDB' in window)) {
                return reject(new Error('IndexedDB non supporté'));
            }
            const req = indexedDB.open(DB_NAME, DB_VERSION);
            req.onupgradeneeded = function (e) {
                const db = e.target.result;
                if (!db.objectStoreNames.contains(STORE_NAME)) {
                    const store = db.createObjectStore(STORE_NAME, { keyPath: 'key' });
                    store.createIndex('categorie', 'categorie', { unique: false });
                    store.createIndex('savedAt', 'savedAt', { unique: false });
                }
            };
            req.onsuccess = function (e) { resolve(e.target.result); };
            req.onerror = function (e) { reject(e.target.error); };
        });
    }

    async function blobToDataURL(blob) {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.onerror = () => resolve(null);
            reader.readAsDataURL(blob);
        });
    }

    async function fetchMediaWithFallback(meta) {
        const mediaUrl = meta.pdfUrl || meta.audioUrl || `/proxy-pdf/${meta.categorie}/${meta.id}/`;
        try {
            const resp = await fetch(mediaUrl, {
                credentials: mediaUrl.startsWith('/') ? 'same-origin' : 'omit'
            });
            if (resp.ok) return resp;
        } catch (e) {}

        // Fallback CORS via notre proxy Django pour garantir 100% de réussite hors-ligne
        if (String(meta.categorie) === 'son') {
            const proxyResp = await fetch(`/proxy-audio/${meta.id}/`, { credentials: 'same-origin' });
            if (proxyResp.ok) return proxyResp;
        } else {
            const proxyResp = await fetch(`/proxy-pdf/${meta.categorie}/${meta.id}/`, { credentials: 'same-origin' });
            if (proxyResp.ok) return proxyResp;
        }
        throw new Error('Échec du téléchargement du fichier média');
    }

    const SDMOfflineVault = {
        CATEGORY_LABELS,

        async saveItem(meta, onProgress) {
            const key = `${meta.categorie}_${meta.id}`;
            const mediaUrl = meta.pdfUrl || meta.audioUrl || `/proxy-pdf/${meta.categorie}/${meta.id}/`;
            const readUrl = meta.readUrl || (meta.categorie === 'son' ? `/collection/son/?autoplay=${meta.id}` : `/lire/${meta.categorie}/${meta.id}/`);
            const thumbUrl = meta.thumbUrl || `/thumb-pdf/${meta.categorie}/${meta.id}/`;
            const sousCategorie = (meta.sousCategorie || (meta.categorie === 'son' ? 'KHASSIDA' : String(meta.categorie).toUpperCase())).toUpperCase();
            const dossier = computeDefaultFolder({ ...meta, sousCategorie });

            if (onProgress) onProgress(10, 'Téléchargement...');

            // 1. Télécharger le binaire (PDF ou Audio) avec fallback CORS automatique
            const response = await fetchMediaWithFallback(meta);
            const contentLength = parseInt(response.headers.get('content-length') || '0', 10);
            let blob;

            if (response.body && contentLength > 0 && onProgress) {
                const reader = response.body.getReader();
                const chunks = [];
                let received = 0;
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    chunks.push(value);
                    received += value.length;
                    const pct = Math.min(90, Math.round((received / contentLength) * 85) + 10);
                    onProgress(pct, `${pct}%`);
                }
                const fallbackType = meta.categorie === 'son' ? 'audio/mpeg' : 'application/pdf';
                blob = new Blob(chunks, { type: response.headers.get('content-type') || fallbackType });
            } else {
                blob = await response.blob();
                if (onProgress) onProgress(85, '85%');
            }

            // 2. Récupérer la miniature de la 1re page en Base64 pour les PDF
            let thumbDataUrl = meta.thumbDataUrl || null;
            if (!thumbDataUrl && meta.categorie !== 'son') {
                try {
                    const tRes = await fetch(thumbUrl);
                    if (tRes.ok) {
                        const tBlob = await tRes.blob();
                        thumbDataUrl = await blobToDataURL(tBlob);
                    }
                } catch (e) {}
            }

            // 3. Mettre en cache les pages clés dans CacheStorage
            if ('caches' in window) {
                try {
                    const cache = await caches.open(CACHE_NAME);
                    await Promise.allSettled([
                        cache.add(readUrl),
                        cache.add('/telechargements/'),
                        cache.add('/offline/'),
                    ]);
                } catch (e) {}
            }

            // 4. Stocker dans IndexedDB avec Catégorie + Sous-Catégorie + Dossier
            const record = {
                key: key,
                categorie: String(meta.categorie),
                sousCategorie: sousCategorie,
                dossier: dossier,
                id: String(meta.id),
                titre: meta.titre || 'Document Sacré',
                auteur: meta.auteur || 'Cheikh Ahmadou Bamba',
                readUrl: readUrl,
                mediaUrl: mediaUrl,
                thumbUrl: thumbUrl,
                thumbDataUrl: thumbDataUrl,
                blob: blob,
                sizeBytes: blob.size,
                savedAt: Date.now(),
            };

            const db = await openVaultDB();
            await new Promise((resolve, reject) => {
                const tx = db.transaction(STORE_NAME, 'readwrite');
                tx.objectStore(STORE_NAME).put(record);
                tx.oncomplete = () => resolve();
                tx.onerror = (e) => reject(e.target.error);
            });

            // 5. Synchroniser l'historique côté serveur si connecté
            fetch(`/telechargements/ajouter/${meta.categorie}/${meta.id}/`, {
                method: 'GET',
                headers: { 'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json' },
                credentials: 'same-origin'
            }).catch(() => {});

            if (onProgress) onProgress(100, 'Disponible hors-ligne');
            return record;
        },

        async storeExistingBlob(meta, blob) {
            try {
                const key = `${meta.categorie}_${meta.id}`;
                const db = await openVaultDB();
                const existing = await this.getItem(meta.categorie, meta.id);
                const sousCategorie = (meta.sousCategorie || (existing && existing.sousCategorie) || String(meta.categorie).toUpperCase()).toUpperCase();
                const dossier = (meta.dossier || (existing && existing.dossier)) || computeDefaultFolder({ ...meta, sousCategorie });
                const record = {
                    key: key,
                    categorie: String(meta.categorie),
                    sousCategorie: sousCategorie,
                    dossier: dossier,
                    id: String(meta.id),
                    titre: meta.titre || (existing && existing.titre) || 'Manuscrit Sacré',
                    auteur: meta.auteur || (existing && existing.auteur) || 'Cheikh Ahmadou Bamba',
                    readUrl: meta.readUrl || `/lire/${meta.categorie}/${meta.id}/`,
                    mediaUrl: meta.mediaUrl || `/proxy-pdf/${meta.categorie}/${meta.id}/`,
                    thumbUrl: meta.thumbUrl || `/thumb-pdf/${meta.categorie}/${meta.id}/`,
                    thumbDataUrl: (existing && existing.thumbDataUrl) || null,
                    blob: blob,
                    sizeBytes: blob.size,
                    savedAt: Date.now(),
                };
                await new Promise((resolve, reject) => {
                    const tx = db.transaction(STORE_NAME, 'readwrite');
                    tx.objectStore(STORE_NAME).put(record);
                    tx.oncomplete = () => resolve();
                    tx.onerror = (e) => reject(e.target.error);
                });
                if ('caches' in window) {
                    const cache = await caches.open(CACHE_NAME);
                    cache.add(record.readUrl).catch(() => {});
                }
                return true;
            } catch (e) {
                return false;
            }
        },

        async getItem(categorie, id) {
            try {
                const db = await openVaultDB();
                const key = `${categorie}_${id}`;
                return await new Promise((resolve) => {
                    const tx = db.transaction(STORE_NAME, 'readonly');
                    const req = tx.objectStore(STORE_NAME).get(key);
                    req.onsuccess = () => resolve(req.result || null);
                    req.onerror = () => resolve(null);
                });
            } catch (e) {
                return null;
            }
        },

        async getOfflineArrayBuffer(categorie, id) {
            const item = await this.getItem(categorie, id);
            if (item && item.blob) {
                return await item.blob.arrayBuffer();
            }
            return null;
        },

        async isSaved(categorie, id) {
            const item = await this.getItem(categorie, id);
            return Boolean(item && item.blob);
        },

        async listAll() {
            try {
                const db = await openVaultDB();
                return await new Promise((resolve) => {
                    const tx = db.transaction(STORE_NAME, 'readonly');
                    const req = tx.objectStore(STORE_NAME).getAll();
                    req.onsuccess = () => {
                        const list = (req.result || []).map(item => ({
                            ...item,
                            sousCategorie: item.sousCategorie || (item.categorie === 'son' ? 'KHASSIDA' : String(item.categorie || '').toUpperCase()),
                            dossier: item.dossier || computeDefaultFolder(item)
                        }));
                        list.sort((a, b) => (b.savedAt || 0) - (a.savedAt || 0));
                        resolve(list);
                    };
                    req.onerror = () => resolve([]);
                });
            } catch (e) {
                return [];
            }
        },

        async getSavedKeysSet() {
            const all = await this.listAll();
            return new Set(all.map(x => x.key));
        },

        async moveToFolder(categorie, id, newFolderName) {
            const cleanFolder = String(newFolderName || '').trim();
            if (!cleanFolder) return false;
            const existing = await this.getItem(categorie, id);
            if (!existing) return false;
            existing.dossier = cleanFolder;
            const db = await openVaultDB();
            await new Promise((resolve, reject) => {
                const tx = db.transaction(STORE_NAME, 'readwrite');
                tx.objectStore(STORE_NAME).put(existing);
                tx.oncomplete = () => resolve();
                tx.onerror = (e) => reject(e.target.error);
            });
            this.createFolder(cleanFolder, existing.categorie);
            return true;
        },

        getCustomFolders() {
            return readCustomFolders();
        },

        createFolder(name, mediaType = 'all') {
            const clean = String(name || '').trim();
            if (!clean) return null;
            const list = readCustomFolders();
            const exists = list.find(f => f.name.toLowerCase() === clean.toLowerCase());
            if (!exists) {
                list.push({ name: clean, mediaType: mediaType || 'all', createdAt: Date.now() });
                writeCustomFolders(list);
            }
            return clean;
        },

        deleteCustomFolder(name) {
            const list = readCustomFolders().filter(f => f.name.toLowerCase() !== String(name || '').toLowerCase());
            writeCustomFolders(list);
        },

        async removeItem(categorie, id) {
            try {
                const db = await openVaultDB();
                const key = `${categorie}_${id}`;
                await new Promise((resolve) => {
                    const tx = db.transaction(STORE_NAME, 'readwrite');
                    tx.objectStore(STORE_NAME).delete(key);
                    tx.oncomplete = () => resolve();
                    tx.onerror = () => resolve();
                });
                return true;
            } catch (e) {
                return false;
            }
        },

        showToast(message, isSuccess = true) {
            let toast = document.getElementById('sdm-offline-toast');
            if (!toast) {
                toast = document.createElement('div');
                toast.id = 'sdm-offline-toast';
                toast.style.cssText = 'position:fixed;bottom:92px;left:50%;transform:translateX(-50%);z-index:99999;padding:11px 18px;border-radius:16px;font-family:Inter,sans-serif;font-size:12px;font-weight:700;display:flex;align-items:center;gap:8px;box-shadow:0 14px 35px rgba(0,0,0,0.75);transition:opacity 0.25s,transform 0.25s;';
                document.body.appendChild(toast);
            }
            toast.style.background = isSuccess ? 'rgba(6, 48, 32, 0.96)' : 'rgba(68, 18, 18, 0.96)';
            toast.style.border = isSuccess ? '1px solid #10B981' : '1px solid #F87171';
            toast.style.color = '#FFFFFF';
            toast.innerHTML = `<i class="fa-solid ${isSuccess ? 'fa-circle-check' : 'fa-triangle-exclamation'}" style="color:${isSuccess ? '#34D399' : '#F87171'};"></i><span>${message}</span>`;
            toast.style.opacity = '1';
            clearTimeout(window._sdmToastTimer);
            window._sdmToastTimer = setTimeout(() => {
                toast.style.opacity = '0';
            }, 3200);
        }
    };

    window.SDMOfflineVault = SDMOfflineVault;
})();
