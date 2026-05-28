# Hash Tables

Hash tables are a fundamental data structure that maps keys to values using a hash function. They provide O(1) average-case lookup, insert, and delete. The hash function converts a key into an array index. Collisions (two keys hashing to same index) are handled via chaining (linked list at each slot) or open addressing (probe for next empty slot).

Common variants include the unordered_map in C++, HashMap in Java, and dict in Python. Linear probing and quadratic probing are open addressing techniques. Load factor affects performance — rehashing occurs when load factor exceeds a threshold.

Consistent hashing is a variant used in distributed systems to minimize remapping when nodes are added or removed.
