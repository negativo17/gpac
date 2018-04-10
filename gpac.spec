# AMR Narrow Band Fixed
%global ver_nb_fixed d00
# AMR Narrow Band
%global ver_nb d00
# AMR Wide Band
%global ver_wb d10

Name:       gpac
Version:    0.7.1
Release:    2%{?dist}
Epoch:      1
Summary:    Open Source multimedia framework
License:    LGPLv2+
URL:        https://gpac.wp.mines-telecom.fr/

Source0:    https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:    http://www.3gpp.org/ftp/Specs/archive/26_series/26.073/26073-%{ver_nb_fixed}.zip
Source2:    http://www.3gpp.org/ftp/Specs/archive/26_series/26.104/26104-%{ver_nb}.zip
Source3:    http://www.3gpp.org/ftp/Specs/archive/26_series/26.204/26204-%{ver_wb}.zip

Patch0:     %{name}-0.6.1-manpages.patch

BuildRequires:  a52dec-devel
BuildRequires:  doxygen
BuildRequires:  faad2-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  freetype-devel >= 2.1.4
BuildRequires:  git
#BuildRequires:  libGLU-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libmad-devel
BuildRequires:  libogg-devel
BuildRequires:  libtheora-devel
BuildRequires:  libvorbis-devel 
BuildRequires:  libXv-devel
BuildRequires:  libpng-devel >= 1.2.5
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  SDL-devel
BuildRequires:  wxGTK-devel
BuildRequires:  xmlrpc-c-devel
BuildRequires:  xvidcore-devel >= 1.0.0
BuildRequires:  zlib-devel

%if 0%{?fedora} >= 26 || 0%{?rhel} >= 8
BuildRequires:      compat-openssl10-devel
%else
BuildRequires:      openssl-devel
%endif

%description
GPAC is an Open Source multimedia framework. GPAC is used for research and
academic purposes and beyond through industrial collaborations! The project
covers different aspects of multimedia, with a focus on presentation
technologies (graphics, animation and interactivity) and on multimedia packaging
formats such as MP4.

%package        libs
Summary:        Library for %{name}

%description    libs
GPAC is an Open Source multimedia framework. GPAC is used for research and
academic purposes and beyond through industrial collaborations! The project
covers different aspects of multimedia, with a focus on presentation
technologies (graphics, animation and interactivity) and on multimedia packaging
formats such as MP4.

This package contains the basic libraries.

%package        devel
Summary:        Development libraries and files for %{name}
Requires:       %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}

%description  devel
GPAC is an Open Source multimedia framework. GPAC is used for research and
academic purposes and beyond through industrial collaborations! The project
covers different aspects of multimedia, with a focus on presentation
technologies (graphics, animation and interactivity) and on multimedia packaging
formats such as MP4.

This package contains development libraries and files for gpac.

%prep
%setup -q -a1 -a2 -a3
%patch0 -p1

# AMR Narrow Band Fixed
unzip -q 26073-%{ver_nb_fixed}_ANSI_C_source_code.zip -d 26073-%{ver_nb_fixed}
rm -f 26073-%{ver_nb_fixed}/c-code/typedefs.h
mv 26073-%{ver_nb_fixed}/c-code/* modules/amr_dec/amr_nb

# AMR Narrow Band
unzip -q 26104-%{ver_nb}_ANSI_C_source_code.zip -d 26104-%{ver_nb}
mv 26104-%{ver_nb}/c-code modules/amr_float_dec/amr_nb_ft

# AMR Wide Band
unzip -q 26204-%{ver_wb}_ANSI-C_source_code.zip -d 26204-%{ver_wb}
mv 26204-%{ver_wb}/c-code modules/amr_float_dec/amr_wb_ft

# rpmlint fixes
find . -name "*.h" -exec chmod 644 {} \;
find . -name "*.c" -exec chmod 644 {} \;
for i in doc/ipmpx_syntax.bt Changelog; do
    iconv -f ISO-8859-1 -t UTF8 $i > $i.utf8
    mv $i.utf8 $i
done

sed -i -e 's/-O3//g' configure

%build
# Momentarily disable AMR-NB fixed
# --enable-amr-fixed
%configure \
    --disable-oss-audio \
    --enable-amr \
    --enable-pic \
    --enable-pulseaudio \
    --enable-fixed-point \
    --enable-joystick \
    --enable-depth \
    --extra-cflags="%{optflags}" \
    --libdir=%{_lib} \
    --verbose \
    --X11-path=%{_prefix}

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install install-lib INSTFLAGS="-p"
find %{buildroot} -name "*.a" -delete
rm -f %{buildroot}%{_mandir}/man1/DashCast.*

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%{_bindir}/MP42TS
%{_bindir}/MP4Box
%{_bindir}/MP4Client
%{_datadir}/%{name}/
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man1/MP42TS.1.gz
%{_mandir}/man1/MP4Box.1.gz
%{_mandir}/man1/MP4Client.1.gz

%files libs
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS BUGS Changelog
%{_libdir}/%{name}
%{_libdir}/libgpac.so.*

%files devel
%doc doc/CODING_STYLE
%doc doc/ipmpx_syntax.bt
%{_includedir}/%{name}
%{_libdir}/libgpac.so

%changelog
* Tue Apr 10 2018 Simone Caronni <negativo17@gmail.com> - 1:0.7.1-2
- Rebuild for updated dependencies.

* Sat May 06 2017 Simone Caronni <negativo17@gmail.com> - 1:0.7.1-1
- Update to 0.7.1.

* Wed Nov 09 2016 Simone Caronni <negativo17@gmail.com> - 1:0.6.1-4
- Rebuild for FFmpeg update.

* Fri Jul 22 2016 Simone Caronni <negativo17@gmail.com> - 1:0.6.1-3
- Rebuild for ffmpeg 3.1.1.

* Fri Jul 01 2016 Simone Caronni <negativo17@gmail.com> - 1:0.6.1-2
- Export gf_isom_set_pixel_aspect_ratio for x264.

* Fri Apr 22 2016 Simone Caronni <negativo17@gmail.com> - 1:0.6.1-1
- First build.
- Momentarily disable AMR narrow band fixed-point.
