/**
 * Copyright (c) 2018 Alex Laird.
 *
 * @author Alex Laird
 * @version 0.1.0
 */

function TwilTwilApi() {
    this.SITE_HOST = location.host;
    this.SITE_URL = location.protocol + "//" + this.SITE_HOST;

    this.CSRF_TOKEN = Cookies.get("csrftoken");

    var self = this;

    function csrfSafeMethod(method) {
        // These HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup(
        {
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", self.CSRF_TOKEN);
                }
            },
            contentType: "application/json; charset=UTF-8"
        });

    function ajaxSuccess(callback, data) {
        console.log(data);

        callback(data)
    }

    function ajaxError(callback, xhr, textStatus, errorThrown) {
        if (xhr.hasOwnProperty('responseJSON')) {
            console.log(xhr.responseJSON);
        }

        callback([{
            'xhr': xhr,
            'textStatus': textStatus,
            'errorThrown': errorThrown
        }]);
    }

    this.ajaxRequest = function (callback, type, url, data) {
        data = typeof data === "undefined" ? null : data;

        return $.ajax(
            {
                type: type,
                url: self.SITE_URL + url,
                dataType: "json",
                data: JSON.stringify(data),
                success: function (data) {
                    ajaxSuccess(callback, data);
                },
                error: function (xhr, textStatus, errorThrown) {
                    ajaxError(callback, xhr, textStatus, errorThrown);
                }
            });
    };

    this.getUser = function (callback) {
        return self.ajaxRequest(callback, "GET", "/api/user");
    };

    this.getTwilioWorkerToken = function (callback) {
        return self.ajaxRequest(callback, "POST", "/api/workers/token");
    };

    this.getTwilioChatToken = function (callback, username) {
        return self.ajaxRequest(callback, "POST", "/api/chat/token", {"username": username});
    };
}

var twiltwilapi = new TwilTwilApi();
