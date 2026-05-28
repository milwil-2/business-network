# LRU Cache

An LRU (Least Recently Used) cache is a data structure that evicts the least recently used item when it reaches capacity. Classic implementation uses a doubly linked list + hash map for O(1) get and put.

Used extensively in databases (buffer pool), operating systems (page replacement), and CDN edge caches. Redis supports LRU eviction policy natively. The variant LFU (Least Frequently Used) evicts the item with the fewest accesses instead.
