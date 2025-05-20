%define debug_package %{nil}
%define git_commit a07898e

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
%autosetup -n litespeed-prometheus-exporter-%{git_commit} -p1

%build
CGO_ENABLED=0 GOOS=linux go mod tidy
CGO_ENABLED=0 GOOS=linux go build -o %{name} -ldflags \
	"-X main.version=%{version} -X main.gitRepo=%{git_commit} -linkmode=external"

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
%autochangelog

