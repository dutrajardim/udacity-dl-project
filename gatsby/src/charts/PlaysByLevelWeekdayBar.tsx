import React from 'react'
import { useStaticQuery, graphql } from "gatsby"
import Plot from "react-plotly.js"

import { getWeekdays } from '../helpers'

const gql = graphql`
    query {
        freeLevelData: allOlapLevelWeekdayArtists(
            filter: {name: {eq: null}, level: {eq: "free"}, weekday: {ne: null}}
        ) {
            edges {
                node {
                    weekday
                    count
                }
            }
        },
        paidLevelData: allOlapLevelWeekdayArtists(
            filter: {name: {eq: null}, level: {eq: "paid"}, weekday: {ne: null}}
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

export default function PlaysByLevelWeekdayBar() {
    const resp = useStaticQuery(gql)
    const reducer = (acc, { node }) => ({ ...acc, [node.weekday]: node.count })
    const freeLevelData = resp.freeLevelData.edges.reduce(reducer, {})
    const paidLevelData = resp.paidLevelData.edges.reduce(reducer, {})

    const weekdays = getWeekdays()
    const freeLevelTrace = {
        type: 'bar',
        name: 'Free',
        y: weekdays.map((_, key) => (freeLevelData[key + 1] || 0)),
        x: weekdays
    }

    const paidLevelTrace = {
        type: 'bar',
        name: 'Paid',
        y: weekdays.map((_, key) => (paidLevelData[key + 1] || 0)),
        x: weekdays
    }

    let layout = {
        autosize: true,
        margin: { t: 30, b: 0, r: 25, l: 25 },
        legend: { orientation: "h" }
    }

    return (
        <Plot
            data={[freeLevelTrace, paidLevelTrace]}
            layout={layout}
            useResizeHandler={true}
            style={{ width: '100%', height: '100%', maxHeight: '250px' }} />
    )
}