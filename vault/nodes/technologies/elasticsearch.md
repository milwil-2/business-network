---
id: elasticsearch
label: Elasticsearch
node_type: Technology
tags: [search, nosql, Technology]
summary: "Distributed full-text search and analytics engine built on Apache Lucene. Stores JSON documents, indexes every field by default, and supports full-text search, aggregations, and vector search (kNN)."
properties:
  created_by: "Elastic NV"
  first_release: 2010
  license: "Elastic License 2.0 / SSPL"
  written_in: "Java"
relationships:
  - type: IMPLEMENTS
    target: index
  - type: RELATED_TO
    target: postgres
---

Elasticsearch is the standard for full-text search, log analysis (ELK stack), and vector similarity search. Every indexed document field becomes a searchable inverted index automatically.

## When to use Elasticsearch over Postgres

- Full-text search with relevance scoring (BM25)
- High-volume log ingestion (Kibana dashboards)
- Faceted search with complex aggregations
- kNN vector search for semantic similarity (RAG pipelines)

## Relevance to graph DBs

Elasticsearch is often used alongside Neo4j: Neo4j handles relationship traversal, Elasticsearch handles full-text search over node content. You search ES to find candidate nodes, then traverse in Neo4j.

See also: [[index]], [[postgres]]
