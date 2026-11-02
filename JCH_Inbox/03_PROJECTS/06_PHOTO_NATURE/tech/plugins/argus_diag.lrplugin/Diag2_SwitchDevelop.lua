local LrApplication     = import 'LrApplication'
local LrApplicationView = import 'LrApplicationView'
local LrDialogs         = import 'LrDialogs'
local LrTasks           = import 'LrTasks'

LrTasks.startAsyncTask(function()
  local catalog = LrApplication.activeCatalog()
  local photos  = catalog:getTargetPhotos()
  local photo   = photos[1]
  local vCopy   = nil

  catalog:withWriteAccessDo('DIAG createVirtualCopies', function()
    local copies = catalog:createVirtualCopies({ photo })
    if copies and #copies > 0 then vCopy = copies[1] end
  end, { timeout = 10 })

  if not vCopy then
    LrDialogs.message('DIAG 2 — FAIL', 'Copie virtuelle non creee (DIAG 1 doit passer d\'abord).', 'warning')
    return
  end

  LrApplicationView.switchToModule('develop')
  LrTasks.sleep(0.5)

  catalog:withWriteAccessDo('DIAG setSelected', function()
    catalog:setSelectedPhotos({ vCopy })
  end, { timeout = 10 })

  LrTasks.sleep(2.0)

  -- Vérifier quelle photo est active dans Develop
  local activeSources = catalog:getActiveSources()
  local msg = 'switchToModule OK\nsetSelectedPhotos OK\n\nSources actives: ' .. tostring(#activeSources)

  LrDialogs.message('DIAG 2 — OK', msg, 'info')
end)
