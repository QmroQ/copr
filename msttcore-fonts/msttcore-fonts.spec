%define fontname msttcore
%define fontdir %{_datadir}/fonts/%{fontname} 

%define download_script     /usr/lib/msttcore-fonts-installer/refresh-msttcore-fonts.sh
%define cabfiles_sha256sums /usr/lib/msttcore-fonts-installer/cabfiles.sha256sums
%define license_file        /usr/share/doc/msttcore-fonts-installer/READ_ME!

Name:           %{fontname}-fonts
Version:        2.6
Release:        1%{?dist}

Summary:        Installer for Microsoft core TrueType fonts for better Windows Compatibility
License:        GPL-2.0-only
URL:            https://mscorefonts2.sourceforge.net

Source:         https://downloads.sourceforge.net/mscorefonts2/mscorefonts2-%{version}.tar.gz

BuildArch:      noarch

Requires:       curl
Requires:       cabextract
Requires:       xorg-x11-font-utils
Requires:       fontconfig

%description
This installs the TrueType core fonts for the web that were once
available from http://www.microsoft.com/typography/fontpack/ prior
to 2002, and most recently updated in the European Union Expansion
Update circa May 2007, still available on the Microsoft website.
This also installs Microsoft's ClearType fonts, see
http://www.microsoft.com/typography/ClearTypeFonts.mspx for more info.

Note that the TrueType fonts are not part of the rpm.  They are
downloaded by the rpm when the rpm is installed.

The font cab files are downloaded from a Sourceforge project mirror
and unpacked at install time. Therefore this package technically
does not 'redistribute' the cab files.  The fonts are then added to
the core X fonts system as well as the Xft font system.

These are the cab files downloaded:

    andale32.exe, arialb32.exe, comic32.exe, courie32.exe,
    georgi32.exe, impact32.exe, webdin32.exe, EUupdate.EXE,
    wd97vwr32.exe, PowerPointViewer.exe

The following cab files are only downloaded if EUupdate.EXE cannot
be downloaded, since the EUupdate.EXE cab contains updates for
the fonts in these cabs:

    arial32.exe, times32.exe, trebuc32.exe, verdan32.exe

These are the fonts added:

    1998 Andale Mono
    2006 Arial: bold, bold italic, italic, regular
    1998 Arial: black
    2007 Calabri: bold, bold italic, italic, regular
    2007 Cambria: bold, bold italic, italic
    2007 Candara: bold, bold italic, italic, regular
    2007 Consolas: bold, bold italic, italic, regular
    2007 Constantia: bold, bold italic, italic, regular
    2007 Corbel: bold, bold italic, italic, regular
    1998 Comic: bold, regular
    2000 Courier: bold, bold italic, italic, regular
    1998 Impact
    2006 Times: bold, bold italic, italic, regular
    2006 Trebuchet: bold, bold italic, italic, regular
    2006 Verdana: bold, bold italic, italic, regular
    1998 Webdings

%prep
%setup -n msttcore-fonts-installer-2.6

%install
find . | cpio -pdm $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{fontdir}
echo not-empty > $RPM_BUILD_ROOT/%{fontdir}/fonts.dir 
echo not-empty > $RPM_BUILD_ROOT/%{fontdir}/fonts.scale 

mkdir -p $RPM_BUILD_ROOT/etc/X11/xorg.conf.d/
cat -> $RPM_BUILD_ROOT/etc/X11/xorg.conf.d/09-msttcore-fontpath.conf <<'EOT'
Section "Files"
  FontPath "%{fontdir}"
EndSection
EOT

%clean
[ "${RPM_BUILD_ROOT:-nonexistantdir}" != "/" ] && rm -rf ${RPM_BUILD_ROOT:-nonexistantdir}

%post
%{download_script} -F %{fontdir} -L %{license_file}

%postun
if [ "$1" = "0" ]; then
  counter=0
  for ff in %{fontdir}/*.ttf; do
    if [ -f "$ff" ]; then
      if [ $counter -eq 0 ]; then
        echo "### Removing ttf files in %{fontdir}" >&2
      fi

      # these files are installed "manually" so they must be removed "manually".
      # ie, rpm won't do it for us, it doesn't know about them.
      rm -f "$ff"

      counter=`expr $counter + 1`
    fi
  done
  if [ $counter -gt 0 ]; then
    echo "### ttf files already removed" >&2
  fi
  if [ -x %{_bindir}/fc-cache ]; then
    echo "### Rebuilding Xft font cache" >&2
    %{_bindir}/fc-cache -f -v || :
  fi

  [ -f /etc/fonts/conf.d/09-msttcore-fonts.conf ] && rm -f /etc/fonts/conf.d/09-msttcore-fonts.conf
  [ -f "%{license_file}" ] && rm -f "%{license_file}"
  [ -f /usr/lib/msttcore-fonts-installer/installed-list.txt ] && rm -f /usr/lib/msttcore-fonts-installer/installed-list.txt

  echo "### Removing %{fontdir} from the core X fonts path" >&2
  xset -fp %{fontdir} || :
  xset fp rehash || :
fi

%files
%defattr(-,root,root,-)
%attr(-,root,root) %{fontdir}
%config(noreplace) /etc/X11/xorg.conf.d/09-msttcore-fontpath.conf
%docdir /usr/share/doc/msttcore-fonts-installer
%attr(-,root,root) /usr/share/doc/msttcore-fonts-installer

/usr/lib/msttcore-fonts-installer

%changelog
%autochangelog