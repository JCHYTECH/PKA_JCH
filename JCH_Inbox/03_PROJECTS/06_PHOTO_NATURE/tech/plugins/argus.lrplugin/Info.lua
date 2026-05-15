return {
  LrSdkVersion        = 6.0,
  LrSdkMinimumVersion = 6.0,
  LrToolkitIdentifier = 'com.pka-jch.argus',
  LrPluginName        = 'Argus Analyse Photo',

  LrLibraryMenuItems = {
    {
      title        = 'Analyser avec Argus',
      file         = 'ArgusAnalysis.lua',
      enabledWhen  = 'photosSelected',
    },
  },

  VERSION = { major = 1, minor = 0, revision = 0, build = 0 },
}
