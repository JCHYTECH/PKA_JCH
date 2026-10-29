local LrApplication        = import 'LrApplication'
local LrApplicationView    = import 'LrApplicationView'
local LrDevelopController  = import 'LrDevelopController'
local LrDialogs            = import 'LrDialogs'
local LrPathUtils          = import 'LrPathUtils'
local LrTasks              = import 'LrTasks'

local PYTHON = '/usr/local/bin/python3'
local SCRIPT = '/Users/jchavauxm5/.claude/skills/photo-analyse-wildlife/scripts/run_analysis.py'

-- XMP param names → LrDevelopController names
local PARAM_MAP = {
  ColorTemperature = 'Temperature',
  Exposure2012     = 'Exposure',
  Contrast2012     = 'Contrast',
  Highlights2012   = 'Highlights',
  Shadows2012      = 'Shadows',
  Whites2012       = 'Whites',
  Blacks2012       = 'Blacks',
  Clarity2012      = 'Clarity',
  Dehaze           = 'Dehaze',
  Vibrance         = 'Vibrance',
  Saturation       = 'Saturation',
  Tint             = 'Tint',
}

local function trim(s)
  return s and s:match('^%s*(.-)%s*$') or ''
end

local function parse_output(output)
  local result = {}
  for line in output:gmatch('[^\n]+') do
    local key, val = line:match('^(%u+):%s*(.+)$')
    if key then result[key] = trim(val) end
  end
  return result
end


LrTasks.startAsyncTask(function()
  local catalog = LrApplication.activeCatalog()
  local photos  = catalog:getTargetPhotos()

  if #photos == 0 then
    LrDialogs.message('Argus', 'Selectionne une photo.', 'info')
    return
  end

  local photoPath = photos[1]:getRawMetadata('path')
  if not photoPath then
    LrDialogs.message('Argus', 'Chemin introuvable.', 'warning')
    return
  end

  LrDialogs.message(
    'Argus — Analyse en cours',
    'Cmd+\' fait ? (copie virtuelle)\n\n' .. LrPathUtils.leafName(photoPath) .. '\n\n~20 sec.',
    'info'
  )

  local cmd    = string.format('%s "%s" "%s" 2>&1', PYTHON, SCRIPT, photoPath)
  local handle = io.popen(cmd)
  local output = handle and handle:read('*a') or ''
  if handle then handle:close() end

  local parsed = parse_output(output)

  if not parsed.PDF then
    LrDialogs.message('Argus — Erreur', output:sub(1, 500), 'warning')
    return
  end

  -- Basculer en Develop et appliquer les réglages
  local settingsApplied = 0
  if parsed.PARAMS then
    local fn        = loadstring('return ' .. parsed.PARAMS)
    local xmpParams = fn and fn() or {}

    if next(xmpParams) then
      LrApplicationView.switchToModule('develop')
      LrTasks.sleep(2.0)

      local ext = LrPathUtils.extension(photoPath):lower()
      local isJPEG = (ext == 'jpg' or ext == 'jpeg')

      for xmpKey, xmpVal in pairs(xmpParams) do
        local lrKey = PARAM_MAP[xmpKey]
        if lrKey then
          -- Sur JPEG, Temperature est une échelle -100/+100, pas des Kelvins — on ignore
          if isJPEG and lrKey == 'Temperature' then
            -- skip
          else
            LrDevelopController.setValue(lrKey, tonumber(xmpVal) or xmpVal)
            settingsApplied = settingsApplied + 1
          end
        end
      end
    end
  end

  LrDialogs.message(
    'Argus — Termine',
    string.format('%s\nScore : %s\n\n%d reglages appliques.\n\nPDF : %s',
      parsed.ESPECE or '',
      parsed.SCORE  or '?',
      settingsApplied,
      parsed.PDF    or '?'),
    'info'
  )
end)
