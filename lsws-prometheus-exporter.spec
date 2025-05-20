%define debug_package %{nil}
%define git_commit a07898e
%global git_commit_long a07898ee3e3bd4dfeaed29f6863e37f373a0e943
%global commit_dir litespeed-prometheus-exporter-%{git_commit_long}

Name:           lsws-prometheus-exporter
Version:        0.1.2
Release:        1%{?dist}
Summary:        LiteSpeed Prometheus Exporter

License:        GPL3
URL:            https://github.com/litespeedtech/litespeed-prometheus-exporter
Source0:        https://github.com/litespeedtech/litespeed-prometheus-exporter/archive/%{git_commit}/%{name}-%{version}.tar.gz
Source1:        %{name}.service
Source2:        %{name}.env
Patch0:         0001-Implement-basic-auth-w-environmental-variables.patch

BuildRequires:  golang
BuildRequires:  systemd

%description
The LiteSpeed Prometheus Exporter is a specially designed Prometheus application and uses the LiteSpeed Enterprise or the OpenLiteSpeed Web Server controller to export Prometheus compatible data which can also be used by Grafana and other compatible applications.

%prep
%setup -q -n %{commit_dir}
%patch0 -p1

%build
CGO_ENABLED=0 GOOS=linux go mod tidy
CGO_ENABLED=0 GOOS=linux go build -o %{name} -ldflags \
	"-X main.version=%{version} -X main.gitRepo=%{git_commit}"

%install
install -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%files
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_sysconfdir}/sysconfig/%{name}


%changelog
* Tue May 20 2025 Cody Robertson <cody@hawkhost.com> - 0.1.2-1
- Update from upstream

* Wed Oct 04 2023 Cody Robertson <cody@hawkhost.com> - 0.0.1-3
- Update service file to use environment file

* Tue Oct 03 2023 Cody Robertson <cody@hawkhost.com> - 0.0.1-2
- Add patch to support basic auth

* Tue Oct 03 2023 Cody Robertson <cody@hawkhost.com> - 0.0.1-1
- Initial package
