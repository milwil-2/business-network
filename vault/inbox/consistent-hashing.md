# Consistent Hashing

Consistent hashing is a distributed hashing technique where keys and nodes are both mapped onto a circular hash ring. Adding or removing a node only remaps a fraction (1/n) of keys, unlike traditional modulo hashing which remaps nearly all keys.

Used in distributed caches (Amazon DynamoDB, Apache Cassandra), load balancers, and CDNs. Virtual nodes (vnodes) improve load distribution by assigning each physical node multiple positions on the ring.
