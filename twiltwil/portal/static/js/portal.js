/**
 * Copyright (c) 2018 Alex Laird.
 *
 * @author Alex Laird
 * @version 0.1.0
 */

$(function () {
    var USER;
    var CHAT_CLIENT;
    var WORKER;
    var CHANNEL;

    var $chatWindow = $("#chat-window");
    var $lobbyWindow = $("#lobby-window");
    var $messages = $("#messages");
    var $replyBox = $("#reply-box");

    function refreshToken() {
        if (WORKER) {
            console.log("Getting refresh token for worker.");

            twiltwilapi.getTwilioWorkerToken(function (data) {
                WORKER.updateToken(data.token);
            });
        }
    }

    function updateWorkerActivity(activityName) {
        WORKER.activities.fetch(
            function (error, activities) {
                for (var i = 0; i < activities.data.length; i++) {
                    if (activities.data[i].friendlyName === activityName) {
                        WORKER.update("ActivitySid", activities.data[i].sid);

                        break;
                    }
                }
            }
        );
    }

    function displayMessage(message) {
        console.log(message);

        var $time = $('<small class="pull-right time"><i class="fa fa-clock-o"></i></small>').text(message.timestamp.toLocaleString());
        var $user = $('<h5 class="media-heading"></h5>').text(message.author);
        if (message.author === USER.username) {
            $user.addClass('me');
        }
        var $body = $('<small class="col-lg-10"></small>').text(message.body);
        var $container = $('<div class="media msg">');
        $container.append($time).append($user).append($body);
        $messages.append($container);
        $messages.scrollTop($messages[0].scrollHeight);
    }

    function initChannel(channel) {
        channel.join().then(function (channel) {
            CHANNEL = channel;

            $lobbyWindow.hide();
            $chatWindow.show();

            console.log('Joined channel ' + channel.uniqueName);

            channel.getMessages().then(function (messages) {
                $.each(messages.items, function (index, message) {
                    displayMessage(message);
                });
            });
        });

        channel.on('messageAdded', function (message) {
            // TODO: sometimes this double posts, it seems (fine on refresh), so perhaps just filter if already seen
            displayMessage(message);
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

            updateWorkerActivity("Busy");

            reservation.accept();

            var chatContact = reservation.task.attributes.from.substr(1);

            CHAT_CLIENT.getSubscribedChannels().then(function () {
                $messages.html("");

                joinChannel(chatContact);
            });
        });

        // Refresh token every 55 minutes
        setTimeout(refreshToken, 1000 * 60 * 55);
    }

    twiltwilapi.getUser(function (data) {
        USER = data;

        $("#user-details-3").html("Username: " + USER.username);
        $("#user-details-5").html("Languages: " + USER.languages);
        $("#user-details-6").html("Skills: " + USER.skills);

        twiltwilapi.getTwilioChatToken(function (data) {
            initChat(data.token);

            twiltwilapi.getTwilioWorkerToken(function (data) {
                initWorker(data.token);
            });
        }, USER.username);
    });

    $("#send-button").on("click", function () {
        var message = $replyBox.val();

        if ($.trim(message) !== "") {
            CHANNEL.sendMessage($replyBox.val(), {
                "To": "+" + CHANNEL.uniqueName
            });
            $replyBox.val("").focus();
        }
    });

    $("#solve-button").on("click", function () {
        WORKER.fetchReservations(
            function (error, reservations) {
                for (i = 0; i < reservations.data.length; i++) {
                    if (reservations.data[i].task.assignmentStatus === "assigned") {
                        WORKER.completeTask(reservations.data[i].task.sid, function () {
                            $chatWindow.hide();
                            $lobbyWindow.show();
                            CHANNEL.leave();
                            CHANNEL = null;

                            updateWorkerActivity("Idle");
                        });

                        break;
                    }
                }
            }
        );
    });
});