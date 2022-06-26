## Download

Binaries, installers, and source tarballs are available at https://nodejs.org/en/download/.

### Current and LTS releases

https://nodejs.org/download/release/

The [latest](https://nodejs.org/download/release/latest/) directory is an alias for the latest Current release. The latest-*codename* directory is an alias for the latest release from an LTS line. For example, the [latest-fermium](https://nodejs.org/download/release/latest-fermium/) directory contains the latest Fermium (Node.js 14) release.

### Nightly releases

https://nodejs.org/download/nightly/

Each directory name and filename contains a date (in UTC) and the commit SHA at the HEAD of the release.

### API documentation

Documentation for the latest Current release is at https://nodejs.org/api/. Version-specific documentation is available in each release directory in the *docs* subdirectory. Version-specific documentation is also at https://nodejs.org/download/docs/.

## Verifying binaries

Download directories contain a `SHASUMS256.txt` file with SHA checksums for the files.

To download `SHASUMS256.txt` using `curl`:

```
$ curl -O https://nodejs.org/dist/vx.y.z/SHASUMS256.txt
```

To check that a downloaded file matches the checksum, run it through `sha256sum` with a command such as:

```
$ grep node-vx.y.z.tar.gz SHASUMS256.txt | sha256sum -c -
```

For Current and LTS, the GPG detached signature of `SHASUMS256.txt` is in `SHASUMS256.txt.sig`. You can use it with `gpg` to verify the integrity of `SHASUMS256.txt`. You will first need to import [the GPG keys of individuals authorized to create releases](#release-keys). To import the keys:

```
$ gpg --keyserver hkps://keys.openpgp.org --recv-keys DD8F233
```

See [Release keys](#release-keys) for a script to import active release keys.

Next, download the `SHASUMS256.txt.sig` for the release:

```
$ curl -O https://nodejs.org/dist/vx.y.z/SHASUMS256.txt.sig
```

Then use `gpg --verify SHASUMS256.txt.sig SHASUMS256.txt` to verify the file's signature.

## Building Node.js

See [BUILDING.md](BUILDING.md) for instructions on how to build Node.js from source and a list of supported platforms.

## Security

For information on reporting security vulnerabilities in Node.js, see [SECURITY.md](./SECURITY.md).
