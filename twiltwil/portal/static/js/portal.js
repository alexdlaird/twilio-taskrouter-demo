/**
 * Copyright (c) 2018 Alex Laird.
 *
 * @author Alex Laird
 * @version 0.1.0
 */

var WORKER = null;

refresh_token = function () {
    if (WORKER) {
        console.log("Getting refresh token for worker.");

        get_twilio_worker_token(function (data) {
            WORKER.updateToken(data.token);
        });
    }
};

init_worker = function (token) {
    WORKER = new Twilio.TaskRouter.Worker(token);

    WORKER.on("ready", function (worker) {
        console.log(worker.sid);
        console.log(worker.friendlyName);
        console.log(worker.activityName);
        console.log(worker.available);
    });

    // Refresh token every 55 minutes
    setTimeout(refresh_token, 1000 * 60 * 55);
};

get_user(function (data) {
    var user = data;

    get_twilio_worker_token(function (data) {
        init_worker(data.token);
    });
});
