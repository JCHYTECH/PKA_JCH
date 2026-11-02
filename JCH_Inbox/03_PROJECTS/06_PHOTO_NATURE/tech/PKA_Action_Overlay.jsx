/*
 * PKA Action Overlay - Chronophotography Automation
 * Developed by Forge 🦦 for JCH (PKA_JCH)
 * 
 * Instructions:
 * 1. Open your burst sequence as layers in Photoshop.
 * 2. Run this script (File > Scripts > Browse...).
 * 3. The script will align layers, add black masks, and set an opacity gradient.
 * 4. Use a white brush on the masks to reveal the movement.
 */

#target photoshop

function main() {
    if (app.documents.length === 0) {
        alert("Please open a document with multiple layers first.");
        return;
    }

    var doc = app.activeDocument;
    var layers = doc.layers;
    var layerCount = layers.length;

    if (layerCount < 2) {
        alert("You need at least 2 layers to create an overlay.");
        return;
    }

    // 1. Align Layers
    try {
        var idselectAllLayers = stringIDToTypeID("selectAllLayers");
        executeAction(idselectAllLayers, undefined, DialogModes.NO);
        
        var idalign = charIDToTypeID("algn");
        var desc = new ActionDescriptor();
        var idalignType = stringIDToTypeID("alignType");
        var idalignAuto = stringIDToTypeID("alignAuto");
        desc.putEnumerated(idalign, idalignType, idalignAuto);
        executeAction(idalign, desc, DialogModes.NO);
        
        doc.activeLayer = layers[0]; // Deselect
    } catch (e) {
        alert("Auto-alignment failed. You might need to align them manually if the background is too different.");
    }

    // 2. Process Layers
    // Photoshop layers index from top to bottom (0 is the top-most layer)
    // We assume the BOTTOM layer (index layerCount-1) is the "Master"
    
    for (var i = 0; i < layerCount; i++) {
        var currentLayer = layers[i];
        
        // Skip the very bottom layer (Master)
        if (i === layerCount - 1) {
            currentLayer.opacity = 100;
            continue;
        }

        // Set Opacity Gradient (Fade away from the master)
        // Master is 100%, layer above is 80%, etc.
        var reverseIndex = (layerCount - 1) - i;
        var opacityValue = (reverseIndex / (layerCount - 1)) * 100;
        currentLayer.opacity = Math.max(20, opacityValue);

        // Add Black Mask
        doc.activeLayer = currentLayer;
        addBlackMask();
    }

    alert("PKA Action Overlay complete!\n- Layers aligned\n- Opacity gradient applied\n- Black masks added\n\nUse a WHITE BRUSH on the masks to reveal the action.");
}

function addBlackMask() {
    try {
        var idmake = charIDToTypeID("mk  ");
        var desc = new ActionDescriptor();
        var idnew = charIDToTypeID("nw  ");
        var idchannel = charIDToTypeID("ch  ");
        desc.putClass(idnew, idchannel);
        var idat = charIDToTypeID("at  ");
        var ref = new ActionReference();
        var idchannel2 = charIDToTypeID("ch  ");
        var idmask = charIDToTypeID("msk ");
        ref.putEnumerated(idchannel2, idchannel2, idmask);
        desc.putReference(idat, ref);
        var idusing = charIDToTypeID("usng");
        var iduserMaskEnabled = stringIDToTypeID("userMaskEnabled");
        var idrevealNone = stringIDToTypeID("revealNone");
        desc.putEnumerated(idusing, iduserMaskEnabled, idrevealNone);
        executeAction(idmake, desc, DialogModes.NO);
    } catch (e) {}
}

main();
