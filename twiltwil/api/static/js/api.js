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

    this.ajaxRequest = function (type, url, data) {
        data = typeof data === "undefined" ? null : data;

        return $.ajax(
            {
                type: type,
                url: self.SITE_URL + url,
                dataType: "json",
                data: JSON.stringify(data)
            });
    };

    this.getUser = function () {
        return self.ajaxRequest("GET", "/api/user");
    };

    this.getContact = function (sid) {
        return self.ajaxRequest("GET", "/api/contacts/" + sid);
    };

    this.getTwilioWorkspaceToken = function () {
        return self.ajaxRequest("POST", "/api/workspace/token");
    };

    this.getTwilioWorkerToken = function () {
        return self.ajaxRequest("POST", "/api/workers/token");
    };

    this.getTwilioChatToken = function (username) {
        return self.ajaxRequest("POST", "/api/chat/token", {"username": username});
    };
}

var twiltwilapi = new TwilTwilApi();
