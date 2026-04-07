from collections import OrderedDict


class LRUCache:
    """
    A simple least-recently used (LRU) cache.

    The cache stores up to 'capacity' items. When the cache is full and a new item
    is inserted, the least recently used item is evicted.
    """

    def __init__(self, capacity=100):
        self.capacity = capacity
        self._entries = OrderedDict()

    def get(self, key):
        """
        Return the cached value for `key` if present, otherwise None.

        If the key exists, it is marked as recently used.
        """

        if key not in self._entries:
            return None

        self._entries.move_to_end(key)

        return self._entries[key]

    def put(self, key, value):
        """
        Insert or update a cache entry.

        If the key already exists, update it and mark it as recently used.
        If the cache is full, evict the least recently used item first.
        """

        if key in self._entries:
            self._entries.move_to_end(key)
            self._entries[key] = value
            return

        if len(self._entries) >= self.capacity:
            self._entries.popitem(last=False)

        self._entries[key] = value
