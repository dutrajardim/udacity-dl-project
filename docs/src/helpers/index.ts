// related to date

export function getWeekdays(lang: string = navigator.language): string[] {
    const daysInMS = 24 * 60 * 60 * 1000
    const firstSunday = 4 * daysInMS

    return [...Array(7).keys()]
        .map(daysQtd => (new Date(firstSunday + daysQtd * daysInMS))
            .toLocaleDateString(lang, { weekday: 'long' }))
}