function getSelectedCheckboxes(target, attrib) {
    var checkedValues = $('input:checkbox:checked').map(function() {
        return this.value;
    }).get();
    console.log(checkedValues);
    // Get existing URL data
    params = getURLParams(window.location.href) 
    if (checkedValues.length > 0) {
        var url = target + "?" + attrib + "="
        for (i = 0; i < checkedValues.length; i++) {
            url += checkedValues[i] + ",";
        }
        url = url.substring(0, url.length - 1)
        for (i = 0; i < params.length; i++) {
            url += "&" + params[i];
        }
    } else {
        if (params.length > 0) {
            url = target + "?";
            for (i = 0; i < params.length; i++) {
                url += params[i] + "&";
            }
            url = url.substring(0, url.length - 1)
        } else {
            url = target;
        }
    }
    window.location.href = url;
}

function getURLParams(qs) {
    qs = qs.split("?");
    if (qs.length > 1) {
        qs = qs[1].split("&");
        return qs;
    } else {
        return [];
    }
}
