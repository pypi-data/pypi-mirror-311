# Installation

Onionprobe is [available on PyPI](https://pypi.org/project/onionprobe):

    pip install onionprobe

A package should be available for [Debian][]-like systems.

    sudo apt-get install onionprobe

An Arch Linux package is [available on AUR][][^arch-linux-package]:

    pacman -S onionprobe-git

It's also possible to run it directly from the [Git repository][]:

    git clone https://gitlab.torproject.org/tpo/onion-services/onionprobe
    cd onionprobe

[Ansible][] users can use the [Onionprobe Ansible Role][].

[Debian]: https://www.debian.org
[available on AUR]: https://aur.archlinux.org/packages/onionprobe-git
[Git repository]: https://gitlab.torproject.org/tpo/onion-services/onionprobe
[Ansible]: https://ansible.com
[Onionprobe Ansible Role]: https://gitlab.torproject.org/tpo/onion-services/ansible/onionprobe-role

[^arch-linux-package]: See also https://gitlab.torproject.org/tpo/onion-services/onionprobe/-/issues/16
