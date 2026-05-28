---
id: hash-table
label: Hash Table
node_type: Concept
tags: [data-structures, hashing, Concept]
summary: "A data structure that maps keys to values using a hash function, giving average O(1) lookup, insertion, and deletion."
relationships:
  - type: RELATED_TO
    target: big-o-notation
  - type: RELATED_TO
    target: index
---

A hash table stores key-value pairs in an array of buckets. A **hash function** converts each key into a bucket index, allowing the table to find a value without scanning every entry. On average this yields O(1) lookup, insertion, and deletion — the property that makes hash tables ubiquitous.

Two distinct keys can hash to the same bucket, a **collision**. Common resolution strategies are *separate chaining* (each bucket holds a linked list) and *open addressing* (probe for the next free slot). When the load factor grows too high, the table is *resized* and all entries are rehashed.

Hash tables underpin dictionaries, sets, caches, and database hash [[index]] structures. Their performance depends on a good hash function and is analyzed with [[big-o-notation]]; in the worst case all keys collide and operations degrade to O(n).
