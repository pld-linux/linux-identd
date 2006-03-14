Summary:	Simple ident daemon
Summary(pl):	Prosty demon ident
Name:		linux-identd
Version:	1.3
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://www.fukt.bth.se/~per/identd/%{name}-%{version}.tar.gz
# Source0-md5:	c3517f612b351e46951d2ecb0c60b767
Source1:	%{name}.inetd
Source2:	%{name}.sysconfig
Source3:	%{name}.init
URL:		http://www.fukt.bth.se/~per/identd/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	linux-identd-frontend
Provides:	identserver
Obsoletes:	oidentd
Obsoletes:	pidentd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
linux-identd is a user identification daemon for Linux, which
implements the Identification Protocol (RFC1413). This protocol is
used to identify active TCP connections. The daemon listens to TCP
port 113 (auth), and can be run either as a stand-alone daemon, or
through inetd.

%description -l pl
linux-identd to demon identyfikacji u¿ytkowników dla Linuksa, bêd±cy
implementacj± protoko³u identyfikacji (RFC1413). Protokó³ s³u¿y do
identyfikowania aktywnych po³±czeñ TCP. Demon s³ucha na porcie 113
(auth) i mo¿e byæ uruchamiany jako samodzielny demon lub poprzez
inetd.

%package standalone
Summary:	Simple ident daemon
Summary(pl):	Prosty demon ident
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}
Requires:	rc-scripts
Provides:	linux-identd-frontend
Obsoletes:	linux-identd-inetd

%description standalone
linux-identd standalone version.

%description standalone -l pl
Samodzielna wersja demona linux-identd.

%package inetd
Summary:	Simple ident daemon
Summary(pl):	Prosty demon ident
Group:		Networking/Daemons
Requires:	%{name} = %{version}
Requires:	inetdaemon
Requires:	rc-inetd
Provides:	linux-identd-frontend
Obsoletes:	linux-identd-standalone

%description inetd
linux-identd inetd version.

%description inetd -l pl
Wersja demona linux-identd uruchamiana z inetd.

%prep
%setup -q

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig/rc-inetd,rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/identd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/identd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/identd

%clean
rm -rf $RPM_BUILD_ROOT

%post inetd
%service -q rc-inetd reload

%postun inetd
if [ "$1" = "0" ]; then
	%service -q rc-inetd reload
fi

%post standalone
/sbin/chkconfig --add identd
%service identd restart "ident daemon"

%preun standalone
if [ "$1" = "0" ]; then
	%service identd stop
	/sbin/chkconfig --del identd
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(755,root,root) %{_sbindir}/identd
%{_mandir}/man8/identd.8*

%files inetd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/identd

%files standalone
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/identd
%attr(754,root,root) /etc/rc.d/init.d/identd
