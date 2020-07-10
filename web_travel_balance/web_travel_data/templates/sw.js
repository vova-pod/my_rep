const VERSION = '{{ version }}';

const FILES_TO_CACHE = [  
  "{% url 'web_travel_data:offline' %}",
];
var CACHE_NAME = 'my-site-cache-v1';


self.addEventListener('install', (event) => {  
console.log('[SW] Installing SW version:', VERSION);  
event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[ServiceWorker] Pre-caching offline page');
      return cache.addAll(FILES_TO_CACHE);
    })
)
});

self.addEventListener('fetch', function(event) {
  if (event.request.mode !== 'navigate') {
  // Not a page navigation, bail.
  return;
}
event.respondWith(
    fetch(event.request)
        .catch(() => {
          return caches.open(CACHE_NAME)
              .then((cache) => {
                return cache.match("{% url 'web_travel_data:offline' %}");
              });
        })
);
});
