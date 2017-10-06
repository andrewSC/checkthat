Checkthat
=========
A automated Arch Linux AUR package builder and analyzer written in Python.::

  ------------------------------ Build Results ------------------------------
  Successfully built [gtk4-git-3.91.2.r653.gfbf24d1bd0-1-x86_64.pkg.tar]
  Successfully built [git-git-2.15.0.rc0.r0.g217f2767cb-1-x86_64.pkg.tar]
  Successfully built [vlc-git-3.0.0.r14788.g168bd3f8e7-1-x86_64.pkg.tar]
  Successfully built [atk-git-2.26.0.4.g9146905.9146905-1-x86_64.pkg.tar]
  Successfully built [glib2-git-2.54.0.85.g860dc949c-1-x86_64.pkg.tar]
  Successfully built [gnome-common-git-3.14.0.r14.1df0aa1-1-any.pkg.tar]
  Successfully built [pango-git-1.40.12.3946.a22187d6-1-x86_64.pkg.tar]
  Successfully built [gobject-introspection-git-debug-1:1.55.0.3674.0e37344f-1-x86_64.pkg.tar]
  Successfully built [wayland-git-1.14.90.2026.f6bbc97-1-x86_64.pkg.tar]
  Successfully built [firefox-developer-57.0b6-1-x86_64.pkg.tar]
  Successfully built [opencv-git-3.3.0.r440.gfe58b58937-1-x86_64.pkg.tar]

  Total build time: 25.0m 17.19808006286621s
  ---------------------------------------------------------------------------

  ------------------------------ Namcap PKGBUILD Analysis ------------------------------
  PKGBUILD (gtk4-git) I: Missing Contributor tag
  --------------------------------------------------------------------------------------

  ------------------------------ Namcap Pkg Analysis ------------------------------
  gtk4-git W: File (usr/libexec/) exists in a non-standard directory.
  gtk4-git W: File (usr/libexec/installed-tests/) exists in a non-standard directory.
  gtk4-git W: File (usr/libexec/installed-tests/gtk-4.0/) exists in a non-standard directory.
                                        ...
  ---------------------------------------------------------------------------------


System Requirements
------------
- This tool requires that you have namcap_, ``makepkg`` (which is provided by pacman_), and you'll most likely want to have the base-devel_ group installed too.

.. _namcap: https://www.archlinux.org/packages/extra/any/namcap/
.. _pacman: https://www.archlinux.org/packages/core/x86_64/pacman/
.. _base-devel: https://www.archlinux.org/groups/x86_64/base-devel/


Installation
-----
Clone the repo and run ``pip install .``


Usage
------
``checkthat <path_to_folder>``
