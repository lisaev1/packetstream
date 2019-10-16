# Arch Linux package sources

This directory contains buildscripts for Arch Linux packages used by PacktStream that are not available in the official repos (core, extra and community). These packages are customized versions of the corresponding AUR packages and all credits should go to their respective authors. Thanks for you work and contributions!

We used [UplinkLabs](https://www.uplinklabs.net/projects/arch-linux-on-ec2/) AMIs described in [ArchWiki](https://wiki.archlinux.org/index.php/Arch_Linux_AMIs_for_Amazon_Web_Services) and did the following customization to launched instances:

1. Enable color output and comment `[multilib]` in `/etc/pacman.conf`.
2. Enable `kernel.org` mirrors in `/etc/pacman.d/mirrorlist`.
3. Remove unneeded packages:
```
pacman -Rsn xfsprogs vim vi usbutils lvm2 sudo nano s-nail reiserfsprogs logrotae man-db man-pages mdadm licenses jfsutils systemd-sysvcompat netctl dhcpcd

# linux-firmware is required by linux-ec2, but is not actually used...
# With FS#59834 implemented, no -dd should be necessary.
pacman -Rdd linux-firmware
```
4. Set up `vi` alias:
```
alias vi="/usr/lib/initcpio/busybox vi"
```
5. Make systemd-journal volatile.
6. Configure Yama security, set `kernel.yama.ptrace_scope = 3` in `/etc/sysctl.d/99-security.conf`.
7. Kernel cmdline:
```
audit=0 ipv6.disable=1 security=yama init=/usr/lib/systemd/systemd ro
```
and run `grub-mkconfig -o /boot/grub/grub.cfg`.
8. Disable services:
```
systemctl disable rc-local.service auditd.service getty@tty1.service
```
9. Configure `/etc/fstab`.
10. Update.
