Name:           mosquitto
Version:        1.4.11
Release:        2%{?dist}
Summary:        An Open Source MQTT v3.1/v3.1.1 Broker

License:        BSD
URL:            http://mosquitto.org/
Source0:        http://mosquitto.org/files/source/%{name}-%{version}.tar.gz

BuildRequires:  openssl-devel
BuildRequires:  tcp_wrappers-devel
BuildRequires:  systemd
BuildRequires:  uthash-devel
BuildRequires:  c-ares-devel
BuildRequires:  libuuid-devel
BuildRequires:  libwebsockets-devel
BuildRequires:  gcc-c++

Requires(pre):  shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Mosquitto is an open source message broker that implements the MQ Telemetry
Transport protocol version 3.1 and 3.1.1 MQTT provides a lightweight method
of carrying out messaging using a publish/subscribe model. This makes it
suitable for "machine to machine" messaging such as with low power sensors 
or mobile devices such as phones, embedded computers or micro-controllers 
like the Arduino.

%package devel
Requires:     %{name}%{?_isa} = %{version}-%{release}
Summary:      Development files for %{name}

%description devel
Development headers and libraries for %{name}

%prep
%setup -q
# Remove bundled uthash.h
rm -r src/uthash.h
# Set the install prefix to /usr
sed -i "s|prefix=/usr/local|prefix=/usr|" config.mk
# Don't strip binaries on install: rpmbuild will take care of it
sed -i "s|(INSTALL) -s|(INSTALL)|g" lib/Makefile src/Makefile client/Makefile

%build
export CFLAGS="%{optflags}"
export LDFLAGS="%{optflags} %{__global_ldflags} -Wl,--as-needed"
make all %{?_smp_mflags} WITH_WEBSOCKETS=yes

%install
%if "%{_lib}" == "lib64"
export LIB_SUFFIX=64
%endif
%make_install

cat > mosquitto.service << FOE
[Unit]
Description=Mosquitto MQTT v3.1/v3.1.1 Broker
Documentation=man:mosquitto.conf(5) man:mosquitto(8)

[Service]
ExecStart=/usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf
User=mosquitto

[Install]
WantedBy=multi-user.target
FOE

mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service
mv %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf.example %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf

%check
#make test

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_sysconfdir}/%{name} -s /sbin/nologin \
    -c "Mosquitto Broker" %{name}
exit 0

%post
%systemd_post %{name}.service
/sbin/ldconfig

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
/sbin/ldconfig

%files
%doc ChangeLog.txt CONTRIBUTING.md readme.md
%license LICENSE.txt 
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*.so.*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config%{_sysconfdir}/%{name}/*.example
%{_unitdir}/%{name}.service
%{_mandir}/man1/*.1.*
%{_mandir}/man5/*.5.*
%{_mandir}/man7/*.7.*
%{_mandir}/man8/*.8.*

%files devel
%{_includedir}/*.h
%{_libdir}/*.so
%{_mandir}/man3/*.3.*

%changelog
* Tue Apr 11 2017 Tristan Cacqueray <tdecacqu@redhat.com> - 1.4.11-2
- Fix build requires

* Thu Mar 02 2017 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.11-1
- Update to new upstream version 1.4.11

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 29 2016 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.10-2
- Rebuild for libwebsockets (rhbz#1406779)

* Fri Nov 18 2016 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.10-1
- Update to new upstream version 1.4.10

* Mon Aug 08 2016 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.9-3
- Rebuild

* Fri Jul 01 2016 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.9-2
- Fix configuration example

* Fri Jul 01 2016 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.9-1
- Use sample configuration (rhbz#1272342)
- Update to new upstream version 1.4.9

* Sun May 08 2016 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.8-2
- Enable websockets support (rhbz#1197678)

* Wed Mar 09 2016 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.8-1
- Update to new upstream version 1.4.8

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 24 2016 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.7-1
- Update to new upstream version 1.4.7

* Fri Nov 27 2015 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.5-1
- Update to new upstream version 1.4.5

* Wed Oct 07 2015 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.4-1
- Update to new upstream version 1.4.4

* Thu Sep 03 2015 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.3-1
- Update to new upstream version 1.4.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 10 2015 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.2-1
- Update to new upstream version 1.4.2

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.4-2
- Rebuilt for GCC 5 C++11 ABI change

* Wed Feb 25 2015 Fabian Affolter <mail@fabian-affolter.ch> - 1.4-1
- Update BRs
- Python subpackage is replaced by python-paho-mqtt
- Update to new upstream version 1.4

* Thu Oct 16 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1.3.5-1
- Update to new upstream version 1.3.5

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1.3.4-1
- Update to new upstream version 1.3.4

* Mon Aug 11 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1.3.3-1
- Update to new upstream version 1.3.3

* Mon Jul 14 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1.3.2-1
- Update to new upstream version 1.3.2 (rhbz#1119238)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Apr 06 2014 Rich Mattes <richmattes@gmail.com> - 1.3.1-1
- Update to latest upstream release 1.3.1

* Sat Mar 22 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1.3-1
- Update to latest upstream release 1.3

* Sat Dec 21 2013 Fabian Affolter <mail@fabian-affolter.ch> - 1.2.3-2
- Add install section to service file

* Sat Dec 21 2013 Fabian Affolter <mail@fabian-affolter.ch> - 1.2.3-1
- Update to latest upstream release 1.2.3

* Mon Oct 28 2013 Fabian Affolter <mail@fabian-affolter.ch> - 1.2.2-1
- Update to latest upstream release 1.2.2

* Sat Sep 21 2013 Fabian Affolter <mail@fabian-affolter.ch> - 1.2.1-1
- Update to latest upstream release 1.2.1

* Wed Aug 14 2013 Rich Mattes <richmattes@gmail.com> - 1.2-1
- Update to release 1.2

* Sat Aug 10 2013 Rich Mattes <richmattes@gmail.com> - 1.1.3-3
- Switch to Makefiles from CMake scripts
- Add User=mosquitto to systemd unit

* Tue Jul 23 2013 Rich Mattes <richmattes@gmail.com> - 1.1.3-2
- Unbundle uthash
- Add as-needed to ldflags to avoid spurious links

* Wed May 1 2013 Rich Mattes <richmattes@gmail.com> - 1.1.3-1
- Initial package
