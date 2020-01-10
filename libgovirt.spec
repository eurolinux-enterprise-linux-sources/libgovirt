# -*- rpm-spec -*-

%global with_gir 0

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%global with_gir 1
%endif

Summary: A GObject library for interacting with oVirt REST API
Name: libgovirt
Version: 0.3.3
Release: 5%{?dist}%{?extra_release}
License: LGPLv2+
Group: Development/Libraries
Source: http://ftp.gnome.org/pub/GNOME/sources/libgovirt/0.3/%{name}-%{version}.tar.xz
URL: http://people.freedesktop.org/~teuf/govirt/
Patch0001: 0001-collection-unref-the-resource-instead-of-the-resourc.patch
Patch0002: 0002-proxy-Document-OvirtProxy-properties.patch
Patch0003: 0003-proxy-Readd-additional-header-API.patch
Patch0004: 0004-proxy-Add-OvirtProxy-sso-token.patch
Patch0005: 0005-proxy-Remove-jsessionid-cookie-when-its-value-is-NUL.patch
Patch0006: 0006-proxy-Only-set-Prefer-persistent-auth-with-jsession-.patch
Patch0007: 0007-proxy-Fix-persistent-session-with-oVirt-3.6.patch
Patch0008: 0008-Force-use-of-v3-REST-API.patch
Patch0009: 0009-New-storage-format-added-in-oVirt-4.1.patch
Patch0010: 0010-proxy-Fix-bug-in-cancelled-disconnection-after-async.patch
Patch0011: 0011-proxy-Hold-reference-to-cancellable-object.patch
Patch0012: 0012-proxy-Check-if-operation-is-cancelled-before-disconn.patch

BuildRequires: glib2-devel
BuildRequires: intltool
BuildRequires: rest-devel >= 0.7.92
%if %{with_gir}
BuildRequires: gobject-introspection-devel
%endif

%description
libgovirt is a library that allows applications to use oVirt REST API
to list VMs managed by an oVirt instance, and to get the connection
parameters needed to make a SPICE/VNC connection to them.

%package devel
Summary: Libraries, includes, etc. to compile with the libgovirt library
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: glib2-devel

%description devel
libgovirt is a library that allows applications to use oVirt REST API
to list VMs managed by an oVirt instance, and to get the connection
parameters needed to make a SPICE/VNC connection to them.

Libraries, includes, etc. to compile with the libgovirt library

%prep
%autosetup -S git_am

%build
%if %{with_gir}
%global gir_arg --enable-introspection=yes
%else
%global gir_arg --enable-introspection=no
%endif

%configure %{gir_arg}
%__make %{?_smp_mflags} V=1

%install
%__make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
%find_lang %{name} --with-gnome

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc AUTHORS COPYING MAINTAINERS README
%{_libdir}/%{name}.so.2*
%if %{with_gir}
%{_libdir}/girepository-1.0/GoVirt-1.0.typelib
%endif

%files devel
%{_libdir}/%{name}.so
%dir %{_includedir}/govirt-1.0/
%dir %{_includedir}/govirt-1.0/govirt/
%{_includedir}/govirt-1.0/govirt/*.h
%{_libdir}/pkgconfig/govirt-1.0.pc
%if %{with_gir}
%{_datadir}/gir-1.0/GoVirt-1.0.gir
%endif

%changelog
* Mon Mar 13 2017 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 0.3.3-5
- New storage format added in oVirt 4.1
  Resolves: rhbz#1346215
- Check if operation was cancelled before disconnecting signal
  Resolves: rhbz#1431275

* Fri Jul 01 2016 Christophe Fergeau <cfergeau@redhat.com> - 0.3.3-4
- Add upstream patch forcing use of the older v3 REST API as we don't support
  yet the v4 API
  Resolves: rhbz#1346215

* Tue Jun 14 2016 Christophe Fergeau <cfergeau@redhat.com> - 0.3.3-3
- Add upstream patch fixing unwanted authentication dialog for foreign menu
  when using remote-viewer ovirt://
  Resolves: rhbz#1346256

* Mon Jan 04 2016 Fabiano Fidêncio <fidencio@redhat.com> 0.3.3-2
- Fix crash when VM has several ISO domains
  Resolves: rhbz#1274356
- Add OvirtProxy::sso-token support for oVirt 4.0
  Resolves: rhbz#1324457

* Tue May 12 2015 Christophe Fergeau <cfergeau@redhat.com> 0.3.3-1
- Rebase to 0.3.3
  Resolves: rhbz#1214234

* Fri Oct 10 2014 Christophe Fergeau <cfergeau@redhat.com> 0.3.1-3
- Add upstream patch allowing to remove CD images from an OvirtCdrom
  Resolves: rhbz#1151171

* Tue Sep 30 2014 Christophe Fergeau <cfergeau@redhat.com> 0.3.1-2
- Requires a new enough librest as we use symbols not available in older
  librest
  Related: rhbz#1116844

* Mon Sep 08 2014 Christophe Fergeau <cfergeau@redhat.com> 0.3.1-1
- Rebase to libgovirt 0.3.1.
  Resolves: rhbz#1116844

* Mon Jul  7 2014 Marc-Andre Lureau <marcandre.lureau@redhat.com> - 0.3.0-1
- Rebase to libgovirt 0.3.0.
  Resolves: rhbz#1116844

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.1.0-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.1.0-2
- Mass rebuild 2013-12-27

* Tue Jun 11 2013 Christophe Fergeau <cfergeau@redhat.com> 0.1.0-1
- Update to upstream release 0.1.0

* Mon Mar 11 2013 Christophe Fergeau <cfergeau@redhat.com> 0.0.3-2
- Removed definition of BuildRoot and cleanup of BuildRoot in %clean
- Added missing arch to versioned Requires: %%{name} in the -devel package
- Don't include empty NEWS and ChangeLog in built RPM

* Wed Feb 20 2013 Christophe Fergeau <cfergeau@redhat.com> 0.0.3-1
- Initial import of libgovirt 0.0.3


