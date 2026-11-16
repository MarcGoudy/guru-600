// Guru-600: the editor as an installable application, which also works offline (16/11/2026, Marc).
// At the site's root so that it covers editor/ and guide/ (the editor's ? opens ../guide/); nothing else on the site is touched.
// Online: always the network (the latest editor), and the copy kept up to date; offline: the copy.
// make_site_guru.py fills FILES and VERSION (a hash of the files: a new editor installs a new worker, and its files at once).
const VERSION = "b04703632186c99e";
const FILES = [
"editor/",
"guide/",
"editor/fm1ota.js",
"editor/fm1pkg.js",
"editor/fonts/BarlowCondensed-Bold.ttf",
"editor/fonts/BarlowCondensed-SemiBold.ttf",
"editor/fonts/Guru600.woff2",
"editor/fonts/MonRong-licence.txt",
"editor/fonts/MonRong.ttf",
"editor/fonts/OFL-Barlow.txt",
"editor/guru-allsounds.js",
"editor/guru-app.js",
"editor/guru-arp.js",
"editor/guru-backup.js",
"editor/guru-backupio.js",
"editor/guru-dialog.js",
"editor/guru-families.js",
"editor/guru-fx.js",
"editor/guru-gloss.js",
"editor/guru-guide-ch.js",
"editor/guru-i18n.js",
"editor/guru-labels.js",
"editor/guru-link.js",
"editor/guru-mod.js",
"editor/guru-projects.js",
"editor/guru-sampleio.js",
"editor/guru-samples.js",
"editor/guru-seq.js",
"editor/guru-settings.js",
"editor/guru-song.js",
"editor/guru-tips.js",
"editor/guru-tracks.js",
"editor/guru-tx.js",
"editor/icons/icon-180.png",
"editor/icons/icon-192.png",
"editor/icons/icon-32.png",
"editor/icons/icon-512.png",
"editor/icons/maskable-512.png",
"editor/index.html",
"editor/manifest.webmanifest",
"guide/fonts/InterTight.ttf",
"guide/fonts/MonRong-licence.txt",
"guide/fonts/MonRong.ttf",
"guide/fonts/OFL-InterTight.txt",
"guide/index.html",
"guide/shots/de/fx.jpg",
"guide/shots/de/settings.jpg",
"guide/shots/en/arp.jpg",
"guide/shots/en/backup.jpg",
"guide/shots/en/cover.jpg",
"guide/shots/en/fx.jpg",
"guide/shots/en/header.jpg",
"guide/shots/en/keyboard.jpg",
"guide/shots/en/mod.jpg",
"guide/shots/en/morph.jpg",
"guide/shots/en/projects.jpg",
"guide/shots/en/samples.jpg",
"guide/shots/en/seq.jpg",
"guide/shots/en/settings.jpg",
"guide/shots/en/song.jpg",
"guide/shots/en/sound.jpg",
"guide/shots/en/sounds.jpg",
"guide/shots/en/tracks.jpg",
"guide/shots/es/fx.jpg",
"guide/shots/es/settings.jpg",
"guide/shots/fr/fx.jpg",
"guide/shots/fr/settings.jpg",
"guide/shots/it/fx.jpg",
"guide/shots/it/settings.jpg",
"guide/shots/ja/fx.jpg",
"guide/shots/ja/settings.jpg",
"guide/shots/zh/fx.jpg",
"guide/shots/zh/settings.jpg"
];
const CACHE = "guru600-editor-" + VERSION;
const PATHS = ["editor/", "guide/"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys()
    .then((ks) => Promise.all(ks.filter((k) => k.startsWith("guru600-editor-") && k !== CACHE).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener("fetch", (e) => {
  const r = e.request;
  if (r.method !== "GET") return;
  const u = new URL(r.url), base = new URL(self.registration.scope);
  if (u.origin !== base.origin || !PATHS.some((p) => u.pathname.startsWith(base.pathname + p))) return;
  e.respondWith(fetch(r, { cache: "no-cache" }).then((res) => {   // (no-cache: checked with the server each time, never an old copy)
    if (res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(r, copy)); }
    return res;
  }).catch(() => caches.match(r, { ignoreSearch: true }).then((m) => m || caches.match(r.url.split("?")[0] + "index.html"))
    .then((m) => m || Response.error())));
});
