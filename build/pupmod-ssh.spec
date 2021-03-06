Summary: SSH Puppet Module
Name: pupmod-ssh
Version: 4.1.0
Release: 10
License: Apache License, Version 2.0
Group: Applications/System
Source: %{name}-%{version}-%{release}.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: pupmod-concat >= 4.0.0-0
Requires: pupmod-iptables >= 4.1.0-3
Requires: puppet >= 3.3.0
Requires: pupmod-augeasproviders_ssh
Buildarch: noarch
Requires: simp-bootstrap >= 4.2.0
Obsoletes: pupmod-ssh-test

Prefix: %{_sysconfdir}/puppet/environments/simp/modules

%package augeas-lenses
Summary: SSH Puppet Module Patched Augeas Lenses
License: LGPLv2
Requires: pupmod-ssh

%description
This Puppet module manages the configuration of the system-wide SSH server and
client.

%description augeas-lenses
Provides patched Augeas lenses from the Augeas project to fix various bugs.

%prep
%setup -q

%build

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}/%{prefix}/ssh

files='README.md LICENSE CONTRIBUTING.md'
for file in $files; do
  test -f $file && cp $file %{buildroot}/%{prefix}/ssh
done

dirs='files lib manifests templates'
for dir in $dirs; do
  test -d $dir && cp -r $dir %{buildroot}/%{prefix}/ssh
done

mkdir -p %{buildroot}/usr/share/simp/tests/modules/ssh

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}/%{prefix}/ssh

%files
%defattr(0640,root,puppet,0750)
%{prefix}/ssh
%exclude %{prefix}/ssh/files/augeas_lenses

%files augeas-lenses
%{prefix}/ssh/files/augeas_lenses

%post
#!/bin/sh

if [ -d %{prefix}/ssh/plugins ]; then
  /bin/mv %{prefix}/ssh/plugins %{prefix}/ssh/plugins.bak
fi

%postun
# Post uninitall stuff

%changelog
* Fri Sep 18 2015 Nick Markowski <nmarkowski@keywcorp.com> - 4.1.0-10
- Updated the ssh client ciphers to match the ssh server ciphers.

* Wed Jul 29 2015 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-9
- Incorporated the updated SSH Augeas Lenses
- Created a sub-rpm for the lenses to account for the modified license terms
- Added support for default KexAlgorithms
- Added sensible defaults for the SSH server in both FIPS and non-FIPS mode
- Note: I have not yet tested these in FIPS enforcing mode so adjustments may
        need to be made

* Fri Feb 20 2015 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-8
- Added support for the new augeasproviders_ssh module
- Migrated to the new 'simp' environment.

* Fri Feb 06 2015 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-7
- Made all of the custom functions environment aware
- Enhanced the ssh_keygen function to return private keys if so instructed
  since we can use that to eradicate some automatically generated cruft in the
  module spaces.
- Changed puppet-server requirement to puppet

* Fri Dec 19 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-6
- Added a function, ssh_format_host_entry_for_sorting, that is explicitly for
  use by the concat_fragment part of ssh::client::add_entry. It handles proper
  sorting order when wildcards and question marks are used.

* Sun Jun 22 2014 Kendall Moore <kmoore@keywcorp.com> - 4.1.0-5
- Removed all non FIPS compliant ciphers from ssh server and client configs.

* Thu Jun 19 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-5
- Added support for the 'AuthorizedKeysCommandUser' in sshd_config
  since this is now required in RHEL >= 7.

* Thu Jun 05 2014 Nick Markowski <nmarkowski@keywcorp.com> - 4.1.0-4
- Set compression off in sshd_config by default.

* Thu May 22 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-3
- Fixed a resource chaining issue with /etc/ssh/ldap.conf. The source
  had not been declared properly so the dependency chain was not being
  enforced.

* Fri Apr 11 2014 Kendall Moore <kmoore@keywcorp.com> - 4.1.0-2
- Refactored manifests and removed singleton defines for puppet 3 and
  hiera compatibility.
- Added spec tests.
- Added function sshd_config_bool_translate to translate booleans into yes/no variables.

* Sun Apr 06 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-2
- Added hooks for various top-level variables for increased configuration
  flexibility.

* Tue Jan 28 2014 Kendall Moore <kmoore@keywcorp.com> 4.1.0-1
- Update to remove warnings about IPTables not being detected. This is a
  nuisance when allowing other applications to manage iptables legitimately.
- Removed the management of most variables by default from ssh::server::conf.
  The remainder are now managed by an sshd augeas provider.
- ALL supported variables are now settable via extdata as
  ssh::server::conf::<varname>
- This means that you can easily manipulate any variable as well as setting
  those that are not natively managed using the augeas provider.
- This work was done for supporting OpenShift

* Thu Jan 02 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-0
- AVC errors were being generated due to the /etc/ssh/ldap.conf file
  being a symlink. This is now copied directly from /etc/pam_ldap.conf
  instead of linked.

* Mon Oct 07 2013 Kendall Moore <kmoore@keywcorp.com> - 4.0.0-2
- Updated all erb templates to properly scope variables.

* Wed Sep 25 2013 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.0.0-1
- Added the ability to modify the hosts that can connect to sshd via
  IPTables using a client_nets variable.

* Thu May 02 2013 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.0.0-0
- Changed all localtime symlinks to file copies since SELinux does not like
  symlinks in these cases.

* Tue Apr 16 2013 Nick Markowski <nmarkowski@keywcorp.com> - 2.0.0-9
- All ssh public key authentication now directly uses LDAP.
- Added ldap.conf to /etc/ssh.
- Added openssh-ldap rpm and authorizedkeyscommand wrapper to template.
- SSH fully manages /etc/ssh/local_keys.

* Mon Dec 10 2012 Maintenance
2.0.0-8
- Created a Cucumber test to ensure that the SSH daemon is running.
- Created a Cucumber test which creates a temporary user, and ensures
  that they can SSH into the puppet server.

* Thu Nov 08 2012 Maintenance
2.0.0-7
- The ssh_global_known_hosts function now automatically deletes any short name
  key files that conflict with a long name file prior to manipulating the
  catalog.

* Fri Jul 20 2012 Maintenance
2.0.0-6
- Added a custom type 'sshkey_prune' that, given a target file, prunes all ssh
  keys that Puppet doesn't know about.
- Updated the ssh_global_known_hosts function to expire old keys after 7 days
  by default. Users may specify their own number of expire days or set to 0 to
  never expire any keys.

* Wed Apr 11 2012 Maintenance
2.0.0-5
- Fixed bug with ssh_global_known_hosts such that it uses
  'host_aliases' instead of 'alias' since the latter has be
  deprecated.
- Moved mit-tests to /usr/share/simp...
- Updated pp files to better meet Puppet's recommended style guide.

* Fri Mar 02 2012 Maintenance
2.0.0-4
- Added the CBC ciphers back to the SSH server default config since
  their absence was causing issues with various scripting languages.
- Reformatted against the Puppet Labs style guide.
- Improved test stubs.

* Mon Dec 26 2011 Maintenance
2.0.0-3
- Updated the spec file to not require a separate file list.

* Tue May 31 2011 Maintenance - 2.0.0-2
- Set PrintLastLog to 'no' by default since this is now handled by PAM.
- Removed CBC ciphers from the client and server.
- No longer enable X11 forwarding on SSH servers by default.
- Reduce the acceptable SSH cipher set to AES without CBC.

* Fri Feb 11 2011 Maintenance - 2.0.0-1
- Changed all instances of defined(Class['foo']) to defined('foo') per the
  directions from the Puppet mailing list.
- Updated to use concat_build and concat_fragment types.

* Tue Jan 11 2011 Maintenance
2.0.0-0
- Refactored for SIMP-2.0.0-alpha release

* Tue Oct 26 2010 Maintenance - 1-2
- Converting all spec files to check for directories prior to copy.

* Wed Jun 30 2010 Maintenance
1.0-1
- /etc/ssh/ssh_known_hosts is now collected from all puppet managed hosts
  without using stored configs.

* Tue May 25 2010 Maintenance
1.0-0
- Code refactoring.
