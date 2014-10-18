Summary:	GNOME keyboard shared library
Name:		libgnomekbd
Version:	3.6.0
Release:	2
License:	LGPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/libgnomekbd/3.6/%{name}-%{version}.tar.xz
# Source0-md5:	2f000ed5aa11454936c846a784e484c7
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	intltool
BuildRequires:	libglade-devel
BuildRequires:	libtool
BuildRequires:	libxklavier-devel >= 5.2.1
BuildRequires:	pkg-config
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME keyboard shared library.

%package devel
Summary:	Include files for the libgnomekbd
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package provides the necessary include files to develop programs
using the libgnomekbd.

%package runtime
Summary:	GNOME keyboard
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires(post,postun):  glib-gio-gsettings

%description runtime
GNOME keyboard runtime.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules	\
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post runtime
%update_gsettings_cache

%postun runtime
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog*
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_libdir}/girepository-1.0/Gkbd-3.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/%{name}
%{_pkgconfigdir}/*.pc
%{_datadir}/gir-1.0/Gkbd-3.0.gir

%files runtime -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gkbd-keyboard-display
%{_datadir}/GConf/gsettings/libgnomekbd.convert
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/libgnomekbd
%{_desktopdir}/gkbd-keyboard-display.desktop

