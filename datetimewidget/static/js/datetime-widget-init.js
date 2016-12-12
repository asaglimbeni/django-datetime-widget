$(function () {
    $('[data-ddw]').each(function (index, el) {
        var ddwOptions = {};
        // We parse attributes in order to set appropriate options for component
        var attributes = $(el)[0].attributes;
        $.each(attributes, function (index, attr) {
            if (attr.name.startsWith("ddw-")) {
                var ddwKey = attr.name.replace("ddw-", "");
                ddwKey = ddwKey.replace(/-([a-z])/g, function (m, w) {
                    return w.toUpperCase();
                });
                // Cast string value into respective value
                var value = $.isNumeric(attr.value) ? parseInt(attr.value) : attr.value;
                value = (value == "True") ? true : value;
                value = (value == "False") ? false : value;

                ddwOptions[ddwKey] = value;
            }
        });
        $(el).datetimepicker(ddwOptions);
    });
});