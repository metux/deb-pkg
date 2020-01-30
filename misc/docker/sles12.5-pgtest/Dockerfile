FROM metux/sles12.5-devel

ADD files/upload/zyprepo/		/var/lib/zyprepo/pg12/
ADD files/etc/zypp/repos.d/pg12.repo	/etc/zypp/repos.d/

## postgresql12-base / dev
#ADD files/etc/zypp/repos.d/pgdg-12.repo      /etc/zypp/repos.d/pgdg-12.repo
#ADD files/etc/zypp/repos.d/pgdg-12-srpm.repo /etc/zypp/repos.d/pgdg-12-srpm.repo
#RUN wget https://download.postgresql.org/pub/repos/zypp/12/suse/sles-12.4-x86_64/repodata/repomd.xml.key && \
#    rpm --import repomd.xml.key && \
#    rm -f repomd.xml.key && \
#    wget https://download.postgresql.org/pub/repos/zypp/srpms/12/suse/sles-12-x86_64/repodata/repomd.xml.key && \
#    rpm --import repomd.xml.key && \
#    rm -f repomd.xml.key && \
#    zypper refresh

RUN find /var/lib/zyprepo
RUN find /etc/zypp/repos.d

RUN zypper refresh

#COPY files/rebuild-src-rpm /
#COPY files/entrypoint.sh   /
# ENTRYPOINT [ "/entrypoint.sh" ]

ENTRYPOINT [ "/sbin/init" ]
CMD [ "/sbin/init" ]
