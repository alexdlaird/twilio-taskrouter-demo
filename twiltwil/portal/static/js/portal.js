/**
 * Copyright (c) 2018 Alex Laird.
 *
 * @author Alex Laird
 * @version 0.1.0
 */

$(function () {
    var CHAT_CLIENT;
    var WORKER;

    function refreshToken() {
        if (WORKER) {
            console.log("Getting refresh token for worker.");

            twiltwilapi.getTwilioWorkerToken(function (data) {
                WORKER.updateToken(data.token);
            });
        }
    }

    function displayMessage(message) {
        console.log(message);
    }

    function initChannel(channel) {
        channel.join().then(function (channel) {
            console.log('Join channel ' + channel.uniqueName);

            channel.getMessages().then(function (messages) {
                $.each(messages.items, function (index, message) {
                    displayMessage(message);
                });
            });
        });

        channel.on('messageAdded', function (message) {
            console.log(message);
        });
    }

    function joinChannel(uniqueName) {
        var promise = CHAT_CLIENT.getChannelByUniqueName(uniqueName);
        promise.then(function (channel) {
            console.log('Found ' + channel.uniqueName + ' channel');
            console.log(channel);

            initChannel(channel);
        });
    }

    function initChat(token) {
        CHAT_CLIENT = new Twilio.Chat.Client(token);

        CHAT_CLIENT.getSubscribedChannels().then(function (channels) {
            $.each(channels.items, function (index, channel) {
                joinChannel(channel.uniqueName);
            });
        });
    }

    function initWorker(token) {
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

            var chatContact = reservation.task.attributes.from.substr(1);

            CHAT_CLIENT.getSubscribedChannels().then(function () {
                joinChannel(chatContact);
            });
        });

        // Refresh token every 55 minutes
        setTimeout(refreshToken, 1000 * 60 * 55);
    }

    twiltwilapi.getUser(function (data) {
        var user = data;

        $("#user-details-3").html("Username: " + user.username);
        $("#user-details-5").html("Languages: " + user.languages);
        $("#user-details-6").html("Skills: " + user.skills);

        twiltwilapi.getTwilioChatToken(function (data) {
            initChat(data.token);

            twiltwilapi.getTwilioWorkerToken(function (data) {
                initWorker(data.token);
            });
        }, user.username);
    });
});