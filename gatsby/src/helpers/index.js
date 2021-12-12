// related to date

export function getWeekdays(lang = navigator.language) {
    const daysInMS = 24 * 60 * 60 * 1000
    const firstSunday = 4 * daysInMS

    return [...Array(7).keys()]
        .map(daysQtd => (new Date(firstSunday + daysQtd * daysInMS))
            .toLocaleDateString(lang, { weekday: 'long' }))
}

// related to text

export function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1)
}


// others

// do not include the until value
export function range(from, until, increment = 1) {
    const length = Math.ceil((until - from) / increment)
    return Array.from({ length }, (_, idx) => from + (idx * increment))
} 