local LrApplication = import 'LrApplication'
local LrDialogs     = import 'LrDialogs'
local LrTasks       = import 'LrTasks'

LrTasks.startAsyncTask(function()
  local catalog = LrApplication.activeCatalog()
  local photos  = catalog:getTargetPhotos()  -- séquence LR native
  local photo   = photos[1]
  local results = {}

  -- A : séquence native de getTargetPhotos (1 photo sélectionnée)
  local vA = nil
  catalog:withWriteAccessDo('DIAG A', function()
    local c = catalog:createVirtualCopies(photos)
    if c and #c > 0 then vA = c[1] end
  end, { timeout = 5 })
  results[#results+1] = 'A getTargetPhotos()  : ' .. (vA and 'OK' or 'nil')

  -- B : appel sans argument (opère sur la sélection courante)
  local vB = nil
  catalog:withWriteAccessDo('DIAG B', function()
    local ok, c = pcall(catalog.createVirtualCopies, catalog)
    if ok and c and #c > 0 then vB = c[1] end
  end, { timeout = 5 })
  results[#results+1] = 'B sans arg (pcall)   : ' .. (vB and 'OK' or 'nil')

  -- C : nom singulier createVirtualCopy(photo)
  local vC = nil
  catalog:withWriteAccessDo('DIAG C', function()
    local ok, c = pcall(catalog.createVirtualCopy, catalog, photo)
    if ok and c then vC = c end
  end, { timeout = 5 })
  results[#results+1] = 'C createVirtualCopy  : ' .. (vC and 'OK' or 'nil')

  LrDialogs.message('DIAG 1', table.concat(results, '\n'), 'info')
end)
