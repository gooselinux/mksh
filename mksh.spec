%define _bindir   /bin

Summary:          MirBSD enhanced version of the Korn Shell
Name:             mksh
Version:          39
Release:          4%{?dist}
#BSD (setmode.c), ISC (strlcpy.c), MirOS (the rest)
License:          MirOS and ISC and BSD
Group:            System Environment/Shells
URL:              http://www.mirbsd.de/%{name}.htm
Source0:          http://www.mirbsd.org/MirOS/dist/mir/%{name}/%{name}-R%{version}.cpio.gz
# our own /etc/skel/.mkshrc to source original /etc/mkshrc
Source1:          dotmkshrc
Requires(post):   grep
Requires(postun): coreutils, grep
BuildRequires:    util-linux, ed
BuildRoot:        %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
mksh is the MirBSD enhanced version of the Public Domain Korn shell (pdksh),
a bourne-compatible shell which is largely similar to the original AT&T Korn
shell. It includes bug fixes and feature improvements in order to produce a
modern, robust shell good for interactive and especially script use, being a
bourne shell replacement, pdksh successor and an alternative to the C shell.

%prep
%setup -q -T -c

# rpm.org has no support for *.cpio.gz
gzip -dc %{SOURCE0} | cpio -imd
mv %{name}/* . && rm -rf %{name}

%build
CFLAGS="$RPM_OPT_FLAGS" sh Build.sh -r -combine

%install
rm -rf $RPM_BUILD_ROOT
install -D -m 755 %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}
install -D -m 644 %{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1
install -D -m 644 dot.mkshrc $RPM_BUILD_ROOT%{_sysconfdir}/mkshrc
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/skel/.mkshrc

%check
echo > test.wait
script -qc './test.sh -v; x=$?; rm -f test.wait; exit $x'
maxwait=0
while test -e test.wait; do
  sleep 1
  maxwait=$(expr $maxwait + 1)
  test $maxwait -lt 900 || break
done

%post
grep -q "^%{_bindir}/%{name}$" %{_sysconfdir}/shells 2>/dev/null || \
  echo "%{_bindir}/%{name}" >> %{_sysconfdir}/shells

%postun
if [ ! -x %{_bindir}/%{name} ]; then
  sed -i -e 's|^%{_bindir}/%{name}$|POSTUNREMOVE|' -e '/^POSTUNREMOVE$/ d' %{_sysconfdir}/shells
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc dot.mkshrc
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%config(noreplace) %{_sysconfdir}/mkshrc
%config(noreplace) %{_sysconfdir}/skel/.mkshrc

%changelog
* Fri Jun 25 2010 Michal Hlavinka <mhlavink@redhat.com> - 39-4
- add .mkshrc to /etc/skel

* Fri Apr 23 2010 Michal Hlavinka <mhlavink@redhat.com> - 39-3
- fix license

* Thu Mar 18 2010 Michal Hlavinka <mhlavink@redhat.com> - 39-2
- remove arc4random, we don't need it

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 39-1.1
- Rebuilt for RHEL 6

* Thu Aug 13 2009 Robert Scheck <robert@fedoraproject.org> 39-1
- Upgrade to 39 and updated arc4random.c file

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 38b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 31 2009 Robert Scheck <robert@fedoraproject.org> 38b-1
- Upgrade to 38b

* Sun May 31 2009 Robert Scheck <robert@fedoraproject.org> 38-1
- Upgrade to 38 and updated arc4random.c file
- Used -combine (-fwhole-program) rather the old -j switch

* Sun Apr 05 2009 Robert Scheck <robert@fedoraproject.org> 37b-1
- Upgrade to 37b

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 36b-2
- Rebuild against gcc 4.4 and rpm 4.6

* Sun Dec 14 2008 Robert Scheck <robert@fedoraproject.org> 36b-1
- Upgrade to 36b and updated arc4random.c file

* Tue Dec 02 2008 Robert Scheck <robert@fedoraproject.org> 36-2
- Upstream patch for command hang/high cpu workload (#474115)

* Sat Oct 25 2008 Robert Scheck <robert@fedoraproject.org> 36-1
- Upgrade to 36

* Sat Jul 19 2008 Robert Scheck <robert@fedoraproject.org> 35b-1
- Upgrade to 35b

* Sun Jul 13 2008 Robert Scheck <robert@fedoraproject.org> 35-1
- Upgrade to 35

* Sat Apr 12 2008 Robert Scheck <robert@fedoraproject.org> 33d-1
- Upgrade to 33d

* Fri Apr 04 2008 Robert Scheck <robert@fedoraproject.org> 33c-1
- Upgrade to 33c and updated arc4random.c file

* Mon Mar 03 2008 Robert Scheck <robert@fedoraproject.org> 33-1
- Upgrade to 33

* Sun Feb 10 2008 Robert Scheck <robert@fedoraproject.org> 32-2
- Rebuild against gcc 4.3

* Sat Nov 10 2007 Robert Scheck <robert@fedoraproject.org> 32-1
- Upgrade to 32
- Solved fork problems in %%check (thanks to Thorsten Glaser)

* Mon Oct 15 2007 Robert Scheck <robert@fedoraproject.org> 31d-1
- Upgrade to 31d

* Wed Sep 12 2007 Robert Scheck <robert@fedoraproject.org> 31c-1
- Upgrade to 31c
- Added a buildrequirement to ed, added arc4random.c file

* Tue Sep 11 2007 Robert Scheck <robert@fedoraproject.org> 31b-1
- Upgrade to 31b
- Use script to get %%check happy (thanks to Thorsten Glaser)

* Sat Sep 08 2007 Robert Scheck <robert@fedoraproject.org> 31-1
- Upgrade to 31

* Tue Aug 28 2007 Robert Scheck <robert@fedoraproject.org> 30-2
- Updated the license tag according to the guidelines

* Sat Jul 28 2007 Robert Scheck <robert@fedoraproject.org> 30-1
- Upgrade to 30

* Sat Jul 14 2007 Robert Scheck <robert@fedoraproject.org> 29g-1
- Upgrade to 29g

* Sun Jun 03 2007 Robert Scheck <robert@fedoraproject.org> 29f-1
- Upgrade to 29f
- Initial spec file for Fedora and Red Hat Enterprise Linux
