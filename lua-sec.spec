%define luaver 5.1
%define lualibdir %{_libdir}/lua/%{luaver}
%define luapkgdir %{_datadir}/lua/%{luaver}

%define real_name luasec

Summary:	Lua binding for OpenSSL library
Name:		lua-sec
Version:	0.4.1
Release:	1

License:	MIT
Group:		Development/Libraries
URL:		http://www.inf.puc-rio.br/~brunoos/luasec/
Source0:	http://www.inf.puc-rio.br/~brunoos/%{real_name}/download/%{real_name}-%{version}.tar.gz
# Source0-md5:	b8a5fde3b3fdb6174f54cd51d7f53e12
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

BuildRequires:	lua-devel
BuildRequires:	openssl-devel
Requires:	lua-socket

%description
Lua binding for OpenSSL library to provide TLS/SSL communication. It
takes an already established TCP connection and creates a secure
session between the peers.


%prep
%setup -q -n %{real_name}-%{version}
for file in CHANGELOG LICENSE; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done


%build
%{__make} %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -I%{_includedir}/lua51 -fPIC" linux


%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT%{luapkgdir}
%{__mkdir} -p $RPM_BUILD_ROOT%{lualibdir}
%{__make} install DESTDIR=$RPM_BUILD_ROOT LUAPATH=$RPM_BUILD_ROOT%{luapkgdir} LUACPATH=$RPM_BUILD_ROOT%{lualibdir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE
%{lualibdir}/ssl.so
%{luapkgdir}/ssl.lua
%dir %{luapkgdir}/ssl
%{luapkgdir}/ssl/*
