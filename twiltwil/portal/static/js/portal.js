/**
 * Copyright (c) 2018 Alex Laird.
 *
 * @author Alex Laird
 * @version 0.1.0
 */

var CHAT_CLIENT = null;
var WORKER = null;

var chat_contact = null;

refresh_token = function () {
    if (WORKER) {
        console.log("Getting refresh token for worker.");

        get_twilio_worker_token(function (data) {
            WORKER.updateToken(data.token);
        });
    }
};

display_message = function (message) {
    console.log(message);
};

init_chat = function (token) {
    CHAT_CLIENT = new Twilio.Chat.Client(token);

    CHAT_CLIENT.getSubscribedChannels().then(join_channel);
};

init_channel = function (channel) {
    channel.join().then(function (channel) {
        console.log('Join channel ' + channel.sid);

        channel.getMessages().then(function (messages) {
            $.each(messages, function (message) {
                display_message(message);
            });
        });
    });

    channel.on('messageAdded', function (message) {
        console.log(message);
    });
};

join_channel = function (channel) {
    channel = typeof channel === "undefined" ? null : channel;

    if (channel) {
        chat_contact = channel.uniqueName;
    }

    var promise = CHAT_CLIENT.getChannelByUniqueName(chat_contact);
    promise.then(function (channel) {
        console.log('Found ' + channel.sid + ' channel');
        console.log(channel);

        init_channel(channel);
    });
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

        reservation.accept();

        chat_contact = reservation.task.attributes.from;

        CHAT_CLIENT.getSubscribedChannels().then(join_channel);
    });

    // Refresh token every 55 minutes
    setTimeout(refresh_token, 1000 * 60 * 55);
};

get_user(function (data) {
    var user = data;

    $("#user-details-3").html("Username: " + user.username);
    $("#user-details-5").html("Languages: " + user.languages);
    $("#user-details-6").html("Skills: " + user.skills);

    get_twilio_chat_token(function (data) {
        init_chat(data.token);

        get_twilio_worker_token(function (data) {
            init_worker(data.token);
        });
    }, user.username);
});
