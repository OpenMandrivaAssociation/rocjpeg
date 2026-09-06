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
CXXFLAGS=$(printf '%s' "%{optflags}" | sed 's/-mfpmath=sse//g')
export CXXFLAGS
%cmake %{rocm_cmake_fhs} %{rocm_cmake_gpu_targets} \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DCMAKE_HIP_COMPILER=clang++ \
	-DCMAKE_HIP_ARCHITECTURES="%{rocm_gpu_targets}" \
	-DCMAKE_CXX_FLAGS="$CXXFLAGS" \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja
%ninja_build

%install
%ninja_install -C build
# Samples/tests/images are not part of the runtime package.
rm -rf %{buildroot}%{_datadir}/rocjpeg
rm -f %{buildroot}%{_docdir}/rocjpeg/LICENSE

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_libdir}/librocjpeg.so.*

%files devel
%{_includedir}/rocjpeg/
%{_libdir}/librocjpeg.so
%{_libdir}/cmake/rocjpeg/
