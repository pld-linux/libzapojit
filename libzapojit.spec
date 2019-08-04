#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries

Summary:	GLib/GObject wrapper for the SkyDrive and Hotmail REST APIs
Summary(pl.UTF-8):	Obudowanie GLib/GObject dla API REST-owych SkyDrive'a i Hotmaila
Name:		libzapojit
Version:	0.0.3
Release:	5
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libzapojit/0.0/%{name}-%{version}.tar.xz
# Source0-md5:	9de0d94e2c6a86852133a6f2f0b5fee1
URL:		https://wiki.gnome.org/Projects/Zapojit
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.28.0
BuildRequires:	gnome-common >= 3.6.0
BuildRequires:	gnome-online-accounts-devel
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gtk-doc >= 1.11
BuildRequires:	intltool >= 0.40.0
BuildRequires:	json-glib-devel
BuildRequires:	libsoup-devel >= 2.38.0
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	rest-devel >= 0.7
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.28.0
Requires:	libsoup >= 2.38.0
Requires:	rest >= 0.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libzapojit is a GLib/GObject wrapper for the SkyDrive and Hotmail REST
APIs. It supports SkyDrive file and folder objects, and the following
SkyDrive operations:
- Deleting a file, folder or photo.
- Listing the contents of a folder.
- Reading the properties of a file, folder or photo.
- Uploading files and photos.

%description -l pl.UTF-8
libzapojit to obudowanie GLib/GObject dla API REST-owych SkyDrive'a i
Hotmaila. Obsługuje obiekty plików i folderów SkyDrive'a oraz
następujące operacje SkyDrive:
- usuwanie pliku, folderu lub zdjęcia,
- listowanie zawartości folderu,
- odczyt właściwości pliku, folderu lub zdjecia,
- przesyłanie plików i zdjęć.

%package devel
Summary:	Header files for libzapojit library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libzapojit
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.28.0
Requires:	gnome-online-accounts-devel
Requires:	json-glib-devel
Requires:	libsoup-devel >= 2.38.0
Requires:	rest-devel >= 0.7

%description devel
Header files for libzapojit library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libzapojit.

%package static
Summary:	Static libzapojit library
Summary(pl.UTF-8):	Statyczna biblioteka libzapojit
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libzapojit library.

%description static -l pl.UTF-8
Statyczna biblioteka libzapojit.

%package apidocs
Summary:	libzapojit API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libzapojit
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for libzapojit library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libzapojit.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{__enable_disable apidocs gtk-doc} \
	%{__enable_disable static_libs static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libzapojit-*.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libzapojit-0.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzapojit-0.0.so.0
%{_libdir}/girepository-1.0/Zpj-0.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzapojit-0.0.so
%{_includedir}/libzapojit-0.0
%{_pkgconfigdir}/zapojit-0.0.pc
%{_datadir}/gir-1.0/Zpj-0.0.gir

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libzapojit-0.0.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libzapojit-0.0
%endif
