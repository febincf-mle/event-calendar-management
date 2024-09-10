var summaryElements = document.querySelectorAll('.event-list-container');

changeSummary(-1);

function changeSummary(number) {

    let summaryIndex = (number + 1) % 4;
    
    for (element of summaryElements) {
        element.style.display = 'none';
    }
    summaryElements[summaryIndex].style.display = 'block';

    return;
};