// Guru-600: the editor as an installable application, which also works offline (16/11/2026, Marc).
// At the site's root so that it covers editor/ and guide/ (the editor's ? opens ../guide/); nothing else on the site is touched.
// Online: always the network (the latest editor), and the copy kept up to date; offline: the copy.
// make_site_guru.py fills FILES and VERSION (a hash of the files: a new editor installs a new worker, and its files at once).
const VERSION = "__VERSION__";
const FILES = __FILES__;
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
  e.respondWith(fetch(r).then((res) => {
    if (res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(r, copy)); }
    return res;
  }).catch(() => caches.match(r, { ignoreSearch: true }).then((m) => m || caches.match(r.url.split("?")[0] + "index.html"))
    .then((m) => m || Response.error())));
});
