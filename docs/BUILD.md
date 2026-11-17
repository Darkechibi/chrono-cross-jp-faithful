# Rebuilding the patch from a stock lang.dat

1. Copy a **stock** Steam `data/lang.dat` (before this pack) into a working folder as `lang.dat`.
2. Run the tools in `source/` in roughly this order (paths inside those scripts may need a one-line edit to point at your `lang.dat`):
   - dialect flatten / `fix_dialect.py` (and related accent cleanup)
   - `restore_names.py` (romaji names + places)
   - invent / option fix scripts (`fix_invent.py`, `fix_inv_opts.py`, etc.)
3. Extract the members listed in `installer/install.py` (`PATCH_FILES`) into `patch/`.
4. Test with `python installer/install.py`.

The prebuilt `patch/` folder is what end users need. Rebuilding is only for contributors.
