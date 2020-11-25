Summary:	A code-searching tool similar to ack, but faster
Name:		the_silver_searcher
Version:	2.2.0
Release:	2
License:	Appache v2.0
Group:		Applications
Source0:	https://geoff.greer.fm/ag/releases/%{name}-%{version}.tar.gz
# Source0-md5:	958a614cbebf47b2f27a7d00a5bb1bcb
Patch0:		gcc10.patch
Patch1:		hl_multi_matches_nomultiline.patch
URL:		https://geoff.greer.fm/ag/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
Suggests:	bash-completion-%{name}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         zshdir %{_datadir}/zsh/site-functions

%description
An attempt to make something better than ack (which itself is better
than grep).

Why use Ag?
- It searches code about 3–5× faster than ack.
- It ignores file patterns from your .gitignore and .hgignore.
- If there are files in your source repo you don't want to search,
  just add their patterns to a .ignore file. *cough* extern *cough*
- The command name is 33% shorter than ack!

How is it so fast?
- Searching for literals (no regex) uses Boyer-Moore-Horspool strstr.
- Files are mmap()ed instead of read into a buffer.
- If you're building with PCRE 8.21 or greater, regex searches use the
  JIT compiler.
- Ag calls pcre_study() before executing the regex on a jillion files.
- Instead of calling fnmatch() on every pattern in your ignore files,
  non-regex patterns are loaded into an array and binary searched.
- Ag uses Pthreads to take advantage of multiple CPU cores and search
  files in parallel.

%package -n bash-completion-%{name}
Summary:	bash-completion for the_silver_searcher
Group:		Applications/Shells
Requires:	bash-completion
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n bash-completion-%{name}
This package provides bash-completion for the_silver_searcher.

%package -n zsh-completion-%{name}
Summary:	zsh-completion for the_silver_searcher
Group:		Applications/Shells
Requires:	zsh
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n zsh-completion-%{name}
This package provides zsh-completion for the_silver_searcher.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/bash_completion.d
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/completions/ag.bashcomp.sh
cp -p ag.bashcomp.sh $RPM_BUILD_ROOT/etc/bash_completion.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/ag
%{_mandir}/man1/ag.1*

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/*

%files -n zsh-completion-%{name}
%defattr(644,root,root,755)
%{zshdir}/_the_silver_searcher
