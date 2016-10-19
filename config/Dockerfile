# Dockerfile for Building OrientDB Container for Bacch
FROM orientdb:latest
MAINTAINER Kenneth P. J. Dyer <kenneth@avoceteditors.com>

ENV ORIENTDB_ROOT_PASSWORD mybacchpasswd

RUN mkdir -k /bacch/document
RUN mkdir /bacch/data
RUN mkdir /bacch/tmp

VOLUME ["/bacch/document", "/bacch/data", "/bacch/tmp"]
