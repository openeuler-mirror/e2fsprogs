Name:           e2fsprogs
Version:        1.45.6
Release:        7
Summary:        Second extended file system management tools
License:        GPLv2 and LGPLv2 and GPLv2+
URL:            http://e2fsprogs.sourceforge.net/
Source0:        https://www.kernel.org/pub/linux/kernel/people/tytso/%{name}/v%{version}/%{name}-%{version}.tar.xz

Patch1:      0001-e2fsprogs-set-hugefile-from-4T-to-1T-in-hugefile-tes.patch
Patch2:      0002-e2fsck-fix-off-by-one-check-when-validating-depth-of.patch
Patch3:      0003-mke2fs-fix-up-check-for-hardlinks-always-false-if-in.patch
Patch4:      0004-add-device-check-in-ismount-process.patch
Patch5:      0005-libss-add-newer-libreadline.so.8-to-dlopen-path.patch

Patch6:		0006-e2fsck-fix-indexed-dir-rehash-failure-with-metadata_.patch
Patch7:		0007-libext2fs-retry-reading-superblock-on-open-when-chec.patch
Patch8:		0008-libext2fs-fix-potential-buffer-overrun-in-__get_dire.patch
Patch9:		0009-tune2fs-reset-MMP-state-on-error-exit.patch
Patch10:	0010-e2fsck-use-size_t-instead-of-int-in-string_copy.patch
Patch11:	0011-libext2fs-fix-incorrect-negative-error-return-in-uni.patch
Patch12:	0012-debugfs-fix-double-free-in-realloc-error-path-in-rea.patch
Patch13:	0013-tune2fs-fix-resource-leak-in-handle_quota_options.patch
Patch14:	0014-libext2fs-fix-UBSAN-warning-in-ext2fs_mmp_new_seq.patch
Patch15:	0015-libext2fs-fix-segault-when-setting-an-xattr-with-an-.patch
Patch16:	0016-mke2fs-fix-a-importing-a-directory-with-an-ACL-and-i.patch
Patch17:	0017-mke2fs-fix-resource-leak-on-error-path-when-creating.patch
Patch18:	0018-libext2fs-fix-incorrect-error-code-return-in-ext2fs_.patch
Patch19:	0019-debugfs-fix-memory-allocation-failures-when-parsing-.patch
Patch20:	0020-debugfs-fix-logdump-on-file-systems-with-block-sizes.patch
Patch21:	0021-libext2fs-fix-crash-when-ext2fs_mmp_stop-is-called-b.patch
Patch22:	0022-debugfs-fix-dump_metadata_block-for-block-sizes-8192.patch
Patch23:	0023-debugfs-fix-memory-leak-problem-in-read_list.patch
Patch24:	0024-debugfs-fix-rdump-and-ls-to-handle-uids-and-gids-655.patch
Patch25:	0025-e2image-fix-overflow-in-l2-table-processing.patch
Patch26:	0026-e2fsck-fix-last-mount-write-time-when-e2fsck-is-forc.patch
Patch27:	0027-profile_create_node-set-magic-before-strdup-name-to-.patch
Patch28:	0028-tdb_transaction_recover-fix-memory-leak.patch
Patch29:	0029-zap_sector-fix-memory-leak.patch
Patch30:	0030-misc-fix-potential-segmentation-fault-problem-in-sca.patch
Patch31:	0031-ext2ed-fix-potential-NULL-pointer-dereference-in-dup.patch
Patch32:	0032-ss_add_info_dir-fix-error-handling-when-memory-alloc.patch
Patch33:	0033-ss_create_invocation-fix-error-handling-when-memory-.patch
Patch34:	0034-ss_create_invocation-fix-potential-unititalized-refe.patch
Patch35:	0035-libext2fs-fix-unexpected-NULL-variable.patch
Patch36:	0036-libsupport-fix-potental-NULL-pointer-dereferences-in.patch
Patch37:	0037-libext2fs-fix-coverity-nits-in-tdb.c.patch

BuildRequires:  gcc pkgconfig texinfo
BuildRequires:  fuse-devel libblkid-devel libuuid-devel
BuildRequires:  audit
Recommends:	%{name}-help = %{version}-%{release}

Provides:       e2fsprogs-libs%{?_isa} e2fsprogs-libs
Obsoletes:      e2fsprogs-libs
Provides:       libcom_err%{?_isa} libcom_err
Obsoletes:      libcom_err
Provides:       libss%{?_isa} libss
Obsoletes:      libss

%description
The e2fsprogs package consists of a lot of tools for users to create,
check, modify, and correct any inconsistencies in second extended file
system.

%package devel
Summary: Second extended file system libraries and headers
License: GPLv2 and LGPLv2 and MIT
Requires: e2fsprogs = %{version}-%{release}
Requires: gawk
Requires: pkgconfig
Requires(post): info
Requires(preun): info
Provides: libcom_err-devel%{?_isa} libcom_err-devel
Obsoletes: libcom_err-devel
Provides: libss-devel%{?_isa} libss-devel
Obsoletes: libss-devel
Provides: e2fsprogs-static{?_isa} e2fsprogs-static
Obsoletes: e2fsprogs-static

%description devel
This package provides libraries and header files to develop
second extended file system userspace programs.

%package help
Summary: man files for e2fsprogs
Requires: man
BuildArch: noarch

%description help
This packages includes man files for e2fsprogs.

%prep
%autosetup -n %{name}-%{version} -p1


%build
%configure CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" \
           --enable-elf-shlibs --enable-nls --disable-uuidd --disable-fsck \
           --disable-e2initrd-helper --disable-libblkid --disable-libuuid \
           --enable-quota --with-root-prefix=/usr
%make_build V=1

%install
make install install-libs DESTDIR=%{buildroot} INSTALL="%{__install} -p" \
    root_sbindir=%{_sbindir} root_libdir=%{_libdir}
chmod +w %{buildroot}%{_libdir}/*.a

%find_lang %{name}

rm -f %{buildroot}/etc/cron.d/e2scrub_all
rm -f %{buildroot}%{_libdir}/e2fsprogs/e2scrub_all_cron

%check
make fullcheck

%ldconfig_scriptlets

%post devel
if [ -f %{_infodir}/libext2fs.info.gz ]; then
   /sbin/install-info %{_infodir}/libext2fs.info.gz %{_infodir}/dir || :
fi

%preun devel
if [ $1 = 0 -a -f %{_infodir}/libext2fs.info.gz ]; then
   /sbin/install-info --delete %{_infodir}/libext2fs.info.gz %{_infodir}/dir || :
fi
exit 0

%files -f %{name}.lang
%doc README
%license NOTICE
%config(noreplace) /etc/mke2fs.conf
%config(noreplace) /etc/e2scrub.conf
%{_bindir}/chattr
%{_bindir}/fuse2fs
%{_bindir}/lsattr
%{_libdir}/e2fsprogs/e2scrub_fail
%{_libdir}/libe2p.so.*
%{_libdir}/libext2fs.so.*
%{_libdir}/libcom_err.so.*
%{_libdir}/libss.so.*
%{_sbindir}/*
%{_udevrulesdir}/*.rules
%{_unitdir}/e2scrub*

%files devel
%{_bindir}/compile_et
%{_bindir}/mk_cmds
%{_datadir}/et
%{_datadir}/ss
%{_infodir}/libext2fs.info*
%{_includedir}/e2p
%{_includedir}/ext2fs
%{_includedir}/et
%{_includedir}/com_err.h
%{_includedir}/ss
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_libdir}/*.a

%files help
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%changelog
* Mon Nov 15 2021 zhanchengbin <zhanchengbin1@huawei.com> - 1.45.6-7
- DESC: integrate community patches.

* Sun Sep 13 2021 lixiaokeng <lixiaokeng@huawei.com> - 1.45.6-6
- DESC: add newer libreadline.so.8 to dlopen path

* Fri Aug 20 2021 chenyanpanHW <chenyanpan@huawei.com> - 1.45.6-5
- DESC: add necessary BuildRequires audit

* Thu Aug 5 2021 wuguanghao<wuguanghao3@huawei.com> - 1.45.6-4
- DESC: delete -Sgit from %autosetup, and delete BuildRequire git  

* Wed Dec 16 2020 yanglongkang <yanglongkang@huawei.com> - 1.45.6-1
- Set help package as install require
  backport upstream patches-epoch2 to fix some problems

* Fri Apr 17 2020 luoshijie <luoshijie1@huawei.com> - 1.45.6-0
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:update package to 1.45.6.

* Thu Mar 5 2020 luoshijie <luoshijie1@huawei.com> - 1.45.3-6
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:remove soft link RELEASE-NOTES from rpm, because this one
       is no need to be packaged.

* Fri Feb 28 2020 luoshijie <luoshijie1@huawei.com> - 1.45.3-5
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:sync bugfix patch from next.
       add device check in ismount process.

* Mon Feb 3 2020 luoshijie <luoshijie1@huawei.com> - 1.45.3-4
- Type:cves
- ID:CVE-2019-5094
- SUG:restart
- DESC:backport patch to fix CVE-2019-5094.

* Wed Jan 22 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.45.3-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:change path to remove no used file.

* Wed Jan 22 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.45.3-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix local rpmbuild error.

* Mon Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.45.3-1
- Type:cves
- ID:CVE-2019-5188
- SUG:restart
- DESC:backport patch to fix CVE-2019-5188.

* Mon Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.45.3-0
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update package from 1.44.3 to 1.45.3.

* Mon Jan 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.44.3-8
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update spec.

* Wed Sep 18 2019 luoshijie <luoshijie1@huawei.com> - 1.44.3-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:modify spec file to follow spec rules.

* Fri Sep 6 2019 luoshijie <luoshijie1@huawei.com> - 1.44.3-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:openEuler Debranding

* Tue Aug 20 2019 luoshijie <luoshijie1@huawei.com> - 1.44.3-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:rename patch name

* Wed Jul 10 2019 zhangyujing <zhangyujing1@huawei.com> - 1.44.3-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:e2freefrag: fix memory leak in scan_online()
       create_inode: fix potential memory leak in path_append()
       mke2fs: fix check for absurdly large devices

* Fri Mar 15 2019 zhangyujing <zhangyujing1@huawei.com> - 1.44.3-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:blkid avoid FPE crash when probing a HFS superblock
       AOSP e2fsdroid Fix crash with invalid command line a
       e2fsck fix fd leak in reserve_stdio_fds
       libext2fs fix uninitialized length in rep_strdup
       tune2fs fix dereference of freed memory after journa
       libe2p avoid segfault when s_nr_users is too high
       e2freefrag fix free blocks count during live scan

* Wed Jan 23 2019 wangxiao <wangxiao65@huawei.com> - 1.44.3-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:disable the metadata_csum creat by mke2fs -t ext4 by default
- Package init

