return {
  LrSdkVersion        = 6.0,
  LrSdkMinimumVersion = 6.0,
  LrToolkitIdentifier = 'com.pka-jch.argus-diag',
  LrPluginName        = 'Argus Diagnostic',

  LrLibraryMenuItems = {
    { title = 'DIAG 1 — createVirtualCopies', file = 'Diag1_VirtualCopy.lua', enabledWhen = 'photosSelected' },
    { title = 'DIAG 2 — switchToModule',      file = 'Diag2_SwitchDevelop.lua', enabledWhen = 'photosSelected' },
    { title = 'DIAG 3 — setValue',            file = 'Diag3_SetValue.lua', enabledWhen = 'photosSelected' },
  },

  VERSION = { major = 1, minor = 0, revision = 0, build = 0 },
}
