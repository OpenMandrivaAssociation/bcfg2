Name:		bcfg2
Version:	1.3.6
Release:	1
Summary:	A configuration management system
Group:		System/Base
License:	BSD
URL:		http://bcfg2.org
Source0:	ftp://ftp.mcs.anl.gov/pub/bcfg/bcfg2-%{version}.tar.gz
Source1:	ftp://ftp.mcs.anl.gov/pub/bcfg/bcfg2-%{version}.tar.gz.gpg
BuildArch:	noarch
Requires(post):	rpm-helper
Requires(preun): rpm-helper

BuildRequires:	python-setuptools
Requires:	python-lxml

%description
Bcfg2 helps system administrators produce a consistent, reproducible,
and verifiable description of their environment, and offers
visualization and reporting tools to aid in day-to-day administrative
tasks. It is the fifth generation of configuration management tools
developed in the Mathematics and Computer Science Division of Argonne
National Laboratory.

It is based on an operational model in which the specification can be
used to validate and optionally change the state of clients, but in a
feature unique to bcfg2 the client's response to the specification can
also be used to assess the completeness of the specification. Using
this feature, bcfg2 provides an objective measure of how good a job an
administrator has done in specifying the configuration of client
systems. Bcfg2 is therefore built to help administrators construct an
accurate, comprehensive specification.

Bcfg2 has been designed from the ground up to support gentle
reconciliation between the specification and current client states. It
is designed to gracefully cope with manual system modifications.

Finally, due to the rapid pace of updates on modern networks, client
systems are constantly changing; if required in your environment,
Bcfg2 can enable the construction of complex change management and
deployment strategies.

%package server
Summary:	Configuration management server
Group:		System/Base
Requires:	bcfg2 = %{version}-%{release}
Requires:	sendmail
Requires:	openssl
Requires:	python-gamin
Requires:	python-genshi
Requires:	python-cheetah
Requires:	graphviz
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description server
Configuration management server

%package doc
Summary:	Documentation for Bcfg2
Group:		Development/Other

BuildRequires:	python-sphinx
BuildRequires:	python-docutils

%description doc
Documentation for Bcfg2.

%prep
%setup -q -n %{name}-%{version}%{?_rc:rc%{_rc}}

# fixup some paths
perl -pi -e 's@/etc/default@%{_sysconfdir}/sysconfig@g' debian/bcfg2.init
perl -pi -e 's@/etc/default@%{_sysconfdir}/sysconfig@g' debian/bcfg2-server.init
perl -pi -e 's@/etc/default@%{_sysconfdir}/sysconfig@g' tools/bcfg2-cron

perl -pi -e 's@/usr/lib/bcfg2@%{_libexecdir}@g' debian/bcfg2.cron.daily
perl -pi -e 's@/usr/lib/bcfg2@%{_libexecdir}@g' debian/bcfg2.cron.hourly

# don't start servers by default
perl -pi -e 's@chkconfig: (\d+)@chkconfig: -@' debian/bcfg2.init
perl -pi -e 's@chkconfig: (\d+)@chkconfig: -@' debian/bcfg2-server.init

# get rid of extraneous shebangs
for f in `find src/lib -name \*.py`
do
    sed -i -e '/^#!/,1d' $f
done

%build
python -c 'import setuptools; execfile("setup.py")' build
python -c 'import setuptools; execfile("setup.py")' build_sphinx

%install
python -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}

mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/cron.daily
mkdir -p %{buildroot}%{_sysconfdir}/cron.hourly
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_libexecdir}
mkdir -p %{buildroot}%{_var}/lib/bcfg2
mkdir -p %{buildroot}%{_var}/cache/bcfg2
mkdir -p %{buildroot}%{_defaultdocdir}/bcfg2-doc-%{version}%{?_pre:pre%{_pre}}

mv %{buildroot}%{_bindir}/bcfg2* %{buildroot}%{_sbindir}

install -m 755 debian/bcfg2.init %{buildroot}%{_initrddir}/bcfg2
install -m 755 debian/bcfg2-server.init %{buildroot}%{_initrddir}/bcfg2-server
install -m 755 debian/bcfg2.cron.daily %{buildroot}%{_sysconfdir}/cron.daily/bcfg2
install -m 755 debian/bcfg2.cron.hourly %{buildroot}%{_sysconfdir}/cron.hourly/bcfg2
install -m 755 tools/bcfg2-cron %{buildroot}%{_libexecdir}/bcfg2-cron

install -m 644 debian/bcfg2.default %{buildroot}%{_sysconfdir}/sysconfig/bcfg2
install -m 644 debian/bcfg2-server.default %{buildroot}%{_sysconfdir}/sysconfig/bcfg2-server

touch %{buildroot}%{_sysconfdir}/bcfg2.cert
touch %{buildroot}%{_sysconfdir}/bcfg2.conf
touch %{buildroot}%{_sysconfdir}/bcfg2.key

mv build/sphinx/html/* %{buildroot}%{_defaultdocdir}/bcfg2-doc-%{version}%{?_pre:pre%{_pre}}

%post
%_post_service bcfg2

%preun
%_preun_service bcfg2

%post server
%_post_service bcfg2-server

%preun server
%_preun_service bcfg2-server

%files
%doc AUTHORS examples COPYRIGHT README
%{_mandir}/man1/bcfg2.1*
%{_mandir}/man5/bcfg2*.5*
%ghost %attr(600,root,root) %config(noreplace) %{_sysconfdir}/bcfg2.cert
%ghost %attr(600,root,root) %config(noreplace) %{_sysconfdir}/bcfg2.conf
%config(noreplace) %{_sysconfdir}/sysconfig/bcfg2
%{_sysconfdir}/cron.daily/bcfg2
%{_sysconfdir}/cron.hourly/bcfg2
%{_initrddir}/bcfg2
%{_sbindir}/bcfg2
%{_libexecdir}/bcfg2-cron
%dir %{_var}/cache/bcfg2
%{python_sitelib}/Bcfg2*.egg-info
%dir %{python_sitelib}/Bcfg2
%{python_sitelib}/Bcfg2/__init__.*
%{python_sitelib}/Bcfg2/Client
%{python_sitelib}/Bcfg2/Component.*
%{python_sitelib}/Bcfg2/Logger.*
%{python_sitelib}/Bcfg2/Options.*
%{python_sitelib}/Bcfg2/Proxy.*
%{python_sitelib}/Bcfg2/SSLServer.*
%{python_sitelib}/Bcfg2/Statistics.*
%{python_sitelib}/Bcfg2/Bcfg2Py3k.*

%files server
%{_mandir}/man8/bcfg2*.8*
%ghost %attr(600,root,root) %config(noreplace) %{_sysconfdir}/bcfg2.key
%config(noreplace) %{_sysconfdir}/sysconfig/bcfg2-server
%{_initrddir}/bcfg2-server
%{_datadir}/bcfg2
%{_sbindir}/bcfg2-*
%dir %{_var}/lib/bcfg2
%{python_sitelib}/Bcfg2/Server

%files doc
%doc %{_defaultdocdir}/bcfg2-doc-%{version}%{?_pre:pre%{_pre}}


%changelog
* Tue Apr 17 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.2.2-1
+ Revision: 791423
- version update 1.2.2

* Wed Dec 28 2011 Alexander Khrukin <akhrukin@mandriva.org> 1.2.0-1
+ Revision: 745876
- imported package bcfg2

