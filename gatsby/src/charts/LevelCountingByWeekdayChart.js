import React from 'react'

import { useStaticQuery, graphql } from "gatsby"
import Plot from "react-plotly.js"

const gql = graphql`
    query {
        freeLevelCountByWeekday: allOlapLevelWeekdayArtists(
            filter: {name: {eq: null}, level: {eq: "free"}, weekday: {ne: null}}
            sort: {fields: weekday, order: ASC}
        ) {
            edges {
                node {
                    weekday
                    count
                }
            }
        },
        paidLevelCountByWeekday: allOlapLevelWeekdayArtists(
            filter: {name: {eq: null}, level: {eq: "paid"}, weekday: {ne: null}}
            sort: {fields: weekday, order: ASC}
        ) {
            edges {
                node {
                    weekday
                    count
                }
            }
        }
    }
`

const getWeekdays = (lang = navigator.language) => {
    const daysInMS = 24 * 60 * 60 * 1000
    const firstSunday = 4 * daysInMS

    return [...Array(7).keys()]
        .map(daysQtd => (new Date(firstSunday + daysQtd * daysInMS))
            .toLocaleDateString(lang, { weekday: 'long' }))
}

export default function LevelCountByWeekdayChart() {
    const resp = useStaticQuery(gql)

    const freeLevelCountByWeekday = resp.freeLevelCountByWeekday.edges.reduce((acc, { node }) => ({ ...acc, [node.weekday]: node.count }), {})
    const paidLevelCountByWeekday = resp.paidLevelCountByWeekday.edges.reduce((acc, { node }) => ({ ...acc, [node.weekday]: node.count }), {})

    const weekdays = getWeekdays()
    const freeLevelTrace = {
        type: 'bar',
        name: 'Free',
        y: weekdays.map((_, key) => (freeLevelCountByWeekday[key + 1] || 0)),
        x: weekdays
    }

    const paidLevelTrace = {
        type: 'bar',
        name: 'Paid',
        y: weekdays.map((_, key) => (paidLevelCountByWeekday[key + 1] || 0)),
        x: weekdays
    }

    return (
        <Plot
            data={[freeLevelTrace, paidLevelTrace]}
            layout={{ title: 'Count by weekday' }} />
    )
}