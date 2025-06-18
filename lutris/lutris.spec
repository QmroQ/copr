%define debug_package %{nil}

%global snapshot 1
%define commit0 6d0fc12b95689f72127ed82516dc2ebae21a8963
%define shortcommit0 6d0fc12

Name:           lutris
Version:        0.5.19
Release:        2.git.%{shortcommit0}%{?dist}

Summary:        free and open source game manager for Linux
License:        GPL-3.0-or-later
URL:            https://github.com/lutris/lutris

%if 0%{?snapshot}
Source0:        %{url}/archive/%{commit0}.tar.gz
%else
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  python3-devel

Requires:       cabextract
Requires:       gtk3
Requires:       psmisc
Requires:       xorg-x11-server-Xephyr
Requires:       xrandr
Requires:       hicolor-icon-theme
Requires:       gnome-desktop3
Requires:       python3-distro
Requires:       python3-cairo
Requires:       umu-launcher

# Tests
BuildRequires:  python3dist(pytest)
BuildRequires:  pkgconfig(gdk-3.0)
BuildRequires:  pkgconfig(webkit2gtk-4.1)
BuildRequires:  pkgconfig(py3cairo)

%ifarch x86_64
Requires:       mesa-dri-drivers(x86-32)
Requires:       mesa-vulkan-drivers(x86-32)
Requires:       vulkan-loader(x86-32)
Requires:       mesa-libGL(x86-32)
Recommends:     pipewire(x86-32)
Recommends:     libFAudio(x86-32)
Recommends:     wine-pulseaudio(x86-32)
Recommends:     wine-core(x86-32)
%endif

Requires:       mesa-vulkan-drivers
Requires:       mesa-dri-drivers
Requires:       vulkan-loader
Requires:       mesa-libGL
Requires:       glx-utils
Requires:       gvfs
Requires:       webkit2gtk4.1
Recommends: 	p7zip, p7zip-plugins
Recommends: 	curl
Recommends:	    fluid-soundfont-gs
Recommends:     wine-core
Recommends: 	gamemode
Recommends:     libFAudio
Recommends:     gamescope

BuildRequires:  fdupes
BuildRequires:  libappstream-glib
BuildRequires:  meson
BuildRequires:  gettext

%description
Lutris is a gaming platform for GNU/Linux. Its goal is to make
gaming on Linux as easy as possible by taking care of installing
and setting up the game for the user. The only thing you have to
do is play the game. It aims to support every game that is playable
on Linux.

%prep
%autosetup -n %{name}-%{commit0} -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel
%meson
%meson_build

%install
%pyproject_install
%pyproject_save_files lutris
%meson_install
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/metainfo/net.%{name}.Lutris.metainfo.xml
%fdupes %{buildroot}%{python3_sitelib}
desktop-file-install --dir=%{buildroot}%{_datadir}/applications share/applications/net.%{name}.Lutris.desktop

%check
%pytest --ignore=tests/test_dialogs.py --ignore=tests/test_installer.py --ignore=tests/test_api.py -k "not GetNvidiaDriverInfo and not GetNvidiaGpuInfo and not import_module and not options"

%files -f %{pyproject_files}
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/net.%{name}.Lutris.desktop
%{_datadir}/icons/hicolor/scalable/apps/net.%{name}.Lutris.svg
%{_datadir}/icons/hicolor/16x16/apps/net.%{name}.Lutris.png
%{_datadir}/icons/hicolor/22x22/apps/net.%{name}.Lutris.png
%{_datadir}/icons/hicolor/24x24/apps/net.%{name}.Lutris.png
%{_datadir}/icons/hicolor/32x32/apps/net.%{name}.Lutris.png
%{_datadir}/icons/hicolor/48x48/apps/net.%{name}.Lutris.png
%{_datadir}/icons/hicolor/64x64/apps/net.%{name}.Lutris.png
%{_datadir}/icons/hicolor/128x128/apps/net.%{name}.Lutris.png
%{_datadir}/man/man1/%{name}.1.gz

%{python3_sitelib}/%{name}/__pycache__/optional_settings.*.pyc
%{python3_sitelib}/%{name}/optional_settings.py

%{_datadir}/metainfo/
%{_datadir}/locale/

%changelog
%autochangelog