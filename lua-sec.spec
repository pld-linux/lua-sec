%define		luaver 5.1
%define		lualibdir %{_libdir}/lua/%{luaver}
%define		luapkgdir %{_datadir}/lua/%{luaver}
%define		real_name luasec
Summary:	Lua binding for OpenSSL library
Name:		lua-sec
Version:	0.5
Release:	1
License:	MIT
Group:		Development/Libraries
Source0:	https://github.com/brunoos/luasec/archive/luasec-%{version}.tar.gz
# Source0-md5:	0518f4524f399f33424c6f450e1d06db
URL:		https://github.com/brunoos/luasec
BuildRequires:	lua-devel
BuildRequires:	lua-socket-devel
BuildRequires:	openssl-devel
Requires:	lua-socket
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lua binding for OpenSSL library to provide TLS/SSL communication. It
takes an already established TCP connection and creates a secure
session between the peers.

%prep
%setup -q -n %{real_name}-%{real_name}-%{version}
for file in CHANGELOG LICENSE; do
	iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file
	touch -r $file $file.new
	mv $file.new $file
done

%build
%{__make} linux \
	CC="%{__cc} %{rpmcppflags} %{rpmcflags} %{rpmldflags}" \
	INC_PATH="-I%{_includedir}/lua51"

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
