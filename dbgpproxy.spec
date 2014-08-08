# TODO
# - initscript+config
%define	rel		1
%define	subver	83298
Summary:	DBGp Proxy for PHP Xdebug
Name:		dbgpproxy
Version:	8.5.3
Release:	0.%{subver}.%{rel}
License:	MIT
Group:		Libraries
# SourceDownload: http://code.activestate.com/komodo/remotedebugging/
Source0:	http://downloads.activestate.com/Komodo/releases/%{version}/remotedebugging/Komodo-PythonRemoteDebugging-%{version}-%{subver}-linux-x86.tar.gz
# Source0-md5:	9490a78e5bb1e68257d88dd089e690b0
Source1:	http://downloads.activestate.com/Komodo/releases/%{version}/remotedebugging/Komodo-PythonRemoteDebugging-%{version}-%{subver}-linux-x86_64.tar.gz
# Source1-md5:	a485c07846fb82a69194b5099cf173d4
URL:		http://derickrethans.nl/debugging-with-multiple-users.html
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# avoid empty debuginfo package
%define		_enable_debug_packages	0

%description
DBGp is protocol to facilitate communication between an IDE (such as
Komodo, or any of the other clients) and PHP+Xdebug.

%prep
%ifarch %{ix86}
%setup -qcT -b 0
%endif
%ifarch %{x8664}
%setup -qcT -b 1
%endif
mv Komodo-PythonRemoteDebugging-%{version}-%{subver}-linux-*/* .

cd pythonlib
py_ver=$(echo %py_ver | tr -d .)
mv dbgp/_client$py_ver.so .
rm -vf dbgp/_client??.so
mv _client$py_ver.so dbgp

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{py_sitescriptdir}/dbgp}
install -p pydbgpproxy $RPM_BUILD_ROOT%{_bindir}
cp -a pythonlib/* $RPM_BUILD_ROOT%{py_sitescriptdir}

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt
%attr(755,root,root) %{_bindir}/pydbgpproxy
%{py_sitescriptdir}/dbgpClient.py[co]
%{py_sitescriptdir}/dbgp/*.py[co]
%dir %{py_sitescriptdir}/dbgp
%dir %{py_sitescriptdir}/dbgp/_logging
%attr(755,root,root) %{py_sitescriptdir}/dbgp/_client*.so
%{py_sitescriptdir}/dbgp/_logging/*.py[co]
