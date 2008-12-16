%define major		11
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Summary:	Powermanagement daemon supporting APM, ACPI and CPU frequency scaling
Name:		powersave
Version:	0.15.20
Release:	%{mkrel 1}
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:	powersave-initscript
Patch0:		powersave-0.15.20-underlink.patch
Requires:	cpufrequtils >= 0.4
Requires:	hal >= 0.5.5.1
Requires:	dbus >= 0.61
Conflicts:	cpufreqd
Conflicts:	apmd
Conflicts:	powernowd
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://powersave.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	cpufrequtils
BuildRequires:	libcpufreq-devel
BuildRequires:	hal-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	liblazy-devel
BuildRequires:	doxygen
BuildRequires:	lynx
BuildRequires:	texinfo

Requires(post):		rpm-helper
Requires(preun):	rpm-helper

%description
Powersave gives you control over the ACPI power buttons, three user
defined battery states (warning, low, critical) and supports proper
standby/suspend handling.

Additionally it could control the frequency of your processor if it
supports SpeedStep(Intel) or PowerNow(AMD) technology. This will
greatly reduce power consumption and heat production in your system.

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run %{name}.

%package -n %{develname}
Summary:	Development header files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname powersave 10 -d}

%description -n %{develname}
Libraries, include files and other resources you can use to develop
%{name} applications.

%prep
%setup -q
%patch0 -p1 -b .underlink

%build
# Needed by underlink.patch
autoreconf
%configure2_5x --enable-docs \
	--disable-on_ac_power  \
	--with-kde-bindir=%{_bindir} \
	--with-gnome-bindir=%{_bindir} \
	--enable-doc-dir=%{_datadir}/doc/%{name}

%make -e 'VERSION_NO="\"%{version}\""'

%install
rm -rf %{buildroot}
%makeinstall_std POWERSAVE_LIB_VERSION=%{version} TRANSLATION_DIR="%{_datadir}/locale/"

rm -rf %{buildroot}/%{_sysconfdir}/init.d
install -D -m 755 %{SOURCE1} %{buildroot}/%{_initrddir}/powersaved

mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
mv %{buildroot}/%{_sysconfdir}/%{name} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
ln -s %{_sysconfdir}/sysconfig/%{name} %{buildroot}/%{_sysconfdir}/%{name}
chmod 644 %{buildroot}/%{_datadir}/doc/%{name}/contrib/README.contrib

export DONT_GPRINTIFY=1

%find_lang power-management

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%post
%_post_service powersaved

%preun 
%_preun_service powersaved

%clean
rm -rf %{buildroot}

%files -f power-management.lang
%defattr(-,root,root)
%{_sbindir}/*
%{_bindir}/*
%_mandir/*/*
%{_libdir}/%{name}
%{_initrddir}/powersaved
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/powersave.conf
%config(noreplace) %{_sysconfdir}/acpi/events.ignore/events.ignore
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%doc %{_datadir}/doc/%{name}

%files -n  %{develname}
%defattr(-,root,root)
%_includedir/*
%_libdir/lib*.la
%_libdir/lib*.a
%_libdir/lib*.so
%_libdir/pkgconfig/*.pc

%files -n %{libname}
%defattr(-,root,root)
%_libdir/lib*.so.%{major}*

