/**
 * Copyright (c) 2018 Alex Laird.
 *
 * @author Alex Laird
 * @version 0.2.0
 */

$(function () {
    var INFO;
    var USER;
    var CONVERSATION_CLIENT;
    var VOICE_CLIENT;
    var WORKSPACE_CLIENT;
    var WORKER_CLIENT;

    var currentConversation;
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
        if (CONVERSATION_CLIENT) {
            console.log("Getting refresh token for Chat.");

            twiltwilapi.getTwilioChatToken(USER.username).done(function (data) {
                CONVERSATION_CLIENT.updateToken(data.token);
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
        console.log("displayMessage", message);

        var $time = $('<small class="pull-right time"><i class="fa fa-clock-o"></i></small>')
            .text(message.dateCreated.toLocaleString());
        var $user;
        if (message.author === USER.username) {
            $user = $('<h5 class="media-heading me"></h5>').text(USER.username + " (me)");
        } else if (message.author === "system") {
            $user = $('<h5 class="media-heading me"></h5>').text("system");
        } else if (message.author !== currentContact.uuid &&
            message.author !== currentContact.phone_number) {
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

    function initConversation(conversation) {
        currentConversation = conversation;

        twiltwilapi.getContact(currentConversation.uniqueName).done(function (contact) {
            currentContact = contact;

            lobbyVideoCommand('pauseVideo');
            $lobbyWindow.hide();
            $chatWindow.show();

            console.log('Joined Conversation ' + currentConversation.uniqueName);

            currentConversation.getMessages().then(function (messages) {
                $.each(messages.items, function (index, message) {
                    displayMessage(message);
                });
            });
        });
    }

    function joinConversation(uniqueName) {
        CONVERSATION_CLIENT.getConversationByUniqueName(uniqueName).then(function (conversation) {
            console.log("conversation", conversation);

            initConversation(conversation);
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
            options = {};
            if (INFO.region === 'dev' || INFO.region === 'stage') {
                options.realm = INFO.region.concat('-us1');
            }

            CONVERSATION_CLIENT = new Twilio.Conversations.Client(token, options)

            CONVERSATION_CLIENT.on("messageAdded", function (message) {
                displayMessage(message);
            });

            CONVERSATION_CLIENT.getSubscribedConversations().then(function (conversations) {
                $.each(conversations.items, function (index, conversation) {
                    console.log("conversation", conversation);

                    initConversation(conversation);
                });

                getCurrentTask().then(function (task) {
                    if (task) {
                        initTaskTimer(task);
                    }

                    resolve();
                });
            });
        });
    }

    function initVoiceDevice(token) {
        VOICE_CLIENT = new Twilio.Device(region = INFO.region);
        VOICE_CLIENT.setup(token);

        VOICE_CLIENT.on("incoming", function (connection) {
            console.log('Incoming connection from ' + connection.parameters.From);

            currentConnection = connection;
        });
    }

    function updateWorkspaceStatistics() {
        WORKSPACE_CLIENT.statistics.fetch({"Minutes": statisticsTimeRange}, function (error, statistics) {
            if (error) {
                console.log("error", error);
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

            console.log("updateWorkspaceStatistics", statistics);
        });
    }

    function updateWorkerStatistics() {
        WORKER_CLIENT.statistics.fetch({"Minutes": statisticsTimeRange}, function (error, statistics) {
            if (error) {
                console.log("error", error);
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

            console.log("updateWorkerStatistics", statistics);
        });
    }

    function initWorkspace(token) {
        WORKSPACE_CLIENT = new Twilio.TaskRouter.Workspace(token, null, null, INFO.max_http_retries, INFO.api_base_url, INFO.event_bridge_base_url);

        WORKSPACE_CLIENT.on("token.expired", function () {
            console.log("Getting refresh token for Workspace.");

            twiltwilapi.getTwilioWorkspaceToken().done(function (data) {
                WORKSPACE_CLIENT.updateToken(data.token);
            });
        });

        WORKSPACE_CLIENT.on("ready", function (workspace) {
            console.log("workspace.ready", workspace);
        });

        // Refresh token every 2 minutes
        setInterval(refreshTokens, 1000 * 60 * 2);
    }

    function initWorker(token) {
        WORKER_CLIENT = new Twilio.TaskRouter.Worker(token, null, null, null, null, null, INFO.max_http_retries, INFO.api_base_url, INFO.event_bridge_base_url);

        WORKER_CLIENT.on("token.expired", function () {
            console.log("Getting refresh token for Worker.");

            twiltwilapi.getTwilioWorkerToken().done(function (data) {
                WORKER_CLIENT.updateToken(data.token);
            });
        });

        WORKER_CLIENT.on("ready", function (worker) {
            console.log("worker.ready", worker);

            $userDetailsStatus.html(worker.activityName);
        });

        WORKER_CLIENT.on("activity.update", function (worker) {
            console.log("worker.activity.update", worker);

            $userDetailsStatus.html(worker.activityName);
        });

        WORKER_CLIENT.on("reservation.created", function (reservation) {
            console.log("reservation.created", reservation);

            if (reservation.task.taskChannelUniqueName === "voice") {
                $("#mark-solved-text").text("Mark Solved (Hang Up)");
                $("#solve-button").addClass("disabled");
                $("#voice-call-notice").show();
                $("#voice-call-answer").show();

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
                        console.log("error", error);
                        return;
                    }

                    console.log("Conference initiated");
                }, options);
            } else {
                $("#mark-solved-text").text("Mark Solved");
                $("#solve-button").removeClass("disabled");
                $("#voice-call-notice").hide();
                $("#voice-call-answer").hide();

                reservation.accept();
            }

            var conversation = reservation.task.attributes.conversation;

            initTaskTimer(reservation.task);

            WORKER_CLIENT.on("reservation.accepted", function (reservation) {
                joinConversation(conversation);
            });
        });

        WORKER_CLIENT.on("reservation.accepted", function (reservation) {
            updateWorkerActivity("Busy");
        });

        WORKER_CLIENT.on("reservation.wrapup", function (reservation) {
            console.log("reservation.wrapup", reservation);

            markTaskComplete(reservation.task);
        });

        WORKER_CLIENT.on("task.canceled", wrapupQuestion);
    }

    twiltwilapi.getInfo().done(function (data) {
        INFO = data;

        if (INFO.disable_lobby_video) {
            $lobbyVideo.remove();
            $lobbyVideo = $("#lobby-video");
        }
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
        currentConversation.leave().then(function () {
            console.log('Left Conversation ' + currentConversation.uniqueName);

            currentConversation = null;
            currentContact = null;

            updateWorkerActivity("Idle");

            $userDetailsCurrentTaskTime.html("");
            clearInterval(taskInterval);
            $messages.html("");

            if (currentConnection) {
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

    $("#voice-call-answer").on("click", function () {
        if (currentConnection) {
            currentConnection.accept();

            $(this).hide();

            $("#solve-button").removeClass("disabled");
        }
    });

    $("#send-button").on("click", function () {
        var message = $replyBox.val();

        if ($.trim(message) !== "") {
            currentConversation.sendMessage($replyBox.val(), {
                "To": currentConversation.uniqueName
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
