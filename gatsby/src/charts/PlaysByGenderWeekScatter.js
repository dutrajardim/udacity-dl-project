import React from 'react'
import { useStaticQuery, graphql } from 'gatsby'
import Plot from 'react-plotly.js'

import { range } from '../helpers'

const gql = graphql`
    query  {
        femaleData:allOlapYaerWeekGender(
            filter: {week: {ne: null}, year: {eq: null}, gender: {eq: "F"}}
        ) {
            edges {
                node {
                    count
                    week
                }
            }
        }
        maleData:allOlapYaerWeekGender(
            filter: {week: {ne: null}, year: {eq: null}, gender: {eq: "M"}}
        ) {
            edges {
                node {
                    count
                    week
                }
            }
        }
        anonymousData:allOlapYaerWeekGender(
            filter: {week: {ne: null}, year: {eq: null}, gender: {eq: "unknown"}}
        ) {
            edges {
                node {
                    count
                    week
                }
            }
        }
        range: allOlapYaerWeekGender(
            filter: {week: {ne: null}, year: {eq: null}}
        ) {
            max(field: week)
            min(field: week)
        }
    }
`

export default function PlaysByGenderWeekScatter() {
    const resp = useStaticQuery(gql)
    const reducer = (acc, { node }) => ({ ...acc, [node.week]: node.count })

    const femaleData = resp.femaleData.edges.reduce(reducer, {})
    const maleData = resp.maleData.edges.reduce(reducer, {})
    const anonymousData = resp.anonymousData.edges.reduce(reducer, {})

    const min = resp.range.min
    const max = resp.range.max

    const weekRange = range(min, max + 1)

    const fTrace = {
        type: 'scatter',
        name: 'Female',
        x: weekRange,
        y: weekRange.map(week => femaleData[week] || 0)
    }

    const mTrace = {
        type: 'scatter',
        name: 'Male',
        x: weekRange,
        y: weekRange.map(week => maleData[week] || 0)
    }

    const anTrace = {
        type: 'scatter',
        name: 'Anonymous',
        x: weekRange,
        y: weekRange.map(week => anonymousData[week] || 0)
    }

    return (
        <Plot
            data={[fTrace, mTrace, anTrace]}
            layout={{ title: "Counting plays by gender and week of year" }} />
    )
}