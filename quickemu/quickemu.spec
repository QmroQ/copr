Name:           quickemu
Version:        4.9.7
Release:        1%{?dist}

Summary:        Quickly create and run optimised Windows, macOS and Linux virtual machines.
License:        MIT
URL:            https://github.com/quickemu-project/quickemu

Source0:        %{url}/archive/refs/tags/%{version}.tar.gz

BuildArch:      noarch

Requires:       coreutils, util-linux, xdg-user-dirs, procps-ng, bash, grep, sed, jq, curl, unzip
Requires:       qemu, edk2-tools, spice-gtk-tools, swtpm
Requires:       usbutils, pciutils
Requires:       genisoimage
Requires:       mesa-demos
Requires:       python3
Requires:       xrandr
Requires:       socat
Requires:       zsync

Recommends: 	quickgui

%description
Features:
    Host support for Linux and macOS
    macOS Sonoma, Ventura, Monterey, Big Sur, Catalina & Mojave
    Windows 10 and 11 including TPM 2.0
    Windows Server 2022 2019 2016
    Ubuntu and all the official Ubuntu flavours
    Nearly 1000 operating system editions are supported!
    Full SPICE support including host/guest clipboard sharing
    VirtIO-webdavd file sharing for Linux and Windows guests
    VirtIO-9p file sharing for Linux and macOS guests
    QEMU Guest Agent support; provides access to a system-level agent via standard QMP commands
    Samba file sharing for Linux, macOS and Windows guests (if smbd is installed on the host)
    VirGL acceleration
    USB device pass-through
    Smartcard pass-through
    Automatic SSH port forwarding to guests
    Network port forwarding
    Full duplex audio
    Braille support
    EFI (with or without SecureBoot) and Legacy BIOS boot

%prep
%autosetup

%install
# Install binaries
install -Dpm755 chunkcheck %{buildroot}%{_bindir}/chunkcheck
install -Dpm755 quickemu %{buildroot}%{_bindir}/quickemu
install -Dpm755 quickget %{buildroot}%{_bindir}/quickget
install -Dpm755 quickreport %{buildroot}%{_bindir}/quickreport

# Install manpages
install -Dpm644 docs/quickemu_conf.5 %{buildroot}%{_mandir}/man5/quickemu_conf.5
install -Dpm644 docs/quickemu.1 %{buildroot}%{_mandir}/man1/quickemu.1
install -Dpm644 docs/quickget.1 %{buildroot}%{_mandir}/man1/quickget.1

%files
%license LICENSE
%doc README.md

# binaries
%{_bindir}/chunkcheck
%{_bindir}/quickemu
%{_bindir}/quickget
%{_bindir}/quickreport

# manpages
%{_mandir}/man5/quickemu_conf.5*
%{_mandir}/man1/quickemu.1*
%{_mandir}/man1/quickget.1*

%changelog
%autochangelog