function handleMessages() {
    const $popup = $("#messagePopup");

    // Показать попап, если есть сообщения
    if ($popup.children().length > 0) {
        $popup.fadeIn();

        // Скрыть попап после 5 секунд
        setTimeout(function () {
            $popup.fadeOut();
        }, 5000);
    }

    // Скрытие сообщения по клику
    $popup.on("click", ".alert", function () {
        $(this).fadeOut();
    });
}

$(document).ready(function () {
    handleMessages();
});