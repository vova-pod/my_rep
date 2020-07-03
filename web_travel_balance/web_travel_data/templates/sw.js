const VERSION = '{{ version }}';
const staticCachePrefix = 'static';
const staticCacheName = `${staticCachePrefix}-${VERSION}`;
const dynamicCacheName = 'dynamic';


self.addEventListener('install', (event) => {
    console.log('[SW] Installing SW version:', VERSION);
});
