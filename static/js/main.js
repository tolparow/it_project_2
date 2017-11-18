/**
 * Created by RuslanFarkhutdinov on 06.11.2017.
 */
var input = ".send-message", button = ".send", sel = $('#single-chat'); //often used selectors

function sendAJAX(input) {
    if ($(input).val().length > 0) {
        $.ajax({
            type: "POST",
            data: {message: $(input).val()}
        });
        $(input).val("");
        $(input).focus();
    }
}

function setMessageSizes() {
    $(".message.to").each(function () {
        $(this).css({left: $(this).parent().width() - $(this).width() - 30});
        console.log($(this).width());
    });
}

function getNewMessages() {
    setInterval(function () {
        var sel = $('#single-chat');
        $(sel).load(document.URL + ' #messages');
    }, 1000);
}


$(input).keydown(function (e) {

    if ((e.keyCode || e.which) === 13 && !e.shiftKey) {
        e.preventDefault();
        sendAJAX(input);
    }
});
$(button).click(function () {
    sendAJAX(input);
});


$(document).ready(function () {
    getNewMessages();
    $(sel).scrollTop($(sel).prop("scrollHeight"));
});