/**
 * Copyright (c) 2018 Alex Laird.
 *
 * @author Alex Laird
 * @version 0.2.0
 */

$(function () {
    var INFO;
    var USER;
    var CHAT_CLIENT;
    var VOICE_CLIENT;
    var WORKSPACE_CLIENT;
    var WORKER_CLIENT;

    var currentChannel;
    var currentContact;
    var currentConnection;
    var taskInterval;
    var taskSecondCounter;
    var statisticsTimeRange = "10080";

    var $chatWindow = $("#chat-window");
    var $lobbyWindow = $("#lobby-window");
    var $lobbyVideo = $("#lobby-video");
    var $messages = $("#messages");
    var $replyBox = $("#reply-box");
    var $userDetailsStatus = $("#user-details-status");
    var $userDetailsStatistics = $("#user-details-statistics");
    var $userDetailsStatisticsTimeRange = $("#statistics-time-range");
    var $userDetailsAverageTaskTime = $("#user-details-average-task-time");
    var $userDetailsCurrentTaskTime = $("#user-details-current-task-time");

    function lobbyVideoCommand(command) {
        if ($lobbyVideo.length > 0) {
            $lobbyVideo[0].contentWindow.postMessage('{"event":"command","func":"' + command + '","args":""}', '*');
        }
    }

    function refreshTokens() {
        // TODO: after a while a stats token starts getting 400s from event-bridge, should be investigated
        if (WORKSPACE_CLIENT) {
            console.log("Getting refresh token for Workspace.");

            twiltwilapi.getTwilioWorkspaceToken().done(function (data) {
                WORKSPACE_CLIENT.updateToken(data.token);
            });
        }

        if (WORKER_CLIENT) {
            console.log("Getting refresh token for Worker.");

            twiltwilapi.getTwilioWorkerToken().done(function (data) {
                WORKER_CLIENT.updateToken(data.token);
            });
        }

        if (CHAT_CLIENT) {
            console.log("Getting refresh token for Chat.");

            twiltwilapi.getTwilioChatToken(USER.username).done(function (data) {
                CHAT_CLIENT.updateToken(data.token);
            });
        }

        if (VOICE_CLIENT) {
            console.log("Getting refresh token for Voice.");

            twiltwilapi.getTwilioVoiceToken(USER.username).done(function (data) {
                VOICE_CLIENT.updateToken(data.token);
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

        $userDetailsCurrentTaskTime.html("Time since question asked: " + pad(parseInt(taskSecondCounter / 60) + ":"
                                         + pad(taskSecondCounter % 60)));
    }

    function updateWorkerActivity(activityName) {
        WORKER_CLIENT.activities.fetch(
            function (error, activities) {
                for (var i = 0; i < activities.data.length; i++) {
                    if (activities.data[i].friendlyName === activityName) {
                        WORKER_CLIENT.update("ActivitySid", activities.data[i].sid);

                        break;
                    }
                }
            }
        );
    }

    function displayMessage(message) {
        console.log(message);

        var $time = $('<small class="pull-right time"><i class="fa fa-clock-o"></i></small>')
            .text(message.timestamp.toLocaleString());
        var $user;
        if (message.author === USER.username) {
            $user = $('<h5 class="media-heading me"></h5>').text(USER.username + " (me)");
        } else if (message.author !== currentContact.uuid) {
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

    function initTaskTimer(task) {
        if (taskInterval) {
            clearInterval(taskInterval);
        }

        taskSecondCounter = parseInt(new Date().getTime() / 1000 - task.dateCreated.getTime() / 1000);
        taskInterval = setInterval(incrementTaskTimer, 1000);
    }

    function initChatClient(token) {
        return new Promise(function (resolve) {
            Twilio.Chat.Client.create(token).then(function (client) {
                CHAT_CLIENT = client;

                CHAT_CLIENT.on('messageAdded', function (message) {
                    displayMessage(message);
                });

                CHAT_CLIENT.getSubscribedChannels().then(function (channels) {
                    $.each(channels.items, function (index, channel) {
                        initChannel(channel);
                    });

                    getCurrentTask().then(function (task) {
                        if (task) {
                            initTaskTimer(task);
                        }

                        resolve();
                    });
                });
            });
        });
    }

    function initVoiceDevice(token) {
        VOICE_CLIENT = new Twilio.Device();
        VOICE_CLIENT.setup(token);

        VOICE_CLIENT.on("incoming", function (connection) {
            console.log('Incoming connection from ' + connection.parameters.From);

            connection.accept();
            currentConnection = connection;
        });
    }

    function updateWorkspaceStatistics() {
        WORKSPACE_CLIENT.statistics.fetch({"Minutes": statisticsTimeRange}, function (error, statistics) {
            if (error) {
                console.log(error.code);
                console.log(error.message);
                return;
            }

            var $onlineAgents = $('<li>Online agents: ' + statistics.realtime.totalWorkers + '</li>');
            var $pendingTasks = $('<li>Queued questions: ' + statistics.realtime.tasksByStatus.pending
                                  + '</li>');
            var $assignedTasks = $('<li>Assigned questions: ' + statistics.realtime.tasksByStatus.assigned
                                   + '</li>');
            var $completedTasks = $('<li>Answered this week: ' + statistics.cumulative.tasksCompleted
                                    + '</li>');
            var $longestWaitTime = $('<li>Longest wait time: '
                                     + (pad(parseInt(statistics.cumulative.waitDurationUntilAccepted.max / 60) + ":"
                                     + pad(statistics.cumulative.waitDurationUntilAccepted.max % 60)))
                                     + '</li>');
            var $averageWaitTime = $('<li>Average wait time: '
                                     + (pad(parseInt(statistics.cumulative.waitDurationUntilAccepted.avg / 60) + ":"
                                     + pad(statistics.cumulative.waitDurationUntilAccepted.avg % 60)))
                                     + '</li>');

            $userDetailsStatistics.html("").append($onlineAgents).append($pendingTasks).append($assignedTasks)
                .append($completedTasks).append($longestWaitTime).append($averageWaitTime);

            console.log(statistics);
        });
    }

    function updateWorkerStatistics() {
        WORKER_CLIENT.statistics.fetch({"Minutes": statisticsTimeRange}, function (error, statistics) {
            if (error) {
                console.log(error.code);
                console.log(error.message);
                return;
            }

            var busyActivity;
            $.each(statistics.cumulative.activityDurations, function (index, activityDuration) {
                if (activityDuration.friendlyName === "Busy") {
                    busyActivity = activityDuration;

                    return false;
                }
            });

            if (busyActivity && busyActivity.avg !== 0) {
                $userDetailsAverageTaskTime.html("Average solving time: " + pad(parseInt(
                    busyActivity.avg / 60) + ":" + pad(
                    busyActivity.avg % 60)));
            }

            console.log(statistics);
        });
    }

    function initWorkspace(token) {
        WORKSPACE_CLIENT = new Twilio.TaskRouter.Workspace(token);

        WORKSPACE_CLIENT.on("ready", function (workspace) {
            console.log(workspace.sid);
            console.log(workspace.friendlyName);
            console.log(workspace.prioritizeQueueOrder);
            console.log(workspace.defaultActivityName);
        });

        // Refresh token every 2 minutes
        setInterval(refreshTokens, 1000 * 60 * 2);
    }

    function initWorker(token) {
        WORKER_CLIENT = new Twilio.TaskRouter.Worker(token);

        WORKER_CLIENT.on("ready", function (worker) {
            console.log(worker.sid);
            console.log(worker.friendlyName);
            console.log(worker.activityName);
            console.log(worker.available);
            console.log(worker.attributes);

            $userDetailsStatus.html(worker.activityName);
        });

        WORKER_CLIENT.on("activity.update", function (worker) {
            console.log(worker.sid);
            console.log(worker.friendlyName);
            console.log(worker.activityName);
            console.log(worker.available);

            $userDetailsStatus.html(worker.activityName);
        });

        WORKER_CLIENT.on("reservation.created", function (reservation) {
            console.log(reservation.sid);
            console.log(reservation.task.sid);
            console.log(reservation.task.priority);
            console.log(reservation.task.age);
            console.log(reservation.task.attributes);

            if (reservation.task.taskChannelUniqueName === "voice") {
                $("#mark-solved-text").text("Mark Solved (Hang Up)");
                $("#voice-call-notice").show();

                var options = {
                    "ConferenceStatusCallback": INFO.conference_status_callback_url,
                    "ConferenceStatusCallbackEvent": "start,end,join,leave",
                    "ConferenceRecord": "true",
                    "EndConferenceOnExit": "true",
                    "EndConferenceOnCustomerExit": "true",
                    "BeepOnCustomerEntrance": "false"
                };
                reservation.conference(null, null, null, null, function (error, reservation) {
                    if (error) {
                        console.log(error.code);
                        console.log(error.message);
                        return;
                    }

                    console.log("Conference initiated");
                }, options);
            } else {
                $("#mark-solved-text").text("Mark Solved");
                $("#voice-call-notice").hide();

                reservation.accept();
            }

            var chatContact = reservation.task.attributes.channel;

            initTaskTimer(reservation.task);

            CHAT_CLIENT.getSubscribedChannels().then(function () {
                joinChannel(chatContact);
            });
        });

        WORKER_CLIENT.on("reservation.accepted", function (reservation) {
            updateWorkerActivity("Busy");
        });

        WORKER_CLIENT.on("reservation.wrapup", function (reservation) {
            console.log(reservation.sid);
            console.log(reservation.task.sid);
            console.log(reservation.task.priority);
            console.log(reservation.task.age);
            console.log(reservation.task.attributes);

            markTaskComplete(reservation.task);
        });

        WORKER_CLIENT.on("task.canceled", wrapupQuestion);
    }

    twiltwilapi.getInfo().done(function (data) {
        INFO = data;
    });

    twiltwilapi.getUser().done(function (data) {
        USER = data;

        $("#user-details-welcome").html("Welcome, " + USER.username);
        var $userDetailsLanuages = $("#user-details-languages").html("");
        $.each(USER.languages, function (index, language) {
            $userDetailsLanuages.append('<li>' + language + '</li>');
        });

        var $userDetailsSkills = $("#user-details-skills").html("");
        $.each(USER.skills, function (index, skill) {
            $userDetailsSkills.append('<li>' + skill + '</li>');
        });

        twiltwilapi.getTwilioChatToken(USER.username).done(function (chatData) {
            twiltwilapi.getTwilioWorkspaceToken().done(function (workspaceData) {
                twiltwilapi.getTwilioWorkerToken().done(function (workerData) {
                    initWorkspace(workspaceData.token);

                    initWorker(workerData.token);

                    // Refresh statistics every 30 seconds
                    setInterval(updateWorkspaceStatistics, 1000 * 30);
                    setInterval(updateWorkerStatistics, 1000 * 30);

                    $userDetailsStatisticsTimeRange.change();

                    initChatClient(chatData.token);

                    twiltwilapi.getTwilioVoiceToken(USER.username).done(function (voiceData) {
                        initVoiceDevice(voiceData.token);
                    });
                });
            });
        });
    });

    function wrapupQuestion() {
        $chatWindow.hide();
        $lobbyWindow.show();
        lobbyVideoCommand('playVideo');
        currentChannel.leave().then(function () {
            console.log('Left channel ' + currentChannel.uniqueName);

            currentChannel = null;
            currentContact = null;

            updateWorkerActivity("Idle");

            $userDetailsCurrentTaskTime.html("");
            clearInterval(taskInterval);
            $messages.html("");

            if (currentConnection) {
                // FIXME: when the Worker disconnects here, the customer leg stays live; the conference should be terminated
                currentConnection.disconnect();

                currentConnection = null;
            }
        });
    }

    function markTaskComplete(task) {
        WORKER_CLIENT.completeTask(task.sid, wrapupQuestion);
    }

    function getCurrentTask() {
        return new Promise(function (resolve) {
            var task = null;
            WORKER_CLIENT.fetchReservations(function (error, reservations) {
                for (var i = 0; i < reservations.data.length; i++) {
                    if (reservations.data[i].task.assignmentStatus === "assigned") {
                        task = reservations.data[i].task;

                        break;
                    }
                }

                resolve(task);
            });
        });
    }

    // Triggers

    $("#send-button").on("click", function () {
        var message = $replyBox.val();

        if ($.trim(message) !== "") {
            currentChannel.sendMessage($replyBox.val(), {
                "To": currentChannel.uniqueName
            });
            $replyBox.val("").focus();
        }
    });

    $("#solve-button").on("click", function () {
        getCurrentTask().then(markTaskComplete);
    });

    $("#logout-button").on("click", function (e) {
        e.preventDefault();

        if ($chatWindow.filter(":visible").length) {
            bootbox.confirm({
                                title: "Unsolved Question",
                                message: "<p>Hey, a question is currently assigned to you but hasn't been solved. If you have "
                                         +
                                         "already answered this question, click \"Mark Solved\" before logging out.</p><p>Logging out anyway "
                                         +
                                         "will caused the question to be reasigned to the next available agent.</p>",
                                buttons: {
                                    cancel: {
                                        label: '<i class="fa fa-times"></i> Cancel'
                                    },
                                    confirm: {
                                        label: '<i class="fa fa-check"></i> Logout'
                                    }
                                },
                                callback: function (result) {
                                    if (result) {
                                        window.location = $("#logout-button").attr("href");
                                    }
                                }
                            });
        } else {
            window.location = $("#logout-button").attr("href");
        }
    });

    $userDetailsStatisticsTimeRange.on("change", function () {
        statisticsTimeRange = $userDetailsStatisticsTimeRange.val();

        updateWorkspaceStatistics();
        updateWorkerStatistics();
    });
});
