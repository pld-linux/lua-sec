# TODO
# - use system lua-socket

%define		luaver 5.3
%define		real_name luasec

%define		luasuffix %(echo %{luaver} | tr -d .)
%if "%{luaver}" == "5.1"
%define		luaincludedir %{_includedir}/lua51
%else
%define		luaincludedir %{_includedir}/lua%{luaver}
%endif
%define		lualibdir %{_libdir}/lua/%{luaver}
%define		luapkgdir %{_datadir}/lua/%{luaver}

Summary:	Lua binding for OpenSSL library
Name:		lua%{luasuffix}-sec
Version:	0.9
Release:	1
License:	MIT
Group:		Development/Libraries
Source0:	https://github.com/brunoos/luasec/archive/v%{version}/%{real_name}-%{version}.tar.gz
# Source0-md5:	b31b56f6bf034a8240fcc47f0f4041c8
Patch0:		makefile.patch
URL:		https://github.com/brunoos/luasec
BuildRequires:	lua%{luasuffix}-devel
#BuildRequires:	lua%{luasuffix}-socket-devel
BuildRequires:	openssl-devel
#Requires:	lua%{luasuffix}-socket
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lua binding for OpenSSL library to provide TLS/SSL communication. It
takes an already established TCP connection and creates a secure
session between the peers.

%prep
%setup -q -n %{real_name}-%{version}
%patch0 -p1

for file in CHANGELOG LICENSE; do
	iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file
	touch -r $file $file.new
	mv $file.new $file
done

%build
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
LDFLAGS="%{rpmldflags}" \
%{__make} linux \
	CC="%{__cc}" \
	INC_PATH="-I%{luaincludedir}"

%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT%{luapkgdir}
%{__mkdir} -p $RPM_BUILD_ROOT%{lualibdir}
%{__make} install \
	LUAPATH=%{luapkgdir} \
	LUACPATH=%{lualibdir} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE
%attr(755,root,root) %{lualibdir}/ssl.so
%{luapkgdir}/ssl.lua
%dir %{luapkgdir}/ssl
%{luapkgdir}/ssl/https.lua
