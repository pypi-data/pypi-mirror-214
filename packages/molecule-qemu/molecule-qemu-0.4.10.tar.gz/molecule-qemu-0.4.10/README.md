# `molecule-qemu`

Molecule QEMU driver for testing Ansible roles.

## Usage

```bash
pip install molecule-qemu
```

Install QEMU and CDRTools on macOS:

```bash
brew install qemu cdrtools
```

Supported platforms:
* MacOS 13.x (aaarch64)

Support guest OS:
* Ubuntu 20.04 LTS (aarch64, x86_64)
* Ubuntu 22.04 LTS (aarch64, x86_64)
* Debian 11 (aarch64, x86_64)

Support of other platforms and guest OS is possible, but not tested. Please, open an issue if you want to add support for other platforms.

## Network modes

Network mode is selected by setting `vm_network` in `molecule.yml`. Supported modes are: `user` and `vmnet-shared`. Default mode is `user`. All modes are mutually exclusive.

### `user` network mode

This is the default network mode. It uses QEMU's user networking mode.

Mode is selected by setting `vm_network: user` in `molecule.yml`.

### `vmnet-shared` network mode

This mode uses QEMU's `vmnet-shared` networking mode. It requires `vmnet.framework` to be installed on the host. This mode is only supported on MacOS. It requires *passwordless* `sudo` access for current user.

Mode is selected by setting `vm_network: vmnet-shared` in `molecule.yml`.

# Examples

## Example scenario
```bash
molecule init scenario default --driver-name molecule-qemu --verifier-name testinfra
```

## Example `molecule.yml` for `user` network mode

```yaml
---
dependency:
  name: galaxy
driver:
  name: molecule-qemu
platforms:
  - name: ubuntu-focal-arm64
    image: https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-arm64.img
    image_checksum: sha256:https://cloud-images.ubuntu.com/focal/current/SHA256SUMS
    image_arch: aarch64
    ssh_port: 10000
    ssh_user: ubuntu
  - name: ubuntu-focal-amd64
    image: https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img
    image_checksum: sha256:https://cloud-images.ubuntu.com/focal/current/SHA256SUMS
    image_arch: x86_64
    ssh_port: 10001
    ssh_user: ubuntu
  - name: ubuntu-jammy-arm64
    image: https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-arm64.img
    image_checksum: sha256:https://cloud-images.ubuntu.com/jammy/current/SHA256SUMS
    image_arch: aarch64
    ssh_port: 10002
    ssh_user: ubuntu
  - name: ubuntu-jammy-amd64
    image: https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img
    image_checksum: sha256:https://cloud-images.ubuntu.com/jammy/current/SHA256SUMS
    image_arch: x86_64
    ssh_port: 10003
    ssh_user: ubuntu
  - name: debian-bullseye-arm64
    image: https://cloud.debian.org/images/cloud/bullseye/latest/debian-11-genericcloud-arm64.qcow2
    image_checksum: sha512:https://cloud.debian.org/images/cloud/bullseye/latest/SHA512SUMS
    image_arch: aarch64
    ssh_port: 10004
    ssh_user: debian
  - name: debian-bullseye-amd64
    image: https://cloud.debian.org/images/cloud/bullseye/latest/debian-11-genericcloud-amd64.qcow2
    image_checksum: sha512:https://cloud.debian.org/images/cloud/bullseye/latest/SHA512SUMS
    image_arch: x86_64
    ssh_port: 10005
    ssh_user: debian
provisioner:
  name: ansible
verifier:
  name: ansible
```

## Example `molecule.yml` for `vmnet-shared` network mode

```yaml
---
dependency:
  name: galaxy
driver:
  name: molecule-qemu
platforms:
  - name: ubuntu-1
    image: https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-arm64.img
    image_checksum: sha256:https://cloud-images.ubuntu.com/focal/current/SHA256SUMS
    image_arch: aarch64
    ssh_user: ubuntu
    vm_network: vmnet-shared
  - name: ubuntu-2
    image: https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img
    image_checksum: sha256:https://cloud-images.ubuntu.com/focal/current/SHA256SUMS
    image_arch: x86_64  # default
    ssh_user: ubuntu
    vm_network: vmnet-shared
provisioner:
  name: ansible
verifier:
  name: ansible
```

# Cloud Images

## [Ubuntu](https://cloud-images.ubuntu.com/)
* https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-arm64.img
* https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img
* https://cloud-images.ubuntu.com/focal/current/SHA256SUMS
* https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-arm64.img
* https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img
* https://cloud-images.ubuntu.com/jammy/current/SHA256SUMS

## [Debian](https://cloud.debian.org/images/cloud/)
* https://cloud.debian.org/images/cloud/bullseye/latest/debian-11-genericcloud-amd64.qcow2
* https://cloud.debian.org/images/cloud/bullseye/latest/debian-11-genericcloud-arm64.qcow2
* https://cloud.debian.org/images/cloud/bullseye/latest/SHA512SUMS

# Reference

* [Ansible](https://www.ansible.com/)
* [Molecule](https://molecule.readthedocs.io/en/latest/)
* [QEMU](https://www.qemu.org/)
* [QEMU BIOS](https://packages.debian.org/bullseye/qemu-efi-aarch64)

## QEMU vmnet-shared networking

* [vmnet.framework modes](https://lore.kernel.org/all/20220315230741.21578-7-Vladislav.Yaroshchuk@jetbrains.com/T/)

