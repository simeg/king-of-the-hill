"use strict";

const initInterval = ((selectorId, seconds, intervalTime) => {
    const timeElement = document.getElementById(selectorId);
    setTime(seconds, timeElement);
    setInterval(() => {
        seconds++;
        setTime(seconds, timeElement);
    }, intervalTime);
});

const setTime = ((seconds, element) => {
    const timeObj = convertSeconds(seconds);
    const output = `${timeObj.d ? timeObj.d + `${timeObj.d > 1 ? ' days ' : ' day '}` : ''}
                    ${timeObj.h ? timeObj.h + `${timeObj.h > 1 ? ' hours ' : ' hour '}` : ''}
                    ${timeObj.m ? timeObj.m + `${timeObj.m > 1 ? ' minutes ' : ' minute '}` : ''}
                    ${timeObj.s ? timeObj.s + `${timeObj.s > 1 ? ' seconds ' : ' second '}` : ''}`;
    element.innerHTML = output;
});

const convertSeconds = ((seconds) => {
    // Convert seconds into days,
    // hours, minutes and seconds
    let d, h, m, s;
    s = seconds;
    m = Math.floor(s / 60);
    s = s % 60;
    h = Math.floor(m / 60);
    m = m % 60;
    d = Math.floor(h / 24);
    h = h % 24;
    return { d, h, m, s };
});

const convertItems = ((selector)  => {
    const items = document.querySelectorAll(selector);
    for (let i = 0; i < items.length; i++) {
        const item = items[i];
        const time = item.innerHTML;
        const timeObj = convertSeconds(time);
        item.innerHTML = `${timeObj.d ? timeObj.d + 'd' : ''}
                          ${timeObj.h ? timeObj.h + 'h' : ''}
                          ${timeObj.m ? timeObj.m + 'm' : ''}
                          ${timeObj.s ? timeObj.s + 's' : ''}`;
    }
});
