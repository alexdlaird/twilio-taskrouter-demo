/**
 * Copyright (c) 2018 Alex Laird.
 *
 * @author Alex Laird
 * @version 0.1.0
 */

var SITE_HOST = location.host;
var SITE_URL = location.protocol + "//" + SITE_HOST;

var CSRF_TOKEN = Cookies.get("csrftoken");

function csrfSafeMethod(method) {
    "use strict";

    // These HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup(
    {
        beforeSend: function (xhr, settings) {
            "use strict";

            if (!csrfSafeMethod(settings.type)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
            }
        },
        contentType: "application/json; charset=UTF-8"
    });

ajax_success = function (callback, data) {
    console.log(data);

    callback(data)
};

ajax_error = function (callback, xhr, textStatus, errorThrown) {
    if (xhr.hasOwnProperty('responseJSON')) {
        console.log(xhr.responseJSON);
    }

    callback([{
        'xhr': xhr,
        'textStatus': textStatus,
        'errorThrown': errorThrown
    }]);
};

ajax_request = function (callback, type, url, data) {
    data = typeof data === "undefined" ? null : data;

    return $.ajax(
        {
            type: type,
            url: SITE_URL + url,
            dataType: "json",
            data: JSON.stringify(data),
            success: function (data) {
                ajax_success(callback, data);
            },
            error: function (xhr, textStatus, errorThrown) {
                ajax_error(callback, xhr, textStatus, errorThrown);
            }
        });
};

get_user = function (callback) {
    return ajax_request(callback, "GET", "/api/user");
};

get_twilio_worker_token = function (callback) {
    return ajax_request(callback, "POST", "/api/workers/token");
};

get_twilio_chat_token = function (callback, username) {
    return ajax_request(callback, "POST", "/api/chat/token", {"username": username});
};
