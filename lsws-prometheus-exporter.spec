Name:           lsws-prometheus-exporter
Version:        0.0.1
Release:        2%{?dist}
Summary:        LiteSpeed Prometheus Exporter

License:       	GPL3
URL:            https://github.com/codyro/litespeed-prometheus-exporter
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.service
Patch0:		    0001-Implement-basic-auth-w-environmental-variables.patch

BuildRequires:  golang
BuildRequires:  systemd
#BuildRequires:	systemd-rpm-macros

%description
The LiteSpeed Prometheus Exporter is a specially designed Prometheus application and uses the LiteSpeed Enterprise or the OpenLiteSpeed Web Server controller to export Prometheus compatible data which can also be used by Grafana and other compatible applications.

%prep
%autosetup -p1

%build
CGO_ENABLED=0 GOOS=linux go mod tidy
CGO_ENABLED=0 GOOS=linux go build -o %{name} -ldflags \
	"-X main.version=%{version} -X main.gitRepo=b10b77f -linkmode=external"

%install
install -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%files
%{_bindir}/%{name}
%{_unitdir}/%{name}.service


%changelog
* Tue Oct 03 2023 - Cody Robertson <cody@hawkhost.com> - 0.0.1-2
- Add patch to support basic auth

* Tue Oct 03 2023 - Cody Robertson <cody@hawkhost.com> - 0.0.1-1
- Initial package

