# JPEG decode on GPU. TheRock 10.0.

Name:		rocjpeg
Version:	10.0.0
Release:	1
Summary:	ROCm JPEG decode library
License:	MIT
Group:		System/Libraries
URL:		https://github.com/ROCm/rocm-systems
Source0:	https://github.com/ROCm/rocm-systems/releases/download/therock-10.0/rocjpeg.tar.gz#/rocjpeg-%{version}.tar.gz

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	hipcc
BuildRequires:	rocm-hip-devel
BuildRequires:	pkgconfig(libva)
BuildRequires:	pkgconfig(libdrm)

%description
rocJPEG decodes JPEG images into HIP device memory using VCN/VA-API.

%package devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and CMake package for rocJPEG.

%prep
%autosetup -n rocjpeg -p1

%build
export CXX=hipcc
export CC=clang
%cmake %{rocm_cmake_fhs} \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja
%ninja_build -C build

%install
%ninja_install -C build

%files
%license LICENSE.md
%doc README.md
%{_libdir}/librocjpeg.so.*
%{_bindir}/rocjpeg*

%files devel
%{_includedir}/rocjpeg/
%{_libdir}/librocjpeg.so
%{_libdir}/cmake/rocjpeg/
