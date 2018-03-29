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
        console.log(worker.attributes);

        $("#user-details-2").html("Status: " + worker.activityName);
    });

    WORKER.on("activity.update", function (worker) {
        console.log(worker.sid);
        console.log(worker.friendlyName);
        console.log(worker.activityName);
        console.log(worker.available);

        $("#user-details-2").html("Status: " + worker.activityName);
    });

    WORKER.on("reservation.created", function (reservation) {
        console.log(reservation.sid);
        console.log(reservation.task.sid);
        console.log(reservation.task.priority);
        console.log(reservation.task.age);
        console.log(reservation.task.attributes);

        reservation.accept();

        WORKER.activities.fetch(
            function (error, activities) {
                for (var i = 0; i < activities.data.length; i++) {
                    if (activities.data[i].friendlyName === "Busy") {
                        WORKER.update("ActivitySid", activities.data[i].sid);

                        break;
                    }
                }
            }
        );
    });

    // Refresh token every 55 minutes
    setTimeout(refresh_token, 1000 * 60 * 55);
};

get_user(function (data) {
    var user = data;

    $("#user-details-3").html("Username: " + user.username);
    $("#user-details-5").html("Languages: " + user.languages);
    $("#user-details-6").html("Skills: " + user.skills);

    get_twilio_worker_token(function (data) {
        init_worker(data.token);
    });
});
