# -*- rpm-spec -*-

%global with_gir 0

# Default to skipping autoreconf.  Distros can change just this one line
# (or provide a command-line override) if they backport any patches that
# touch configure.ac or Makefile.am.

# Force running autoreconf because data center patches touch Makefile.am.
# To disable autoreconf, change the value to 0.
%{!?enable_autotools:%global enable_autotools 1}

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%global with_gir 1
%endif

Summary: A GObject library for interacting with oVirt REST API
Name: libgovirt
Version: 0.3.4
Release: 3%{?dist}%{?extra_release}
License: LGPLv2+
Group: Development/Libraries
Source: http://ftp.gnome.org/pub/GNOME/sources/libgovirt/0.3/%{name}-%{version}.tar.xz
URL: http://people.freedesktop.org/~teuf/govirt/
Patch01: 0001-proxy-Fix-persistent-session-with-oVirt-3.6.patch
Patch02: 0002-Force-use-of-v3-REST-API.patch
Patch03: 0003-New-storage-format-added-in-oVirt-4.1.patch
Patch04: 0004-proxy-Hold-reference-to-cancellable-object.patch
Patch05: 0005-proxy-Check-if-operation-is-cancelled-before-disconn.patch
Patch06: 0006-storage-domain-Factor-out-property-value-setting-fro.patch
Patch07: 0007-storage-domain-use-explicit-initialization-of-struct.patch
Patch08: 0008-storage-domain-Move-out-ovirt_resource_parse_xml-to-.patch
Patch09: 0009-utils-Remove-unused-function-ovirt_rest_xml_node_get.patch
Patch10: 0010-utils-Rename-ovirt_rest_xml_node_get_content_va-to-o.patch
Patch11: 0011-utils-Retrieve-node-attributes-in-ovirt_resource_par.patch
Patch12: 0012-utils-Support-G_TYPE_STRING-in-_set_property_value_f.patch
Patch13: 0013-utils-Support-G_TYPE_STRV-in-_set_property_value_fro.patch
Patch14: 0014-Introduce-auxiliary-function-ovirt_sub_collection_ne.patch
Patch15: 0015-New-API-functions-to-enable-search-queries-of-collec.patch
Patch16: 0016-Introduce-ovirt_resource_new-functions.patch
Patch17: 0017-Use-ovirt_resource_new-functions-instead-of-g_initab.patch
Patch18: 0018-Move-resource-type-definitions-to-ovirt-types.h.patch
Patch19: 0019-Initial-support-for-hosts.patch
Patch20: 0020-Initial-support-for-clusters.patch
Patch21: 0021-Initial-support-for-data-centers.patch
Patch22: 0022-vm-Introduce-ovirt_vm_get_host.patch
Patch23: 0023-vm-Introduce-ovirt_vm_get_cluster.patch
Patch24: 0024-host-Introduce-ovirt_host_get_cluster.patch
Patch25: 0025-cluster-Introduce-ovirt_cluster_get_data_center.patch
Patch26: 0026-storage-domain-Retrieve-data-center-ids.patch
Patch27: 0027-Add-missing-include-in-govirt.h.patch
Patch28: 0028-resource-Fix-ovirt_resource_rest_call_sync-return-va.patch
Patch29: 0029-resource-Fix-ovirt_resource_rest_call_sync-crash-on-.patch
Patch30: 0030-resource-Fix-ovirt_resource_init_from_xml_real-preco.patch
Patch31: 0031-resource-Update-xml-node-in-ovirt_resource_init_from.patch
Patch32: 0032-utils-Drop-type-member-from-OvirtXmlElement-struct.patch
Patch33: 0033-utils-Support-G_TYPE_UINT-in-_set_property_value_fro.patch
Patch34: 0034-utils-Improve-log-message-when-subnode-is-not-found.patch
Patch35: 0035-utils-Factor-out-basic-value-type-setting-from-_set_.patch
Patch36: 0036-utils-Get-enum-default-value-from-GParamSpec.patch
Patch37: 0037-vm-Set-vm-state-property-using-OvirtXmlElement-struc.patch
Patch38: 0038-vm-Set-values-of-OvirtVmDisplay-using-OvirtXmlElemen.patch
Patch39: 0039-vm-display-Move-XML-parsing-from-ovirt-vm-xml.c-file.patch
Patch40: 0040-vm-Set-ticket-expiry-using-OvirtXmlElement-struct.patch
Patch41: 0041-test-govirt-Add-display-node-to-vm-XMLs.patch
Patch42: 0042-proxy-Set-detailed-error-message-for-async-call.patch
Patch43: 0043-cdrom-Set-file-property-using-OvirtXmlElement-struct.patch
Patch44: 0044-proxy-Don-t-try-to-unref-NULL-root-node.patch
Patch45: 0045-utils-Check-for-valid-data-before-calling-rest_xml_p.patch
Patch46: 0046-Update-tests-certificates.patch

%if 0%{?enable_autotools}
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gettext-devel
BuildRequires: libtool
%endif

BuildRequires: pkgconfig(glib-2.0)
BuildRequires: rest-devel >= 0.7.92
# needed for make check to complete successfully
BuildRequires: dconf

BuildRequires: intltool
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
%if 0%{?enable_autotools}
autoreconf -if
%endif

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
* Tue Apr 09 2019 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 0.3.4-2
- Parse XML nodes automatically
  Related: rhbz#1427467
- Set detailed error message for async call
  Related: rhbz#1427467

* Fri Jun 08 2018 Christophe Fergeau <cfergeau@redhat.com> - 0.3.4-1
- Rebase to latest 0.3.4 upstream release. Still quite a few patches as
  there was no 0.3.5 release yet
  Resolves: rhbz#1584266

* Mon Oct 02 2017 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 0.3.3-6
- Add support for Hosts, Clusters and Data Centers
  Resolves: rhbz#1428401

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


