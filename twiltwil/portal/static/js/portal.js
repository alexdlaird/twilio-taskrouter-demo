/**
 * Copyright (c) 2018 Alex Laird.
 *
 * @author Alex Laird
 * @version 0.1.0
 */

$(function () {
    var USER;
    var CHAT_CLIENT;
    var WORKSPACE;
    var WORKER;

    var currentChannel;
    var currentContact;
    var taskInterval;
    var taskSecondCounter;

    var $chatWindow = $("#chat-window");
    var $lobbyWindow = $("#lobby-window");
    var $lobbyVideo = $("#lobby-video");
    var $messages = $("#messages");
    var $replyBox = $("#reply-box");
    var $userDetailsStatistics = $("#user-details-statistics");
    var $userDetailsTaskTime = $("#user-details-task-time");

    function lobbyVideoCommand(command) {
        $lobbyVideo[0].contentWindow.postMessage('{"event":"command","func":"' + command + '","args":""}', '*');
    }

    function refreshWorkspaceToken() {
        if (WORKSPACE) {
            console.log("Getting refresh token for Workspace.");

            twiltwilapi.getTwilioWorkspaceToken().done(function (data) {
                WORKSPACE.updateToken(data.token);
            });
        }
    }

    function refreshWorkerToken() {
        if (WORKER) {
            console.log("Getting refresh token for Worker.");

            twiltwilapi.getTwilioWorkerToken().done(function (data) {
                WORKER.updateToken(data.token);
            });
        }
    }

    function pad(val) {
        var valString = val + "";
        if (valString.length < 2) {
            return "0" + valString;
        } else {
            return valString;
        }
    }

    function incrementTaskTimer() {
        ++taskSecondCounter;

        $userDetailsTaskTime.html("Current task time: " + pad(parseInt(taskSecondCounter / 60) + ":" + pad(taskSecondCounter % 60)));
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
        var $user;
        if (message.author === USER.username) {
            $user = $('<h5 class="media-heading me"></h5>').text(USER.username + " (me)");
        } else if (message.author !== currentContact.sid) {
            $user = $('<h5 class="media-heading me"></h5>').text(message.author + " (previous agent)");
        } else {
            $user = $('<h5 class="media-heading"></h5>').text(currentContact.card);
        }
        var $body = $('<small class="col-lg-10"></small>').text(message.body);
        var $container = $('<div class="media msg">');
        $container.append($time).append($user).append($body);
        $messages.append($container);
        $messages.scrollTop($messages[0].scrollHeight);
    }

    function initChannel(channel) {
        currentChannel = channel;

        twiltwilapi.getContact(currentChannel.uniqueName).done(function (contact) {
            currentContact = contact;

            lobbyVideoCommand('pauseVideo');
            $lobbyWindow.hide();
            $chatWindow.show();

            console.log('Joined channel ' + currentChannel.uniqueName);

            currentChannel.getMessages().then(function (messages) {
                $.each(messages.items, function (index, message) {
                    displayMessage(message);
                });
            });
        });
    }

    function joinChannel(uniqueName) {
        CHAT_CLIENT.getChannelByUniqueName(uniqueName).then(function (channel) {
            console.log('Found ' + channel.uniqueName + ' channel');
            console.log(channel);

            channel.join().then(initChannel);
        });
    }

    function initChatClient(token) {
        return new Promise(function (resolve) {
            Twilio.Chat.Client.create(token).then(function (client) {
                CHAT_CLIENT = client;

                CHAT_CLIENT.on('messageAdded', function (message) {
                    displayMessage(message);
                }).on('channelLeft', function (channel) {
                    console.log('Left channel ' + currentChannel.uniqueName);
                });

                CHAT_CLIENT.getSubscribedChannels().then(function (channels) {
                    $.each(channels.items, function (index, channel) {
                        initChannel(channel);
                    });

                    resolve();
                });
            });
        });
    }

    function updateStatistics() {
        WORKSPACE.realtimeStats.fetch({}, function (error, statistics) {
            if (error) {
                console.log(error.code);
                console.log(error.message);
                return;
            }

            var $longestWaitTime = $('<li><small>Longest wait time: ' + (statistics.longestTaskWaitingAge ? statistics.longestTaskWaitingAge !== 0 : 'N/A') + '</small></li>');
            var $onlineAgents = $('<li><small>Online agents: ' + statistics.totalWorkers + '</small></li>');
            var $pendingTasks = $('<li><small>Pending tasks: ' + statistics.tasksByStatus.pending + '</small></li>');
            var $assignedTasks = $('<li><small>Assigned tasks: ' + statistics.tasksByStatus.assigned + '</small></li>');

            $userDetailsStatistics.html("").append($longestWaitTime).append($onlineAgents).append($pendingTasks).append($assignedTasks);
        });
    }

    function initWorkspace(token) {
        WORKSPACE = new Twilio.TaskRouter.Workspace(token);

        WORKSPACE.on("ready", function (workspace) {
            console.log(workspace.sid);
            console.log(workspace.friendlyName);
            console.log(workspace.prioritizeQueueOrder);
            console.log(workspace.defaultActivityName);

            updateStatistics();

            // Refresh statistics every 30 seconds
            setInterval(updateStatistics, 1000 * 30);
        });

        // Refresh token every 4 minutes
        setInterval(refreshWorkspaceToken, 1000 * 60 * 4);
    }

    function initWorker(token) {
        WORKER = new Twilio.TaskRouter.Worker(token);

        WORKER.on("ready", function (worker) {
            console.log(worker.sid);
            console.log(worker.friendlyName);
            console.log(worker.activityName);
            console.log(worker.available);
            console.log(worker.attributes);

            $("#user-details-status").html(worker.activityName);
        });

        WORKER.on("activity.update", function (worker) {
            console.log(worker.sid);
            console.log(worker.friendlyName);
            console.log(worker.activityName);
            console.log(worker.available);

            $("#user-details-status").html(worker.activityName);
        });

        WORKER.on("reservation.created", function (reservation) {
            console.log(reservation.sid);
            console.log(reservation.task.sid);
            console.log(reservation.task.priority);
            console.log(reservation.task.age);
            console.log(reservation.task.attributes);

            updateWorkerActivity("Busy");

            reservation.accept();

            var chatContact = reservation.task.attributes.from;

            taskSecondCounter = 0;
            taskInterval = setInterval(incrementTaskTimer, 1000);

            CHAT_CLIENT.getSubscribedChannels().then(function () {
                joinChannel(chatContact);
            });
        });

        // Refresh token every 2 minutes
        setInterval(refreshWorkerToken, 1000 * 60 * 2);
    }

    twiltwilapi.getUser().done(function (data) {
        USER = data;

        $("#user-details-welcome").html("Welcome, " + USER.username);
        var $userDetailsLanuages = $("#user-details-languages").html("");
        $.each(USER.languages, function (index, language) {
            $userDetailsLanuages.append('<li><small>' + language + '</small></li>');
        });

        var $userDetailsSkills = $("#user-details-skills").html("");
        $.each(USER.skills, function (index, skill) {
            $userDetailsSkills.append('<li><small>' + skill + '</small></li>');
        });

        twiltwilapi.getTwilioChatToken(USER.username).done(function (data) {
            initChatClient(data.token).then(function () {
                twiltwilapi.getTwilioWorkspaceToken().done(function (data) {
                    initWorkspace(data.token);
                });

                twiltwilapi.getTwilioWorkerToken().done(function (data) {
                    initWorker(data.token);
                });
            });
        });
    });

    $("#send-button").on("click", function () {
        var message = $replyBox.val();

        if ($.trim(message) !== "") {
            currentChannel.sendMessage($replyBox.val(), {
                "To": currentChannel.uniqueName
            });
            $replyBox.val("").focus();
        }
    });

    function markTaskComplete(task) {
        WORKER.completeTask(task.sid, function () {
            $chatWindow.hide();
            $lobbyWindow.show();
            lobbyVideoCommand('playVideo');
            currentChannel.leave().then(function () {
                currentChannel = null;
                currentContact = null;

                updateWorkerActivity("Idle");

                $userDetailsTaskTime.html("");
                clearInterval(taskInterval);
                $messages.html("");
            });
        });
    }

    $("#solve-button").on("click", function () {
        WORKER.fetchReservations(
            function (error, reservations) {
                for (var i = 0; i < reservations.data.length; i++) {
                    if (reservations.data[i].task.assignmentStatus === "assigned") {
                        markTaskComplete(reservations.data[i].task);

                        break;
                    }
                }
            }
        );
    });
});
