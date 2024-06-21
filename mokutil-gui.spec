Name:           mokutil-gui
Version:        1
Release:        1%{?dist}
Summary:        Rpmfusion mokutil Gui to create and enroll key for secure boot

License:        GPLv2+
URL:            https://rpmfusion.org/
Source0:        %{name}.py
Source1:        %{name}
Source2:        %{name}.policy
Source3:        %{name}.desktop
Source4:        %{name}.svg

BuildArch:	   noarch

BuildRequires:      desktop-file-utils

Requires:      akmods
Requires:      mokutil
Requires:      openssl
Requires:      PolicyKit-authentication-agent
Requires:      python3-pyqt6


%description
Rpmfusion mokutil Gui to create and enroll key for secure boot.

%prep


%build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_prefix}/lib/%{name}/
mkdir -p %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
mkdir -p %{buildroot}%{_datadir}/polkit-1/actions/
install -p -m 0755 %{SOURCE0} %{buildroot}%{_prefix}/lib/%{name}/
install -p -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/
install -p -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/polkit-1/actions/
install -p -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/applications/
install -p -m 0644 %{SOURCE4} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%{_bindir}/%{name}
%{_prefix}/lib/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/polkit-1/actions/%{name}.policy



%changelog
* Thu Jun 20 2024 Leigh Scott <leigh123linux@gmail.com> 1-1
- First build
