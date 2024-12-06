%global python3_pkgversion 3.11

Name:           python-parsync
Version:        1.0.0
Release:        1%{?dist}
Summary:        Example Python library

License:        MIT
URL:            https://github.com/fedora-python/parsync
Source:         %{url}/archive/v%{version}/parsync-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python%{python3_pkgversion}-devel

# Build dependencies needed to be specified manually
BuildRequires:  python%{python3_pkgversion}-setuptools


%description
Parsync recursively copies missing files to a directory

%package -n python%{python3_pkgversion}-parsync
Summary:        %{summary}

%description -n python%{python3_pkgversion}-parsync
Parsync recursively copies missing files to a directory

%prep
%autosetup -p1 -n parsync-%{version}


%build
# The macro only supported projects with setup.py
%py3_build


%install
# The macro only supported projects with setup.py
%py3_install


# Note that there is no %%files section for the unversioned python module
%files -n python%{python3_pkgversion}-parsync
%doc README.md
%license LICENSE.txt
%{_bindir}/parsync

# The library files needed to be listed manually
%{python3_sitelib}/parsync/

# The metadata files needed to be listed manually
%{python3_sitelib}/parsync-*.egg-info/