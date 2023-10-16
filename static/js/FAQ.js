const accordion1ItemHeaders = document.querySelectorAll(
    ".accordion1-item-header"
    );

    accordion1ItemHeaders.forEach((accordion1ItemHeader) => {
    accordion1ItemHeader.addEventListener("click", (event) => {
        // Uncomment in case you only want to allow for the display of only one collapsed item at a time!

        const currentlyActiveaccordion1ItemHeader = document.querySelector(
        ".accordion1-item-header.active"
        );
        if (
        currentlyActiveaccordion1ItemHeader &&
        currentlyActiveaccordion1ItemHeader !== accordion1ItemHeader
        ) {
        currentlyActiveaccordion1ItemHeader.classList.toggle("active");
        currentlyActiveaccordion1ItemHeader.nextElementSibling.style.maxHeight = 0;
        }
        accordion1ItemHeader.classList.toggle("active");
        const accordion1ItemBody = accordion1ItemHeader.nextElementSibling;
        if (accordion1ItemHeader.classList.contains("active")) {
        accordion1ItemBody.style.maxHeight = accordion1ItemBody.scrollHeight + "px";
        } else {
        accordion1ItemBody.style.maxHeight = 0;
        }
    });
    });