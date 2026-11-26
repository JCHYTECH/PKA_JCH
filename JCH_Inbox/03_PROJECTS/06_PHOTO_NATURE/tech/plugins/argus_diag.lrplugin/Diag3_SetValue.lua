local LrApplication        = import 'LrApplication'
local LrApplicationView    = import 'LrApplicationView'
local LrDevelopController  = import 'LrDevelopController'
local LrDialogs            = import 'LrDialogs'
local LrTasks              = import 'LrTasks'

-- Test minimal : crée une copie virtuelle, bascule en Develop,
-- applique UN seul réglage (Exposure +1.0) et vérifie qu'il est visible.
LrTasks.startAsyncTask(function()
  local catalog = LrApplication.activeCatalog()
  local photos  = catalog:getTargetPhotos()
  local photo   = photos[1]
  local vCopy   = nil

  -- Étape 1 : copie virtuelle
  catalog:withWriteAccessDo('DIAG vCopy', function()
    local copies = catalog:createVirtualCopies({ photo })
    if copies and #copies > 0 then vCopy = copies[1] end
  end, { timeout = 10 })

  if not vCopy then
    LrDialogs.message('DIAG 3 — FAIL', 'Copie virtuelle non creee.', 'warning')
    return
  end

  -- Étape 2 : Develop + sélection
  LrApplicationView.switchToModule('develop')
  LrTasks.sleep(0.5)
  catalog:withWriteAccessDo('DIAG select', function()
    catalog:setSelectedPhotos({ vCopy })
  end, { timeout = 10 })
  LrTasks.sleep(2.0)

  -- Étape 3 : setValue Exposure = +1.0 (changement visible)
  local ok, err = xpcall(
    function() LrDevelopController.setValue('Exposure', 1.0) end,
    function(e) return e end
  )

  if ok then
    LrDialogs.message('DIAG 3 — setValue OK',
      'Exposure = +1.0 applique.\nVerifie visuellement que la copie virtuelle est surexposee.', 'info')
  else
    LrDialogs.message('DIAG 3 — setValue FAIL', tostring(err), 'warning')
  end
end)
