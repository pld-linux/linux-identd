Summary:	Simple ident daemon
Summary(pl):	Prosty demon ident
Name:		linux-identd
Version:	1.2
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://www.fukt.bth.se/~per/identd/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Source2:	%{name}.sysconfig
Source3:	%{name}.init
URL:		http://www.fukt.bth.se/~per/identd/
Requires:	linux-identd-frontend
Provides:	identserver
Obsoletes:	pidentd oidentd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
linux-identd is a user identification daemon for Linux, which
implements the Identification Protocol (RFC1413). This protocol is
used to identify active TCP connections. The daemon listens to TCP
port 113 (auth), and can be run either as a stand-alone daemon, or
through inetd.

%package standalone
Summary:	Simple ident daemon
Summary(pl):	Prosty demon ident
Group:		Networking/Daemons
Provides:	linux-identd-frontend
Prereq:		%{name} = %{version}
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
Obsoletes:	%{name}-inetd

%description standalone
linux-identd standalone version.

%package inetd
Summary:	Simple ident daemon
Summary(pl):	Prosty demon ident
Group:		Networking/Daemons
Provides:	linux-identd-frontend
Prereq:		%{name} = %{version}
Prereq:		rc-inetd
Requires:	inetdaemon
Obsoletes:	%{name}-standalone

%description inetd
linux-identd inetd version.

%prep
%setup -q

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig/rc-inetd,rc.d/init.d}

%{__make} install DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/identd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/identd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/identd

%clean
rm -rf $RPM_BUILD_ROOT

%post inetd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun inetd
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
fi

%post standalone
/sbin/chkconfig --add identd
if [ -f /var/lock/subsys/identd ]; then
	/etc/rc.d/init.d/identd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/identd start\" to start ident daemon."
fi

%preun standalone
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/identd ]; then
		/etc/rc.d/init.d/identd stop 1>&2
	fi
	/sbin/chkconfig --del identd
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(755,root,root) %{_sbindir}/identd
%{_mandir}/man8/identd.8.gz

%files inetd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/identd

%files standalone
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/identd
%attr(754,root,root) /etc/rc.d/init.d/identd
