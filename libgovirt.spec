# -*- rpm-spec -*-

%global with_gir 0

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%global with_gir 1
%endif

Summary: A GObject library for interacting with oVirt REST API
Name: libgovirt
Version: 0.3.2
Release: 2%{?dist}%{?extra_release}
License: LGPLv2+
Group: Development/Libraries
Source: http://ftp.gnome.org/pub/GNOME/sources/libgovirt/0.3/%{name}-%{version}.tar.xz
Patch0: 0001-Add-fallback-for-G_DEPRECATED_FOR-in-older-glib.patch
Patch1: 0002-storage-domain-Silence-warning-during-XML-parsing.patch
Patch2: 0003-Access-oVirt-API-through-ovirt-engine-api-rather-tha.patch
Patch3: 0004-ovirt-proxy-Do-not-handle-REST_PROXY_ERROR_CANCELLED.patch
Patch4: 0005-proxy-Fix-bug-in-cancelled-disconnection-after-async.patch
Patch5: 0006-collection-unref-the-resource-instead-of-the-resourc.patch
Patch6: 0007-vm-Don-t-print-ticket-value-to-stdout.patch
Patch7: 0008-Add-OvirtVmDisplay-proxy-url.patch
URL: http://people.freedesktop.org/~teuf/govirt/
BuildRequires: glib2-devel
BuildRequires: intltool
BuildRequires: rest-devel >= 0.7.92
%if %{with_gir}
BuildRequires: gobject-introspection-devel
%endif
Requires: rest >= 0.7.92

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
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

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
* Thu Dec 17 2015 Christophe Fergeau <cfergeau@redhat.com> 0.3.2-2
- Silence unnecessary warning
  Resolves: rhbz#1201846
- Access oVirt REST API through /ovirt-engine/api rather than /api
  Resolves: rhbz#1277447
- Allow to cancel ovirt:// authentication dialog in virt-viewer
  Resolves: rhbz#1201604
- Make sure 'cancelled' signal is disconnected when objects die
  Related: rhbz#1201604
- Fix crash when VM has several ISO domains
  Resolves: rhbz#1274355
- Don't print ticket value to stdout
  Resolves: rhbz#1216118
- Add support for accessing VMs behind proxies
  Resolves: rhbz#1292754

* Tue Jan 20 2015 Christophe Fergeau <cfergeau@redhat.com> 0.3.2-1
- Update to libgovirt 0.3.2
  Related: rhbz#981678

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
