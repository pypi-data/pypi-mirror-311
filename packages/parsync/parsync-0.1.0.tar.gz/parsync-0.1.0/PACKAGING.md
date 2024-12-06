# Packaging instructions

## RPM

1. Install build dependencies: 
```
dnf install python3-devel rpmdevtools
```
2. Edit the packaging/rpm/spec file and set *python3_pkgversion* to your system python version (`python3 -V`).
3. Update the *Version* and *Release* fields if necessary.
4. Build the package (update versions accordingly):
```sh
mkdir -p rpmbuild/SOURCES
git archive --prefix=parsync-1.0.0/ -o rpmbuild/SOURCES/parsync-1.0.0.tar.gz HEAD
rpmbuild --define "_topdir $PWD/rpmbuild" -bb packaging/rpm/parsync.spec
```
