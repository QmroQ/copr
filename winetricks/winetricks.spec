%global commit0 50417b23b5d3e79c6c8fa4d1af69167dfa3de719
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 1

Name:           winetricks
Version:        20250620
Release:        %{bumpver}.git%{shortcommit0}

Summary:        Winetricks is an easy way to work around problems in Wine
License:        LGPL-2.1-or-later
URL:            https://github.com/Winetricks/winetricks

Source0:        %{url}/archive/%{commit0}.tar.gz

BuildArch:      noarch

ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64
ExcludeArch:    ppc64 ppc64le

BuildRequires:  desktop-file-utils
BuildRequires:  make

Requires:       cabextract gzip unzip wget which
Requires:       hicolor-icon-theme
Requires:       wine-common
Requires:       zenity

%description
Winetricks is an easy way to work around problems in Wine.

It has a menu of supported games/apps for which it can do all the
workarounds automatically. It also allows the installation of missing DLLs
and tweaking of various Wine settings.

%prep
%setup -qn %{name}-%{commit0}
sed -i -e s:steam:: -e s:flash:: tests/*

%install
%make_install
install -m0644 -D -t %{buildroot}%{_datadir}/metainfo src/io.github.winetricks.Winetricks.metainfo.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license COPYING debian/copyright
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/metainfo/io.github.winetricks.Winetricks.metainfo.xml

%changelog
%autochangelog